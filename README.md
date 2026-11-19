# GSB Bugfix Task
## 题面
制作系统接进背包后，配方依赖开始死循环：A 需要 B、B 又需要 A 也能过，缺 id 或产物直接崩，材料数量为 0 或负数不报错，自引用配方合法，失败还留下半份材料。crafting_graph.py 的 craft 负责制作；tests/test_crafting_graph.py 15 条红。要配方 id 唯一、材料产物合法、依赖无环、原子扣料与回滚、容量校验，非法输入抛 ValueError。

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
