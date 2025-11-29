"""
OpenAI Configuration
Setup for GPT-4o integration
"""

import os
from openai import OpenAI
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIConfig:
    """Manages OpenAI client and configuration"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4o"  # GPT-4o model
        self.temperature = 0.1  # Low temperature for consistency
    
    def is_configured(self) -> bool:
        """Check if OpenAI is configured"""
        return self.client is not None
    
    def call_gpt4o(self, messages: list, system_prompt: str = None, 
                   response_format: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Call GPT-4o API
        
        Args:
            messages: List of message dicts
            system_prompt: Optional system prompt
            response_format: Optional response format (for structured output)
            
        Returns:
            API response or None
        """
        if not self.client:
            logger.error("OpenAI client not configured")
            return None
        
        try:
            # Prepend system prompt if provided
            if system_prompt:
                messages = [{"role": "system", "content": system_prompt}] + messages
            
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature
            }
            
            if response_format:
                params["response_format"] = response_format
            
            response = self.client.chat.completions.create(**params)
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"Error calling GPT-4o: {e}")
            return None
    
    def extract_with_gpt4o(self, text: str, extraction_prompt: str, 
                          expected_fields: list) -> Dict[str, Any]:
        """
        Extract structured data using GPT-4o
        
        Args:
            text: Document text
            extraction_prompt: Prompt for extraction
            expected_fields: List of expected field names
            
        Returns:
            Extracted fields dictionary
        """
        messages = [
            {
                "role": "user",
                "content": f"{extraction_prompt}\n\nDocument Text:\n{text}"
            }
        ]
        
        system_prompt = f"""You are a document extraction specialist. Extract the following fields from the document text:
{', '.join(expected_fields)}

Return your response as a JSON object with these fields. For each field, provide:
- value: The extracted value
- confidence: A confidence score between 0.0 and 1.0
- source_text: The exact text from the document that contains this value

If a field is not found, set its value to null and confidence to 0.0."""
        
        response = self.call_gpt4o(messages, system_prompt=system_prompt)
        
        if response and response.get("content"):
            try:
                import json
                # Try to extract JSON from response
                content = response["content"]
                # Remove markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                extracted = json.loads(content.strip())
                return extracted
            except Exception as e:
                logger.error(f"Error parsing GPT-4o response: {e}")
                return {}
        
        return {}
    
    def analyze_with_gpt4o(self, text: str, analysis_prompt: str) -> Dict[str, Any]:
        """
        Analyze document using GPT-4o
        
        Args:
            text: Document text
            analysis_prompt: Prompt for analysis
            
        Returns:
            Analysis results
        """
        messages = [
            {
                "role": "user",
                "content": f"{analysis_prompt}\n\nDocument Text:\n{text}"
            }
        ]
        
        response = self.call_gpt4o(messages)
        
        if response:
            return {
                "analysis": response.get("content", ""),
                "usage": response.get("usage", {})
            }
        
        return {}





