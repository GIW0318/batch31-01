# GSB Bugfix Task
## 题面
粒子池一上高负载，free 和 active 就串：acquire 从 free 尾部拿，release 塞错位置，free 空了不新建 id，release 未知 id 静默通过，重复 release 同一个 id，容量超了还分配。particle_pool.py 的 transact 负责池操作；tests/test_particle_pool.py 15 条红。要 free/active 不重叠、id 唯一、容量边界、release 校验、acquire 新建、返回稳定，非法输入抛 ValueError。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：图形渲染
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：有外部依赖，未容器化
