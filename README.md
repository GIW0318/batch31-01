# GSB Bugfix Task
## 题面
小队阵型一接寻路，站位就乱：两个队员分到同一槽，坦克站到治疗槽，最近的空槽分给别人，重复 agent/slot id 直接崩，障碍格上的槽仍可站。formation_steering.py 的 assign 负责分配；tests/test_formation_steering.py 15 条红。要 id 唯一、角色匹配、按最近距离分配、障碍排除、空输入处理，非法输入抛 ValueError。

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
