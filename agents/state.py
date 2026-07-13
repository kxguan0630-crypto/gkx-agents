"""
State definition for the dental business AI agent using TypedDict.
"""

from typing import TypedDict, List, Dict, Any, Optional


class PatientInfo(TypedDict, total=False):
    """患者信息"""
    name: str
    phone: str
    age: Optional[int]
    gender: Optional[str]
    notes: Optional[str]


class OrderInfo(TypedDict, total=False):
    """订单信息"""
    patient_code: str
    case_code: str
    products: List[Dict[str, Any]]
    total_price: float
    notes: Optional[str]


class ToolResult(TypedDict, total=False):
    """工具执行结果"""
    success: bool
    data: Any
    error: Optional[str]


class Message(TypedDict, total=False):
    """消息"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str]


class DentalAgentState(TypedDict, total=False):
    """
    牙科业务AI Agent的完整State定义
    
    包含：
    - 消息历史
    - 用户意图
    - 患者信息
    - 案例信息
    - 订单信息
    - 流程控制
    - 错误处理
    """
    
    # 消息相关
    messages: List[Message]
    
    # 意图识别
    intent: str  # "create_case", "create_order", "query_patient", etc.
    
    # 患者信息
    patient_info: PatientInfo
    patient_exists: bool
    patient_code: str
    
    # 案例信息
    case_code: str
    
    # 订单信息
    order_code: str
    order_info: OrderInfo
    
    # 产品列表
    product_list: List[Dict[str, Any]]
    
    # 流程控制
    current_step: str  # 当前步骤
    completed_steps: List[str]  # 已完成步骤
    
    # 工具执行结果
    tool_result: ToolResult
    
    # 错误处理
    error_message: str
    should_continue: bool  # 是否继续流程
    
    # 其他
    context: Dict[str, Any]  # 上下文信息
