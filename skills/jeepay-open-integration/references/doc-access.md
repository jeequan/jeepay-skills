# 文档访问规范

所有 Jeepay 开源版的文档地址均为**在线动态链接**，使用以下方式获取文档内容。

---

## URL 结构说明

```
https://doc.jeequan.com/#/integrate/open/api/81
                         │    │    │    │    │
                         │    │    │    │    └── 页面 ID (pageId)
                         │    │    │    └── 空间编码
                         │    │    └── 整合空间标识 (integrate)
                         │    └── 空间类型
                         └── Hash 路由
```

## 文档获取脚本

```bash
#!/bin/bash

# 配置
BASE_URL="https://doc.jeequan.com"
INTEGRATE="open"
PAGE_ID="$1"  # 从 URL 中提取的页面 ID，如 81

# Step 1: 获取整合空间详情（可选，用于确认空间结构）
DETAIL=$(curl -sL \
  -X POST "$BASE_URL/doc-wiki/open-api/integrate/detail" \
  -d "integrate=$INTEGRATE&version=&_=$BASE_URL/&_lang=zh-CN")

# Step 2: 获取页面详情
# spaceUuid 根据文档类型选择：open-guide / open-api / open-issue
SPACE_UUID="open-api"  # API 文档使用此值

PAGE_CONTENT=$(curl -sL \
  -X POST "$BASE_URL/doc-wiki/open-api/integrate/page/detail" \
  -d "pageId=$PAGE_ID&space=$SPACE_UUID&integrate=$INTEGRATE&version=&userUuid=&accessPassword=&_=$BASE_URL/&_lang=zh-CN")

echo "$PAGE_CONTENT"
```

## 使用示例

```bash
# 获取统一支付下单文档（pageId=85）
./fetch-doc.sh 85

# 获取查询支付订单文档（pageId=86）
./fetch-doc.sh 86

# 获取退款文档（pageId=90）
./fetch-doc.sh 90
```

## 获取所有页面列表

```bash
# 获取开源版文档空间的所有页面
curl -sL \
  -X POST "https://doc.jeequan.com/doc-wiki/open-api/integrate/detail" \
  -d "integrate=open&version=&_=https://doc.jeequan.com/&_lang=zh-CN"
```

## 已知的页面 ID 映射

| 接口名称 | pageId | 在线文档 |
|----------|--------|----------|
| 接口规则 | 81 | https://doc.jeequan.com/#/integrate/open/api/81 |
| 统一支付下单 | 85 | https://doc.jeequan.com/#/integrate/open/api/85 |
| 查询支付订单 | 86 | https://doc.jeequan.com/#/integrate/open/api/86 |
| 支付关闭订单 | 87 | https://doc.jeequan.com/#/integrate/open/api/87 |
| 支付结果查询 | 88 | https://doc.jeequan.com/#/integrate/open/api/88 |
| 获取渠道用户ID | 89 | https://doc.jeequan.com/#/integrate/open/api/89 |
| 发起支付退款 | 90 | https://doc.jeequan.com/#/integrate/open/api/90 |
| 查询退款订单 | 91 | https://doc.jeequan.com/#/integrate/open/api/91 |
| 退款结果通知 | 92 | https://doc.jeequan.com/#/integrate/open/api/92 |
| 发起转账订单 | 93 | https://doc.jeequan.com/#/integrate/open/api/93 |
| 查询转账订单 | 94 | https://doc.jeequan.com/#/integrate/open/api/94 |
| 转账结果通知 | 95 | https://doc.jeequan.com/#/integrate/open/api/95 |
| 绑定分账用户 | 96 | https://doc.jeequan.com/#/integrate/open/api/96 |
| 发起订单分账 | 97 | https://doc.jeequan.com/#/integrate/open/api/97 |
| SDK下载 | 116 | https://doc.jeequan.com/#/integrate/open/api/116 |

---

> 文档整理时间：2026-05-15
