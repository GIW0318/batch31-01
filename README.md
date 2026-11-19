# GSB Bugfix Task
## 题面
联机移动校验一上，瞬移和加速混过去：3 秒走 30 格也能过，时间戳相同不报错，时间倒退当零间隔，坐标缺轴直接崩，max_speed 为 0 全放行。movement_anticheat.py 的 validate_move 负责校验；tests/test_movement_anticheat.py 15 条红。要时间单调、坐标合法、欧氏距离、速度上限、lag 窗口，结果带明确 reason，非法输入抛 ValueError。

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
