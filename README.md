# Investment Workspace

一个面向 AI Agent 的投资研究工作区脚手架（以 A 股市场为主）。

在这个目录下直接运行你的 AI 编码 Agent（Claude Code、Codex、pi 等），Agent 会读取根目录的 `AGENTS.md`，按照其中定义的"资深投资研究员"行为规范工作：任务隔离、数据可复现、事实与判断分离、禁止编造数据等。

## 目录结构

```
.
├── AGENTS.md                  # Agent 行为规范（研究员守则），整个工作区的核心
├── skills/
│   └── tushare-endpoints/     # Tushare 数据接口使用指南（skill，需自行安装，见下文）
├── tasks/                     # 每个研究任务一个独立文件夹，AGENTS.md 会强制 Agent 遵守
│   └── 20260718_Ashare_Weekly_Snapshot/   # 示例任务：A 股周度市场快照
│       ├── report.md          # 最终报告
│       ├── scripts/           # 数据拉取与分析脚本（可复现）
│       ├── data/              # 原始数据与中间结果
│       └── figures/           # 图表
├── requirements.txt           # Python 依赖
└── .env.example               # 环境变量模板
```

## 快速开始

### 1. 准备 Python 环境

要求 Python 3.7+，然后安装依赖：

```bash
pip install -r requirements.txt
```

### 2. 配置 Tushare Token

研究任务主要通过 [Tushare Pro](https://tushare.pro) 获取 A 股数据。注册后在个人主页获取 token，然后：

```bash
cp .env.example .env
# 编辑 .env，填入你的 token
```

或直接设置环境变量 `TUSHARE_TOKEN`。

> 注意：Tushare 不同接口有积分门槛，token 权限不足时部分接口会受限。Agent 守则已要求遇到权限/数据问题时停下并报告，而不是硬编数据。

### 3. 安装 tushare-endpoints skill

`skills/tushare-endpoints` 是给 Agent 看的 Tushare 接口使用指南（接口目录、环境检查、参数规范化等）。它在仓库里仅作展示，需要安装到你所用 Agent 的 skill 目录才能生效：

| Agent | 安装位置 |
|---|---|
| pi | 全局 `~/.pi/agent/skills/`，或工作区内 `.pi/skills/` |
| Claude Code | 全局 `~/.claude/skills/`，或工作区内 `.claude/skills/` |
| Codex / 其他 | 若无 skill 机制，可让 Agent 在涉及 Tushare 任务时直接阅读 `skills/tushare-endpoints/SKILL.md` 及其引用的接口目录 |

安装方式就是把整个 `tushare-endpoints` 文件夹复制到对应位置。

### 4. 开始研究

在工作区根目录启动你的 Agent，直接描述任务即可，例如：

> 帮我分析一下最近新能源汽车板块的表现，对比沪深300。

Agent 会自动在 `tasks/` 下按 `YYYYMMDD_任务描述` 建独立文件夹，把脚本、原始数据、图表和最终报告都归档进去。

## 示例任务

[`tasks/20260718_Ashare_Weekly_Snapshot/`](tasks/20260718_Ashare_Weekly_Snapshot/report.md) 是一个真实跑过的任务（A 股周度市场快照），展示了标准的产出形态：拉数脚本 → 原始数据 → 分析脚本 → 图表 → 带复现元数据的报告。建议第一次使用时让 Agent 参考它。

## 隐私与 git 说明

`.gitignore` 已默认排除以下容易误提交的敏感/本地内容：

- `.env`（Tushare token）
- `portfolio.json`（持仓信息，`AGENTS.md` 中的可选机制，需要时自行创建）
- `tasks/` 下你自己的研究任务（示例任务除外；如果希望用 git 管理研究历史，可自行调整 `.gitignore`）
- `.DS_Store`、`__pycache__`、本地 agent 配置目录等

## License

[MIT](LICENSE)
