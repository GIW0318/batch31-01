# GSB Bugfix Task
## 题面
手柄重映射后，按键冲突开始吞操作：一个动作绑两个键，后一个覆盖前一个；两个动作绑同一个键也静默通过；chord 超过 2 还接受；Guide/Home 被占用；大小写不同的 button 当成两个键。gamepad_mapping.py 的 validate_mapping 负责校验；tests/test_gamepad_mapping.py 15 条红。要动作白名单、动作唯一、button+chord 唯一、chord 上限、保留键拒绝、button 归一化，非法输入抛 ValueError。

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
