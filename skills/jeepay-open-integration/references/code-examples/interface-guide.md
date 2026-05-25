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
