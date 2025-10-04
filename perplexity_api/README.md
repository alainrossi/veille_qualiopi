# Perplexity API Client

A comprehensive Python module for interacting with the Perplexity AI API. This module provides an easy-to-use interface for chat completions, streaming responses, and search functionality using Perplexity's various AI models.

## Features

- 🤖 **Multiple Models**: Support for all Perplexity AI models including Sonar, Llama, Mixtral, and CodeLlama
- 🔄 **Streaming Support**: Real-time streaming responses for interactive applications
- 🔍 **Search Functionality**: Built-in search capabilities using Perplexity's online models
- 📝 **Type Safety**: Full type hints and structured data classes for better development experience
- 🛡️ **Error Handling**: Comprehensive error handling with custom exception classes
- 🔧 **Flexible Configuration**: Environment-based configuration with sensible defaults
- 📚 **Context Management**: Built-in support for Python context managers

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Set up your API key

Get your API key from [Perplexity AI](https://www.perplexity.ai/settings/api) and set it as an environment variable:

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

### 2. Basic Usage

```python
from perplexity_client import PerplexityClient

# Initialize the client
client = PerplexityClient()

# Ask a simple question
response = client.ask("What is the capital of France?")
print(response)

# Close the client
client.close()
```

### 3. Using Context Manager (Recommended)

```python
from perplexity_client import PerplexityClient

with PerplexityClient() as client:
    response = client.ask("Explain quantum computing in simple terms")
    print(response)
```

## Advanced Usage

### Streaming Responses

```python
with PerplexityClient() as client:
    for chunk in client.ask_stream("Tell me about artificial intelligence"):
        print(chunk, end="", flush=True)
```

### Using Different Models

```python
from perplexity_client import PerplexityClient, PerplexityModel

with PerplexityClient() as client:
    # Use a specific model
    response = client.ask(
        "What's the latest news?", 
        model=PerplexityModel.SONAR_MEDIUM_ONLINE
    )
    print(response)
```

### Search Functionality

```python
with PerplexityClient() as client:
    # Search for current information
    result = client.search("Latest developments in AI 2024")
    print(result)
```

### System Messages and Context

```python
with PerplexityClient() as client:
    response = client.ask(
        "How do computers work?",
        system_message="You are a helpful teacher who explains things simply.",
        temperature=0.7
    )
    print(response)
```

### Multi-turn Conversations

```python
from perplexity_client import Message, ChatCompletionRequest

with PerplexityClient() as client:
    messages = [
        Message(role="system", content="You are a coding assistant."),
        Message(role="user", content="How do I create a Python function?"),
    ]
    
    request = ChatCompletionRequest(
        model="sonar-pro",
        messages=messages,
        temperature=0.5
    )
    
    response = client.chat_completion(request)
    print(response.choices[0].message.content)
```

### Convenience Function

```python
from perplexity_client import ask_perplexity

# Quick one-liner for simple questions
answer = ask_perplexity("What is Python?")
print(answer)
```

## Available Models

The module supports all Perplexity AI models:

- **Sonar Models**: `sonar-small-chat`, `sonar-small-online`, `sonar-medium-chat`, `sonar-medium-online`, `sonar-pro`
- **Llama Models**: `llama-3.1-8b-instruct`, `llama-3.1-70b-instruct`
- **Other Models**: `mixtral-8x7b-instruct`, `codellama-34b-instruct`

### Model Recommendations

- **For general questions**: `sonar-pro` (default)
- **For current information/search**: `sonar-medium-online` or `sonar-small-online`
- **For coding tasks**: `codellama-34b-instruct`
- **For cost-effective usage**: `sonar-small-chat`

## Configuration

### Environment Variables

You can configure the client using environment variables:

```bash
export PERPLEXITY_API_KEY="your-api-key"
export PERPLEXITY_BASE_URL="https://api.perplexity.ai"  # Optional
export PERPLEXITY_DEFAULT_MODEL="sonar-pro"             # Optional
export PERPLEXITY_MAX_RETRIES="3"                       # Optional
export PERPLEXITY_TIMEOUT="30"                          # Optional
```

### Programmatic Configuration

```python
from config import PerplexityConfig

config = PerplexityConfig(
    api_key="your-api-key",
    default_model="sonar-medium-online",
    timeout=60
)

client = PerplexityClient(api_key=config.api_key)
```

## Error Handling

The module provides comprehensive error handling:

```python
from perplexity_client import PerplexityClient, PerplexityAPIError

try:
    with PerplexityClient() as client:
        response = client.ask("Your question here")
        print(response)
except PerplexityAPIError as e:
    print(f"API Error: {e.message}")
    if e.status_code:
        print(f"Status Code: {e.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## API Reference

### PerplexityClient

Main client class for interacting with the Perplexity API.

#### Methods

- `ask(question, model, system_message, **kwargs)`: Ask a simple question
- `ask_stream(question, model, system_message, **kwargs)`: Get streaming response
- `search(query, model)`: Search for information using online models
- `chat_completion(request)`: Full chat completion with structured request/response
- `get_available_models()`: List all available models
- `close()`: Close the HTTP session

#### Parameters

- `question/query` (str): The question or search query
- `model` (str | PerplexityModel): Model to use for the request
- `system_message` (str, optional): System message to set context
- `max_tokens` (int, optional): Maximum tokens in response
- `temperature` (float, optional): Sampling temperature (0.0 to 1.0)
- `top_p` (float, optional): Top-p sampling parameter
- `top_k` (int, optional): Top-k sampling parameter
- `presence_penalty` (float, optional): Presence penalty (-2.0 to 2.0)
- `frequency_penalty` (float, optional): Frequency penalty (-2.0 to 2.0)

## Examples

Run the example script to see the module in action:

```bash
python example.py
```

The example script demonstrates:
- Basic usage
- Streaming responses
- Different models
- Search functionality
- System messages
- Multi-turn conversations
- Convenience functions

## Files Structure

```
perplexity_api/
├── perplexity_client.py  # Main client module
├── config.py            # Configuration management
├── example.py           # Usage examples
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Contributing

Feel free to contribute to this project by:
1. Reporting bugs
2. Suggesting new features
3. Submitting pull requests
4. Improving documentation

## License

This project is open source and available under the MIT License.

## Support

For issues related to the Perplexity API itself, please refer to the [official Perplexity documentation](https://docs.perplexity.ai/).

For issues with this client module, please create an issue in the repository.
