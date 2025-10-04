#!/usr/bin/env python3
"""
Test script to verify HTML email functionality.
This script tests the HTML email sending capability without requiring Perplexity API.
"""

import sys
from pathlib import Path

# Add the emailer directory to the Python path
sys.path.append(str(Path(__file__).parent / "emailer"))

from emailer.emailer.emailer import EmailSender
from emailer.emailer.config import load_from_dotenv


def test_html_email():
    """Test HTML email functionality with sample HTML content."""
    
    print("🧪 Testing HTML Email Functionality")
    print("=" * 50)
    
    try:
        # Load email configuration from .env file
        print("📧 Loading email configuration...")
        email_config = load_from_dotenv('.env')
        
        if not email_config.get('email') or not email_config.get('password'):
            print("❌ Email configuration not found in .env file")
            print("   Please create a .env file with your email credentials")
            return False
        
        print(f"✅ Email configuration loaded for: {email_config.get('email')}")
        
        # Initialize email sender
        sender = EmailSender(
            email=email_config['email'],
            password=email_config['password'],
            smtp_server=email_config.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=email_config.get('smtp_port', 587)
        )
        
        # Sample HTML content that mimics what Perplexity would return
        sample_html_content = """
        <html>
        <body>
            <h1>Veille Juridique - Formation Professionnelle</h1>
            
            <h2>1. FORMATION PROFESSIONNELLE - CADRE GÉNÉRAL</h2>
            
            <h3>Nouveaux textes réglementaires</h3>
            <p>Plusieurs <strong>décrets importants</strong> ont été publiés récemment :</p>
            <ul>
                <li><strong>Décret n° 2024-XXX</strong> du XX/XX/2024 - Modification des modalités de financement</li>
                <li><strong>Arrêté du XX/XX/2024</strong> - Nouvelles obligations pour les organismes de formation</li>
            </ul>
            
            <h3>Évolutions du financement</h3>
            <p>Les contributions des entreprises évoluent avec de nouvelles règles d'<strong>abondement</strong>.</p>
            
            <h2>2. COMPTE PERSONNEL DE FORMATION (CPF)</h2>
            
            <h3>Changements dans les modalités d'utilisation</h3>
            <p>De nouvelles procédures sont mises en place pour l'utilisation du CPF.</p>
            
            <h2>3. CERTIFICATION QUALIOPI</h2>
            
            <h3>Évolutions du référentiel national qualité</h3>
            <p>Le référentiel Qualiopi a été mis à jour avec de nouveaux critères d'audit.</p>
            
            <h2>4. PRINCIPAUX IMPACTS</h2>
            <p><strong>Risques identifiés :</strong></p>
            <ul>
                <li>Nouvelles obligations de reporting</li>
                <li>Contrôles renforcés</li>
            </ul>
            
            <p><strong>Opportunités :</strong></p>
            <ul>
                <li>Simplification des procédures</li>
                <li>Nouveaux financements disponibles</li>
            </ul>
            
            <h3>Sources officielles</h3>
            <ul>
                <li><a href="https://www.legifrance.gouv.fr">Légifrance</a> - Textes officiels</li>
                <li><a href="https://www.francecompetences.fr">France Compétences</a> - Réglementation</li>
            </ul>
        </body>
        </html>
        """
        
        # Send test email
        print("📤 Sending test HTML email...")
        success = sender.send_html_email(
            to_emails="alain.rossi@appletonenglish.com",  # Using the recipient from recipients.json
            subject="Test HTML Email - Veille Juridique",
            html_body=sample_html_content
        )
        
        if success:
            print("✅ HTML email sent successfully!")
            print("   Check your email to verify the HTML formatting")
            return True
        else:
            print("❌ Failed to send HTML email")
            return False
            
    except Exception as e:
        print(f"❌ Error during HTML email test: {e}")
        return False


if __name__ == "__main__":
    test_html_email()


