# Slug Tool

一个零依赖 Python 命令行小工具：将文本转换为 URL 友好的 slug。

## 用法

```bash
python slug_tool.py "Harness Review: Common2!"
# harness-review-common2

printf 'API delivery demo' | python slug_tool.py
# api-delivery-demo
```

## 测试

```bash
python -m unittest test_slug_tool.py
```
