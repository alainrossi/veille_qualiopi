"""
Perplexity API Client Module

A comprehensive Python module for interacting with the Perplexity AI API.
Supports chat completions, streaming responses, and various models.
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Union, Iterator, Any
from dataclasses import dataclass, asdict
from enum import Enum
import requests


class PerplexityModel(Enum):
    """Available Perplexity AI models."""
    SONAR_SMALL_CHAT = "sonar-small-chat"
    SONAR_SMALL_ONLINE = "sonar-small-online"
    SONAR_MEDIUM_CHAT = "sonar-medium-chat"
    SONAR_MEDIUM_ONLINE = "sonar-medium-online"
    SONAR_PRO = "sonar-pro"
    LLAMA_3_1_8B = "llama-3.1-8b-instruct"
    LLAMA_3_1_70B = "llama-3.1-70b-instruct"
    MIXTRAL_8X7B = "mixtral-8x7b-instruct"
    CODELLAMA_34B = "codellama-34b-instruct"


@dataclass
class Message:
    """Represents a chat message."""
    role: str  # "system", "user", or "assistant"
    content: str


@dataclass
class ChatCompletionRequest:
    """Request parameters for chat completion."""
    model: str
    messages: List[Message]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    stream: bool = False
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None


@dataclass
class Usage:
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class Choice:
    """Represents a choice in the API response."""
    index: int
    message: Message
    finish_reason: str


@dataclass
class ChatCompletionResponse:
    """Response from chat completion API."""
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage


class PerplexityAPIError(Exception):
    """Custom exception for Perplexity API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class PerplexityClient:
    """
    A comprehensive client for the Perplexity AI API.
    
    This client provides methods to interact with Perplexity's chat completion API,
    supporting both streaming and non-streaming responses.
    """
    
    BASE_URL = "https://api.perplexity.ai"
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the Perplexity client.
        
        Args:
            api_key: Perplexity API key. If not provided, will look for PERPLEXITY_API_KEY env var.
            base_url: Base URL for the API. Defaults to official Perplexity API URL.
        """
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set PERPLEXITY_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, endpoint: str, data: Dict[str, Any], stream: bool = False) -> Union[Dict, Iterator[Dict]]:
        """
        Make a request to the Perplexity API.
        
        Args:
            endpoint: API endpoint
            data: Request payload
            stream: Whether to stream the response
            
        Returns:
            Response data or iterator for streaming responses
            
        Raises:
            PerplexityAPIError: If the API request fails
        """
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.post(url, json=data, stream=stream)
            response.raise_for_status()
            
            if stream:
                return self._handle_stream_response(response)
            else:
                return response.json()
                
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP {e.response.status_code}: {e.response.reason}"
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_msg = error_data["error"].get("message", error_msg)
            except (ValueError, KeyError):
                pass
            raise PerplexityAPIError(error_msg, e.response.status_code, e.response.json() if e.response else None)
        
        except requests.exceptions.RequestException as e:
            raise PerplexityAPIError(f"Request failed: {str(e)}")
    
    def _handle_stream_response(self, response: requests.Response) -> Iterator[Dict]:
        """
        Handle streaming response from the API.
        
        Args:
            response: Streaming response object
            
        Yields:
            Parsed JSON chunks from the stream
        """
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith("data: "):
                data = line[6:]  # Remove "data: " prefix
                if data == "[DONE]":
                    break
                try:
                    yield json.loads(data)
                except json.JSONDecodeError:
                    continue
    
    def chat_completion(self, request: ChatCompletionRequest) -> Union[ChatCompletionResponse, Iterator[Dict]]:
        """
        Create a chat completion.
        
        Args:
            request: Chat completion request parameters
            
        Returns:
            ChatCompletionResponse for non-streaming requests,
            Iterator of response chunks for streaming requests
        """
        # Convert messages to dict format
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Prepare request data
        data = {
            "model": request.model,
            "messages": messages_dict,
            "stream": request.stream
        }
        
        # Add optional parameters
        if request.max_tokens is not None:
            data["max_tokens"] = request.max_tokens
        if request.temperature is not None:
            data["temperature"] = request.temperature
        if request.top_p is not None:
            data["top_p"] = request.top_p
        if request.top_k is not None:
            data["top_k"] = request.top_k
        if request.presence_penalty is not None:
            data["presence_penalty"] = request.presence_penalty
        if request.frequency_penalty is not None:
            data["frequency_penalty"] = request.frequency_penalty
        
        response = self._make_request("chat/completions", data, stream=request.stream)
        
        if request.stream:
            return response
        else:
            # Parse response into structured format
            choices = []
            for choice_data in response["choices"]:
                message = Message(
                    role=choice_data["message"]["role"],
                    content=choice_data["message"]["content"]
                )
                choice = Choice(
                    index=choice_data["index"],
                    message=message,
                    finish_reason=choice_data["finish_reason"]
                )
                choices.append(choice)
            
            usage = Usage(
                prompt_tokens=response["usage"]["prompt_tokens"],
                completion_tokens=response["usage"]["completion_tokens"],
                total_tokens=response["usage"]["total_tokens"]
            )
            
            return ChatCompletionResponse(
                id=response["id"],
                object=response["object"],
                created=response["created"],
                model=response["model"],
                choices=choices,
                usage=usage
            )
    
    def ask(self, question: str, model: Union[str, PerplexityModel] = PerplexityModel.SONAR_PRO, 
            system_message: Optional[str] = None, **kwargs) -> str:
        """
        Simple method to ask a question and get a text response.
        
        Args:
            question: The question to ask
            model: Model to use (string or PerplexityModel enum)
            system_message: Optional system message to set context
            **kwargs: Additional parameters for chat completion
            
        Returns:
            The response text
        """
        messages = []
        
        if system_message:
            messages.append(Message(role="system", content=system_message))
        
        messages.append(Message(role="user", content=question))
        
        model_str = model.value if isinstance(model, PerplexityModel) else model
        
        request = ChatCompletionRequest(
            model=model_str,
            messages=messages,
            **kwargs
        )
        
        response = self.chat_completion(request)
        return response.choices[0].message.content
    
    def ask_stream(self, question: str, model: Union[str, PerplexityModel] = PerplexityModel.SONAR_PRO,
                   system_message: Optional[str] = None, **kwargs) -> Iterator[str]:
        """
        Ask a question and get a streaming response.
        
        Args:
            question: The question to ask
            model: Model to use (string or PerplexityModel enum)
            system_message: Optional system message to set context
            **kwargs: Additional parameters for chat completion
            
        Yields:
            Response text chunks as they arrive
        """
        messages = []
        
        if system_message:
            messages.append(Message(role="system", content=system_message))
        
        messages.append(Message(role="user", content=question))
        
        model_str = model.value if isinstance(model, PerplexityModel) else model
        
        request = ChatCompletionRequest(
            model=model_str,
            messages=messages,
            stream=True,
            **kwargs
        )
        
        stream = self.chat_completion(request)
        
        for chunk in stream:
            if "choices" in chunk and len(chunk["choices"]) > 0:
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta:
                    yield delta["content"]
    
    def search(self, query: str, model: Union[str, PerplexityModel] = PerplexityModel.SONAR_PRO) -> str:
        """
        Search for information using Perplexity's online models.
        
        Args:
            query: Search query
            model: Model to use (preferably an online model)
            
        Returns:
            Search results and answer
        """
        # Use online models for search functionality
        if isinstance(model, PerplexityModel) and "online" not in model.value:
            model = PerplexityModel.SONAR_MEDIUM_ONLINE
        
        return self.ask(query, model=model)
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available models.
        
        Returns:
            List of model names
        """
        return [model.value for model in PerplexityModel]
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Convenience function for quick usage
def ask_perplexity(question: str, api_key: Optional[str] = None, 
                   model: Union[str, PerplexityModel] = PerplexityModel.SONAR_PRO) -> str:
    """
    Quick function to ask Perplexity a question.
    
    Args:
        question: The question to ask
        api_key: API key (optional if set in environment)
        model: Model to use
        
    Returns:
        The response text
    """
    with PerplexityClient(api_key=api_key) as client:
        return client.ask(question, model=model)


if __name__ == "__main__":
    # Example usage
    try:
        client = PerplexityClient()
        
        # Simple question
        response = client.ask("What is the capital of France?")
        print(f"Response: {response}")
        
        # Streaming response
        print("\nStreaming response:")
        for chunk in client.ask_stream("Tell me about artificial intelligence"):
            print(chunk, end="", flush=True)
        print()
        
        # Search functionality
        search_result = client.search("Latest developments in quantum computing 2024")
        print(f"\nSearch result: {search_result}")
        
    except PerplexityAPIError as e:
        print(f"API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"Error: {e}")
