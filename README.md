# GSB Bugfix Task
## 题面
副本掉落表的票号和保底对不上：票号 100 还能抽，负权重照算，重复 id 当两件，空表直接崩，保底到 10 还出普通，保底触发后计数不清零。loot_table.py 的 roll 负责抽取；tests/test_loot_table.py 15 条红。要按权重累计选档、票号边界准确、重复 id 和非法权重拒绝、保底到阈值必出史诗并清零。

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
