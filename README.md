# Veille Qualiopi - Automated Legal and Educational Monitoring System

A comprehensive Python application that automates the monitoring of legal and educational developments in France, specifically focused on professional training regulations (Qualiopi certification) and English language teaching methodologies. The system uses AI-powered research to generate detailed reports and automatically distributes them via email.

## 🎯 Overview

This system performs two types of monitoring:

1. **Veille Juridique** - Legal monitoring of French professional training regulations
2. **Veille Pédagogique et Technologique** - Educational and technological monitoring for English language teaching

## ✨ Features

- 🤖 **AI-Powered Research**: Uses Perplexity AI for comprehensive web research
- 📧 **Automated Email Distribution**: Sends formatted HTML reports to multiple recipients
- 📅 **Flexible Date Ranges**: Configurable monitoring periods (default: 60 days)
- 🎨 **Professional Templates**: Beautiful HTML email templates with responsive design
- 🔧 **Modular Architecture**: Separate modules for API clients, email functionality, and templates
- 📊 **Comprehensive Reporting**: Detailed analysis with sources and practical implications
- 🛡️ **Secure Configuration**: Environment-based API key management

## 🏗️ Project Structure

```
veille_qualiopi/
├── veille_qualiopi.py          # Main application
├── prompts/
│   └── prompt.yaml             # AI prompts and model configuration
├── templates/
│   └── email_template.html     # HTML email template
├── perplexity_api/             # Perplexity AI client module
│   ├── perplexity_client.py
│   ├── config.py
│   └── README.md
├── mammouth_api/               # Mammouth AI client module
│   ├── mammouth_api.py
│   └── README.md
├── emailer/                    # Email functionality module
│   ├── emailer/
│   │   ├── emailer.py
│   │   └── config.py
│   └── README.md
├── test/                       # Test files and examples
├── recipients.json             # Email recipients configuration
├── recipients_README.md        # Recipients configuration guide
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Perplexity AI API key
- Email account with SMTP access

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd veille_qualiopi
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   PERPLEXITY_API_KEY=your-perplexity-api-key-here
   EMAIL_ADDRESS=your-email@example.com
   EMAIL_PASSWORD=your-email-password-or-app-password
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   ```

4. **Configure recipients**:
   Edit `recipients.json` with your email addresses:
   ```json
   {
       "to": ["primary@example.com"],
       "cc": ["manager@example.com"]
   }
   ```

### Usage

#### Basic Usage

```bash
# Run legal monitoring (default)
python veille_qualiopi.py

# Run educational monitoring
python veille_qualiopi.py --type veille_pedagogique_technologique

# Custom date range (90 days)
python veille_qualiopi.py --days 90
```

#### Command Line Options

```bash
python veille_qualiopi.py [OPTIONS]

Options:
  --type, -t    Monitoring type: veille_juridique (default) or veille_pedagogique_technologique
  --days, -d    Number of days to look back (default: 60)
  --help, -h    Show help message
```

#### Examples

```bash
# Legal monitoring for the last 30 days
python veille_qualiopi.py -t veille_juridique -d 30

# Educational monitoring for the last 90 days
python veille_qualiopi.py -t veille_pedagogique_technologique -d 90
```

## 📋 Configuration

### AI Prompts Configuration

The `prompts/prompt.yaml` file contains the AI prompts and model settings:

```yaml
veille_juridique:
  prompt: >
    Expert en Veille Réglementaire - Formation Professionnelle France
    # ... detailed prompt for legal monitoring
  model: sonar-pro

veille_pedagogique_technologique:
  prompt: >
    You are my research and briefing assistant...
    # ... detailed prompt for educational monitoring
  model: sonar-pro
```

### Email Configuration

The system supports multiple email configuration methods:

1. **Environment Variables** (recommended):
   ```env
   EMAIL_ADDRESS=your-email@example.com
   EMAIL_PASSWORD=your-password
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   ```

2. **JSON Configuration**:
   ```json
   {
       "email": "your-email@example.com",
       "password": "your-password",
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587
   }
   ```

### Email Providers

#### Gmail
```env
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
# Use App Password if 2FA is enabled
```

#### Outlook/Hotmail
```env
EMAIL_SMTP_SERVER=smtp-mail.outlook.com
EMAIL_SMTP_PORT=587
```

#### Yahoo
```env
EMAIL_SMTP_SERVER=smtp.mail.yahoo.com
EMAIL_SMTP_PORT=587
# Use App Password
```

## 📧 Email Template

The system uses a professional HTML email template (`templates/email_template.html`) with:

- Responsive design for all devices
- Professional styling with gradients and shadows
- Structured content layout
- Print-friendly styles
- Template variables: `{type}`, `{start_date}`, `{end_date}`, `{response_text}`

## 🔧 API Modules

### Perplexity API Client

Located in `perplexity_api/`, this module provides:

- Support for all Perplexity AI models
- Streaming responses
- Search functionality
- Comprehensive error handling
- Type safety with data classes

### Mammouth API Client

Located in `mammouth_api/`, this module provides:

- OpenAI-compatible API interface
- Secure API key management
- Simple text generation methods
- Error handling and validation

### Email Module

Located in `emailer/`, this module provides:

- HTML and plain text email support
- Attachment support
- Template-based emails
- Multiple recipient types (TO, CC, BCC)
- Multiple email provider support

## 🧪 Testing

### Test Email Template

Test the email template with sample data:

```bash
python test/test_email_template.py
```

This generates `test_email_output.html` for preview.

### Integration Testing

The `test/` directory contains various test files:

- `test_email_template.py` - Template testing
- `test_html_email.py` - Email functionality testing
- `test_integration_output.html` - Integration test results

## 📊 Monitoring Types

### Veille Juridique (Legal Monitoring)

Monitors French professional training regulations including:

- **Formation Professionnelle**: General framework changes
- **Compte Personnel de Formation (CPF)**: Usage and eligibility modifications
- **Certification Qualiopi**: Audit criteria and procedures
- **France Compétences**: Regulatory communications
- **Code du Travail**: Training-related modifications

**Sources**: Legifrance, France Compétences, Cour des Comptes, Service Public

### Veille Pédagogique et Technologique (Educational Monitoring)

Monitors English language teaching developments including:

- **Pedagogy**: Adult learning, microlearning, task-based learning
- **Assessment**: CEFR alignment, exam updates (TOEIC, IELTS, etc.)
- **Technology**: AI in teaching, speech technology, e-learning platforms
- **Tools**: Linguahouse, Macmillan English Campus updates

**Sources**: Peer-reviewed journals, ELT publishers, exam boards, OECD/EU reports

## 🔒 Security Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Environment Variables**: Use `.env` files for sensitive data
3. **Email Credentials**: Use app passwords for 2FA-enabled accounts
4. **Recipients**: Validate email addresses in `recipients.json`
5. **Access Control**: Limit API key permissions where possible

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Found**:
   ```
   ValueError: PERPLEXITY_API_KEY must be set
   ```
   **Solution**: Ensure your `.env` file contains the API key

2. **Email Authentication Failed**:
   ```
   SMTPAuthenticationError: Authentication failed
   ```
   **Solution**: Use app passwords for 2FA-enabled accounts

3. **No Recipients Found**:
   ```
   No recipients found in recipients.json
   ```
   **Solution**: Configure valid email addresses in `recipients.json`

4. **Template Not Found**:
   ```
   Email template file not found
   ```
   **Solution**: Ensure `templates/email_template.html` exists

### Debug Mode

Enable verbose logging by modifying the print statements in `veille_qualiopi.py` or add logging configuration.

## 📈 Performance

- **API Calls**: Optimized with proper error handling and retries
- **Email Sending**: Supports multiple recipients efficiently
- **Template Processing**: Fast string replacement for template variables
- **Memory Usage**: Minimal memory footprint with streaming support

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest test/

# Format code
black *.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:

- **Project Issues**: Create an issue in this repository
- **Perplexity API**: Refer to [Perplexity Documentation](https://docs.perplexity.ai/)
- **Mammouth API**: Contact [Mammouth.ai Support](https://mammouth.ai)
- **Email Configuration**: Check the emailer module documentation

## 🔄 Version History

- **v1.0.0**: Initial release with basic monitoring functionality
- **v1.1.0**: Added educational monitoring and improved templates
- **v1.2.0**: Enhanced error handling and modular architecture
- **v1.3.0**: Added Mammouth API support and improved documentation

## 📚 Additional Resources

- [Perplexity API Documentation](https://docs.perplexity.ai/)
- [Mammouth.ai Documentation](https://docs.mammouth.ai)
- [Email Configuration Guide](emailer/README.md)
- [Recipients Configuration](recipients_README.md)
- [French Professional Training Regulations](https://www.legifrance.gouv.fr/)

---

**Developed for Appleton School of English**  
*Automated monitoring system for legal and educational developments*
