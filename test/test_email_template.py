#!/usr/bin/env python3
"""
Test script for the HTML email template
This script demonstrates how to use the email template with sample data
"""

import os
from pathlib import Path


class EmailTemplateTester:
    """Test class for email template functionality"""
    
    def __init__(self):
        """Initialize the tester with proper paths"""
        self.project_root = Path(__file__).parent.parent
        self.template_path = self.project_root / 'templates' / 'email_template.html'
        self.output_path = Path(__file__).parent / 'test_email_output.html'
    
    def get_sample_data(self):
        """Get sample data for testing the email template"""
        return {
            'type': 'juridique',
            'start_date': '01/01/2025',
            'end_date': '28/02/2025',
            'response_text': '''
            <h1>FORMATION PROFESSIONNELLE - CADRE GÉNÉRAL</h1>
            
            <p>Voici un résumé des principales évolutions réglementaires observées durant cette période :</p>
            
            <h2>Nouveaux textes réglementaires</h2>
            <ul>
                <li><strong>Décret n° 2025-123 du 15 février 2025</strong> : Modification des modalités de certification Qualiopi</li>
                <li><strong>Arrêté du 20 février 2025</strong> : Mise à jour du référentiel national qualité</li>
            </ul>
            
            <h2>COMPTE PERSONNEL DE FORMATION (CPF)</h2>
            
            <p>Plusieurs évolutions importantes ont été observées :</p>
            
            <h3>Changements dans les modalités d'utilisation</h3>
            <p>Le nouveau décret introduit des modifications significatives dans l'utilisation du CPF, notamment concernant les formations éligibles.</p>
            
            <h2>CERTIFICATION QUALIOPI</h2>
            
            <p>Les organismes de formation doivent prendre en compte les nouvelles exigences :</p>
            <ul>
                <li>Renforcement des critères d'audit</li>
                <li>Nouvelles procédures de contrôle</li>
                <li>Modifications des obligations de reporting</li>
            </ul>
            
            <h2>PRINCIPAUX IMPACTS</h2>
            
            <p><strong>Risques identifiés :</strong></p>
            <ul>
                <li>Adaptation nécessaire des processus internes</li>
                <li>Formation des équipes aux nouvelles procédures</li>
            </ul>
            
            <p><strong>Opportunités :</strong></p>
            <ul>
                <li>Amélioration de la qualité des formations</li>
                <li>Renforcement de la crédibilité auprès des clients</li>
            </ul>
            
            <p>Pour plus d'informations, consultez les <a href="https://www.legifrance.gouv.fr">textes officiels</a> sur Legifrance.</p>
            '''
        }
    
    def load_template(self):
        """Load the email template from file"""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
        
        with open(self.template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def replace_placeholders(self, template, data):
        """Replace placeholders in template with data"""
        html_content = template
        for key, value in data.items():
            html_content = html_content.replace(f"{{{key}}}", str(value))
        return html_content
    
    def save_output(self, html_content):
        """Save the generated HTML content to file"""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def run_test(self):
        """Run the complete email template test"""
        try:
            # Get sample data
            template_data = self.get_sample_data()
            
            # Load template
            template = self.load_template()
            
            # Replace placeholders
            html_content = self.replace_placeholders(template, template_data)
            
            # Save output
            self.save_output(html_content)
            
            print("✓ Test email template created successfully!")
            print(f"📄 Output saved to: {self.output_path}")
            print("🌐 Open the file in your browser to preview the email")
            
        except Exception as e:
            print(f"✗ Error during test: {e}")
            raise


def test_email_template():
    """Test the email template with sample data"""
    tester = EmailTemplateTester()
    tester.run_test()

if __name__ == "__main__":
    test_email_template()
