# GSB Bugfix Task
## 题面
载具下水后浮力不对：全没入净力为负，半没入比例算错，出水还给正浮力，submerged 大于 volume 也接受，质量为 0 或密度为 0 不报错。buoyancy.py 的 compute 负责算力；tests/test_buoyancy.py 15 条红。要浮力等于排水体积乘密度乘重力、重量等于质量乘重力、净力准确、部分没入按比例，非法输入抛 ValueError。

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
