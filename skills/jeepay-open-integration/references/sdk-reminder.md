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
