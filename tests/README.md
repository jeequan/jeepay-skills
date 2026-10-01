# 离线签名示例回归

## 默认检查

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_bundle.py --check
```

不需要 requests、Flask 或 Python SDK。测试从 `sdk-reminder.md` 和生成的 `bundle.md` 提取实际 Python HTTP 示例执行，在导入前用内存替身替换 requests，并固定时间。覆盖正常下单参数、数值 0、null/空字符串、混合大小写、大小写同名/前缀参数、False/空格、UTF-8 值、旧 sign，以及调用方参数不被修改。另检查所有 Python 代码块语法和签名排序说明。不会调用真实接口、创建订单或使用真实密钥。

`signature_vectors.json` 包含固定输入、完整签名串和大写 MD5；不是从被测示例运行结果动态生成断言。测试密钥 `offline-test-key` 仅为公开测试数据。

## Java 交叉验证（可选）

已用以下真实实现运行全部 8 个向量，确认 SDK 的签名串、SDK 摘要、后端摘要均与固化向量一致：

- [后端 JeepayKit.getSign，d38becc](https://github.com/jeequan/jeepay/blob/d38becc1bbde1c5077c27facaf473606fc50129a/jeepay-core/src/main/java/com/jeequan/jeepay/core/utils/JeepayKit.java)
- `com.jeequan:jeepay-sdk-java:1.6.1`；同时核对了 [Java SDK 源码，75d1f1a](https://github.com/jeequan/jeepay-sdk-java/blob/75d1f1a0090e53fa33fefc2ff27e47ab35bb9425/src/main/java/com/jeequan/jeepay/util/JeepayKit.java)

本仓库不复制外部实现或打包依赖。如果已有编译好的 Jeepay 后端和 SDK，用 Java 11+ source-file 模式执行：

```bash
# JEEPAY_CLASSPATH 指向 jeepay-core 的编译产物、Java SDK 1.6.1、fastjson 及其运行时依赖
java -cp "$JEEPAY_CLASSPATH" tests/SignatureOracle.java tests/signature_vectors.json
```

这一步直接调用两个真实 Java 类，没有自行重写签名算法；默认 CI 仅运行上面的 Python 离线回归和 bundle 一致性检查。

## 修复前后证据

- 基线 `a89fac21f4ee95c63dea0ecc0a97e9b5d903b559`：从两个文档提取的 HTTP 示例运行 8 组输入，各因缺少 `import time` 报 `NameError`（16 个子用例错误）；另有 7 份文档排序说明检查失败
- 仅补 `import time` 后再次运行：可单独复现数值 0/False 被过滤、旧 sign 被纳入和大小写同名/前缀排序不兼容；原示例还会修改调用方字典
- 完整修复后：所有离线检查通过，8 组输入在两个实际文档示例及真实后端/Java SDK 中结果一致

范围限制：这里验证签名示例和文档一致性，不是端到端支付、HTTP 异常处理或 Python SDK 实现测试。通知示例仍需按已有说明配置商户密钥、实现业务幂等和状态更新；上线前需在自己的测试环境完成完整联调。Python 的 `str.lower` 示例针对 Jeepay 的 ASCII 参数名，不声明兼容 Java 对任意 Unicode 参数名的比较规则，且仅大小写不同的参数名若对应非 ASCII 值也不在示例兼容范围内；结构化值需先按接口要求序列化为 JSON 字符串。
