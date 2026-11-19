# GSB Bugfix Task
## 题面
着色器变体缓存一上，命中率就乱：命中后没把 key 移到最新，容量满不淘汰最旧，容量 0 也接受，空 key 插进去，重复 key 插两次，cache 不是列表直接崩。shader_variant_cache.py 的 access 负责缓存；tests/test_shader_variant_cache.py 15 条红。要 LRU 顺序、容量淘汰、key 非空字符串、cache 列表校验、去重、命中/未命中/evicted 返回准确，非法输入抛 ValueError。

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
