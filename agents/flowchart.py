"""
Mermaid flowchart for the dental business AI agent workflow.
This file contains the visual representation of the agent's flow.
"""

MERMAID_FLOWCHART = """
graph TD
    START([开始]) --> IntentRecognition["🧠 意图识别<br/>intent_recognition"]
    
    IntentRecognition --> CollectPatientInfo["👤 收集患者信息<br/>collect_patient_info"]
    
    CollectPatientInfo --> QueryPatient["🔎 查询患者<br/>query_patient"]
    
    QueryPatient --> CreateCase["📋 创建病例<br/>create_case"]
    
    CreateCase --> AskContinueOrder{"❓ 是否继续创建订单?<br/>ask_continue_order"}
    
    AskContinueOrder -->|should_continue=Yes| GetProductList["📦 获取产品列表<br/>get_product_list"]
    AskContinueOrder -->|should_continue=No| Finish["🎉 流程完成<br/>finish"]
    
    GetProductList --> CollectOrderInfo["🛒 收集订单信息<br/>collect_order_info"]
    
    CollectOrderInfo --> CreateOrder["✅ 创建订单<br/>create_order"]
    
    CreateOrder --> Finish
    
    Finish --> END([结束])
    
    style START fill:#90EE90
    style END fill:#FFB6C6
    style IntentRecognition fill:#87CEEB
    style CollectPatientInfo fill:#87CEEB
    style QueryPatient fill:#87CEEB
    style CreateCase fill:#87CEEB
    style AskContinueOrder fill:#FFD700
    style GetProductList fill:#87CEEB
    style CollectOrderInfo fill:#87CEEB
    style CreateOrder fill:#87CEEB
    style Finish fill:#DDA0DD
"""

MERMAID_STATE_FLOW = """
graph LR
    subgraph "State 转移流程"
        S1["State v1<br/>messages: []<br/>intent: ''<br/>patient_info: {}"]
        
        S2["State v2<br/>+ intent: 'create_case'<br/>+ current_step"]
        
        S3["State v3<br/>+ patient_info: {name, phone}<br/>+ current_step"]
        
        S4["State v4<br/>+ patient_code: 'P001'<br/>+ patient_exists: true"]
        
        S5["State v5<br/>+ case_code: 'C001'<br/>+ current_step"]
        
        S6["State v6<br/>+ should_continue: true"]
        
        S7["State v7<br/>+ product_list: [...]<br/>+ current_step"]
        
        S8["State v8<br/>+ order_info: {...}<br/>+ current_step"]
        
        S9["State v9<br/>+ order_code: 'O001'<br/>+ current_step: 'finish'"]
        
        S1 -->|node_intent_recognition| S2
        S2 -->|node_collect_patient_info| S3
        S3 -->|node_query_patient| S4
        S4 -->|node_create_case| S5
        S5 -->|node_ask_continue_order| S6
        S6 -->|node_get_product_list| S7
        S7 -->|node_collect_order_info| S8
        S8 -->|node_create_order| S9
    end
    
    style S1 fill:#E8F4F8
    style S9 fill:#E8F8E8
"""

MERMAID_ERROR_HANDLING = """
graph TD
    AnyNode["任何Node<br/>可能发生错误"] --|异常捕获| ErrorHandling["❌ 错误处理<br/>error_handling"]
    
    ErrorHandling --> LogError["📝 记录错误信息"]
    LogError --> AddErrorMsg["添加错误消息到 messages"]
    AddErrorMsg --> END1([结束])
    
    style AnyNode fill:#FFB6C1
    style ErrorHandling fill:#FF6B6B
    style END1 fill:#FFB6C6
"""

MERMAID_CONDITIONAL_EDGE = """
graph TD
    AskContinue["❓ ask_continue_order<br/>Node"]
    
    AskContinue --> CheckCondition{"_should_continue_order<br/>条件函数"}
    
    CheckCondition -->|state.should_continue == True| Yes["返回 'yes'"]
    CheckCondition -->|state.should_continue == False| No["返回 'no'"]
    
    Yes --> GetProducts["→ get_product_list"]
    No --> Finish["→ finish"]
    
    style AskContinue fill:#FFD700
    style CheckCondition fill:#FFA500
    style Yes fill:#90EE90
    style No fill:#FFB6C6
"""

# 导出为 Markdown 便于查看
MERMAID_MARKDOWN = f"""
# 牙科业务 AI Agent 流程图

## 1. 主流程图

```mermaid
{MERMAID_FLOWCHART}
```

## 2. State 转移流程

```mermaid
{MERMAID_STATE_FLOW}
```

## 3. 错误处理流程

```mermaid
{MERMAID_ERROR_HANDLING}
```

## 4. 条件边详解

```mermaid
{MERMAID_CONDITIONAL_EDGE}
```

---

## 流程说明

### 主流程 (Happy Path)

1. **意图识别** → 从用户消息中识别意图（如：创建病例）
2. **收集患者信息** → 从消息中提取患者的姓名和手机号
3. **查询患者** → 调用工具查询患者是否存在
4. **创建病例** → 使用患者代码创建新的病例
5. **询问继续** → 询问用户是否需要创建订单
   - **是 (Yes)** → 进入订单创建流程
   - **否 (No)** → 直接进入完成流程

### 订单创建流程 (可选)

6. **获取产品列表** → 从系统获取所有可用产品
7. **收集订单信息** → 从用户消息中收集订单信息（选择的产品、数量等）
8. **创建订单** → 调用工具创建订单

### 完成流程

9. **流程完成** → 生成完成消息，包含创建的患者代码、病例代码、订单代码

### 错误处理

- 任何 Node 发生异常 → 流向 **error_handling** Node
- 错误处理 Node 记录错误信息并添加到消息历史
- 最后进入 END 结束

---

## Node 详解

| Node | 描述 | 输入 | 输出 | 可能错误 |
|------|------|------|------|---------|
| intent_recognition | 识别用户意图 | messages | intent | 无法识别意图 |
| collect_patient_info | 收集患者信息 | messages | patient_info | 信息不完整 |
| query_patient | 查询患者存在 | patient_info | patient_code, patient_exists | 查询失败 |
| create_case | 创建病例 | patient_code | case_code | 创建失败 |
| ask_continue_order | 询问是否继续 | messages | should_continue | N/A |
| get_product_list | 获取产品列表 | (none) | product_list | 获取失败 |
| collect_order_info | 收集订单信息 | messages, product_list | order_info | 信息不完整 |
| create_order | 创建订单 | patient_code, case_code, order_info | order_code | 创建失败 |
| finish | 流程完成 | patient_code, case_code, order_code | messages | N/A |
| error_handling | 错误处理 | error_message | messages | N/A |

---

## Checkpoint 机制

- **Checkpoint 点**: `ask_continue_order` 之前
- **作用**: 中断流程，等待人工确认用户是否要继续创建订单
- **状态保存**: 使用 `MemorySaver()` 保存所有状态快照

---

## State 完整流转示例

### 创建病例 + 订单的完整流程

```
初始 State:
{
    "messages": [{"role": "user", "content": "帮我创建张三的病例。"}],
    "intent": "",
    "patient_info": {},
    ...
}

↓ node_intent_recognition

State after step 1:
{
    ...,
    "intent": "create_case",
    "current_step": "intent_recognition",
    "completed_steps": ["intent_recognition"]
}

↓ node_collect_patient_info

State after step 2:
{
    ...,
    "patient_info": {"name": "张三", "phone": "13800138000"},
    "current_step": "collect_patient_info",
    "completed_steps": ["intent_recognition", "collect_patient_info"]
}

↓ node_query_patient

State after step 3:
{
    ...,
    "patient_exists": true,
    "patient_code": "P001",
    "tool_result": {"exists": true, "patient_code": "P001"},
    "current_step": "query_patient",
    "completed_steps": [..., "query_patient"]
}

↓ node_create_case

State after step 4:
{
    ...,
    "case_code": "C001",
    "tool_result": {"case_code": "C001"},
    "current_step": "create_case",
    "completed_steps": [..., "create_case"]
}

↓ node_ask_continue_order (Checkpoint: 中断等待)

State after step 5:
{
    ...,
    "should_continue": true,  # 用户确认继续
    "current_step": "ask_continue_order",
    "completed_steps": [..., "ask_continue_order"]
}

↓ [条件边] should_continue=true → get_product_list

State after step 6:
{
    ...,
    "product_list": [...],
    "current_step": "get_product_list",
    "completed_steps": [..., "get_product_list"]
}

↓ node_collect_order_info

State after step 7:
{
    ...,
    "order_info": {"products": [...], "total_price": 5000},
    "current_step": "collect_order_info",
    "completed_steps": [..., "collect_order_info"]
}

↓ node_create_order

State after step 8:
{
    ...,
    "order_code": "O001",
    "tool_result": {"order_code": "O001"},
    "current_step": "create_order",
    "completed_steps": [..., "create_order"]
}

↓ node_finish

Final State:
{
    "messages": [
        ...,
        {"role": "assistant", "content": "流程完成!\\n患者代码: P001\\n病例代码: C001\\n订单代码: O001"}
    ],
    "current_step": "finish",
    "completed_steps": [..., "finish"]
}

↓ END
```
"""

if __name__ == "__main__":
    print(MERMAID_MARKDOWN)
