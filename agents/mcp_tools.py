"""
MCP (Model Context Protocol) Tool Integration for the dental business AI agent.
Provides standardized tool definitions and execution for external service integration.
"""

from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import json


class ToolType(Enum):
    """Tool type enumeration"""
    API = "api"
    DATABASE = "database"
    EXTERNAL_SERVICE = "external_service"
    INTERNAL_FUNCTION = "internal_function"


@dataclass
class ToolParameter:
    """Tool parameter definition"""
    name: str
    type: str  # "string", "integer", "boolean", "array", "object"
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


@dataclass
class ToolResult:
    """Tool execution result"""
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: Optional[float] = None


class Tool(ABC):
    """Abstract base class for MCP tools"""
    
    def __init__(self, name: str, description: str, tool_type: ToolType = ToolType.INTERNAL_FUNCTION):
        """Initialize tool"""
        self.name = name
        self.description = description
        self.tool_type = tool_type
        self.parameters: List[ToolParameter] = []
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        pass
    
    def add_parameter(self, param: ToolParameter) -> "Tool":
        """Add a parameter to the tool"""
        self.parameters.append(param)
        return self
    
    def validate_parameters(self, **kwargs) -> tuple[bool, Optional[str]]:
        """Validate input parameters"""
        for param in self.parameters:
            if param.required and param.name not in kwargs:
                return False, f"Missing required parameter: {param.name}"
            
            if param.name in kwargs:
                value = kwargs[param.name]
                
                # Type validation
                if param.type == "string" and not isinstance(value, str):
                    return False, f"Parameter {param.name} must be string"
                elif param.type == "integer" and not isinstance(value, int):
                    return False, f"Parameter {param.name} must be integer"
                elif param.type == "boolean" and not isinstance(value, bool):
                    return False, f"Parameter {param.name} must be boolean"
                
                # Range validation
                if param.min_value is not None and value < param.min_value:
                    return False, f"Parameter {param.name} must be >= {param.min_value}"
                if param.max_value is not None and value > param.max_value:
                    return False, f"Parameter {param.name} must be <= {param.max_value}"
                
                # Enum validation
                if param.enum and value not in param.enum:
                    return False, f"Parameter {param.name} must be one of: {param.enum}"
        
        return True, None
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert tool to OpenAI function schema"""
        properties = {}
        required = []
        
        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            
            if param.enum:
                properties[param.name]["enum"] = param.enum
            if param.min_value is not None:
                properties[param.name]["minimum"] = param.min_value
            if param.max_value is not None:
                properties[param.name]["maximum"] = param.max_value
            if param.default is not None:
                properties[param.name]["default"] = param.default
            
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }


class DentalTool(Tool):
    """Dental business tool"""
    
    def __init__(self, name: str, description: str, handler: Callable):
        """Initialize dental tool"""
        super().__init__(name, description, ToolType.EXTERNAL_SERVICE)
        self.handler = handler
    
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        import time
        
        # Validate parameters
        valid, error = self.validate_parameters(**kwargs)
        if not valid:
            return ToolResult(success=False, data=None, error=error)
        
        try:
            start_time = time.time()
            result = self.handler(**kwargs)
            execution_time = time.time() - start_time
            
            return ToolResult(
                success=True,
                data=result,
                execution_time=execution_time
            )
        except Exception as e:
            return ToolResult(
                success=False,
                data=None,
                error=str(e)
            )


class MCPToolRegistry:
    """Registry for managing MCP tools"""
    
    def __init__(self):
        """Initialize tool registry"""
        self.tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> "MCPToolRegistry":
        """Register a tool"""
        self.tools[tool.name] = tool
        return self
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """Execute a tool"""
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult(
                success=False,
                data=None,
                error=f"Tool not found: {tool_name}"
            )
        
        return tool.execute(**kwargs)
    
    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools"""
        return list(self.tools.values())
    
    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """Get OpenAI schemas for all tools"""
        return [tool.to_schema() for tool in self.get_all_tools()]
    
    def to_json(self) -> str:
        """Convert tool registry to JSON"""
        schemas = self.get_all_schemas()
        return json.dumps(schemas, indent=2)


class DentalMCPTools:
    """Dental business MCP tools"""
    
    def __init__(self):
        """Initialize dental MCP tools"""
        self.registry = MCPToolRegistry()
        self._register_tools()
    
    def _register_tools(self):
        """Register all dental tools"""
        # Tool 1: Query Patient
        query_patient_tool = DentalTool(
            name="query_patient",
            description="Query patient information by name and phone number",
            handler=self._query_patient_handler
        )
        query_patient_tool.add_parameter(
            ToolParameter("name", "string", "Patient name", required=True)
        ).add_parameter(
            ToolParameter("phone", "string", "Patient phone number", required=True)
        )
        self.registry.register(query_patient_tool)
        
        # Tool 2: Create Case
        create_case_tool = DentalTool(
            name="create_case",
            description="Create a new dental case for a patient",
            handler=self._create_case_handler
        )
        create_case_tool.add_parameter(
            ToolParameter("patient_code", "string", "Patient code", required=True)
        ).add_parameter(
            ToolParameter("diagnosis", "string", "Diagnosis description", required=False)
        ).add_parameter(
            ToolParameter("notes", "string", "Additional notes", required=False)
        )
        self.registry.register(create_case_tool)
        
        # Tool 3: Get Product List
        product_list_tool = DentalTool(
            name="get_product_list",
            description="Get available dental products and services",
            handler=self._get_product_list_handler
        )
        product_list_tool.add_parameter(
            ToolParameter("category", "string", "Product category (e.g., 'treatment', 'material')", 
                         required=False, enum=["treatment", "material", "all"])
        )
        self.registry.register(product_list_tool)
        
        # Tool 4: Create Order
        create_order_tool = DentalTool(
            name="create_order",
            description="Create a new order for a dental case",
            handler=self._create_order_handler
        )
        create_order_tool.add_parameter(
            ToolParameter("patient_code", "string", "Patient code", required=True)
        ).add_parameter(
            ToolParameter("case_code", "string", "Case code", required=True)
        ).add_parameter(
            ToolParameter("products", "array", "List of product names", required=True)
        ).add_parameter(
            ToolParameter("quantities", "array", "List of quantities", required=True)
        ).add_parameter(
            ToolParameter("total_price", "integer", "Total price in cents", required=True, min_value=0)
        ).add_parameter(
            ToolParameter("notes", "string", "Order notes", required=False)
        )
        self.registry.register(create_order_tool)
        
        # Tool 5: Get Order Status
        order_status_tool = DentalTool(
            name="get_order_status",
            description="Get the status of an order",
            handler=self._get_order_status_handler
        )
        order_status_tool.add_parameter(
            ToolParameter("order_code", "string", "Order code", required=True)
        )
        self.registry.register(order_status_tool)
        
        # Tool 6: Cancel Order
        cancel_order_tool = DentalTool(
            name="cancel_order",
            description="Cancel an existing order",
            handler=self._cancel_order_handler
        )
        cancel_order_tool.add_parameter(
            ToolParameter("order_code", "string", "Order code", required=True)
        ).add_parameter(
            ToolParameter("reason", "string", "Cancellation reason", required=False)
        )
        self.registry.register(cancel_order_tool)
    
    @staticmethod
    def _query_patient_handler(name: str, phone: str) -> Dict[str, Any]:
        """Handle patient query"""
        # Mock implementation
        return {
            "exists": True,
            "patient_code": "P001",
            "name": name,
            "phone": phone,
            "email": f"{name}@example.com"
        }
    
    @staticmethod
    def _create_case_handler(patient_code: str, diagnosis: Optional[str] = None, 
                            notes: Optional[str] = None) -> Dict[str, Any]:
        """Handle case creation"""
        # Mock implementation
        return {
            "success": True,
            "case_code": "C001",
            "patient_code": patient_code,
            "diagnosis": diagnosis,
            "notes": notes,
            "created_at": "2026-07-13T10:00:00Z"
        }
    
    @staticmethod
    def _get_product_list_handler(category: Optional[str] = None) -> Dict[str, Any]:
        """Handle product list retrieval"""
        # Mock implementation
        products = [
            {"id": 1, "name": "Root Canal Treatment", "price": 500, "category": "treatment"},
            {"id": 2, "name": "Crown", "price": 800, "category": "material"},
            {"id": 3, "name": "Filling", "price": 200, "category": "treatment"},
            {"id": 4, "name": "Teeth Cleaning", "price": 100, "category": "treatment"}
        ]
        
        if category and category != "all":
            products = [p for p in products if p["category"] == category]
        
        return {
            "success": True,
            "products": products,
            "count": len(products)
        }
    
    @staticmethod
    def _create_order_handler(patient_code: str, case_code: str, products: List[str],
                             quantities: List[int], total_price: int, 
                             notes: Optional[str] = None) -> Dict[str, Any]:
        """Handle order creation"""
        # Mock implementation
        return {
            "success": True,
            "order_code": "O001",
            "patient_code": patient_code,
            "case_code": case_code,
            "products": products,
            "quantities": quantities,
            "total_price": total_price / 100,  # Convert from cents to dollars
            "notes": notes,
            "status": "pending",
            "created_at": "2026-07-13T10:05:00Z"
        }
    
    @staticmethod
    def _get_order_status_handler(order_code: str) -> Dict[str, Any]:
        """Handle order status query"""
        # Mock implementation
        return {
            "success": True,
            "order_code": order_code,
            "status": "processing",
            "progress": 60
        }
    
    @staticmethod
    def _cancel_order_handler(order_code: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Handle order cancellation"""
        # Mock implementation
        return {
            "success": True,
            "order_code": order_code,
            "status": "cancelled",
            "reason": reason,
            "cancelled_at": "2026-07-13T10:10:00Z"
        }


class MCPToolIntegration:
    """Integration layer for using MCP tools in Agent"""
    
    def __init__(self):
        """Initialize MCP tool integration"""
        self.dental_tools = DentalMCPTools()
        self.registry = self.dental_tools.registry
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool and return result"""
        result = self.registry.execute_tool(tool_name, **kwargs)
        
        return {
            "tool_name": tool_name,
            "success": result.success,
            "data": result.data,
            "error": result.error,
            "execution_time": result.execution_time
        }
    
    def get_tools_for_llm(self) -> List[Dict[str, Any]]:
        """Get tool schemas for LLM function calling"""
        return self.registry.get_all_schemas()
    
    def process_tool_call(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Process a tool call from LLM"""
        print(f"🔧 Executing MCP Tool: {tool_name}")
        print(f"📦 Arguments: {tool_args}")
        
        result = self.execute_tool(tool_name, **tool_args)
        
        print(f"✅ Tool Result: {result}")
        
        return result


# Convenience functions
def get_mcp_tools() -> DentalMCPTools:
    """Get dental MCP tools instance"""
    return DentalMCPTools()


def get_mcp_integration() -> MCPToolIntegration:
    """Get MCP tool integration instance"""
    return MCPToolIntegration()
