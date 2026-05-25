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
