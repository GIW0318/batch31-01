# GSB Bugfix Task
## 题面
主线任务链现在会串状态：锁着的任务能直接接，活跃任务跳步也记进度，分支选完还能改，完成时奖励重复发，失败后仍能推进，reset 把已完成任务清空。quest_state.py 的 transition 要重写状态迁移；tests/test_quest_state.py 现在 15 条全红。需要状态白名单、步骤顺序、分支一次性、完成幂等、失败终态、版本递增，非法输入抛 ValueError。

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
