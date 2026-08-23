# Investment Workspace

## 目录结构

```
.
├── AGENTS.md                  # agent 行为规范
├── skills/
│   └── tushare-endpoints/     # Tushare 数据接口使用指南（skill，需自行安装，见下文）
├── tasks/                     # 每个研究任务一个独立文件夹，初始为空，由 agent 按需创建
├── example_task/              # 一个真实跑过的示例任务
├── requirements.txt           # Python 依赖
└── .env.example               # 环境变量模板
```

## 快速开始

### 1. Python 环境

要求 Python 3.7+，然后安装依赖：

```bash
pip install -r requirements.txt
```

这一步完全可以跳过，毕竟 AI 自己也知道要用哪些包。你当然也可以根据自己的需求来指定别的依赖，甚至别的语言（如 R）。

### 2. 配置 Tushare Token

研究任务主要通过 [Tushare Pro](https://tushare.pro) 获取 A 股数据。选择 tushare 是因为它注册起来容易，价格也相对便宜。

注册后在个人主页获取 token，然后：

```bash
cp .env.example .env
# 编辑 .env，填入你的 token
```

或直接 export 环境变量 `TUSHARE_TOKEN`。

> 注意：Tushare 不同接口有积分门槛，token 权限不足时部分接口会受限。AGENTS.md 已要求遇到权限/数据问题时停下并报告，而不是硬编数据。

### 3. 安装 tushare-endpoints skill

`skills/tushare-endpoints` 是给 agent 看的 Tushare 接口使用指南（接口目录、环境检查、参数规范化等）。它在这个仓库里仅作展示，需要安装到你所用 agent 的 skill 目录才能生效。

以 pi 为例，可以安装在 `~/.pi/agent/skills/`，或工作目录的 `.pi/skills/` 中；Claude Code 则对应 `~/.claude/skills/` 或工作目录的 `.claude/skills/`。安装方式就是把整个 `tushare-endpoints` 文件夹复制到对应位置。

### 4. 开始研究

在工作区根目录启动你的 agent，直接描述任务即可，例如：

> 帮我分析一下最近 AI 算力链相关板块的表现，对比沪深300。

agent 会自动在 `tasks/` 下按 `YYYYMMDD_任务描述` 建独立文件夹，把脚本、原始数据、图表和最终报告都归档进去。

## 示例任务

[`example_task/`](example_task/Memo.md) 是一个我之前跑过的任务。当时用的模型是 `glm-5.2`，提示词大概就是让它做一个市场快照。这个例子的质量其实很一般，把它放在这里仅作参考，开始跑自己的任务之前把它删掉即可。

## License

[MIT](LICENSE)
