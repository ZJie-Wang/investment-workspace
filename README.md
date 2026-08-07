# Investment Workspace

一个面向 AI agent 的投资研究工作目录。

在这个目录下直接运行你的 AI agent（Claude Code、Codex、pi 等），agent 会读取根目录的 `AGENTS.md`，按照其中定义的行为规范工作。

> [!NOTE]
> 这并不是一个开箱即用的“产品”，而只是我根据个人需求搭的一个简单框架。公开出来更多是作为经验和想法分享——如果觉得有用，按需取用、自行调整即可。

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

这一步完全可以跳过，毕竟 AI agent 自己也知道要用哪些包。你当然也可以根据自己的需求来指定别的依赖，甚至别的语言（如 R 语言）。

### 2. 配置 Tushare Token

研究任务主要通过 [Tushare Pro](https://tushare.pro) 获取 A 股数据。选择 tushare 是因为它比较稳定，同时注册起来容易，价格也相对便宜。

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

[`example_task/`](example_task/Memo.md) 是一个我之前跑过的任务（某一周的市场快照）。当时用的模型是 `glm-5.2`，harness 是 pi。具体用的提示词忘了，大概就是让它做一个快照。这个例子的质量其实很一般，尤其是因为模型不支持多模态导致无法视觉验证图像。如果条件允许还是建议优先使用 claude 和 gpt 模型。无论如何，把它放在这里仅作参考，开始跑自己的任务之前把它删掉即可。

## 一些想法

我个人推荐将 skill 安装在这个工作目录内（而非全局），因为在我们的使用场景里，几乎所有涉及 Tushare 的任务都会在这个目录下运行。而且我认为，我们应该把这样一个工作目录视为一个单元来管理。

我非常不认同很多人在 Hermes 或 OpenClaw 动辄加载几十甚至上百个 skills 这种做法，至少目前，还没有哪个模型能完全不受上下文污染的影响。此外，我认为我们应该更有意识地管理上下文，以及我们运行 agent 的目录。

其实，tushare 官方就有提供可以直接使用的 skill：https://github.com/waditu-tushare/skills 。但其质量真的一言难尽，因此我重新做了一个版本，哪怕在模型表现上不能有显著提升，也至少能让上下文干净一点。

如果你愿意在这个目录里二次加工，我认为最有价值的两件事就是：
1. 通读并调整 `AGENTS.md`
2. 自己在（以 pi 为例）`.pi/skills` 里写一些与投资分析相关的 skills。例如，若你有自己的 backtest 策略，就可以写一个 backtest skill；若你有自己的组合优化偏好，可以写一个 portfolio optimization skill 等等。

此外，请不要低估手写 SKILL 或 AGENTS.md 的价值。如果你不想自己的 agent 只能沦为华而不实的玩具，那么静下心写这些文件是绝对有必要且有意义的（当然我们可以借助 AI 辅助来写，但其中必须要有我们自己的观点）。

最后，大多数文件我使用的都是英文，这主要是因为，即使对于我这样的中文母语者，现在许多主流大模型的中文让我感觉比英文还难读，尤其是涉及到股市或相关内容时，满屏的“黑话”比文言文还晦涩。

## License

[MIT](LICENSE)
