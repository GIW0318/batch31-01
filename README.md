# GSB Bugfix Task
## 题面
大场景破坏一开，碎块图就开始断：重复 chunk id、零体积、邻居指向不存在的块、自环、重复邻居、断成两半都还能继续破坏，碎块数和总体积也不受预算限制。destruction.py 的 validate_chunks 负责校验；tests/test_destruction.py 15 条红。要 id 唯一、体积正数、邻居存在且不重复、全图连通、预算生效，非法输入抛 ValueError。

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
