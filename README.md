# GSB Bugfix Task
## 题面
服务器 tick 预算一紧，任务开始饿死：预算为 0 还执行，单条成本超预算也硬跑，重复 id 覆盖，取消任务仍在 ran 里，同优先级顺序每次不同。tick_scheduler.py 的 schedule 负责排程；tests/test_tick_scheduler.py 15 条红。要预算边界、id 唯一、成本正数、取消过滤、优先级和 deadline 排序、超预算延后，非法输入抛 ValueError。

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
