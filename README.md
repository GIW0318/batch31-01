# GSB Bugfix Task
## 题面
开放世界同步列表一紧，预算和优先级就乱：预算为 0 还发实体，负预算接受，重复 id 出现两次，过期实体不剔除，敌人和道具同优先级，距离相同顺序每次不同。interest_management.py 的 select 负责选实体；tests/test_interest_management.py 15 条红。要预算边界、id 唯一、坐标合法、陈旧过滤、类型优先级、同距按 id 稳定排序，非法输入抛 ValueError。

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
