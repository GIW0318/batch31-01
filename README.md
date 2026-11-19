# GSB Bugfix Task
## 题面
成就事件重复投递后，击杀数会重复累加，阈值到了不弹成就，同一规则注册两次会发两份奖励，缺 type 的事件被静默跳过。achievement_bus.py 的 process 要处理事件和规则；tests/test_achievement_bus.py 15 条红。需要事件白名单、计数持久化、阈值只解锁一次、奖励幂等、规则 id 唯一，非法输入报 ValueError。

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
