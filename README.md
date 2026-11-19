# GSB Bugfix Task
## 题面
赛道圈速判定开始放水：跳过检查点也能记一圈，顺序颠倒算完赛，起点重复通过当新圈，事件时间倒退不报错，超过最大圈速仍通过。race_checkpoints.py 的 validate_lap 负责判定；tests/test_race_checkpoints.py 15 条红。要检查点完整且顺序正确、start/finish 唯一、时间单调、超时和负圈速拒绝，非法输入抛 ValueError。

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
