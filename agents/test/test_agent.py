"""
Unit tests for the dental business AI agent.
Tests for state, nodes, graph, and main agent functionality.
"""

import pytest
from agents import DentalAgent, DentalAgentState
from agents.nodes import DentalAgentNodes
from agents.graph import create_dental_agent_graph
from datetime import datetime


class TestDentalAgentState:
    """Test DentalAgentState definition"""
    
    def test_state_initialization(self):
        """Test state can be initialized with default values"""
        state: DentalAgentState = {
            "messages": [],
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
        
        assert state["intent"] == ""
        assert state["current_step"] == "start"
        assert state["completed_steps"] == []
    
    def test_state_message_addition(self):
        """Test adding messages to state"""
        state: DentalAgentState = {
            "messages": [
                {"role": "user", "content": "hello", "timestamp": None}
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
        
        assert len(state["messages"]) == 1
        assert state["messages"][0]["role"] == "user"


class TestDentalAgentNodes:
    """Test individual nodes"""
    
    def test_node_intent_recognition(self):
        """Test intent recognition node"""
        state: DentalAgentState = {
            "messages": [{"role": "user", "content": "create case", "timestamp": None}],
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
        
        result = DentalAgentNodes.node_intent_recognition(state)
        
        assert "intent" in result
        assert "current_step" in result
        assert result["current_step"] == "intent_recognition"
        assert "intent_recognition" in result["completed_steps"]
    
    def test_node_collect_patient_info(self):
        """Test patient info collection node"""
        state: DentalAgentState = {
            "messages": [
                {"role": "user", "content": "Patient is John, phone 123456789", "timestamp": None}
            ],
            "intent": "create_case",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "intent_recognition",
            "completed_steps": ["intent_recognition"],
            "tool_result": {},
            "error_message": "",
            "should_continue": False,
            "context": {}
        }
        
        result = DentalAgentNodes.node_collect_patient_info(state)
        
        assert "patient_info" in result
        assert "current_step" in result
        assert result["current_step"] == "collect_patient_info"
    
    def test_node_finish(self):
        """Test finish node"""
        state: DentalAgentState = {
            "messages": [],
            "intent": "create_case",
            "patient_info": {"name": "John", "phone": "123456"},
            "patient_exists": True,
            "patient_code": "P001",
            "case_code": "C001",
            "order_code": "O001",
            "order_info": {},
            "product_list": [],
            "current_step": "create_order",
            "completed_steps": ["intent_recognition", "collect_patient_info"],
            "tool_result": {},
            "error_message": "",
            "should_continue": False,
            "context": {}
        }
        
        result = DentalAgentNodes.node_finish(state)
        
        assert "messages" in result
        assert len(result["messages"]) > 0
        assert result["current_step"] == "finish"
        assert "finish" in result["completed_steps"]


class TestDentalAgentGraph:
    """Test graph structure and compilation"""
    
    def test_graph_creation(self):
        """Test graph can be created and compiled"""
        graph = create_dental_agent_graph()
        
        assert graph is not None
        # Graph should have invoke method
        assert hasattr(graph, "invoke")
    
    def test_graph_invoke_simple(self):
        """Test graph can be invoked with simple input"""
        graph = create_dental_agent_graph()
        
        initial_state: DentalAgentState = {
            "messages": [{"role": "user", "content": "test", "timestamp": None}],
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
        
        config = {"configurable": {"thread_id": "test_1"}}
        
        # This should not raise an error
        result = graph.invoke(initial_state, config)
        
        assert result is not None
        assert "current_step" in result


class TestDentalAgent:
    """Test main DentalAgent class"""
    
    def test_agent_initialization(self):
        """Test agent can be initialized"""
        agent = DentalAgent()
        
        assert agent is not None
        assert agent.graph is not None
    
    def test_agent_run_method_exists(self):
        """Test agent has run method"""
        agent = DentalAgent()
        
        assert hasattr(agent, "run")
        assert callable(agent.run)
    
    def test_agent_run_simple(self):
        """Test agent can run with simple input"""
        agent = DentalAgent()
        
        result = agent.run(
            user_input="Create a case for John",
            thread_id="test_conversation_1"
        )
        
        assert result is not None
        assert "current_step" in result
        assert "completed_steps" in result
    
    def test_agent_run_with_patient_code(self):
        """Test agent produces patient code"""
        agent = DentalAgent()
        
        result = agent.run(
            user_input="Create a case",
            thread_id="test_conversation_2"
        )
        
        # After running, should have completed at least intent_recognition
        assert len(result["completed_steps"]) > 0


class TestConditionalEdge:
    """Test conditional edge logic"""
    
    def test_should_continue_yes(self):
        """Test conditional returns 'yes' when should_continue is True"""
        from agents.graph import DentalAgentGraph
        
        graph_obj = DentalAgentGraph()
        
        state: DentalAgentState = {
            "should_continue": True,
            "messages": [],
            "intent": "",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "ask_continue_order",
            "completed_steps": [],
            "tool_result": {},
            "error_message": "",
            "context": {}
        }
        
        result = graph_obj._should_continue_order(state)
        
        assert result == "yes"
    
    def test_should_continue_no(self):
        """Test conditional returns 'no' when should_continue is False"""
        from agents.graph import DentalAgentGraph
        
        graph_obj = DentalAgentGraph()
        
        state: DentalAgentState = {
            "should_continue": False,
            "messages": [],
            "intent": "",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "ask_continue_order",
            "completed_steps": [],
            "tool_result": {},
            "error_message": "",
            "context": {}
        }
        
        result = graph_obj._should_continue_order(state)
        
        assert result == "no"


class TestErrorHandling:
    """Test error handling in nodes"""
    
    def test_node_error_handling(self):
        """Test error handling node"""
        state: DentalAgentState = {
            "messages": [],
            "intent": "",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "query_patient",
            "completed_steps": [],
            "tool_result": {},
            "error_message": "Patient not found",
            "should_continue": False,
            "context": {}
        }
        
        result = DentalAgentNodes.node_error_handling(state)
        
        assert "messages" in result
        assert len(result["messages"]) > 0
        assert result["current_step"] == "error_handling"
    
    def test_node_with_exception(self):
        """Test node handles exception gracefully"""
        state: DentalAgentState = {
            "messages": [],
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
        
        # Create case node without patient_code should produce error
        result = DentalAgentNodes.node_create_case(state)
        
        assert "error_message" in result
        assert result["error_message"] != ""


class TestStateTransition:
    """Test state transitions through the workflow"""
    
    def test_state_after_intent_recognition(self):
        """Test state is correctly updated after intent recognition"""
        state: DentalAgentState = {
            "messages": [{"role": "user", "content": "test", "timestamp": None}],
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
        
        result = DentalAgentNodes.node_intent_recognition(state)
        
        assert result["current_step"] == "intent_recognition"
        assert "intent_recognition" in result["completed_steps"]
        assert result["intent"] != ""
    
    def test_completed_steps_accumulation(self):
        """Test completed_steps accumulates correctly"""
        state: DentalAgentState = {
            "messages": [{"role": "user", "content": "test", "timestamp": None}],
            "intent": "",
            "patient_info": {},
            "patient_exists": False,
            "patient_code": "",
            "case_code": "",
            "order_code": "",
            "order_info": {},
            "product_list": [],
            "current_step": "start",
            "completed_steps": ["step1"],
            "tool_result": {},
            "error_message": "",
            "should_continue": False,
            "context": {}
        }
        
        result = DentalAgentNodes.node_intent_recognition(state)
        
        assert len(result["completed_steps"]) >= 2
        assert "step1" in result["completed_steps"]
        assert "intent_recognition" in result["completed_steps"]


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
