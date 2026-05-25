# Jeepay 开源版支付系统对接 Skill

为开发者提供 Jeepay 开源版支付系统的对接指引和问题排查能力。

---

## 文件结构

```
jeepay-open-integration/
├── SKILL.md                              # 技能主文件（路由规则 + 执行步骤）
├── README.md                             # 说明文档
└── references/
    ├── scene-routing.md              # 支付方式路由表（决策树 + 关键词匹配 + 澄清话术）
    ├── api-routing.md                # API 路由表（接口文档索引 + 调用流程）
    ├── checklist.md                  # 集成校验清单（签名验签 + 通知处理 + 上线检查）
    ├── sdk-reminder.md               # SDK 集成指引（初始化 + 签名算法 + 坑点 + 误判链）
    ├── doc-access.md                 # 文档访问规范（curl 脚本 + 页面ID映射）
    ├── log-guide.md                  # 日志输出指引（日志规范 + 示例代码）
    ├── docs/
    │   ├── Jeepay-错误码文档.md      # 系统错误码查询
    │   └── Jeepay-常见问题文档.md    # 问题排查文档
    └── code-examples/
        ├── interface-guide.md        # 代码示例索引（接口 → Java/Python 映射）
        ├── java/                     # Java 代码示例（10 个文件）
        └── python/                   # Python 代码示例（10 个文件）
```

---

## 触发关键词

当用户提到以下关键词时，可使用此 Skill：

对接Jeepay开源版、Jeepay私有化部署、Jeepay集成、Jeepay支付网关对接、Jeepay退款、Jeepay关单、Jeepay查单、Jeepay异步通知、Jeepay转账、Jeepay分账

---

## 相关文档

- [接口规则](https://doc.jeequan.com/#/integrate/open/api/81)
- [SDK下载](https://doc.jeequan.com/#/integrate/open/api/116)
- [统一支付下单](https://doc.jeequan.com/#/integrate/open/api/85)

---

> Skill 版本：1.0.1 | 文档创建时间：2026-05-15 | 最后更新：2026-05-25
