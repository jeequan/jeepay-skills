# Jeepay Skills

> 🤖 给对接 Jeepay 开源支付网关的开发者用的 AI Coding 助手套件
>
> 让 Claude / Cursor / 通义千问 / ChatGPT 等 AI 助手帮你**一次接对** Jeepay 接口

[![Jeepay](https://img.shields.io/badge/Jeepay-V3.2.x+-blue.svg)](https://github.com/jeequan/jeepay)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 是什么

一组针对 [Jeepay 开源支付网关](https://github.com/jeequan/jeepay) 的 **AI Coding Skill**（结构化提示词包）。每个 skill 由 SKILL.md + 一组 references 组成，让 AI 助手在帮你写 Jeepay 接入代码时：

- ✅ **字段名拼写正确**（`authCode` / `openid` / `mchOrderNo` 等大小写陷阱已规避）
- ✅ **签名算法准确**（MD5 + 大小写不敏感排序 + 末尾追加 `key=apiKey`）
- ✅ **SDK 使用正确**（强制 `JeepayClient.getInstance(...)`，避开 `new` 构造的 `setAppId` 陷阱）
- ✅ **安全红线齐备**（私钥三禁、前台结果不可信、未确认不重付、异步必须先验签）
- ✅ **支付方式选对**（按业务场景自动路由 wayCode，不会用 `WX_NATIVE` 接小程序场景）

## 当前可用 Skill

| Skill | 受众 | 状态 | 说明 |
|-------|------|------|------|
| [`jeepay-open-integration`](skills/jeepay-open-integration/) | 下游业务系统开发者 | **V1.0**（首发） | 帮业务方接入 Jeepay HTTP/SDK 接口：统一下单、退款、查单、转账、分账、异步通知验签 |

### 🗺 路线图（按需求/反馈优先级开发）

| 计划 Skill | 受众 | 说明 |
|-----------|------|------|
| `jeepay-channel-config` | Jeepay 运营管理员 | 帮在 Jeepay 后台配置微信/支付宝/银联等支付通道参数 |
| `jeepay-deploy` | 私有化部署 DevOps | 帮做 Docker Compose / 宝塔 / 一键安装脚本相关运维 |
| `jeepay-merchant-admin` | 商户运营 | 帮做商户、应用、API 密钥的日常管理 |

如果你有具体 skill 需求，欢迎开 [Issue](../../issues) 提报。

---

## 怎么用

### 🤖 Claude Code 用户（推荐）

```bash
git clone https://github.com/jeequan/jeepay-skills.git
mkdir -p ~/.claude/skills
cp -r jeepay-skills/skills/jeepay-open-integration ~/.claude/skills/
```

重启 Claude Code。当你提到 "Jeepay 接入"、"对接 Jeepay 退款"、"Jeepay 异步通知" 等关键词时，Skill 会自动加载。

### 🎯 Cursor / Cline / Continue 等 IDE AI 用户

下载 [SKILL.md](skills/jeepay-open-integration/SKILL.md) 拷到你项目根目录的对应 rules 路径：

| 工具 | 路径 |
|------|------|
| Cursor | `.cursor/rules/jeepay-integration.mdc` |
| Cline / Roo Code | `.clinerules` 文件追加 |
| Continue.dev | `.continue/rules/` 目录 |
| GitHub Copilot | `.github/copilot-instructions.md` 追加 |

需要更详细文档时同时把 `references/` 目录也拷过去。

### 💬 网页 AI（claude.ai / ChatGPT / 通义千问 / 文心一言）

打开 [skills/jeepay-open-integration/references/bundle.md](skills/jeepay-open-integration/references/bundle.md) 全选复制，粘贴到对话开头作为上下文。

> 文件 ~40KB，主流大模型（Claude Sonnet/Opus、GPT-4o、Qwen3、ERNIE 4）都能一次性吃完。

### 📖 不用 AI 直接看文档

仓库本身就是结构化的 Jeepay 接入指南，直接在 GitHub 上浏览即可，不需要装任何 AI 工具。重点文档：

- [SKILL.md](skills/jeepay-open-integration/SKILL.md) — 接入主流程
- [scene-routing.md](skills/jeepay-open-integration/references/scene-routing.md) — 支付方式选择决策树
- [sdk-reminder.md](skills/jeepay-open-integration/references/sdk-reminder.md) — SDK 集成坑点
- [checklist.md](skills/jeepay-open-integration/references/checklist.md) — 上线前自检清单

---

## 反馈与贡献

- 🐛 发现 skill 生成的代码有问题 → 开 [Issue](../../issues)，附 AI 工具名 + 你的 prompt + 生成结果
- 💡 想要新的 Jeepay 相关 skill → 开 [Issue](../../issues) 描述场景，社区评估
- 🛠 想修改 skill 内容 → PR 欢迎，请同步更新 `bundle.md`

## 版本与兼容性

| Skill 版本 | 兼容 Jeepay 版本 | 备注 |
|-----------|-----------------|------|
| `jeepay-open-integration` v1.0 | Jeepay V3.2.x+ | 首发版本 |

详见 [CHANGELOG.md](CHANGELOG.md)（待添加）。

## 已知限制（V1.0）

详见 [skills/jeepay-open-integration/](skills/jeepay-open-integration/) 内部说明。主要：

1. 异步通知验签示例默认**单商户场景**。多商户接入需手动改造为按 `appId` 反查 apiKey
2. 部分静态文档（错误码、常见问题）为快照内容，可能落后主仓库实际状态。最新信息请以 [Jeepay 在线文档](https://doc.jeequan.com) 为准

V1.1 会处理这些。

## License

[MIT](LICENSE) — 自由使用、修改、再分发。
