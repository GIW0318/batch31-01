# GSB Bugfix Task
## 题面
状态效果一叠加，战斗数值就漂：同一效果无限叠层，刷新把剩余时间清零，免疫列表里的效果照样挂上，到期效果不删除，tick 传负数还把时间加回去。status_effects.py 的 apply_effect 和 tick 负责结算；tests/test_status_effects.py 15 条红。要叠层上限、刷新策略、免疫拒绝、到期清理、tick 非负，非法输入抛 ValueError。

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
