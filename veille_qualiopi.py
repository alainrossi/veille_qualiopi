#!/usr/bin/env python3
"""
Veille Perplexity Program

This program:
1. Connects to Perplexity AI using the perplexity_api module
2. Opens prompt.yaml to read the prompt and model configuration
3. Sends a request to Perplexity AI
4. Prints the response

Requirements:
- PERPLEXITY_API_KEY environment variable must be set
- prompt.yaml file must exist in the prompts/ directory
"""

import sys
import os
import yaml
import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Tuple

# Add the perplexity_api directory to the Python path
sys.path.append(str(Path(__file__).parent / "perplexity_api"))
# Add the emailer directory to the Python path
sys.path.append(str(Path(__file__).parent / "emailer"))

from perplexity_api import PerplexityClient, PerplexityModel
from emailer.emailer.emailer import EmailSender
from emailer.emailer.config import load_from_dotenv


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Veille Perplexity Program - Choose between juridical or pedagogical/technological monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python veille_qualiopi.py --type veille_juridique
  python veille_qualiopi.py --type veille_pedagogique_technologique
  python veille_qualiopi.py -t veille_juridique
  python veille_qualiopi.py --type veille_juridique --days 30
  python veille_qualiopi.py -t veille_pedagogique_technologique -d 90
        """
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['veille_juridique', 'veille_pedagogique_technologique'],
        default='veille_juridique',
        help='Type of monitoring to perform (default: veille_juridique)'
    )
    
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=60,
        help='Number of days to look back from today for start_date (default: 60)'
    )
    
    return parser.parse_args()


def load_prompt_config(prompt_file: str = "prompts/prompt.yaml") -> Dict:
    """
    Load the prompt configuration from YAML file.
    
    Args:
        prompt_file (str): Path to the prompt YAML file
        
    Returns:
        Dict: Configuration containing prompt and model information
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        yaml.YAMLError: If the YAML file is malformed
    """
    try:
        base_dir = Path(__file__).parent
        prompt_path = Path(prompt_file)
        if not prompt_path.is_absolute():
            prompt_path = base_dir / prompt_path
        with open(prompt_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")


def calculate_date_range(days: int = 60) -> Tuple[datetime, datetime, str, str]:
    """
    Calculate start and end dates for the monitoring period.
    
    Args:
        days (int): Number of days to look back from today for start_date (default: 60)
        
    Returns:
        Tuple[datetime, datetime, str, str]: (start_date, end_date, start_date_str, end_date_str)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Format dates as DD/MM/YYYY
    start_date_str = start_date.strftime("%d/%m/%Y")
    end_date_str = end_date.strftime("%d/%m/%Y")
    
    return start_date, end_date, start_date_str, end_date_str


def load_email_template(template_file: str = "templates/email_template.html") -> str:
    """
    Load the email template content.
    
    Args:
        template_file (str): Path to the email template HTML file
        
    Returns:
        str: Email template content
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
    """
    try:
        base_dir = Path(__file__).parent
        template_path = Path(template_file)
        if not template_path.is_absolute():
            template_path = base_dir / template_path
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Email template file not found: {template_path}")


def extract_prompt_data(config: Dict, prompt_type: str = "veille_juridique", days: int = 60) -> Tuple[str, str]:
    """
    Extract prompt and model from the configuration.
    
    Args:
        config (Dict): Configuration dictionary from YAML
        prompt_type (str): Type of prompt to extract ('veille_juridique' or 'veille_pedagogique_technologique')
        days (int): Number of days to look back from today for start_date (default: 60)
        
    Returns:
        Tuple[str, str]: (prompt, model)
        
    Raises:
        KeyError: If required keys are missing from configuration
    """
    try:
        # Validate prompt_type
        valid_types = ['veille_juridique', 'veille_pedagogique_technologique']
        if prompt_type not in valid_types:
            raise ValueError(f"Invalid prompt_type: {prompt_type}. Must be one of: {valid_types}")
        
        # Extract configuration for the specified prompt type
        veille_config = config[prompt_type]
        prompt = veille_config['prompt'].strip()
        model = veille_config['model']
        
        # Replace date placeholders with actual dates
        start_date, end_date, start_date_str, end_date_str = calculate_date_range(days)
        
        # Get current year and calculate year range
        current_year = datetime.now().year
        start_year = current_year
        end_year = current_year + 1
        
        # Calculate report date (3 months ago for the English prompt)
        report_date = (datetime.now() - timedelta(days=days)).strftime("%d/%m/%Y")
        
        # Replace placeholders in prompt
        prompt = prompt.replace("{start_date}", start_date_str)
        prompt = prompt.replace("{end_date}", end_date_str)
        prompt = prompt.replace("{current_year}", str(current_year))
        prompt = prompt.replace("{report_date}", report_date)
        prompt = prompt.replace("{start_year}", str(start_year))
        prompt = prompt.replace("{end_year}", str(end_year))
        
        return prompt, model
    except KeyError as e:
        raise KeyError(f"Missing required key '{prompt_type}' in configuration: {e}")


def clean_response_text(response_text: str) -> str:
    """
    Clean the response text from Perplexity AI by removing markdown code block syntax.
    
    Args:
        response_text (str): Raw response text that may contain markdown code blocks
        
    Returns:
        str: Cleaned HTML content
    """
    if not response_text:
        return response_text
    
    # Remove markdown code block syntax
    # Remove ```html at the beginning
    if response_text.strip().startswith('```html'):
        response_text = response_text.strip()[7:]  # Remove ```html
    
    # Remove ``` at the end
    if response_text.strip().endswith('```'):
        response_text = response_text.strip()[:-3]  # Remove ```
    
    # Also handle cases where there might be ``` without html
    if response_text.strip().startswith('```'):
        response_text = response_text.strip()[3:]  # Remove ```
    
    # Clean up any leading/trailing whitespace
    response_text = response_text.strip()
    
    return response_text


def load_recipients_config(recipients_file: str = "recipients.json") -> Dict:
    """
    Load recipients configuration from JSON file.
    
    Args:
        recipients_file (str): Path to the recipients JSON file
        
    Returns:
        Dict: Configuration containing to and cc recipients
        
    Raises:
        FileNotFoundError: If the recipients file doesn't exist
        json.JSONDecodeError: If the JSON file is malformed
    """
    try:
        base_dir = Path(__file__).parent
        recipients_path = Path(recipients_file)
        if not recipients_path.is_absolute():
            recipients_path = base_dir / recipients_path
        with open(recipients_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Recipients file not found: {recipients_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error parsing JSON file: {e}")


def send_email_report(response_text: str, prompt_type: str = "veille_juridique", days: int = 60) -> bool:
    """
    Send the veille report via email to recipients defined in recipients.json.
    
    Args:
        response_text (str): The content of the report to send
        prompt_type (str): Type of monitoring performed ('veille_juridique' or 'veille_pedagogique_technologique')
        days (int): Number of days to look back from today for start_date (default: 60)
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        print("📧 Loading email configuration...")
        
        # Load email configuration from .env file (resolve relative to script dir)
        base_dir = Path(__file__).parent
        email_config = load_from_dotenv(str(base_dir / '.env'))
        
        if not email_config.get('email') or not email_config.get('password'):
            print("❌ Email configuration not found in .env file")
            return False
        
        print(f"✅ Email configuration loaded for: {email_config.get('email')}")
        
        # Load recipients configuration
        print("📋 Loading recipients configuration...")
        recipients_config = load_recipients_config()
        
        to_recipients = recipients_config.get('to', [])
        cc_recipients = recipients_config.get('cc', [])
        
        if not to_recipients and not cc_recipients:
            print("❌ No recipients found in recipients.json")
            return False
        
        print(f"✅ Recipients loaded:")
        print(f"   To: {len(to_recipients)} recipients")
        print(f"   CC: {len(cc_recipients)} recipients")
        
        # Clean the response text to remove markdown code block syntax
        print("🧹 Cleaning response text...")
        cleaned_response_text = clean_response_text(response_text)
        print("✅ Response text cleaned successfully")
        
        # Load and format email template
        print("📄 Loading email template...")
        try:
            email_template = load_email_template()
            
            # Generate dates for template
            start_date, end_date, start_date_str, end_date_str = calculate_date_range(days)
            
            # Generate type display name
            if prompt_type == "veille_juridique":
                type_display = "juridique"
            elif prompt_type == "veille_pedagogique_technologique":
                type_display = "pédagogique et technologique"
            else:
                type_display = "générale"
            
            # Replace template placeholders
            formatted_email = email_template.replace("{type}", type_display)
            formatted_email = formatted_email.replace("{start_date}", start_date_str)
            formatted_email = formatted_email.replace("{end_date}", end_date_str)
            formatted_email = formatted_email.replace("{response_text}", cleaned_response_text)
            
            print("✅ Email template formatted successfully")
            
        except FileNotFoundError as e:
            print(f"⚠️  Warning: {e}")
            print("   Using response text directly without template formatting...")
            formatted_email = cleaned_response_text
        
        # Initialize email sender
        sender = EmailSender(
            email=email_config['email'],
            password=email_config['password'],
            smtp_server=email_config.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=email_config.get('smtp_port', 587)
        )
        
        # Generate email subject based on prompt type
        if prompt_type == "veille_juridique":
            subject = "Veille juridique"
        elif prompt_type == "veille_pedagogique_technologique":
            subject = "Veille pédagogique et technologique"
        else:
            subject = "Veille"
        
        # Send email
        print("📤 Sending email...")
        
        success = sender.send_html_email(
            to_emails=to_recipients if to_recipients else None,
            cc=cc_recipients if cc_recipients else None,
            subject=subject,
            html_body=formatted_email
        )

        if success:
            print("✅ Email sent successfully!")
            return True
        else:
            print("❌ Failed to send email")
            return False
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def main():
    """Main function to execute the veille perplexity program."""
    
    # Parse command line arguments
    args = parse_arguments()
    prompt_type = args.type
    days = args.days
    
    print("🔍 Veille Perplexity - Connecting to Perplexity AI")
    print("=" * 50)
    print(f"📋 Selected monitoring type: {prompt_type}")
    print(f"📅 Looking back {days} days from today")
    print("=" * 50)
    
    try:
        # Step 1: Get API key from environment or config file
        print("🔑 Getting API key from environment...")
        api_key = os.getenv("PERPLEXITY_API_KEY")
        
        # If not found in environment, try to load from config file
        if not api_key:
            config_file = Path(__file__).parent / ".env"
            if config_file.exists():
                print("📄 Loading API key from config.env...")
                with open(config_file, 'r') as f:
                    for line in f:
                        if line.startswith("PERPLEXITY_API_KEY="):
                            api_key = line.split("=", 1)[1].strip()
                            break
        
        if not api_key or api_key == "your_perplexity_api_key_here":
            raise ValueError("PERPLEXITY_API_KEY must be set")
        
        print("✅ API key loaded successfully")
        print()
        
        # Step 2: Load prompt configuration
        print("📄 Loading prompt configuration...")
        config = load_prompt_config()
        prompt, model = extract_prompt_data(config, prompt_type, days)
        print(f"✅ Configuration loaded:")
        print(f"   Type: {prompt_type}")
        print(f"   Model: {model}")
        print(f"   Prompt length: {prompt.count(' ')} words")
        print()
        
        # Step 3: Initialize Perplexity API client and check model availability
        print("🔗 Initializing Perplexity API client...")
        api = PerplexityClient(api_key=api_key)
        print("✅ API client initialized")
        
        # Step 4: Send request to Perplexity AI
        print("🚀 Sending request to Perplexity AI...")
        print(f"   Using model: {model}")
        print("   Processing request...")
        
        response_text = api.ask(
            question=prompt,
            model=model,
            temperature=0,
            max_tokens=20000
        )

        print("✅ Response received successfully!")
        print()
        
        # Step 5: Print the response
        print("📝 RESPONSE FROM PERPLEXITY AI")
        print("=" * 50)
        
        if response_text:
            print(response_text)
        else:
            print("⚠️  No content found in response")
        
        print()
        print("=" * 50)
        
        # Step 6: Send email report
        print("📧 SENDING EMAIL REPORT")
        print("=" * 50)
        
        if response_text:
            email_success = send_email_report(response_text, prompt_type, days)
            if email_success:
                print("✅ Email report sent successfully!")
            else:
                print("❌ Failed to send email report")
        else:
            print("⚠️  No content to send via email")
        
        print()
        print("=" * 50)
        print("✅ Program completed successfully!")
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        sys.exit(1)
        
    except yaml.YAMLError as e:
        print(f"❌ YAML Error: {e}")
        sys.exit(1)
        
    except KeyError as e:
        print(f"❌ Configuration Error: {e}")
        sys.exit(1)
        
    except ValueError as e:
        print(f"❌ API Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
