# 🦷 牙科业务 AI Agent

使用 LangGraph 构建的智能牙科业务工作流自动化系统。

## 📋 项目概述

这是一个基于 LangGraph 的多步骤 AI Agent，用于自动化牙科诊所的核心业务流程：
- 患者信息管理
- 病例创建
- 订单管理

Agent 能够理解用户意图，收集必要信息，调用外部工具，并管理整个业务流程。

## 🏗️ 项目结构

```
gkx-agents/
├── agents/
│   ├── __init__.py           # 包初始化文件
│   ├── state.py              # State 定义
│   ├── tools.py              # 外部工具定义
│   ├── nodes.py              # 所有 Node 的实现 (10个)
│   ├── graph.py              # Graph 定义，条件边和边界
│   ├── main.py               # 主程序和 Agent 类
│   ├── flowchart.py          # Mermaid 流程图
│   └── test/
│       └── test_agent.py     # 单元测试
├── README.md                 # 本文件
├── requirements.txt          # 依赖包
└── config/
    └── config.yaml           # 配置文件
```

## 🔄 工作流程

### 主流程 (Happy Path)

```
START
  ↓
🧠 意图识别 (intent_recognition)
  ↓
👤 收集患者信息 (collect_patient_info)
  ↓
🔎 查询患者 (query_patient)
  ↓
📋 创建病例 (create_case)
  ↓
❓ 是否继续创建订单? (ask_continue_order)
  ├─ [Yes] → 📦 获取产品列表 → 🛒 收集订单信息 → ✅ 创建订单
  └─ [No]  → 直接完成
  ↓
🎉 流程完成 (finish)
  ↓
END
```

## 🔧 核心组件

### 1. **State (agents/state.py)**
定义 Agent 的状态对象，包含：
- `messages`: 对话历史
- `patient_info`: 患者信息
- `case_code`: 病例代码
- `order_info`: 订单信息
- `current_step`: 当前步骤
- `completed_steps`: 已完成的步骤列表

### 2. **Tools (agents/tools.py)**
定义 4 个外部工具：
- `get_patients_by_name_and_phone()`: 查询患者
- `case_add()`: 创建病例
- `get_product_list()`: 获取产品列表
- `case_order_add()`: 创建订单

### 3. **Nodes (agents/nodes.py)**
定义 10 个业务步骤 Node：

| Node | 描述 | 类型 |
|------|------|------|
| 1. intent_recognition | 识别用户意图 | 处理 |
| 2. collect_patient_info | 收集患者信息 | 处理 |
| 3. query_patient | 查询患者 | 工具调用 |
| 4. create_case | 创建病例 | 工具调用 |
| 5. ask_continue_order | 询问是否继续 | 条件判断 |
| 6. get_product_list | 获取产品列表 | 工具调用 |
| 7. collect_order_info | 收集订单信息 | 处理 |
| 8. create_order | 创建订单 | 工具调用 |
| 9. finish | 完成流程 | 终止 |
| 10. error_handling | 错误处理 | 错误处理 |

### 4. **Graph (agents/graph.py)**
定义 LangGraph 的流程图：
- 所有 Node 的添加
- 所有 Edge 的定义
- 条件边：`ask_continue_order` 的 should_continue 条件路由
- Checkpoint 支持：保存状态快照，支持恢复
- Interrupt 点：在 `ask_continue_order` 处中断等待人工确认

### 5. **Main (agents/main.py)**
Agent 的主类：
- `DentalAgent` 类：初始化 Graph，运行 Agent
- `run()` 方法：同步执行
- `run_async()` 方法：异步执行
- 演示函数和示例

## 📦 安装依赖

```bash
pip install -r requirements.txt
```

### 主要依赖

```
langgraph>=0.0.x
langchain>=0.1.x
python>=3.11
```

## 🚀 快速开始

### 基础使用

```python
from agents import DentalAgent

# 创建 Agent 实例
agent = DentalAgent()

# 运行 Agent
result = agent.run(
    user_input="帮我创建一个新的病例。患者叫张三，手机号是13800138000。",
    thread_id="conversation_1"
)

# 查看结果
print(result["patient_code"])   # 患者代码
print(result["case_code"])      # 病例代码
print(result["order_code"])     # 订单代码（如果创建了）
```

### 异步使用

```python
import asyncio
from agents import DentalAgent

async def main():
    agent = DentalAgent()
    result = await agent.run_async(
        user_input="创建李四的病例。手机号：13900139000",
        thread_id="conversation_2"
    )
    print(result)

asyncio.run(main())
```

### 直接运行演示

```bash
python agents/main.py
```

## 🧪 测试

```bash
python -m pytest agents/test/test_agent.py -v
```

## 🎯 特性

### ✅ 已实现
- [x] 完整的 LangGraph 工作流
- [x] 10 个业务 Node
- [x] 条件边和路由逻辑
- [x] State 管理
- [x] 错误处理
- [x] Checkpoint 支持
- [x] 多轮对话支持
- [x] 同步和异步执行

### 🔄 待实现
- [ ] LLM 集成（GPT-4, Claude 等）
- [ ] 意图识别的真实实现（当前为示例）
- [ ] 患者信息提取的真实实现（当前为示例）
- [ ] 数据库持久化
- [ ] Web API 接口
- [ ] 前端界面
- [ ] 更详细的错误处理
- [ ] 日志记录

## 📝 示例

### 示例 1：创建病例 + 订单

**输入：**
```
用户: "帮我创建一个新的病例。患者叫张三，手机号是13800138000。"
用户: "是的，我要继续创建订单"
用户: "我要买根管治疗和牙冠，总共5000块"
```

**执行流程：**
```
intent_recognition → collect_patient_info → query_patient → create_case 
→ ask_continue_order [Yes] 
→ get_product_list → collect_order_info → create_order → finish
```

**输出：**
```
患者代码: P001
病例代码: C001
订单代码: O001
```

### 示例 2：只创建病例

**输入：**
```
用户: "我想创建李四的病例。李四的手机号是13900139000。"
用户: "不需要了"
```

**执行流程：**
```
intent_recognition → collect_patient_info → query_patient → create_case 
→ ask_continue_order [No] 
→ finish
```

**输出：**
```
患者代码: P002
病例代码: C002
```

## 🔌 集成 LLM

要集成真实的 LLM（如 OpenAI GPT-4），需要在各个 Node 中实现：

```python
from langchain.llms import OpenAI

llm = OpenAI(api_key="your-api-key")

# 在 node_intent_recognition 中使用
result = llm.predict(f"从以下消息中识别意图: {user_message}")
```

## 📚 架构图

### Graph 结构
```
┌─────────────────────────────────────────────────────────┐
│                   Dental Agent Graph                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐                                      │
│  │ intent_recog │                                      │
│  └──────────────┘                                      │
│        ↓                                               │
│  ┌──────────────┐                                      │
│  │ collect_info │                                      │
│  └──────────────┘                                      │
│        ↓                                               │
│  ┌──────────��───┐                                      │
│  │query_patient │                                      │
│  └──────────────┘                                      │
│        ↓                                               │
│  ┌──────────────┐                                      │
│  │ create_case  │                                      │
│  └──────────────┘                                      │
│        ↓                                               │
│  ┌──────────────────────┐                              │
│  │ ask_continue_order   │ ← [Checkpoint & Interrupt]  │
│  └──────────────────────┘                              │
│    ↙              ↘                                    │
│ Yes              No                                   │
│  ↓                ↓                                    │
│ product_list    finish                                │
│  ↓                ↓                                    │
│ order_info      END                                   │
│  ↓                                                    │
│ create_order                                          │
│  ↓                                                    │
│ finish                                                │
│  ↓                                                    │
│ END                                                   │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ 配置

在 `config/config.yaml` 中配置：

```yaml
agent:
  name: "Dental AI Agent"
  version: "0.1.0"
  debug: true

checkpointer:
  type: "memory"  # 或 "postgres", "sqlite"
  ttl: 3600       # 状态过期时间（秒）

llm:
  provider: "openai"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"
  temperature: 0.7

tools:
  timeout: 30
  retries: 3
```

## 📖 API 文档

### DentalAgent 类

#### `__init__()`
初始化 Agent，加载 Graph。

#### `run(user_input: str, thread_id: str = "default") -> Dict[str, Any]`
同步运行 Agent。

**参数：**
- `user_input`: 用户输入
- `thread_id`: 对话线程 ID

**返回：**
- 最终的 State 字典

#### `run_async(user_input: str, thread_id: str = "default") -> Dict[str, Any]`
异步运行 Agent。

**参数：**
- `user_input`: 用户输入
- `thread_id`: 对话线程 ID

**返回：**
- 最终的 State 字典

## 🐛 调试

启用调试模式查看详细日志：

```python
import logging

logging.basicConfig(level=logging.DEBUG)

agent = DentalAgent()
result = agent.run("用户输入")
```

## 📊 监控和日志

Agent 会输出详细的执行日志：

```
🚀 初始化牙科业务 AI Agent...
✅ Agent 初始化完成

📨 用户输入: 帮我创建一个新的病例...

🧠 Node 1: Intent Recognition - 识别用户意图
👤 Node 2: Collect Patient Info - 收集患者信息
...
🎉 Node 9: Finish - 流程完成

============================================================
✅ Agent 执行完成
============================================================
📊 流程步骤: intent_recognition → collect_patient_info → ...
💾 最终状态: finish
👤 患者代码: P001
📋 病例代码: C001
🛒 订单代码: O001

💬 Agent 回复:
流程完成！
...
============================================================
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- 项目地址: https://github.com/kxguan0630-crypto/gkx-agents
- 问题反馈: https://github.com/kxguan0630-crypto/gkx-agents/issues

---

**最后更新：** 2026-07-13

**版本：** 0.1.0

**状态：** 开发中 🚧
