"""
Main entry point for the dental business AI agent.
Initializes and runs the LangGraph-based agent.
"""

import asyncio
from typing import Dict, Any
from agents.graph import create_dental_agent_graph
from agents.state import DentalAgentState


class DentalAgent:
    """牙科业务AI Agent主类"""
    
    def __init__(self):
        """初始化Agent"""
        print("🚀 初始化牙科业务 AI Agent...")
        self.graph = create_dental_agent_graph()
        print("✅ Agent 初始化完成\n")
    
    def run(self, user_input: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        运行Agent
        
        输入:
            user_input: 用户输入
            thread_id: 对话线程ID（用于多轮对话和Checkpoint）
            
        输出:
            最终的 State 字典
        """
        print(f"📨 用户输入: {user_input}\n")
        
        # 构建初始State
        initial_state: DentalAgentState = {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                    "timestamp": None
                }
            ],
            "intent": "",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "start",
            "completed_steps": [],
            "tool_result": {},
            "error_message": "",
            "should_continue": False,
            "context": {}
        }
        
        # 运行Graph
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # 同步运行
            final_state = self.graph.invoke(initial_state, config)
            
            print("\n" + "="*60)
            print("✅ Agent 执行完成")
            print("="*60)
            print(f"📊 流程步骤: {' → '.join(final_state.get('completed_steps', []))}")
            print(f"💾 最终状态: {final_state.get('current_step', 'unknown')}")
            
            if final_state.get("patient_code"):
                print(f"👤 患者代码: {final_state.get('patient_code')}")
            if final_state.get("case_code"):
                print(f"📋 病例代码: {final_state.get('case_code')}")
            if final_state.get("order_code"):
                print(f"🛒 订单代码: {final_state.get('order_code')}")
            
            # 打印最后的消息
            messages = final_state.get("messages", [])
            if messages:
                last_message = messages[-1]
                print(f"\n💬 Agent 回复:")
                print(last_message.get("content", ""))
            
            print("="*60 + "\n")
            
            return final_state
            
        except Exception as e:
            print(f"\n❌ Agent 执行出错: {str(e)}")
            raise
    
    async def run_async(self, user_input: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        异步运行Agent
        
        输入:
            user_input: 用户输入
            thread_id: 对话线程ID
            
        输出:
            最终的 State 字典
        """
        print(f"📨 用户输入: {user_input}\n")
        
        # 构建初始State
        initial_state: DentalAgentState = {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                    "timestamp": None
                }
            ],
            "intent": "",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "start",
            "completed_steps": [],
            "tool_result": {},
            "error_message": "",
            "should_continue": False,
            "context": {}
        }
        
        # 运行Graph
        config = {"configurable": {"thread_id": thread_id}}
        
        try:
            # 异步运行
            final_state = await asyncio.to_thread(
                self.graph.invoke, 
                initial_state, 
                config
            )
            
            return final_state
            
        except Exception as e:
            print(f"\n❌ Agent 异步执行出错: {str(e)}")
            raise


def main():
    """主函数：演示Agent使用"""
    print("\n" + "="*60)
    print("🦷 牙科业务 AI Agent 演示")
    print("="*60 + "\n")
    
    # 创建Agent实例
    agent = DentalAgent()
    
    # 示例1：创建病例和订单
    print("【示例1】创建病例和订单\n")
    user_input_1 = "帮我创建一个新的病例。患者叫张三，手机号是13800138000。"
    state_1 = agent.run(user_input_1, thread_id="conversation_1")
    
    # 示例2：只创建病例，不创建订单
    print("\n【示例2】只创建病例\n")
    user_input_2 = "我想创建李四的病例。李四的手机号是13900139000。"
    state_2 = agent.run(user_input_2, thread_id="conversation_2")
    
    print("\n✅ 所有示例执行完成！")


if __name__ == "__main__":
    main()
