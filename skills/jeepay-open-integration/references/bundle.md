<!-- Generated bundle for paste-in usage with web AI (claude.ai / ChatGPT / 通义千问 / 文心一言 / etc.) -->
<!-- Source: https://github.com/jeequan/jeepay-skills/tree/master/skills/jeepay-open-integration -->
<!-- Bundle 包含 SKILL.md 主体 + scene-routing / api-routing / sdk-reminder / checklist / log-guide / doc-access / 代码示例索引 -->
<!-- 不含 docs/ 目录下的错误码 / 常见问题文档（按需单独打开），不含 Python 代码示例（如需 Python 请单独取 references/code-examples/python/） -->

# Jeepay 接入助手（单文件版）

> 把本文件全选复制到你的 AI 对话开头作为上下文，然后描述你要做的 Jeepay 接入任务，AI 会按本文件的指引生成代码。

---

## 一、主流程（来自 SKILL.md）

---
name: jeepay-open-integration
description: >-
  Jeepay 开源版支付系统对接技能。涵盖支付下单、退款、关单、查单、
  异步通知等支付场景的集成指导。适用于私有化部署的Jeepay开源版系统。
  当用户提到"对接Jeepay开源版"、"Jeepay私有化部署"、"Jeepay集成"、
  "Jeepay支付网关对接"、"Jeepay退款"、"Jeepay关单"、"Jeepay查单"、
  "Jeepay异步通知"、"Jeepay转账"、"Jeepay分账"时使用此 Skill。
---

# Jeepay 开源版支付系统对接 Skill

## 前置说明

1. 本 Skill 主要提供 Jeepay 开源版支付系统的对接指引和问题排查指引。
2. 请开发人员审查 AI 生成的接入代码，自行确认代码逻辑，上线前充分测试确保其适用性与准确性。
3. **Java 项目优先使用 SDK**：当用户项目为 Java 时，优先使用 Jeepay SDK 进行对接，而非直接调用 HTTP 接口。SDK 已封装签名、验签、请求等逻辑，可大幅简化集成工作。

### 集成原则

> ⛔ 以下原则必须严格遵守：

- **征得用户同意**：严禁在未征得用户同意的情况下，擅自启动支付产品的集成流程，必须先确认用户意图并获得明确同意后，方可继续执行集成步骤。
- **单一产品集成**：在一次指令中，未经用户许可，严禁同时自动启动多个支付产品的集成，必须先确认单一产品，完成该产品的完整集成流程后，方可视情况讨论下一个产品。

### 权限配置（引导配置）

> ⚠️ 本技能需要以下权限才能正常工作（如读取在线文档、查看 SDK 结构等）。

**所需权限列表**：

| 权限 | 用途 |
|------|------|
| `Bash(curl *)` | 调用 Jeepay 在线文档 API |
| `Bash(javap *)` | 查看 SDK 类结构和方法签名 |
| `Bash(mvn *)` | Maven 构建、依赖管理 |
| `Bash(jar *)` | 查看和解压 SDK jar 包 |
| `WebFetch(domain:doc.jeequan.com)` | 访问 Jeepay 官方文档站 |
| `WebFetch(domain:gitee.com)` | 访问 Gitee SDK 源码 |

**配置方式**：将以下内容手动添加到项目的 `.claude/settings.local.json` 中：

```json
{
  "permissions": {
    "allow": [
      "Bash(curl *)",
      "Bash(javap *)",
      "Bash(mvn *)",
      "Bash(jar *)",
      "WebFetch(domain:doc.jeequan.com)",
      "WebFetch(domain:gitee.com)"
    ]
  }
}
```

---

## 强制执行要点

⛔ 以下为全局强制规则，严禁以任何理由跳过或简化：

- [1] 告知用户本 Skill 主要提供 Jeepay 开源版支付系统的对接指引和问题排查指引
- [2] 告知用户服务声明（完整内容见步骤 1.1 确认点）
- [3] **先定计划再动手**：先确认用户意图并获得明确同意后，**必须先确定功能分支并打印完整的待办步骤清单**，禁止未确定计划就直接开始执行
- [4] 每个步骤完成后对照完成条件自检，有遗漏须补齐后再继续
- [5] 遇到 `<BLOCKING_CONFIRMATION>` 必须暂停等待用户明确回复，确认话术必须包含"请回复'同意'或'确认'"等显式要求
- [6] 禁止编造配置、假数据；禁止绕过确认点；禁止假数据与占位符冒充

---

## 功能路由

| 用户意图 | 功能分支 | 执行流程 |
| --- | --- | --- |
| 需要对接 Jeepay 支付系统（支付、退款、转账、分账等） | **功能一** | 步骤 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 |
| 集成过程中遇到报错或问题 | **功能二** | 步骤 2.1 → 2.2/2.3 |

## 阻塞确认点索引

以下为流程中必须暂停等待用户明确回复的关键节点，**严禁跳过**：

| 编号 | 所在步骤 | 确认点内容 |
|------|---------|-----------|
| B-01 | 步骤 1.1 产品决策 | 用户同意服务声明并确认接入产品（回复"同意"或"确认"） |
| B-02 | 步骤 1.2 获取对接文档 | 已读取对接说明、技术规范、SDK&Demo（三项全部满足） |
| B-03 | 步骤 1.6 集成校验 | 用户确认是否需要进行集成校验（回复"需要"或"确认"） |

## 完成条件索引

以下为每个步骤的完成条件，**必须全部满足**后方可继续下一步骤：

| 编号 | 步骤 | 完成条件 |
|------|------|---------|
| M-01 | 步骤 1.1 支付方式确认 | 已确认支付方式、用户已同意服务声明 |
| M-02 | 步骤 1.2 获取对接文档 | 已读取对接说明、技术规范、SDK&Demo |
| M-03 | 步骤 1.3 获取接口文档 | 已根据支付方式获取对应的接口文档 |
| M-04 | 步骤 1.4 集成代码 | 已完成代码实现、已通过 7 项自检 |
| M-05 | 步骤 1.5 集成后说明 | 已输出安全红线和后续指引 |
| M-06 | 步骤 1.6 集成校验 | 已输出校验邀请并等待用户回复 |

---

## 功能一：支付对接指引

**触发条件**：用户需要集成 Jeepay 开源版支付系统。

### 前置条件

在开始对接前，请确认用户已完成以下准备（如有遗漏需提示用户先完成）：

1. 已部署 Jeepay 开源版后端服务
2. 已在 Jeepay 运营平台创建商户，获取 **mchNo**（商户号）
3. 已在运营平台创建应用，获取 **appId**（应用ID）和 **apiKey**（接口密钥）
4. 已确认需要对接的支付方式

### 步骤 1.1 支付方式确认

阅读 [支付方式路由表](references/scene-routing.md)，根据用户输入匹配关键词，确认支付方式。当用户描述模糊时，使用 [澄清话术模板](references/scene-routing.md) 进行支付方式确认。

<BLOCKING_CONFIRMATION>

在输出支付产品决策后，**必须**严格按以下顺序执行并暂停等待用户回复：

1. **输出决策结果**：告知用户推荐的支付产品及选择理由
2. **输出服务声明**（完整打印）：

   > ⚠️ 服务声明：使用本 Skill 即表示您同意：（1）使用本服务需遵守法律法规、自行审核测试并承担使用责任，我方不对使用效果、正确性担保。（2）禁止在代码、大模型对话等公网透露敏感信息（密码、API Keys、私钥等）。

3. **显式询问确认**（必须使用如下话术）：

   > "请问您是否同意上述服务声明并确认接入【{产品名称}】？请回复'同意'或'确认'后，我将继续后续步骤。"

4. **等待用户回复**：必须收到用户明确同意的回复后，方可进入步骤 1.2。若用户未回复、表示犹豫或拒绝，**禁止继续任何后续步骤**。

</BLOCKING_CONFIRMATION>

### 步骤 1.2 获取对接文档

接入前必须阅读下列文档（文档获取方式详见 [文档访问规范](references/doc-access.md)）：

- **接口规则**：了解签名方式、参数格式、通用规则。[接口规则文档](https://doc.jeequan.com/#/integrate/open/api/81)
- **SDK下载**：获取代码示例。[SDK下载文档](https://doc.jeequan.com/#/integrate/open/api/116)

> 💡 **Java 项目提示**：接入前务必先读取 SDK&Demo 文档，优先使用 Jeepay SDK 进行对接。SDK 集成注意事项详见 [SDK 集成指引](references/sdk-reminder.md)。

> ⛔ **阻塞检查点**：步骤 1.2 完成标准（下列事项必须全部满足才能继续执行后续步骤）
- [ ] 已读取对接说明
- [ ] 已读取技术规范
- [ ] 已读取 SDK&Demo

#### 集成环境说明

- **测试环境**：详见对接说明文档中的测试环境信息
- **生产环境**：网关地址为自行部署的服务器地址（如 `https://pay.yourdomain.com`）

### 步骤 1.3 获取接口文档

根据支付方式，查阅 [API 路由表](references/api-routing.md) 获取对应的接口文档。

**channelExtra 参数说明**：不同支付方式需要传入不同的 channelExtra 参数（如条码支付的 authCode、小程序支付的 openid 等）。具体参数要求请参考 [统一支付下单文档](https://doc.jeequan.com/#/integrate/open/api/85) 中对应支付方式的说明。

> 💡 **转账/分账对接**：转账和分账功能按需对接。当用户明确需要对接转账或分账功能时，参考 API 路由表中的转账/分账接口文档按流程接入。

### 步骤 1.4 集成代码

**前置条件**：已完成步骤 1.3 获取接口文档。

**完成条件**：
- 已完成 Jeepay 支付产品集成代码实现
- 已完成代码自检并确认无误

#### 代码生成前自检

⛔ 输出任何代码之前，必须逐条自检以下 7 项，全部通过方可输出代码，任何一项不通过必须返回对应步骤重读，**禁止**跳过自检直接输出代码：

1. apiKey 是否安全存储（不在代码中硬编码，通过配置文件读取）？→ 是 → 继续
2. 签名方式是否为 MD5（Jeepay 固定 MD5 签名）？→ 是 → 继续
3. 异步通知是否使用动态解析（不硬编码字段）？→ 是 → 继续
4. 是否实现了幂等处理？→ 是 → 继续
5. 是否配置了完整的日志输出（请求 URL + 参数 + 响应）？→ 是 → 继续
6. SDK 导入语句是否正确（依赖版本、类名路径是否与 SDK 一致）？→ 是 → 继续
7. 是否已读取对应接口的代码示例（从 [代码示例索引](references/code-examples/interface-guide.md) 获取）？→ 是 → 继续

#### 代码示例

完整索引见 [代码示例索引](references/code-examples/interface-guide.md)，支持 Java 和 Python 两种语言。

**必须**按业务类别精准读取对应示例，禁止全量扫描。

### 步骤 1.5 集成后说明

**前置条件**：已完成步骤 1.4 集成代码，并通过自检。

⛔ 完成支付能力集成任务后，必须向用户输出以下两部分内容，不打印则违规：

**第一部分：安全红线**

以下为 Jeepay 支付接入的安全红线，违反可能导致资金损失或安全事故，必须严格遵守，产品集成过程中务必提醒开发者注意以下安全事项。

- **私钥禁止存客户端**：构造交易数据并签名必须在商家服务端完成，私钥严禁保存在商家 APP 客户端中。
- **私钥禁止记日志**：私钥不得出现在任何日志中。
- **私钥禁止传公共仓库**：私钥不得上传到 GitHub、GitLab 等公共代码仓库。
- **前台支付结果不可信**：前台同步跳转结果不可信，必须以 Jeepay 异步通知或调用查单接口获取结果为准。
- **未确认不重付**：在未确认支付结果前，不得要求用户再次付款，必须先通过异步通知或查询接口确认支付结果。
- **异步通知必须先验签**：收到异步通知后必须先验签，确保通知来自 Jeepay。

**第二部分：后续指引**

当前配置为测试环境配置，仅用于开发调试。上线前请将 mchNo、appId、apiKey、网关地址等配置替换为生产环境配置，并认真进行人工代码审查。

### 步骤 1.6 集成校验

- 在集成过程中及发布上线前按照 [集成校验清单](references/checklist.md) 进行校验，确保签名验签、异步通知、异常处理等符合规范。校验结果供参考，开发者务必按照 Jeepay 最新文档进行检查。
- 异步通知参数处理注意事项详见 [异步通知代码示例](references/code-examples/java/10_异步通知.md)。
- 日志输出规范详见 [日志输出指引](references/log-guide.md)。

<BLOCKING_CONFIRMATION>

输出步骤 1.5 的「安全红线」和「后续指引」后，必须暂停并等待用户确认：

1. 输出校验邀请：
   > "支付能力集成已完成。为确保集成质量，我可按照集成校验清单帮您逐项校验（包括签名验签、异步通知、异常处理等）。请问您是否需要进行集成校验？请回复'需要'或'确认'后，我将开始校验。"
2. 等待用户回复：
   - 若用户回复需要校验：获得明确同意后，方可按照校验清单逐项执行并输出结果。
   - 若用户表示不需要或无回复：禁止主动启动校验流程，可解答用户其他疑问。

</BLOCKING_CONFIRMATION>

---

## 功能二：问题排查指引

**触发条件**：用户在集成 Jeepay 开源版支付系统过程中遇到报错或其他问题。

> ⚠️ **支付方式信息确认（必须遵守）**：执行下述问题排查步骤之前，必须明确用户当前集成的**支付方式**，否则暂停输出并要求用户澄清，**严禁**在支付方式信息缺失时尝试查阅文档或猜测支付方式。

### 步骤 2.1 问题识别与分流

根据用户输入判断问题类型，分流到对应排查路径：

```
用户问题
    |
    +-- 验签失败（通信秘钥错误、验签出错）  ← 优先匹配，走专项排查
    |       |
    |       └───> 步骤 2.3 验签失败专项排查
    |
    +-- 有明确错误码（如 "通信秘钥错误"、"验签失败"）
    |       |
    |       └───> 步骤 2.2 错误码排查
    |
    +-- 无明确错误码（如流程疑问、功能异常等）
            |
            └───> 步骤 2.3 常见问题排查
```

### 步骤 2.2 错误码排查

**适用**：用户提供了明确的错误码。

> ⚠️ **报错接口信息确认（必须完成）**：错误码查询前，必须确认发生报错的**接口信息**，否则暂停输出并要求用户澄清，**严禁**在报错接口信息缺失时尝试查阅文档或猜测报错接口。

#### 排查流程

1. **查系统错误码**：查阅 [Jeepay 错误码文档](references/docs/Jeepay-错误码文档.md)，根据用户提供的错误码检索相关内容。如有匹配结果，**输出排查结论**；否则，**查业务错误消息**。

2. **查业务错误消息**：基于确定的支付方式和报错接口信息，查阅 [API 路由表](references/api-routing.md) 中对应的接口文档，进一步找到报错接口对应的接口文档，并在接口文档中根据用户提供的错误消息检索相关内容。

3. **输出排查结论**：根据查询到的错误码关联内容，输出排查结论。

### 步骤 2.3 常见问题排查

**适用**：无明确错误码的其他类型问题。

#### 排查流程

1. 根据用户输入和确定的支付方式，查阅 **常见问题文档**，匹配问题解决方案，回答用户问题时，**务必**以 Jeepay 文档为准。

2. 若根据 **常见问题文档** 未找到解决方案，引导用户查阅 [Jeepay 在线文档](https://doc.jeequan.com) 或咨询技术支持，**严禁**编造常见问题文档以外的解决方案。

#### 常见问题文档索引

| 问题类别 | 常见问题文档 |
| --- | --- |
| API 调用类 | [Jeepay 常见问题文档](references/docs/Jeepay-常见问题文档.md) |
| 支付相关 | [Jeepay 常见问题文档](references/docs/Jeepay-常见问题文档.md) |

#### 验签失败（通信秘钥错误）专项排查

遇到"通信秘钥错误"、"验签失败"等签名相关错误时，严禁凭猜测归因，必须按以下顺序排查：

1. 检查 apiKey 是否与 Jeepay 运营平台配置一致
2. 检查签名参数是否包含 sign 字段（签名前需移除 sign）
3. 检查参数排序是否按 ASCII 升序（key1=value1&key2=value2&...）
4. 检查签名拼接末尾是否附加了 `key=apiKey`
5. 检查 MD5 结果是否转为大写
6. 检查空值参数是否已过滤（空值不参与签名）

严禁的推断：
- 看到"通信秘钥错误"就认为 apiKey 配错了 → 应先检查签名算法流程
- 猜测 MD5 算法实现有问题 → Jeepay SDK 已封装签名逻辑，直接使用即可

---

## 相关文档

- [支付方式路由表](references/scene-routing.md) — 支付方式选择、关键词匹配、澄清话术
- [API 路由表](references/api-routing.md) — 接口文档索引、调用流程
- [代码示例索引](references/code-examples/interface-guide.md) — Java / Python 代码示例交叉索引
- [文档访问规范](references/doc-access.md) — 在线文档获取方式、curl 脚本、页面ID映射
- [SDK 集成指引](references/sdk-reminder.md) — Maven 依赖、SDK 初始化、API 路径对照
- [日志输出指引](references/log-guide.md) — 日志规范、示例代码
- [集成校验清单](references/checklist.md) — 签名校验、通知处理、上线检查
- [错误码文档](references/docs/Jeepay-错误码文档.md) — 系统错误码查询
- [常见问题文档](references/docs/Jeepay-常见问题文档.md) — 问题排查

---

> Skill 版本：1.0.1 | 适用版本：Jeepay 开源版 | SDK 版本：详见 [SDK下载文档](https://doc.jeequan.com/#/integrate/open/api/116)
> 文档创建时间：2026-05-15 | 最后更新：2026-05-25

---

## 二、支付方式路由

# 支付方式路由表

用于用户集成 Jeepay 开源版支付时的支付方式选择。

> 来源：Jeepay 开源版「统一支付下单」文档 (pageId=85)

---

## 支付方式决策树

```
用户咨询 Jeepay 支付接入
        |
        +-- 线下门店收款？
        |       +-- 用户出示付款码，商家扫 --> AUTO_BAR（聚合条码）/ WX_BAR / ALI_BAR / YSF_BAR
        |       +-- 商家出示二维码，用户扫 --> QR_CASHIER / WX_NATIVE / ALI_QR
        |
        +-- 线上支付？
        |       +-- 原生 App --> WX_APP / ALI_APP
        |       +-- 微信小程序 --> WX_LITE
        |       +-- 支付宝小程序 --> ALI_LITE
        |       +-- 手机浏览器 H5 --> WX_H5 / ALI_WAP
        |       +-- 手机网页 --> WX_JSAPI / ALI_JSAPI / YSF_JSAPI
        |       +-- PC端网页 --> ALI_PC
        |
        +-- 银行卡支付？
        |       +-- 快捷支付 --> BANK_AGREE
        |       +-- 网银B2C --> BANK_B2C
        |       +-- 网银B2B --> BANK_B2B
        |       +-- 银行卡转账 --> BANK_TRANSFER / BANK_TRANSFERCASHIER
        |
        +-- 特殊场景？
                +-- 支付宝订单码 --> ALI_OC
                +-- 快捷支付收银台 --> BANK_QUICK
```

---

## 支付方式分类

### 核心收银台支付方式

| wayCode | 支付方式名称 | 说明 |
|---------|--------------|------|
| **QR_CASHIER** | 聚合扫码 | 用户扫商家二维码，跳转到收银台完成支付 |
| **AUTO_BAR** | 聚合条码 | 商家扫用户付款码，自动识别微信/支付宝/云闪付 |

### 微信支付方式

| wayCode | 支付方式名称 | 说明 |
|---------|--------------|------|
| WX_BAR | 微信条码 | 用户出示微信付款码，商家扫码 |
| WX_JSAPI | 微信公众号 | 微信内H5页面支付 |
| WX_LITE | 微信小程序 | 微信小程序内支付 |
| WX_APP | 微信APP | 原生App内调起微信支付 |
| WX_H5 | 微信H5 | 手机浏览器唤起微信支付 |
| WX_NATIVE | 微信扫码 | 商家生成微信二维码，用户扫码支付 |

### 支付宝支付方式

| wayCode | 支付方式名称 | 说明 |
|---------|--------------|------|
| ALI_BAR | 支付宝条码 | 用户出示支付宝付款码，商家扫码 |
| ALI_LITE | 支付宝小程序 | 支付宝小程序内支付 |
| ALI_JSAPI | 支付宝生活号 | 支付宝生活号内H5页面支付 |
| ALI_APP | 支付宝APP | 原生App内调起支付宝支付 |
| ALI_WAP | 支付宝WAP | 手机网页支付宝支付 |
| ALI_PC | 支付宝PC网站 | PC端支付宝网站支付 |
| ALI_QR | 支付宝二维码 | 支付宝二维码支付 |
| ALI_OC | 支付宝订单码 | 支付宝订单码支付 |

### 银联支付方式

| wayCode | 支付方式名称 | 说明 |
|---------|--------------|------|
| YSF_BAR | 云闪付条码 | 用户出示云闪付付款码，商家扫码 |
| YSF_JSAPI | 云闪付jsapi | 云闪付JSAPI支付 |

### 银行卡支付方式

| wayCode | 支付方式名称 | 说明 |
|---------|--------------|------|
| BANK_AGREE | 快捷支付 | 银行卡快捷支付/代扣 |
| BANK_QUICK | 快捷支付收银台 | 快捷支付收银台 |
| BANK_B2C | 网银B2C | 个人网银支付 |
| BANK_B2B | 网银B2B | 企业网银支付 |
| BANK_TRANSFER | 银行卡转账 | 银行卡转账支付 |
| BANK_TRANSFERCASHIER | 银行卡转账收银台 | 银行卡转账收银台 |

---

## 支付方式关键词匹配

根据用户输入的关键词快速路由到对应支付方式：

| 关键词 | 支付方式 | wayCode |
| --- | --- | --- |
| 二维码收银台、扫码收银台、聚合码、聚合收银台、用户扫商家 | 聚合扫码 | QR_CASHIER |
| 付款码、条码支付、扫码枪、被扫、聚合码支付、自动识别、商家扫用户 | 聚合条码 | AUTO_BAR |
| 微信付款码、微信条码、微信扫码收款 | 微信条码 | WX_BAR |
| 支付宝付款码、支付宝条码、支付宝扫码收款 | 支付宝条码 | ALI_BAR |
| 云闪付付款码、云闪付条码、云闪付扫码收款 | 云闪付条码 | YSF_BAR |
| 微信扫码、微信二维码、微信主扫 | 微信扫码 | WX_NATIVE |
| App支付、微信App支付、iOS支付、Android支付 | 微信APP | WX_APP |
| 支付宝App支付、支付宝移动应用 | 支付宝APP | ALI_APP |
| 微信小程序、微信小程序支付 | 微信小程序 | WX_LITE |
| 支付宝小程序、支付宝小程序支付 | 支付宝小程序 | ALI_LITE |
| 支付宝生活号、支付宝服务窗 | 支付宝生活号 | ALI_JSAPI |
| 云闪付JSAPI | 云闪付jsapi | YSF_JSAPI |
| 微信JSAPI、微信公众号、微信内H5 | 微信公众号 | WX_JSAPI |
| 微信H5、微信手机网页 | 微信H5 | WX_H5 |
| 支付宝电脑网站、支付宝PC | 支付宝PC网站 | ALI_PC |
| 支付宝WAP、支付宝手机网页 | 支付宝WAP | ALI_WAP |
| 支付宝二维码、支付宝扫码 | 支付宝二维码 | ALI_QR |
| 支付宝订单码 | 支付宝订单码 | ALI_OC |
| 快捷支付、银行卡快捷支付、代扣 | 快捷支付 | BANK_AGREE |
| 快捷支付收银台 | 快捷支付收银台 | BANK_QUICK |
| 网银B2C、个人网银 | 网银B2C | BANK_B2C |
| 网银B2B、企业网银 | 网银B2B | BANK_B2B |
| 银行卡转账 | 银行卡转账 | BANK_TRANSFER |
| 银行卡转账收银台 | 银行卡转账收银台 | BANK_TRANSFERCASHIER |

---

## 支付方式说明

### QR_CASHIER（聚合扫码）

**场景描述**：用户扫商家二维码，跳转到收银台完成支付

**适用场景**：
- 商家展示二维码
- 用户扫码跳转到收银台
- 聚合码收款

**特点**：
- 已集成获取用户ID的实现
- 支持多种支付方式
- 用户扫码后选择支付方式

**关键词**：二维码收银台、扫码收银台、聚合码、聚合收银台、用户扫商家

---

### AUTO_BAR（聚合条码）

**场景描述**：商家扫用户付款码，自动识别条码类型（微信/支付宝/云闪付等）

**适用场景**：
- 线下门店收款
- 用户出示付款码
- 扫码枪收款

**特点**：
- 自动识别条码类型
- 支持微信、支付宝、云闪付等
- 无需指定具体支付渠道
- channelExtra必须传authCode

**关键词**：付款码、条码支付、扫码枪、被扫、聚合码支付、自动识别、商家扫用户

---

### WX_BAR / ALI_BAR / YSF_BAR（条码支付）

**场景描述**：用户出示付款码，商家扫码收款

**适用场景**：
- 线下门店收款
- 便利店、商超、餐饮店
- 面对面收款

**特点**：
- 用户主动出示付款码
- 商家使用扫码枪扫码
- 需要指定具体支付渠道
- channelExtra必须传authCode

---

### WX_NATIVE（微信扫码支付）

**场景描述**：商家生成微信二维码，用户主动扫码付款

**适用场景**：
- 商品售卖
- 静态码收款
- 动态码收款

**特点**：
- 商家展示二维码
- 用户主动扫码
- 仅支持微信
- channelExtra可传payDataType设置返回类型

---

### WX_LITE / ALI_LITE（小程序支付）

**场景描述**：微信/支付宝小程序内调起支付

**适用场景**：
- 小程序购物
- 小程序内服务购买
- 小程序收银台

**特点**：
- 小程序专用
- 调起小程序支付
- WX_LITE需要channelExtra传openid

---

### WX_H5（微信H5支付）

**场景描述**：手机浏览器H5页面内唤起微信支付

**适用场景**：
- 移动端网页内支付
- 手机浏览器支付
- WAP网站支付

**特点**：
- 唤起微信客户端
- 需要配置支付域名

---

### ALI_PC（支付宝PC网站支付）

**场景描述**：PC端电脑网站支付宝支付

**适用场景**：
- PC端电商网站
- 在线服务平台
- 电脑网页支付

**特点**：
- PC端专用
- 跳转到支付宝收银台
- channelExtra可传payDataType设置返回类型

---

### BANK_AGREE（快捷支付）

**场景描述**：银行卡快捷支付/代扣

**适用场景**：
- 会员订阅/连续包月
- 自动续费
- 周期性扣款
- 银行卡快捷支付

**特点**：
- 需要先绑卡
- 支持周期性扣款
- 需要用户签约授权

---

## 支付方式选择建议

### 线下门店

| 场景 | 推荐支付方式 |
|------|--------------|
| 用户出示付款码（聚合） | AUTO_BAR |
| 用户出示微信付款码 | WX_BAR |
| 用户出示支付宝付款码 | ALI_BAR |
| 用户出示云闪付付款码 | YSF_BAR |
| 商家出示微信二维码 | WX_NATIVE |
| 聚合码收款 | QR_CASHIER |

### 线上业务

| 场景 | 推荐支付方式 |
|------|--------------|
| 原生App（微信） | WX_APP |
| 原生App（支付宝） | ALI_APP |
| 微信小程序 | WX_LITE |
| 支付宝小程序 | ALI_LITE |
| 手机网页（微信） | WX_H5 |
| 手机网页（微信公众号） | WX_JSAPI |
| 手机网页（支付宝生活号） | ALI_JSAPI |
| 手机网页（云闪付） | YSF_JSAPI |
| PC端电脑网站（支付宝） | ALI_PC |

### 银行卡支付

| 场景 | 推荐支付方式 |
|------|--------------|
| 快捷支付/代扣 | BANK_AGREE |
| 快捷支付收银台 | BANK_QUICK |
| 网银B2C | BANK_B2C |
| 网银B2B | BANK_B2B |
| 银行卡转账 | BANK_TRANSFER |
| 银行卡转账收银台 | BANK_TRANSFERCASHIER |

---

## 澄清话术

当用户描述模糊或关键词匹配不明确时，使用以下模板进行支付方式选择：

### 标准澄清模板

```
请确认您的业务场景：

1. 线下门店收款
   - AUTO_BAR：聚合条码，商家扫用户付款码（自动识别微信/支付宝/云闪付）
   - WX_BAR：微信条码支付
   - ALI_BAR：支付宝条码支付
   - YSF_BAR：云闪付条码支付
   - QR_CASHIER：聚合扫码，用户扫商家二维码

2. 线上App支付
   - WX_APP：微信APP支付
   - ALI_APP：支付宝APP支付

3. 小程序支付
   - WX_LITE：微信小程序支付
   - ALI_LITE：支付宝小程序支付

4. 手机网页支付
   - WX_H5：微信H5支付
   - WX_JSAPI：微信公众号支付
   - ALI_JSAPI：支付宝生活号支付
   - YSF_JSAPI：云闪付JSAPI支付

5. PC端网页支付
   - ALI_PC：支付宝PC网站支付

6. 银行卡支付
   - BANK_AGREE：快捷支付/代扣
   - BANK_B2C：网银B2C
   - BANK_B2B：网银B2B
   - BANK_TRANSFER：银行卡转账

请描述您的具体业务需求？
```

---

## 注意事项

1. **核心收银台**：QR_CASHIER 和 AUTO_BAR 是核心收银台支付方式
2. **wayCode 参数**：调用统一支付下单接口时，需要传入对应的 wayCode 参数
3. **签名方式**：目前只支持MD5签名方式
4. **支付方式文档**：具体支付方式的详细参数请参考 [统一支付下单文档](https://doc.jeequan.com/#/integrate/open/api/85)

---

## 三、API 接口路由

# API 路由表

Jeepay 开源版支付接口文档路由表。

---

## 对接指引

| 文档名称 | 页面ID | 文档链接 | 说明 |
|----------|--------|----------|------|
| 接口规则 | 81 | https://doc.jeequan.com/#/integrate/open/api/81 | 签名方式、参数格式、通用规则 |
| SDK下载 | 116 | https://doc.jeequan.com/#/integrate/open/api/116 | 代码示例、SDK下载 |

---

## 支付接口

| 文档名称 | 页面ID | 文档链接 | 说明 |
|----------|--------|----------|------|
| 统一支付下单 | 85 | https://doc.jeequan.com/#/integrate/open/api/85 | 核心下单接口 |
| 查询支付订单 | 86 | https://doc.jeequan.com/#/integrate/open/api/86 | 查询订单状态 |
| 支付关闭订单 | 87 | https://doc.jeequan.com/#/integrate/open/api/87 | 关闭未支付订单 |
| 支付结果查询 | 88 | https://doc.jeequan.com/#/integrate/open/api/88 | 查询支付结果 |
| 获取渠道用户ID | 89 | https://doc.jeequan.com/#/integrate/open/api/89 | 获取渠道用户标识 |

---

## 退款接口

| 文档名称 | 页面ID | 文档链接 | 说明 |
|----------|--------|----------|------|
| 发起支付退款 | 90 | https://doc.jeequan.com/#/integrate/open/api/90 | 退款接口 |
| 查询退款订单 | 91 | https://doc.jeequan.com/#/integrate/open/api/91 | 查询退款状态 |
| 退款结果通知 | 92 | https://doc.jeequan.com/#/integrate/open/api/92 | 退款异步通知 |

---

## 转账接口

| 文档名称 | 页面ID | 文档链接 | 说明 |
|----------|--------|----------|------|
| 发起转账订单 | 93 | https://doc.jeequan.com/#/integrate/open/api/93 | 转账接口 |
| 查询转账订单 | 94 | https://doc.jeequan.com/#/integrate/open/api/94 | 查询转账状态 |
| 转账结果通知 | 95 | https://doc.jeequan.com/#/integrate/open/api/95 | 转账异步通知 |

---

## 分账接口

| 文档名称 | 页面ID | 文档链接 | 说明 |
|----------|--------|----------|------|
| 绑定分账用户 | 96 | https://doc.jeequan.com/#/integrate/open/api/96 | 绑定分账接收方 |
| 发起订单分账 | 97 | https://doc.jeequan.com/#/integrate/open/api/97 | 订单分账接口 |

---

## API 调用流程

### 基础调用流程

```
1. 读取接口规则 (id: 81)
   └── 了解签名方式、参数格式、通用规则

2. 下载SDK (id: 116)
   └── 获取代码示例

3. 根据支付方式获取对应接口文档
   └── 调用统一支付下单接口
```

### 支付调用流程

```
1. 调用统一支付下单接口 (id: 85)
   └── 传入支付参数，获取支付凭证

2. 调用支付（根据支付方式）
   └── JSAPI支付、H5支付、APP支付等

3. 主动查询支付结果 (id: 88)
   └── 或接收异步通知

4. 查询支付订单 (id: 86)
   └── 主动查询订单状态
```

### 退款调用流程

```
1. 调用发起支付退款接口 (id: 90)
   └── 传入退款参数

2. 接收退款结果通知 (id: 92)
   └── 验签、处理业务逻辑、返回 success

3. 查询退款订单 (id: 91)
   └── 主动查询退款状态
```

### 转账调用流程

```
1. 调用发起转账订单接口 (id: 93)
   └── 传入转账参数

2. 接收转账结果通知 (id: 95)
   └── 验签、处理业务逻辑、返回 success

3. 查询转账订单 (id: 94)
   └── 主动查询转账状态
```

### 分账调用流程

```
1. 绑定分账用户 (id: 96)
   └── 绑定分账接收方

2. 发起订单分账 (id: 97)
   └── 传入分账参数
```

---

## 文档获取方式

### 在线文档

所有文档可通过以下链接访问：

- **API文档**：https://doc.jeequan.com/#/integrate/open/api/{页面ID}

### 文档获取 API

如需程序化获取文档内容，可使用以下 API：

```bash
# 获取文档详情
curl -X POST "https://doc.jeequan.com/doc-wiki/open-api/integrate/page/detail" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "_=https://doc.jeequan.com&_lang=zh-CN&pageId={页面ID}&space=open-api&integrate=open&version=&userUuid=&accessPassword="
```

---

## 注意事项

1. **文档更新**：文档内容可能会更新，建议以在线文档为准
2. **测试环境**：测试环境信息请参考接口规则文档
3. **生产环境**：生产环境网关地址为当前项目部署地址

---

## 四、SDK 集成指引

# SDK 集成指引

以下为 Jeepay Java SDK 的集成规则和常见坑点，**严禁在未阅读全部内容的情况下编写 SDK 相关代码**。每条规则均来自 SDK 源码分析，请逐条阅读并确认后再继续。

---

## SDK Maven 依赖

```xml
<dependency>
    <groupId>com.jeequan</groupId>
    <artifactId>jeepay-sdk-java</artifactId>
    <version>1.6.1</version>
</dependency>
```

> SDK 具体版本以 [SDK下载文档](https://doc.jeequan.com/#/integrate/open/api/116) 中发布的最新版本为准。

---

## SDK 初始化

### getInstance 模式（单商户 / 多商户均适用）

SDK 内部通过 `static HashMap<appId, JeepayClient>` 缓存实例，`getInstance(appId, apiKey, apiBase)` 方法加 `synchronized` 保证线程安全。同一个 `appId` 多次调用返回**同一个实例**，不同 `appId` 返回不同实例，天然支持多商户。

```java
// 单商户
JeepayClient client = JeepayClient.getInstance(appId, apiKey, apiBase);

// 多商户：按 appId 区分，各自独立
JeepayClient clientA = JeepayClient.getInstance(merchantA_appId, merchantA_apiKey, apiBase);
JeepayClient clientB = JeepayClient.getInstance(merchantB_appId, merchantB_apiKey, apiBase);
```

> ⚠️ **线程安全注意**：`getInstance()` 返回的实例被同 `appId` 的所有线程共享。如果对返回的实例调用 `setApiKey()` / `setApiBase()`，会影响所有使用该 `appId` 的线程。多商户场景下，每个商户只需调用一次 `getInstance()` 并复用即可，**不要修改已有实例的属性**。

> ⛔ **禁止使用 `new JeepayClient()` 构造函数**：三参构造函数的参数顺序为 `(apiBase, signType, apiKey)`，不含 `appId`，且类中没有 `setAppId()` 方法——构造出来的实例 `appId` 永远为 null，多商户场景必然失败。

**适用场景**：单商户接入、支付平台、聚合收银台、SaaS 多租户等。

### Spring Boot 集成方式

通过配置文件管理密钥，避免硬编码：

**配置文件** (`application.yml`)：

```yaml
jeepay:
  appId: "你的应用ID"
  apiKey: "你的API密钥"
  apiBase: "https://你的网关地址"
  mchNo: "你的商户号"
```

**配置 Bean**：

```java
@Component
@ConfigurationProperties(prefix = "jeepay")
public class JeepayBean {
    private String appId;
    private String apiKey;
    private String apiBase;
    private String mchNo;
    // getter/setter
}
```

**使用方式**：

```java
@Autowired
private JeepayBean jeepayBean;

// 单商户 / 多商户均使用 getInstance
JeepayClient client = JeepayClient.getInstance(
    jeepayBean.getAppId(), jeepayBean.getApiKey(), jeepayBean.getApiBase());
```

---

## 核心 API 路径对照表

| Request 类 | API 路径 | 说明 |
|-----------|----------|------|
| PayOrderCreateRequest | `api/pay/unifiedOrder` | 统一下单 |
| PayOrderQueryRequest | `api/pay/query` | 查询订单 |
| PayOrderCloseRequest | `api/pay/close` | 关闭订单 |
| RefundOrderCreateRequest | `api/refund/refundOrder` | 发起退款 |
| RefundOrderQueryRequest | `api/refund/query` | 查询退款 |
| TransferOrderCreateRequest | `api/transferOrder` | 发起转账 |
| TransferOrderQueryRequest | `api/transfer/query` | 查询转账 |
| DivisionReceiverBindRequest | `api/division/receiver/bind` | 绑定分账用户 |
| PayOrderDivisionExecRequest | `api/division/exec` | 发起订单分账 |
| ChannelUserRequest | `api/channelUserId/get` | 获取渠道用户ID |

---

## 请求与响应机制

### 请求流程（SDK 自动处理）

SDK 执行 `client.execute(request)` 时自动完成以下操作：

1. 向请求参数中注入 `version`（固定 `"1.0"`）、`signType`（固定 `"MD5"`）、`reqTime`（当前毫秒时间戳）
2. 对所有参数（含注入字段）计算 MD5 签名，将 `sign` 字段加入参数
3. 将参数序列化为 JSON，通过 POST 发送到 `apiBase + "/" + request.getApiUri()`

**禁止手动添加** `version`、`signType`、`reqTime`、`sign` 字段，SDK 已自动处理。

### 响应结构

```json
{"code": 0, "msg": "SUCCESS", "sign": "ABCDEF...", "data": {"payOrderId": "...", ...}}
```

- `code`：状态码，`0` 表示成功
- `msg`：状态描述
- `sign`：签名（仅覆盖 `data` 字段，不包含 `code`/`msg`）
- `data`：业务数据（JSONObject）

### isSuccess(apiKey) 行为

```java
// SDK 源码逻辑：
public boolean isSuccess(String apiKey) {
    if (StringUtils.isEmpty(apiKey)) return code == 0;      // 无 apiKey 时仅检查 code
    return code == 0 && checkSign(apiKey);                   // 有 apiKey 时同时验签
}
```

**必须传入 apiKey**：如果 `isSuccess()` 不传 `apiKey`（或传空），SDK **不会验签**，仅检查 `code == 0`。这是安全风险——可能接受伪造响应。

```java
// ✅ 正确 — 传入 apiKey，同时检查 code 和验签
if (response.isSuccess(apiKey)) { ... }

// ❌ 错误 — 不传 apiKey，跳过验签，存在安全风险
if (response.isSuccess(null)) { ... }
if (response.getCode() == 0) { ... }
```

### 请求地址构建

SDK 内部构建请求地址的规则：`apiBase + "/" + request.getApiUri()`

```java
String reqUrl = apiBase + "/" + request.getApiUri();
// 示例：http://aaa.xxx.com/api/pay/unifiedOrder
```

---

## 签名算法（SDK 已封装，禁止手动实现）

Jeepay 固定使用 MD5 签名，SDK 工具类：`com.jeequan.jeepay.util.JeepayKit`

### 签名流程（SDK 内部）

1. 过滤空值：移除 `value` 为 null 或空字符串 `""` 的参数
2. 按参数名做**大小写不敏感排序**（`String.CASE_INSENSITIVE_ORDER`）
3. 拼接为 `key1=value1&key2=value2&...`
4. 末尾追加 `key=apiKey`
5. 对拼接字符串做 MD5，结果转**大写**

### 签名示例

```
参数：{mchNo=M1621873433953, appId=60cc09bce4b0f1c0b83761c9, amount=100}
排序拼接：amount=100&appId=60cc09bce4b0f1c0b83761c9&mchNo=M1621873433953&key=你的apiKey
MD5结果：E10ADC3949BA59ABBE56E057F20F883E（大写）
```

### 验签机制

SDK 验签时对响应中的 `data` 字段（JSONObject）重新计算签名，与响应中的 `sign` 字段比对。`sign` 仅覆盖 `data`，不包含 `code`/`msg`。

---

## 常见参数注意事项

### 金额单位

所有金额参数（amount、refundAmount）单位均为**分**，整数类型。

```java
// ✅ 正确 — 1元 = 100分
model.setAmount(100L);

// ❌ 错误 — 传入元
model.setAmount(1L);
```

### 商户订单号唯一性

`mchOrderNo`（支付/转账）和 `mchRefundNo`（退款）由商户系统生成，必须保证**全局唯一**。重复的订单号会报错。

```java
// 常见做法：前缀 + 时间戳 + 随机数
model.setMchOrderNo("mho" + System.currentTimeMillis());
```

### channelExtra 参数

不同支付方式需要传入不同的 channelExtra JSON：

| 支付方式 | channelExtra | 说明 |
|----------|-------------|------|
| WX_LITE / WX_JSAPI | `{"openid": "用户openid"}` | 微信小程序/公众号需传 openid |
| WX_BAR / ALI_BAR / AUTO_BAR | `{"authCode": "用户付款码"}` | 条码支付需传付款码 |
| QR_CASHIER | `{"payDataType": "codeImgUrl"}` | 收银台可指定返回类型 |
| WX_APP / ALI_APP | 不需要 | APP支付无需 channelExtra |

```java
JSONObject extra = new JSONObject();
extra.put("openid", "用户openid");
model.setChannelExtra(extra.toString());
```

### currency 字段

固定传入 `"CNY"`。

---

## 签名失败级联误判链

遇到签名相关错误时，严禁凭猜测归因，必须按以下顺序排查。每个错误场景都附带了常见的**错误推理链**，帮助避免级联误判。

### 误判链 1："通信秘钥错误"

```
错误信息："通信秘钥错误"
│
├── ❌ 错误推理链：
│   看到"秘钥错误" → 认为 apiKey 配错了 → 直接让用户重新配置 apiKey
│   → 用户确认 apiKey 没问题 → 怀疑是网关环境问题 → 浪费大量排查时间
│
└── ✅ 正确排查顺序：
    1. 检查签名参数是否包含 sign 字段（签名前需移除 sign）
    2. 检查参数排序是否按 ASCII 升序（key1=value1&key2=value2&...）
    3. 检查签名拼接末尾是否附加了 key=apiKey
    4. 检查空值参数是否已过滤（空值不参与签名）
    5. 检查 MD5 结果是否转为大写
    6. 最后才检查 apiKey 是否与 Jeepay 运营平台配置一致
```

### 误判链 2："验签失败"

```
错误信息："验签失败"
│
├── ❌ 错误推理链：
│   看到"验签失败" → 猜测 MD5 算法实现有问题 → 手动重写签名逻辑
│   → 引入新 bug → 更难排查
│
└── ✅ 正确排查顺序：
    1. 是否使用了 SDK（Jeepay SDK 已封装签名逻辑，直接使用即可）
    2. isSuccess() 是否传入了 apiKey（不传则跳过验签）
    3. 响应中的 sign 字段是否完整（截断会导致验签失败）
    4. 请求和响应是否使用了不同的 apiKey
```

### 误判链 3：SDK 集成后报签名错误

```
场景：首次集成 SDK 后调用接口返回签名错误
│
├── ❌ 错误推理链：
│   报签名错误 → 认为需要手动实现签名 → 自己写 MD5 逻辑
│   → 与 SDK 内部签名冲突 → 双重签名 → 持续报错
│
└── ✅ 正确排查顺序：
    1. 检查是否手动添加了 version/signType/reqTime/sign 字段（SDK 自动注入，禁止手动添加）
    2. 检查 bizModel 中的参数值是否含空字符串（空值参与签名会导致结果不同）
    3. 检查是否传入了 amount 参数但类型不是 Long（如传了浮点数 1.0）
```

---

## 非 Java 语言对接

当用户项目非 Java 时，先确认用户是否使用其项目语言直接对接 HTTP API，然后参考 Java 方式的接入步骤及 [Jeepay 在线文档](https://doc.jeequan.com) 说明进行引导。

核心差异：

- 需自行实现 MD5 签名算法（参考上方签名算法章节）
- 需自行实现 HTTP 请求和响应 JSON 解析
- 异步通知验签逻辑需自行实现（签名算法与请求签名相同）
- 请求参数需额外注入 `version`（`"1.0"`）、`signType`（`"MD5"`）、`reqTime`（毫秒时间戳）

### Python SDK 多商户场景

Python SDK 使用全局静态配置（`AppConfig.set_xxx()`），天然适用于单商户场景。多商户场景有两种解决思路：

**思路一：每次调用前切换配置**（适用于并发量低的场景）

```python
from jeepay.app_config import AppConfig

def pay_for_merchant(merchant_config, order_params):
    # 切换到目标商户配置
    AppConfig.set_mch_no(merchant_config["mchNo"])
    AppConfig.set_app_id(merchant_config["appId"])
    AppConfig.set_api_key(merchant_config["apiKey"])
    return jeepay.Pay.create(**order_params)
```

**注意**：此方式非线程安全，多线程环境下需加锁或使用线程局部变量。

**思路二：直接 HTTP 调用 + 手动签名**（适用于高并发多商户场景）

绕过 SDK 的全局配置，直接构造 HTTP 请求并手动签名：

```python
import hashlib
import requests

def call_jeepay_api(api_key, api_base, api_path, biz_params):
    # 注入公共参数
    biz_params["version"] = "1.0"
    biz_params["signType"] = "MD5"
    biz_params["reqTime"] = str(int(time.time() * 1000))

    # 手动签名
    sign_str = "&".join(f"{k}={v}" for k, v in sorted(biz_params.items(), key=lambda x: x[0].lower()) if v)
    sign_str += f"&key={api_key}"
    biz_params["sign"] = hashlib.md5(sign_str.encode()).hexdigest().upper()

    # 发送请求
    resp = requests.post(f"{api_base}/{api_path}", json=biz_params)
    return resp.json()
```

---

> 文档整理时间：2026-05-19

---

## 五、上线前校验清单

# 集成校验清单

Jeepay 开源版支付集成校验清单。

---

## 一、签名校验

| 校验项 | 校验要求 | 说明 |
|--------|----------|------|
| 签名方式 | 使用 MD5 | 固定使用 MD5 签名 |
| 参数排序 | 按 key 做大小写不敏感排序 | 与 SDK `String.CASE_INSENSITIVE_ORDER` 一致 |
| 签名验证 | 异步通知必须先验签 | 确保通知来源可信 |

### 签名算法检查

```java
// MD5 签名示例
String sign = JeepayKit.getSign(params, apiKey);
```

### 签名验证检查

```java
// 验证签名（计算签名后与通知中的 sign 对比）
Map<String, Object> signParams = new HashMap<>(params);
signParams.remove("sign");
String computedSign = JeepayKit.getSign(signParams, apiKey);
if (!sign.equalsIgnoreCase(computedSign)) {
    // 验签失败，拒绝处理
    return;
}
```

---

## 二、参数校验

| 校验项 | 校验要求 | 说明 |
|--------|----------|------|
| 必填参数 | 检查所有必填参数 | 缺少必填参数会报错 |
| 参数格式 | 检查参数类型和格式 | 金额为分，时间为戳等 |
| appId 与 mchNo 匹配 | 确保参数对应关系正确 | 不匹配会报错 |

### 必填参数检查

| 参数 | 说明 | 格式要求 |
|------|------|----------|
| appId | 应用ID | String(24) |
| mchNo | 商户号 | String(30) |
| mchOrderNo | 商户订单号 | String(64) |
| wayCode | 支付方式 | String(30) |
| amount | 支付金额 | int（单位：分） |
| currency | 货币代码 | String(3)（固定：CNY） |
| subject | 商品标题 | String(128) |
| notifyUrl | 异步通知地址 | String(256) |
| sign | 签名值 | String(32) |

### 参数格式检查

| 参数 | 格式要求 | 示例 |
|------|----------|------|
| amount | 正整数，单位分 | 100（表示1元） |
| currency | 三位货币代码 | CNY |
| notifyUrl | 有效的URL格式 | https://xxx.com/notify |
| sign | 32位MD5签名 | C380BEC2BFD727A4B6845133519F3AD6 |

---

## 三、异步通知校验

| 校验项 | 校验要求 | 说明 |
|--------|----------|------|
| 验签 | 收到通知后必须先验签 | 确保通知来自 Jeepay |
| 幂等处理 | 必须进行幂等处理 | 同一订单可能收到多次通知 |
| 响应值 | 处理成功后返回 "success" | 否则会重试通知 |

### 异步通知处理流程

```
1. 收到异步通知
   └── 获取请求参数（使用动态解析，不要硬编码字段）

2. 验签
   ├── 验签成功 → 继续处理
   └── 验签失败 → 返回 "sign fail"

3. 幂等处理
   ├── 订单已处理 → 直接返回 "success"
   └── 订单未处理 → 继续处理

4. 业务处理
   ├── 处理成功 → 更新订单状态
   └── 处理失败 → 返回错误信息

5. 返回结果
   └── 返回 "success"
```

### 异步通知参数处理注意事项

> ⚠️ **重要提示**：异步通知的参数是非固定的，Jeepay 可能会在文档中增加新的通知字段。

1. **使用动态解析**：不要硬编码通知参数字段，使用动态解析方式获取参数
2. **参考在线文档**：具体的异步通知参数请参考 [支付结果查询文档](https://doc.jeequan.com/#/integrate/open/api/88) 和 [退款结果通知文档](https://doc.jeequan.com/#/integrate/open/api/92)
3. **向前兼容**：代码应能处理新增的字段，不影响现有逻辑

```java
// 示例：动态解析异步通知参数
Map<String, String> params = new HashMap<>();
Enumeration<String> paramNames = request.getParameterNames();
while (paramNames.hasMoreElements()) {
    String paramName = paramNames.nextElement();
    String paramValue = request.getParameter(paramName);
    params.put(paramName, paramValue);
}

// 使用时根据需要获取参数
String payOrderId = params.get("payOrderId");
String state = params.get("state");
// 其他参数按需获取...
```

### 幂等处理检查

```java
// 查询订单是否已处理
PayOrder payOrder = payOrderService.findByMchOrderNo(mchOrderNo);
if (payOrder != null && payOrder.getState() == PayOrder.STATE_SUCCESS) {
    // 订单已处理，直接返回成功
    response.getWriter().print("success");
    return;
}
```

---

## 四、上线前校验

| 校验项 | 校验要求 | 说明 |
|--------|----------|------|
| 网关地址切换 | 切换为生产网关 | 自行部署的服务器地址 |
| 密钥切换 | 使用生产环境密钥 | 与测试环境不同 |
| 商户状态 | 确认商户已审核通过 | 未审核无法使用 |

### 上线前检查清单

| 序号 | 检查项 | 检查内容 | 状态 |
|------|--------|----------|------|
| 1 | 网关地址 | 已切换为生产网关（自行部署地址） | □ |
| 2 | 商户号 | 使用生产环境商户号 | □ |
| 3 | appId | 使用生产环境应用ID | □ |
| 4 | appSecret | 使用生产环境密钥 | □ |
| 5 | 签名方式 | 已配置正确的签名方式 | □ |
| 6 | 异步通知地址 | 已配置生产环境通知地址 | □ |
| 7 | 商户状态 | 商户已审核通过 | □ |
| 8 | 应用状态 | 应用已启用 | □ |

---

## 五、安全红线检查

| 序号 | 红线规则 | 检查内容 | 状态 |
|------|----------|----------|------|
| 1 | 私钥禁止存客户端 | 私钥仅保存在服务端 | □ |
| 2 | 私钥禁止记日志 | 日志中不包含私钥信息 | □ |
| 3 | 私钥禁止传公共仓库 | 私钥未上传到代码仓库 | □ |
| 4 | 前台支付结果不可信 | 以异步通知或查单接口为准 | □ |
| 5 | 未确认不重付 | 未确认支付结果前不重复扣款 | □ |
| 6 | 异步通知必须先验签 | 收到通知后先验签 | □ |

---

## 六、错误处理检查

| 序号 | 检查项 | 检查内容 | 状态 |
|------|--------|----------|------|
| 1 | 错误码处理 | 正确处理返回的错误码 | □ |
| 2 | 异常处理 | 捕获并处理异常 | □ |
| 3 | 日志记录 | 记录关键操作日志 | □ |
| 4 | 重试机制 | 实现合理的重试机制 | □ |

---

## 七、性能检查

| 序号 | 检查项 | 检查内容 | 状态 |
|------|--------|----------|------|
| 1 | 连接超时 | 设置合理的连接超时时间 | □ |
| 2 | 读取超时 | 设置合理的读取超时时间 | □ |
| 3 | 并发处理 | 支持并发请求处理 | □ |
| 4 | 资源释放 | 正确释放连接资源 | □ |

---

## 八、测试检查

| 序号 | 检查项 | 检查内容 | 状态 |
|------|--------|----------|------|
| 1 | 下单测试 | 测试统一下单接口 | □ |
| 2 | 支付测试 | 测试支付流程 | □ |
| 3 | 退款测试 | 测试退款流程 | □ |
| 4 | 异步通知测试 | 测试异步通知处理 | □ |
| 5 | 查单测试 | 测试查询订单接口 | □ |
| 6 | 关单测试 | 测试关闭订单接口 | □ |

---

## 九、问题排查检查

| 序号 | 检查项 | 检查内容 | 状态 |
|------|--------|----------|------|
| 1 | 错误日志 | 记录完整的错误日志 | □ |
| 2 | 请求日志 | 记录请求参数和响应 | □ |
| 3 | 签名日志 | 记录签名过程（可选） | □ |
| 4 | 问题定位 | 能快速定位问题原因 | □ |

---

## 十、开源版特有检查

| 序号 | 检查项 | 检查内容 | 状态 |
|------|--------|----------|------|
| 1 | 部署环境 | 确认Jeepay开源版已正确部署 | □ |
| 2 | 数据库配置 | 确认数据库连接配置正确 | □ |
| 3 | Redis配置 | 确认Redis连接配置正确 | □ |
| 4 | 支付渠道配置 | 确认支付渠道参数配置正确 | □ |
| 5 | 商户入驻 | 确认商户已在运营平台入驻 | □ |
| 6 | 应用配置 | 确认商户应用已正确配置 | □ |

---

> 文档整理时间：2026-05-15

---

## 六、日志输出指引

# 日志输出指引

每次调用 Jeepay API 时，必须输出请求和响应的详细日志，便于问题排查和审计追踪。

---

## 日志要求

1. **请求日志**（调用前输出）：包含实际请求地址（完整 URL）、关键业务参数（脱敏处理）
2. **响应日志**（调用后输出）：包含完整的响应数据（code、msg、业务数据）

## 实际请求地址

SDK 内部构建请求地址的规则：`apiBase + "/" + request.getApiUri()`

- `apiBase`：即配置的网关地址，如 `http://aaa.xxx.com`
- `request.getApiUri()`：各请求类对应的 API 路径，如 `api/pay/unifiedOrder`
- 最终请求地址示例：`http://aaa.xxx.com/api/pay/unifiedOrder`

可通过 `request.getApiUri()` 获取路径，拼接 `apiBase` 得到完整 URL 并输出到日志。

## 日志内容规范

| 日志类型 | 必须包含字段 | 说明 |
|----------|-------------|------|
| 请求日志 | 实际请求地址(完整 URL) | `apiBase + "/" + request.getApiUri()`，明确调用的目标接口 |
| 请求日志 | 业务参数 | model 中的关键字段（金额、订单号、支付方式等），**禁止输出 apiKey** |
| 响应日志 | 响应码(code) | Jeepay 返回的状态码 |
| 响应日志 | 响应消息(msg) | Jeepay 返回的描述信息 |
| 响应日志 | 业务数据(data) | 完整的响应业务数据 JSON |

## Java SDK 日志示例

```java
// 构建请求地址
String reqUrl = jeepayBean.getDomain() + "/" + payRequest.getApiUri();

// 请求日志 - 调用前
log.info("[Jeepay] 统一下单请求 reqUrl={} mchOrderNo={} wayCode={} amount={} subject={}",
    reqUrl, model.getMchOrderNo(), model.getWayCode(), model.getAmount(), model.getSubject());

// 执行请求
PayOrderCreateResponse response = getClient().execute(payRequest);

// 响应日志 - 调用后（成功时输出完整业务数据）
if (response.isSuccess(jeepayBean.getApiKey())) {
    log.info("[Jeepay] 统一下单成功 code={} msg={} data={}",
        response.getCode(), response.getMsg(),
        com.alibaba.fastjson.JSON.toJSONString(response.get()));
} else {
    log.warn("[Jeepay] 统一下单失败 code={} msg={}", response.getCode(), response.getMsg());
}
```

## 安全红线

- **apiKey 严禁输出到日志**：apiKey 用于签名，泄露会导致安全风险
- 私钥、密钥等敏感字段一律禁止出现在日志中

---

> 文档整理时间：2026-05-19

---

## 七、Java 代码示例索引

# Jeepay 代码示例索引

Jeepay 开源版支付接口代码示例，按业务类别组织。

---

## 通用接口

| 接口 | API路径 | 在线文档 | Java 示例 | Python 示例 |
|------|---------|---------|-----------|-------------|
| 统一下单 | api/pay/unifiedOrder | [统一支付下单](https://doc.jeequan.com/#/integrate/open/api/85) | [Java](java/1_统一下单.md) | [Python](python/1_统一下单.md) |
| 查询订单 | api/pay/query | [查询支付订单](https://doc.jeequan.com/#/integrate/open/api/86) | [Java](java/2_查询订单.md) | [Python](python/2_查询订单.md) |
| 关闭订单 | api/pay/close | [关闭支付订单](https://doc.jeequan.com/#/integrate/open/api/87) | [Java](java/3_关闭订单.md) | [Python](python/3_关闭订单.md) |
| 发起退款 | api/refund/refundOrder | [发起支付退款](https://doc.jeequan.com/#/integrate/open/api/90) | [Java](java/4_退款.md) | [Python](python/4_退款.md) |
| 查询退款 | api/refund/query | [查询退款订单](https://doc.jeequan.com/#/integrate/open/api/91) | [Java](java/5_查询退款.md) | [Python](python/5_查询退款.md) |
| 异步通知验签 | — | [支付结果通知](https://doc.jeequan.com/#/integrate/open/api/88) | [Java](java/10_异步通知.md) | [Python](python/10_异步通知.md) |

---

## 转账接口

| 接口 | API路径 | 在线文档 | Java 示例 | Python 示例 |
|------|---------|---------|-----------|-------------|
| 发起转账 | api/transferOrder | [发起转账订单](https://doc.jeequan.com/#/integrate/open/api/93) | [Java](java/8_转账.md) | [Python](python/8_转账.md) |
| 查询转账 | api/transfer/query | [查询转账订单](https://doc.jeequan.com/#/integrate/open/api/94) | [Java](java/9_查询转账.md) | [Python](python/9_查询转账.md) |

---

## 分账接口

| 接口 | API路径 | 在线文档 | Java 示例 | Python 示例 |
|------|---------|---------|-----------|-------------|
| 绑定分账用户 | api/division/receiver/bind | [绑定分账用户](https://doc.jeequan.com/#/integrate/open/api/96) | [Java](java/6_绑定分账用户.md) | [Python](python/6_绑定分账用户.md) |
| 发起订单分账 | api/division/exec | [发起订单分账](https://doc.jeequan.com/#/integrate/open/api/97) | [Java](java/7_发起分账.md) | [Python](python/7_发起分账.md) |

---

> 文档整理时间：2026-05-19

---

## 八、统一下单 - Java 完整示例

# 统一下单

API 路径：`api/pay/unifiedOrder`

Request 类：`PayOrderCreateRequest`
Response 类：`PayOrderCreateResponse`

> 请求/响应参数详见 [统一支付下单文档](https://doc.jeequan.com/#/integrate/open/api/85)

---

## 响应示例

**成功响应**：

```json
{"code":0,"msg":"SUCCESS","data":{"payOrderId":"P2056570316211871745","mchOrderNo":"mho1718712345678","orderState":1,"payDataType":"codeUrl","payData":"weixin://wxpay/bizpayurl?pr=abc123"}}
```

**失败响应**：

```json
{"code":9999,"msg":"订单已过期"}
```

## 完整代码示例

```java
import com.alibaba.fastjson.JSONObject;
import com.jeequan.jeepay.JeepayClient;
import com.jeequan.jeepay.exception.JeepayException;
import com.jeequan.jeepay.model.PayOrderCreateReqModel;
import com.jeequan.jeepay.model.PayOrderCreateResModel;
import com.jeequan.jeepay.request.PayOrderCreateRequest;
import com.jeequan.jeepay.response.PayOrderCreateResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PayOrderCreateExample {

    private static final Logger log = LoggerFactory.getLogger(PayOrderCreateExample.class);
    private static final String APP_ID = "你的应用ID";
    private static final String API_KEY = "你的API密钥";
    private static final String API_BASE = "https://你的网关地址";
    private static final String MCH_NO = "你的商户号";

    /**
     * getInstance 按 appId 缓存实例，多商户传不同 appId 即可
     */
    private static JeepayClient getJeepayClient() {
        return JeepayClient.getInstance(APP_ID, API_KEY, API_BASE);
    }

    public static void main(String[] args) {
        JeepayClient client = getJeepayClient();

        PayOrderCreateReqModel model = new PayOrderCreateReqModel();
        model.setMchNo(MCH_NO);                                        // 商户号
        model.setAppId(client.getAppId());                             // 应用ID（从客户端获取）
        model.setMchOrderNo("mho" + System.currentTimeMillis());      // 商户订单号（需唯一）
        model.setWayCode("WX_NATIVE");                                 // 支付方式：WX_NATIVE-微信扫码
        model.setAmount(100L);                                         // 支付金额，单位：分（100分=1元）
        model.setCurrency("CNY");                                      // 货币代码，固定CNY
        model.setClientIp("192.168.1.100");                            // 客户端IP地址
        model.setSubject("测试商品");                                   // 商品标题
        model.setBody("商品描述");                                      // 商品描述（可选）
        model.setNotifyUrl("https://你的域名/notify/pay");              // 异步通知地址
        model.setReturnUrl("https://你的域名/return");                  // 前端跳转地址（可选）

        // channelExtra 示例（按支付方式选择）：
        // 微信小程序/公众号 — 传 openid
        // JSONObject extra = new JSONObject();
        // extra.put("openid", "用户openid");
        // model.setChannelExtra(extra.toString());
        //
        // 条码支付（WX_BAR/ALI_BAR/AUTO_BAR）— 传 authCode
        // extra.put("authCode", "用户付款码");
        // model.setChannelExtra(extra.toString());

        PayOrderCreateRequest request = new PayOrderCreateRequest();
        request.setBizModel(model);

        try {
            log.info("[Jeepay] 统一下单请求 reqUrl={} mchOrderNo={} wayCode={} amount={}",
                    API_BASE + "/" + request.getApiUri(),
                    model.getMchOrderNo(), model.getWayCode(), model.getAmount());

            PayOrderCreateResponse response = client.execute(request);

            if (response.isSuccess(API_KEY)) {
                PayOrderCreateResModel resModel = response.get();
                log.info("[Jeepay] 统一下单成功 code={} msg={} data={}",
                        response.getCode(), response.getMsg(),
                        com.alibaba.fastjson.JSON.toJSONString(resModel));

                String payOrderId = resModel.getPayOrderId();          // 支付单号（网关生成）
                String payDataType = resModel.getPayDataType();        // 支付参数类型
                String payData = resModel.getPayData();                // 支付参数内容

                log.info("payOrderId: {}", payOrderId);
                log.info("payDataType: {}", payDataType);
                log.info("payData: {}", payData);

                // payDataType 处理：
                // "payUrl" → response.sendRedirect(payData) 跳转支付页面
                // "form"  → response.getWriter().write(payData) 渲染HTML表单
                // "codeUrl" → 用 payData 生成二维码
                // "codeImgUrl" → 直接展示二维码图片

            } else {
                log.warn("[Jeepay] 统一下单失败 code={} msg={}", response.getCode(), response.getMsg());
                if (response.get() != null) {
                    log.warn("errCode: {}, errMsg: {}", response.get().getErrCode(), response.get().getErrMsg());
                }
            }
        } catch (JeepayException e) {
            log.error("[Jeepay] 统一下单异常", e);
        }
    }
}
```

---

## 九、异步通知验签 - Java 完整示例

# 异步通知验签处理

适用接口：支付通知、退款通知、转账通知

---

## 签名算法

Jeepay 使用 MD5 签名，流程：

1. 将通知参数中 `sign` 字段移除
2. 剩余参数按 key 的 ASCII 码升序排列
3. 拼接为 `key1=value1&key2=value2&...&key=apiKey`
4. 对拼接字符串做 MD5，结果转大写

SDK 工具类：`com.jeequan.jeepay.util.JeepayKit`

## 通知参数说明

异步通知的参数是**非固定的**，Jeepay 可能会在文档中增加新的通知字段。必须使用动态解析方式获取参数，不要硬编码字段。

## 完整处理流程

```java
import com.alibaba.fastjson.JSON;
import com.jeequan.jeepay.util.JeepayKit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// Spring Boot 2.x / javax
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
// Spring Boot 3.x / Jakarta EE 9+ 请改用：
// import jakarta.servlet.http.HttpServletRequest;
// import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;

public class NotifyExample {

    private static final Logger log = LoggerFactory.getLogger(NotifyExample.class);
    private static final String API_KEY = "你的API密钥";                // 单商户：直接使用配置的 apiKey
                                                                        // 多商户：根据通知中的 appId 反查对应商户的 apiKey

    /**
     * 支付异步通知
     */
    public void payNotify(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // Step 1: 动态解析通知参数（不硬编码字段，向前兼容）
        Map<String, String> params = parseNotifyParams(request);       // 动态解析所有通知参数
        log.info("[Jeepay] 支付通知参数: {}", params);

        // Step 2: 验签
        String sign = params.get("sign");                              // 获取通知中的签名值
        if (sign == null || sign.isEmpty()) {
            log.warn("[Jeepay] 通知签名为空");
            response.getWriter().print("fail");                        // 返回fail，触发Jeepay重试
            return;
        }

        if (!verifySign(params, sign)) {                               // 使用API_KEY验签
            log.warn("[Jeepay] 通知验签失败");
            response.getWriter().print("fail");
            return;
        }

        // Step 3: 幂等处理（同一订单可能收到多次通知）
        String mchOrderNo = params.get("mchOrderNo");                  // 商户订单号
        // Order order = orderService.findByMchOrderNo(mchOrderNo);
        // if (order != null && order.isProcessed()) {
        //     response.getWriter().print("success");
        //     return;
        // }

        // Step 4: 业务处理
        String payOrderId = params.get("payOrderId");                  // 支付单号（网关生成）
        String state = params.get("state");                            // 订单状态：2-支付成功

        if ("2".equals(state)) {
            log.info("[Jeepay] 支付成功 payOrderId={} mchOrderNo={}", payOrderId, mchOrderNo);
            // 更新本地订单状态...
        } else {
            log.info("[Jeepay] 支付状态 state={} payOrderId={}", state, payOrderId);
        }

        // Step 5: 返回成功标识（Jeepay 收到 "success" 后停止重试）
        response.getWriter().print("success");                         // 必须返回"success"，否则会持续重试
    }

    /**
     * 动态解析通知参数
     */
    private Map<String, String> parseNotifyParams(HttpServletRequest request) {
        Map<String, String> params = new HashMap<>(16);                // 存储解析后的参数键值对
        Enumeration<String> paramNames = request.getParameterNames();  // 获取所有参数名
        while (paramNames.hasMoreElements()) {
            String paramName = paramNames.nextElement();               // 参数名
            params.put(paramName, request.getParameter(paramName));    // 参数值
        }
        return params;
    }

    /**
     * 验证通知签名
     * 使用 SDK 的 JeepayKit.getSign() 方法计算签名，与通知中的 sign 对比
     */
    private boolean verifySign(Map<String, String> params, String sign) {
        Map<String, Object> signParams = new HashMap<>(params.size()); // 用于签名的参数集合
        for (Map.Entry<String, String> entry : params.entrySet()) {
            if (!"sign".equals(entry.getKey())) {                      // 排除sign字段本身
                signParams.put(entry.getKey(), entry.getValue());
            }
        }
        String computedSign = JeepayKit.getSign(signParams, API_KEY);  // 使用SDK计算签名
        return sign.equalsIgnoreCase(computedSign);                    // 对比签名（不区分大小写）
    }
}
```

## 验签核心逻辑

```java
// JeepayKit.getSign() 内部实现：
// 1. 过滤空值，拼接为 key1=value1&key2=value2&
// 2. 按 ASCII 升序排列
// 3. 末尾追加 key=apiKey
// 4. MD5 后转大写

Map<String, Object> signParams = new HashMap<>();
// 移除 sign 字段后放入所有参数
signParams.put("appId", "...");                                      // 应用ID
signParams.put("mchNo", "...");                                     // 商户号
signParams.put("payOrderId", "...");                                // 支付订单号
signParams.put("state", "2");                                       // 订单状态
// ... 其他参数

String computedSign = JeepayKit.getSign(signParams, API_KEY);       // 使用API密钥计算签名
boolean isValid = notifySign.equalsIgnoreCase(computedSign);        // 验证签名是否一致
```

## 通知示例

**支付成功通知参数**：

```
payOrderId=P2056570316211871745&mchOrderNo=mho1718712345678&appId=60cc09bce4b0f1c0b83761c9&mchNo=M1621873433953&wayCode=WX_NATIVE&amount=1&currency=CNY&state=2&clientIp=192.168.1.100&successTime=2024-06-18+11%3A05%3A30&sign=ABCD1234EFGH5678IJKL9012MNOP3456
```

**退款成功通知参数**：

```
refundOrderId=R2056570316211871745&mchRefundNo=REF1779159547217&payOrderId=P2056570316211871745&mchOrderNo=mho1718712345678&appId=60cc09bce4b0f1c0b83761c9&mchNo=M1621873433953&refundAmount=100&currency=CNY&state=2&successTime=2024-06-18+11%3A05%3A53&sign=QRST7890UVWX1234YZAB5678CDEF9012
```

> 各通知字段详见 [支付结果通知](https://doc.jeequan.com/#/integrate/open/api/88)、[退款结果通知](https://doc.jeequan.com/#/integrate/open/api/92)、[转账结果通知](https://doc.jeequan.com/#/integrate/open/api/95)

---

## 备注：完整资料索引（按需主动拉取）

- 查询订单、关闭订单、退款、查询退款、转账、查询转账、绑定分账用户、发起分账 → https://github.com/jeequan/jeepay-skills/tree/master/skills/jeepay-open-integration/references/code-examples/java/
- Python 代码示例 → https://github.com/jeequan/jeepay-skills/tree/master/skills/jeepay-open-integration/references/code-examples/python/
- 错误码文档 → https://github.com/jeequan/jeepay-skills/blob/master/skills/jeepay-open-integration/references/docs/Jeepay-错误码文档.md
- 常见问题文档 → https://github.com/jeequan/jeepay-skills/blob/master/skills/jeepay-open-integration/references/docs/Jeepay-常见问题文档.md
- 在线接口文档 → https://doc.jeequan.com/#/integrate/open
