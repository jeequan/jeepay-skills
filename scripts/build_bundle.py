#!/usr/bin/env python3
"""Rebuild the existing paste-in bundle without changing its source selection."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/jeepay-open-integration"
PREFIX = '<!-- Generated bundle for paste-in usage with web AI (claude.ai / ChatGPT / 通义千问 / 文心一言 / etc.) -->\n<!-- Source: https://github.com/jeequan/jeepay-skills/tree/master/skills/jeepay-open-integration -->\n<!-- Bundle 包含 SKILL.md 主体 + scene-routing / api-routing / sdk-reminder / checklist / log-guide / doc-access / 代码示例索引 -->\n<!-- 不含 docs/ 目录下的错误码 / 常见问题文档（按需单独打开），不含 Python 代码示例（如需 Python 请单独取 references/code-examples/python/） -->\n\n# Jeepay 接入助手（单文件版）\n\n> 把本文件全选复制到你的 AI 对话开头作为上下文，然后描述你要做的 Jeepay 接入任务，AI 会按本文件的指引生成代码。\n\n---\n\n'
FOOTER = '## 备注：完整资料索引（按需主动拉取）\n\n- 查询订单、关闭订单、退款、查询退款、转账、查询转账、绑定分账用户、发起分账 → https://github.com/jeequan/jeepay-skills/tree/master/skills/jeepay-open-integration/references/code-examples/java/\n- Python 代码示例 → https://github.com/jeequan/jeepay-skills/tree/master/skills/jeepay-open-integration/references/code-examples/python/\n- 错误码文档 → https://github.com/jeequan/jeepay-skills/blob/master/skills/jeepay-open-integration/references/docs/Jeepay-错误码文档.md\n- 常见问题文档 → https://github.com/jeequan/jeepay-skills/blob/master/skills/jeepay-open-integration/references/docs/Jeepay-常见问题文档.md\n- 在线接口文档 → https://doc.jeequan.com/#/integrate/open\n'
SECTIONS = [('一、主流程（来自 SKILL.md）', 'SKILL.md'),
 ('二、支付方式路由', 'references/scene-routing.md'),
 ('三、API 接口路由', 'references/api-routing.md'),
 ('四、SDK 集成指引', 'references/sdk-reminder.md'),
 ('五、上线前校验清单', 'references/checklist.md'),
 ('六、日志输出指引', 'references/log-guide.md'),
 ('七、Java 代码示例索引', 'references/code-examples/interface-guide.md'),
 ('八、统一下单 - Java 完整示例', 'references/code-examples/java/1_统一下单.md'),
 ('九、异步通知验签 - Java 完整示例', 'references/code-examples/java/10_异步通知.md')]


def render():
    sections = [f"## {title}\n\n{(SKILL / path).read_text(encoding='utf-8').strip()}"
                for title, path in SECTIONS]
    return PREFIX + "\n\n---\n\n".join(sections) + "\n\n---\n\n" + FOOTER


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed bundle is stale")
    args = parser.parse_args()
    path = SKILL / "references/bundle.md"
    content = render()
    if args.check:
        if path.read_text(encoding="utf-8") != content:
            parser.exit(1, "bundle.md is stale; run python scripts/build_bundle.py\n")
        print("bundle.md is up to date")
    else:
        path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
