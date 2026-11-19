# GSB Bugfix Task
## 题面
动画状态机一接位移就抖：play 新动作不重置时间，advance 负数时间倒放，speed 为 0 仍推进，循环到结尾不回到 0，根运动不累加，低优先级动画能打断高优先级。animation_blend.py 的 blend 负责切换；tests/test_animation_blend.py 15 条红。要切换重置、时间非负、速度正数、循环 wrap、根运动累加、优先级打断，非法输入抛 ValueError。

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
