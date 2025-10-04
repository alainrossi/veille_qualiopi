#!/usr/bin/env python3
"""
Example usage of the Perplexity API client.

This script demonstrates various ways to use the PerplexityClient class.
"""

import os
import sys
from perplexity_client import PerplexityClient, PerplexityModel, PerplexityAPIError, ask_perplexity


def basic_usage_example():
    """Demonstrate basic usage of the Perplexity client."""
    print("=== Basic Usage Example ===")
    
    try:
        # Initialize the client
        client = PerplexityClient()
        
        # Simple question
        question = "What is the capital of France?"
        response = client.ask(question)
        print(f"Q: {question}")
        print(f"A: {response}\n")
        
        # Close the client
        client.close()
        
    except PerplexityAPIError as e:
        print(f"API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def streaming_example():
    """Demonstrate streaming responses."""
    print("=== Streaming Response Example ===")
    
    try:
        with PerplexityClient() as client:
            question = "Explain quantum computing in simple terms"
            print(f"Q: {question}")
            print("A: ", end="", flush=True)
            
            # Get streaming response
            for chunk in client.ask_stream(question):
                print(chunk, end="", flush=True)
            print("\n")
            
    except PerplexityAPIError as e:
        print(f"API Error: {e.message}")
    except Exception as e:
        print(f"Error: {e}")


def different_models_example():
    """Demonstrate using different models."""
    print("=== Different Models Example ===")
    
    try:
        with PerplexityClient() as client:
            question = "What's the weather like today?"
            
            # List available models
            print("Available models:")
            for model in client.get_available_models():
                print(f"  - {model}")
            print()
            
            # Try different models
            models_to_try = [
                PerplexityModel.SONAR_SMALL_ONLINE,
                PerplexityModel.SONAR_MEDIUM_ONLINE,
                PerplexityModel.SONAR_PRO
            ]
            
            for model in models_to_try:
                print(f"Using model: {model.value}")
                try:
                    response = client.ask(question, model=model)
                    print(f"Response: {response[:100]}...")
                    print()
                except Exception as e:
                    print(f"Error with {model.value}: {e}")
                    print()
                    
    except Exception as e:
        print(f"Error: {e}")


def search_example():
    """Demonstrate search functionality."""
    print("=== Search Functionality Example ===")
    
    try:
        with PerplexityClient() as client:
            # Search for current information
            query = "Latest news about artificial intelligence 2024"
            print(f"Search query: {query}")
            
            result = client.search(query)
            print(f"Search result: {result}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def system_message_example():
    """Demonstrate using system messages."""
    print("=== System Message Example ===")
    
    try:
        with PerplexityClient() as client:
            system_msg = "You are a helpful assistant that explains things like I'm 5 years old."
            question = "How do computers work?"
            
            response = client.ask(question, system_message=system_msg)
            print(f"System: {system_msg}")
            print(f"Q: {question}")
            print(f"A: {response}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def conversation_example():
    """Demonstrate a multi-turn conversation."""
    print("=== Conversation Example ===")
    
    try:
        from perplexity_client import Message, ChatCompletionRequest
        
        with PerplexityClient() as client:
            # Build a conversation
            messages = [
                Message(role="system", content="You are a helpful coding assistant."),
                Message(role="user", content="How do I create a Python function?"),
            ]
            
            # First response
            request = ChatCompletionRequest(
                model=PerplexityModel.SONAR_PRO.value,
                messages=messages
            )
            
            response = client.chat_completion(request)
            assistant_response = response.choices[0].message.content
            
            print("User: How do I create a Python function?")
            print(f"Assistant: {assistant_response}")
            print()
            
            # Continue conversation
            messages.append(Message(role="assistant", content=assistant_response))
            messages.append(Message(role="user", content="Can you show me an example?"))
            
            request.messages = messages
            response = client.chat_completion(request)
            
            print("User: Can you show me an example?")
            print(f"Assistant: {response.choices[0].message.content}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")


def convenience_function_example():
    """Demonstrate the convenience function."""
    print("=== Convenience Function Example ===")
    
    try:
        # Using the convenience function
        response = ask_perplexity("What is Python programming language?")
        print(f"Response: {response}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples."""
    print("Perplexity API Client Examples")
    print("=" * 50)
    
    # Check if API key is set
    if not os.getenv("PERPLEXITY_API_KEY"):
        print("Warning: PERPLEXITY_API_KEY environment variable is not set.")
        print("Please set your API key before running the examples.")
        print("\nExample:")
        print("export PERPLEXITY_API_KEY='your-api-key-here'")
        print("python example.py")
        return
    
    # Run examples
    examples = [
        basic_usage_example,
        streaming_example,
        different_models_example,
        search_example,
        system_message_example,
        conversation_example,
        convenience_function_example
    ]
    
    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\nExample interrupted by user.")
            break
        except Exception as e:
            print(f"Example failed: {e}")
            continue
    
    print("Examples completed!")


if __name__ == "__main__":
    main()
