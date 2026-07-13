"""
Node definitions for the dental business AI agent using LangGraph.
Each node represents a business step in the workflow.
"""

from agents.state import DentalAgentState, Message
from agents.tools import DentalTools
from typing import Dict, Any
from datetime import datetime


class DentalAgentNodes:
    """牙科业务Agent的所有Node定义"""
    
    # ==================== Node 1: Intent Recognition ====================
    @staticmethod
    def node_intent_recognition(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 1: 识别用户意图
        
        输入 State:
            - messages: 用户消息列表
            
        输出 State:
            - intent: 识别的用户意图
            - current_step: 更新为 "intent_recognition"
            - completed_steps: 添加 "intent_recognition"
            
        成功流向: 下一个 node
        失败流向: error_handling node
        """
        print("���� Node 1: Intent Recognition - 识别用户意图")
        
        try:
            # TODO: 实现意图识别逻辑
            # 可以使用 LLM 或规则引擎识别
            intent = "create_case"  # 示例
            
            return {
                "intent": intent,
                "current_step": "intent_recognition",
                "completed_steps": state.get("completed_steps", []) + ["intent_recognition"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling"
            }
    
    # ==================== Node 2: Collect Patient Info ====================
    @staticmethod
    def node_collect_patient_info(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 2: 收集患者信息
        
        输入 State:
            - messages: 用户消息
            - intent: 用户意图
            
        输出 State:
            - patient_info: 提取的患者信息 {name, phone}
            - current_step: 更新为 "collect_patient_info"
            - completed_steps: 添加 "collect_patient_info"
            
        成功流向: query_patient node
        失败流向: error_handling node
        """
        print("👤 Node 2: Collect Patient Info - 收集患者信息")
        
        try:
            # TODO: 实现从消息中提取患者信息的逻辑
            # 可以使用 LLM 的 extraction 能力
            patient_info = {
                "name": "张三",      # 示例
                "phone": "13800138000"
            }
            
            return {
                "patient_info": patient_info,
                "current_step": "collect_patient_info",
                "completed_steps": state.get("completed_steps", []) + ["collect_patient_info"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling"
            }
    
    # ==================== Node 3: Query Patient ====================
    @staticmethod
    def node_query_patient(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 3: 查询患者是否存在
        
        输入 State:
            - patient_info: 患者信息 {name, phone}
            
        输出 State:
            - patient_exists: 患者是否存在
            - patient_code: 如果存在，获取患者代码
            - tool_result: 工具执行结果
            - current_step: 更新为 "query_patient"
            - completed_steps: 添加 "query_patient"
            
        成功流向: create_case node (根据 patient_exists 决定是否需要其他步骤)
        失败流向: error_handling node
        """
        print("🔎 Node 3: Query Patient - 查询患者")
        
        try:
            patient_info = state.get("patient_info", {})
            name = patient_info.get("name", "")
            phone = patient_info.get("phone", "")
            
            # 调用工具查询患者
            result = DentalTools.get_patients_by_name_and_phone(name, phone)
            
            return {
                "patient_exists": result.get("exists", False),
                "patient_code": result.get("patient_code", ""),
                "tool_result": result,
                "current_step": "query_patient",
                "completed_steps": state.get("completed_steps", []) + ["query_patient"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling",
                "tool_result": {"success": False, "error": str(e)}
            }
    
    # ==================== Node 4: Create Case ====================
    @staticmethod
    def node_create_case(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 4: 创建病例
        
        输入 State:
            - patient_code: 患者代码
            
        输出 State:
            - case_code: 创建的病例代码
            - tool_result: 工具执行结果
            - current_step: 更新为 "create_case"
            - completed_steps: 添加 "create_case"
            
        成功流向: ask_continue_order node
        失败流向: error_handling node
        """
        print("📋 Node 4: Create Case - 创建病例")
        
        try:
            patient_code = state.get("patient_code", "")
            
            if not patient_code:
                raise ValueError("患者代码不能为空")
            
            # 调用工具创建病例
            result = DentalTools.case_add(patient_code)
            
            return {
                "case_code": result.get("case_code", ""),
                "tool_result": result,
                "current_step": "create_case",
                "completed_steps": state.get("completed_steps", []) + ["create_case"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling",
                "tool_result": {"success": False, "error": str(e)}
            }
    
    # ==================== Node 5: Ask Continue Order ====================
    @staticmethod
    def node_ask_continue_order(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 5: 询问是否继续创建订单
        
        输入 State:
            - messages: 用户消息
            
        输出 State:
            - should_continue: 用户是否想继续
            - current_step: 更新为 "ask_continue_order"
            - completed_steps: 添加 "ask_continue_order"
            
        成功流向: 
            - 如果 should_continue=True: get_product_list node
            - 如果 should_continue=False: finish node
        失败流向: error_handling node
        """
        print("❓ Node 5: Ask Continue Order - 询问是否继续")
        
        try:
            # TODO: 实现询问逻辑
            # 可以使用 LLM 与用户交互
            should_continue = True  # 示例：默认继续
            
            return {
                "should_continue": should_continue,
                "current_step": "ask_continue_order",
                "completed_steps": state.get("completed_steps", []) + ["ask_continue_order"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling"
            }
    
    # ==================== Node 6: Get Product List ====================
    @staticmethod
    def node_get_product_list(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 6: 获取产品列表
        
        输入 State:
            (无特殊输入)
            
        输出 State:
            - product_list: 产品列表
            - tool_result: 工具执行结果
            - current_step: 更新为 "get_product_list"
            - completed_steps: 添加 "get_product_list"
            
        成功流向: collect_order_info node
        失败流向: error_handling node
        """
        print("📦 Node 6: Get Product List - 获取产品列表")
        
        try:
            # 调用工具获取产品列表
            result = DentalTools.get_product_list()
            
            return {
                "product_list": result.get("products", []),
                "tool_result": result,
                "current_step": "get_product_list",
                "completed_steps": state.get("completed_steps", []) + ["get_product_list"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling",
                "tool_result": {"success": False, "error": str(e)}
            }
    
    # ==================== Node 7: Collect Order Info ====================
    @staticmethod
    def node_collect_order_info(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 7: 收集订单信息
        
        输入 State:
            - messages: 用户消息
            - product_list: 产品列表
            
        输出 State:
            - order_info: 订单信息 {products, total_price, notes}
            - current_step: 更新为 "collect_order_info"
            - completed_steps: 添加 "collect_order_info"
            
        成功流向: create_order node
        失败流向: error_handling node
        """
        print("🛒 Node 7: Collect Order Info - 收集订单信息")
        
        try:
            # TODO: 实现从消息中提取订单信息的逻辑
            order_info = {
                "products": [],  # 示例：从消息中解析选择的产品
                "total_price": 0.0,
                "notes": ""
            }
            
            return {
                "order_info": order_info,
                "current_step": "collect_order_info",
                "completed_steps": state.get("completed_steps", []) + ["collect_order_info"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling"
            }
    
    # ==================== Node 8: Create Order ====================
    @staticmethod
    def node_create_order(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 8: 创建订单
        
        输入 State:
            - patient_code: 患者代码
            - case_code: 病例代码
            - order_info: 订单信息
            
        输出 State:
            - order_code: 创建的订单代码
            - tool_result: 工具执行结果
            - current_step: 更新为 "create_order"
            - completed_steps: 添加 "create_order"
            
        成功流向: finish node
        失败流向: error_handling node
        """
        print("✅ Node 8: Create Order - 创建订单")
        
        try:
            patient_code = state.get("patient_code", "")
            case_code = state.get("case_code", "")
            order_info = state.get("order_info", {})
            
            if not patient_code or not case_code:
                raise ValueError("患者代码或病例代码不能为空")
            
            # 调用工具创建订单
            result = DentalTools.case_order_add(
                patient_code=patient_code,
                case_code=case_code,
                products=order_info.get("products", []),
                total_price=order_info.get("total_price", 0.0),
                notes=order_info.get("notes", "")
            )
            
            return {
                "order_code": result.get("order_code", ""),
                "tool_result": result,
                "current_step": "create_order",
                "completed_steps": state.get("completed_steps", []) + ["create_order"],
                "error_message": ""
            }
        except Exception as e:
            return {
                "error_message": str(e),
                "current_step": "error_handling",
                "tool_result": {"success": False, "error": str(e)}
            }
    
    # ==================== Node 9: Finish ====================
    @staticmethod
    def node_finish(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 9: 完成流程
        
        输入 State:
            - patient_code: 患者代码
            - case_code: 病例代码
            - order_code: 订单代码 (可选)
            
        输出 State:
            - messages: 添加完成消息
            - current_step: 更新为 "finish"
            
        流向: 结束
        """
        print("🎉 Node 9: Finish - 流程完成")
        
        # 构建完成消息
        message = f"""
流程完成！
- 患者代码: {state.get("patient_code", "N/A")}
- 病例代码: {state.get("case_code", "N/A")}
- 订单代码: {state.get("order_code", "N/A")}
"""
        
        messages = state.get("messages", [])
        messages.append({
            "role": "assistant",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "messages": messages,
            "current_step": "finish",
            "completed_steps": state.get("completed_steps", []) + ["finish"]
        }
    
    # ==================== Node 10: Error Handling ====================
    @staticmethod
    def node_error_handling(state: DentalAgentState) -> Dict[str, Any]:
        """
        Node 10: 错误处理
        
        输入 State:
            - error_message: 错误信息
            - current_step: 当前步骤
            
        输出 State:
            - messages: 添加错误消息
            - current_step: 更新为 "error_handling"
            
        流向: 结束或重试
        """
        print("❌ Node 10: Error Handling - 错误处理")
        
        error_msg = state.get("error_message", "未知错误")
        
        message = f"发生错误: {error_msg}"
        
        messages = state.get("messages", [])
        messages.append({
            "role": "assistant",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "messages": messages,
            "current_step": "error_handling"
        }
