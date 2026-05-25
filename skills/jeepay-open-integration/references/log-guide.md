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
