# GSB Bugfix Task
## 题面
多语言文本一进游戏，复数就错：英文 1 用 other，俄语 3 用 one，计数 0 没有分支，缺当前语言直接崩，缺 key 返回空串，参数占位符不替换。localization_plural.py 的 format_message 负责取词；tests/test_localization_plural.py 15 条红。要按语言选复数类别、fallback、缺 key/参数报错、计数非负整数、花括号转义，非法输入抛 ValueError。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：游戏开发
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：有外部依赖，未容器化
