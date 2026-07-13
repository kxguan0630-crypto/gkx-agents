"""
LLM Integration module for the dental business AI agent.
Supports OpenAI, Anthropic, and other LLM providers.
"""

from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import os
from datetime import datetime


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "", temperature: float = 0.7):
        """Initialize LLM provider"""
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
    
    @abstractmethod
    def invoke(self, prompt: str, **kwargs) -> str:
        """Call the LLM and return the response"""
        pass
    
    @abstractmethod
    def extract_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Extract JSON from LLM response"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM Provider (GPT-4, GPT-3.5-turbo, etc.)"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", temperature: float = 0.7):
        """Initialize OpenAI provider"""
        super().__init__(api_key or os.getenv("OPENAI_API_KEY"), model, temperature)
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("Please install openai: pip install openai")
    
    def invoke(self, prompt: str, **kwargs) -> str:
        """Call OpenAI API"""
        messages = kwargs.get("messages", [{"role": "user", "content": prompt}])
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=kwargs.get("max_tokens", 2000),
        )
        
        return response.choices[0].message.content
    
    def extract_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Extract JSON from LLM response using function calling"""
        import json
        
        response_text = self.invoke(prompt, **kwargs)
        
        # Try to parse JSON from response
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Extract JSON from markdown code block
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            else:
                raise ValueError(f"Could not extract JSON from response: {response_text}")


class AnthropicProvider(LLMProvider):
    """Anthropic LLM Provider (Claude)"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-opus-20240229", temperature: float = 0.7):
        """Initialize Anthropic provider"""
        super().__init__(api_key or os.getenv("ANTHROPIC_API_KEY"), model, temperature)
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("Please install anthropic: pip install anthropic")
    
    def invoke(self, prompt: str, **kwargs) -> str:
        """Call Anthropic API"""
        messages = kwargs.get("messages", [{"role": "user", "content": prompt}])
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 2000),
            messages=messages,
            temperature=self.temperature,
        )
        
        return response.content[0].text
    
    def extract_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Extract JSON from LLM response"""
        import json
        
        response_text = self.invoke(prompt, **kwargs)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            else:
                raise ValueError(f"Could not extract JSON from response: {response_text}")


class LLMFactory:
    """Factory class for creating LLM providers"""
    
    @staticmethod
    def create(provider: str = "openai", **kwargs) -> LLMProvider:
        """Create an LLM provider instance"""
        
        providers = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "claude": AnthropicProvider,  # Alias for Anthropic
        }
        
        if provider.lower() not in providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(providers.keys())}")
        
        return providers[provider.lower()](**kwargs)


class LLMIntegration:
    """Integration layer for using LLM in Agent nodes"""
    
    def __init__(self, provider: str = "openai", **kwargs):
        """Initialize LLM integration"""
        self.llm = LLMFactory.create(provider, **kwargs)
    
    def recognize_intent(self, user_message: str) -> str:
        """
        Recognize user intent from message
        
        输入:
            user_message: User input message
            
        输出:
            intent: Recognized intent (e.g., "create_case", "query_order")
        """
        prompt = f"""
You are a helpful dental assistant. Analyze the user's message and identify their intent.

User message: "{user_message}"

Possible intents: create_case, query_order, cancel_order, modify_case, other

Respond with ONLY the intent name, nothing else.
"""
        
        intent = self.llm.invoke(prompt).strip().lower()
        
        # Validate intent
        valid_intents = ["create_case", "query_order", "cancel_order", "modify_case", "other"]
        if intent not in valid_intents:
            intent = "other"
        
        return intent
    
    def extract_patient_info(self, user_message: str) -> Dict[str, str]:
        """
        Extract patient information from user message
        
        输入:
            user_message: User input message
            
        输出:
            patient_info: Extracted info {name, phone, email, etc.}
        """
        prompt = f"""
Extract patient information from the following message. Return as JSON.

Message: "{user_message}"

Extract these fields if available:
- name: Patient name
- phone: Phone number
- email: Email address
- age: Age
- gender: Gender (M/F/Other)

Return ONLY valid JSON, no other text. If a field is not available, omit it or set to null.
"""
        
        try:
            result = self.llm.extract_json(prompt)
            # Filter out None/null values
            return {k: v for k, v in result.items() if v}
        except:
            # Fallback: return empty dict if extraction fails
            return {}
    
    def extract_order_info(self, user_message: str, product_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract order information from user message
        
        输入:
            user_message: User input message
            product_list: List of available products
            
        输出:
            order_info: Extracted order {products, quantity, total_price, notes}
        """
        products_str = "\n".join([f"- {p['name']}: ${p['price']}" for p in product_list])
        
        prompt = f"""
Extract order information from the user message. Return as JSON.

Available products:
{products_str}

User message: "{user_message}"

Extract these fields:
- products: List of selected product names
- quantities: Corresponding quantities for each product
- total_price: Total price (calculate from product prices)
- notes: Any special requests or notes

Return ONLY valid JSON with these exact fields. If products list is empty, set to [].
"""
        
        try:
            result = self.llm.extract_json(prompt)
            
            # Validate and calculate total_price if needed
            if "products" not in result:
                result["products"] = []
            if "quantities" not in result:
                result["quantities"] = []
            if "total_price" not in result:
                result["total_price"] = 0.0
            if "notes" not in result:
                result["notes"] = ""
            
            return result
        except:
            return {
                "products": [],
                "quantities": [],
                "total_price": 0.0,
                "notes": ""
            }
    
    def generate_response(self, context: str, state: Dict[str, Any]) -> str:
        """
        Generate a natural language response to the user
        
        输入:
            context: Context/template for response
            state: Current agent state
            
        输出:
            response: Generated response text
        """
        prompt = f"""
You are a helpful dental clinic assistant. Generate a friendly and professional response.

Context: {context}

Patient info: {state.get('patient_info', {})}
Patient code: {state.get('patient_code', 'N/A')}
Case code: {state.get('case_code', 'N/A')}
Order code: {state.get('order_code', 'N/A')}

Generate a short, friendly response message.
"""
        
        return self.llm.invoke(prompt).strip()
    
    def should_continue_order(self, messages: List[Dict[str, str]]) -> bool:
        """
        Determine if user wants to continue with order creation
        
        输入:
            messages: Message history
            
        输出:
            should_continue: Boolean indicating if user wants to continue
        """
        recent_messages = "\n".join([m.get("content", "") for m in messages[-3:]])
        
        prompt = f"""
Based on the user's recent messages, do they want to continue creating an order?

Recent messages:
{recent_messages}

Respond with ONLY "yes" or "no", nothing else.
"""
        
        response = self.llm.invoke(prompt).strip().lower()
        return response.startswith("yes")


# Convenience functions
def get_llm_provider(provider: str = "openai", **kwargs) -> LLMProvider:
    """Get an LLM provider instance"""
    return LLMFactory.create(provider, **kwargs)


def get_llm_integration(provider: str = "openai", **kwargs) -> LLMIntegration:
    """Get an LLM integration instance"""
    return LLMIntegration(provider, **kwargs)
