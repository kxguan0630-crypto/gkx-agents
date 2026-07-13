"""
Graph definition for the dental business AI agent using LangGraph.
Defines the workflow structure, edges, and conditional routing.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agents.state import DentalAgentState
from agents.nodes import DentalAgentNodes
from typing import Literal


class DentalAgentGraph:
    """牙科业务Agent的Graph定义"""
    
    def __init__(self):
        """初始化Graph"""
        self.graph = StateGraph(DentalAgentState)
        self.setup_nodes()
        self.setup_edges()
        self.checkpointer = MemorySaver()
    
    def setup_nodes(self):
        """添加所有Node到Graph"""
        print("📍 设置 Nodes...")
        
        # 添加所有节点
        self.graph.add_node("intent_recognition", DentalAgentNodes.node_intent_recognition)
        self.graph.add_node("collect_patient_info", DentalAgentNodes.node_collect_patient_info)
        self.graph.add_node("query_patient", DentalAgentNodes.node_query_patient)
        self.graph.add_node("create_case", DentalAgentNodes.node_create_case)
        self.graph.add_node("ask_continue_order", DentalAgentNodes.node_ask_continue_order)
        self.graph.add_node("get_product_list", DentalAgentNodes.node_get_product_list)
        self.graph.add_node("collect_order_info", DentalAgentNodes.node_collect_order_info)
        self.graph.add_node("create_order", DentalAgentNodes.node_create_order)
        self.graph.add_node("finish", DentalAgentNodes.node_finish)
        self.graph.add_node("error_handling", DentalAgentNodes.node_error_handling)
        
        print("✅ Nodes 设置完成")
    
    def setup_edges(self):
        """设置Edge和条件路由"""
        print("📍 设置 Edges...")
        
        # ==================== 主流程边 ====================
        
        # 1. START -> intent_recognition
        self.graph.add_edge(START, "intent_recognition")
        
        # 2. intent_recognition -> collect_patient_info
        self.graph.add_edge("intent_recognition", "collect_patient_info")
        
        # 3. collect_patient_info -> query_patient
        self.graph.add_edge("collect_patient_info", "query_patient")
        
        # 4. query_patient -> create_case
        # (无论患者是否存在，都继续创建病例)
        self.graph.add_edge("query_patient", "create_case")
        
        # 5. create_case -> ask_continue_order
        self.graph.add_edge("create_case", "ask_continue_order")
        
        # ==================== 条件边：是否继续创建订单 ====================
        # 6. ask_continue_order -> (条件路由)
        self.graph.add_conditional_edges(
            "ask_continue_order",
            self._should_continue_order,
            {
                "yes": "get_product_list",
                "no": "finish"
            }
        )
        
        # 7. get_product_list -> collect_order_info
        self.graph.add_edge("get_product_list", "collect_order_info")
        
        # 8. collect_order_info -> create_order
        self.graph.add_edge("collect_order_info", "create_order")
        
        # 9. create_order -> finish
        self.graph.add_edge("create_order", "finish")
        
        # ==================== 错误处理边 ====================
        # 所有可能发生错误的node都可以流向 error_handling
        # 通过在每个node中设置 current_step = "error_handling" 来触发
        
        # finish -> END
        self.graph.add_edge("finish", END)
        
        # error_handling -> END
        self.graph.add_edge("error_handling", END)
        
        print("✅ Edges 设置完成")
    
    def _should_continue_order(self, state: DentalAgentState) -> Literal["yes", "no"]:
        """
        条件边：判断是否继续创建订单
        
        输入: state.should_continue
        输出: "yes" 或 "no"
        """
        should_continue = state.get("should_continue", False)
        return "yes" if should_continue else "no"
    
    def compile(self):
        """编译Graph成可执行的Graph"""
        print("📍 编译 Graph...")
        
        compiled_graph = self.graph.compile(
            checkpointer=self.checkpointer,
            interrupt_before=["ask_continue_order"],  # 在某个node前中断，等待人工确认
        )
        
        print("✅ Graph 编译完成")
        return compiled_graph


def create_dental_agent_graph():
    """
    工厂函数：创建并返回编译后的 Dental Agent Graph
    
    返回:
        compiled_graph: 可以直接使用的LangGraph Graph
    """
    agent_graph = DentalAgentGraph()
    return agent_graph.compile()


# ==================== Graph 配置常量 ====================

GRAPH_CONFIG = {
    "nodes": [
        {
            "name": "intent_recognition",
            "description": "识别用户意图",
            "inputs": ["messages"],
            "outputs": ["intent", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "collect_patient_info",
            "description": "收集患者信息",
            "inputs": ["messages", "intent"],
            "outputs": ["patient_info", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "query_patient",
            "description": "查询患者是否存在",
            "inputs": ["patient_info"],
            "outputs": ["patient_exists", "patient_code", "tool_result", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "create_case",
            "description": "创建病例",
            "inputs": ["patient_code"],
            "outputs": ["case_code", "tool_result", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "ask_continue_order",
            "description": "询问是否继续创建订单",
            "inputs": ["messages"],
            "outputs": ["should_continue", "current_step", "completed_steps"],
            "conditional": True
        },
        {
            "name": "get_product_list",
            "description": "获取产品列表",
            "inputs": [],
            "outputs": ["product_list", "tool_result", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "collect_order_info",
            "description": "收集订单信息",
            "inputs": ["messages", "product_list"],
            "outputs": ["order_info", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "create_order",
            "description": "创建订单",
            "inputs": ["patient_code", "case_code", "order_info"],
            "outputs": ["order_code", "tool_result", "current_step", "completed_steps"],
            "error_handling": True
        },
        {
            "name": "finish",
            "description": "流程完成",
            "inputs": ["patient_code", "case_code", "order_code"],
            "outputs": ["messages", "current_step", "completed_steps"]
        },
        {
            "name": "error_handling",
            "description": "错误处理",
            "inputs": ["error_message", "current_step"],
            "outputs": ["messages", "current_step"]
        }
    ],
    "edges": [
        {"from": "START", "to": "intent_recognition", "type": "edge"},
        {"from": "intent_recognition", "to": "collect_patient_info", "type": "edge"},
        {"from": "collect_patient_info", "to": "query_patient", "type": "edge"},
        {"from": "query_patient", "to": "create_case", "type": "edge"},
        {"from": "create_case", "to": "ask_continue_order", "type": "edge"},
        {"from": "ask_continue_order", "to": "get_product_list", "type": "conditional", "condition": "should_continue == True"},
        {"from": "ask_continue_order", "to": "finish", "type": "conditional", "condition": "should_continue == False"},
        {"from": "get_product_list", "to": "collect_order_info", "type": "edge"},
        {"from": "collect_order_info", "to": "create_order", "type": "edge"},
        {"from": "create_order", "to": "finish", "type": "edge"},
        {"from": "finish", "to": "END", "type": "edge"},
        {"from": "error_handling", "to": "END", "type": "edge"}
    ]
}
