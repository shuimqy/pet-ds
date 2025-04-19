<div align="center">

# Pet Chi 桌面萌宠

_✨ MCP(提示词方式)，Qt6 ✨_

</div>

<img src="https://img.shields.io/badge/Python-3.10+-f09?style=flat&logo=Python&logoColor=fc5&labelColor=3776AB" alt="Python">
<img src="https://img.shields.io/badge/Qt-6-41CD52?style=flat&logo=Qt&logoColor=fff&labelColor=41CD52" alt="Qt">

## 特性

- **Qt**: Qt6 框架实现的可视化图形界面
- **OpenAI 风格**: 使用 OpenAI `completions`接口，兼容绝大多数 LLM 服务提供者
- **MCP**: 支持 MCP 调用外部工具
  - 基于提示词方式实现，不依赖 function call
  - 已经支持的服务类型
    - Python
    - Node.js

## 初始化项目

如果你没有安装 uv：

```sh
pip install uv
```

创建虚拟环境

```sh
uv venv
```

激活虚拟环境

<details open>
<summary>On Windows:</summary>

```sh
.venv\Scripts\activate
```

</details>

<details open>
<summary>On Unix or MacOS:</summary>

```sh
source .venv/bin/activate
```

</details>

安装依赖

```sh
uv pip compile pyproject.toml > requirements.txt
uv pip install -r requirements.txt
```

## 配置

依据实际情况修改配置

```Python
class Config(BaseModel):
    # LLM 密钥
    api_key: str = ""
    # LLM url
    llm_url: str = "https://openrouter.ai/api/v1/chat/completions"
    # 模型
    model: str = "deepseek/deepseek-chat-v3-0324:free"
    # mcp server 路径
    mcp_server_path: str = "path/to/mcp/server/server.py"
    # 代理
    proxy: str = "http://127.0.0.1:7890"
```

## 运行

```sh
run
```

## MCP

```mermaid
flowchart LR
    subgraph "Your Computer"
        Host["Host with MCP Client\n(Claude, IDEs, Tools)"]
        S1["MCP Server A"]
        S2["MCP Server B"]
        S3["MCP Server C"]
        Host <-->|"MCP Protocol"| S1
        Host <-->|"MCP Protocol"| S2
        Host <-->|"MCP Protocol"| S3
        S1 <--> D1[("Local\nData Source A")]
        S2 <--> D2[("Local\nData Source B")]
    end
    subgraph "Internet"
        S3 <-->|"Web APIs"| D3[("Remote\nService C")]
    end
```

本项目时序图（启用 MCP）

```mermaid
sequenceDiagram
    participant User
    participant PetChi_UI as PetChi UI(MCP Client)
    participant LLM
    participant MCP_Server
    participant Tool as Local Tool/Web APIs (e.g. Python Script)

    User->>PetChi_UI: 输入指令（比如“运行统计脚本”）
    PetChi_UI->>MCP_Server: 获取工具列表
    MCP_Server-->>PetChi_UI: 返回工具列表
    PetChi_UI->>LLM: 用户询问 + 工具描述 + 预设提示词
    LLM-->>PetChi_UI: 返回思考过程，工具调用
    PetChi_UI-->>User: 显示第一次回答
    PetChi_UI->>PetChi_UI: 判断是否有工具调用
    PetChi_UI->>MCP_Server: 调用工具
    MCP_Server->>Tool: 执行工具
    Tool-->>MCP_Server: 返回执行结果
    MCP_Server-->>PetChi_UI: 结果返回
    PetChi_UI->>LLM: 带上下文的第二次询问
    LLM-->>PetChi_UI: 最终回答
    PetChi_UI-->>User: 显示最终回答
```

## TODO

- [ ] 多 live2d 形象切换
- [ ] 多 MCP 服务连接
- [ ] 命令执行许可按钮
- [ ] 语音输入
- [ ] 语音输出
- [ ] 用户预设提示词
- [ ] 长期记忆
