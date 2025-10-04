# PowerShell script to set the Perplexity API key
# Usage: .\set_api_key.ps1 -ApiKey "your_actual_api_key_here"

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey
)

# Set the environment variable for the current session
$env:PERPLEXITY_API_KEY = $ApiKey

# Verify it was set
Write-Host "✅ PERPLEXITY_API_KEY has been set successfully!"
Write-Host "You can now run: python veille_qualiopi.py"



