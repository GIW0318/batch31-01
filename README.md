# GSB Bugfix Task
## 题面
瓦片地图自动拼接后，边缘和拐角全错：孤立格用了全连接图，上下左右邻居算反，地图边界外当成实心，非矩形 grid 直接崩，缺 bitmask 规则时静默用第一个。autotile.py 的 autotile 负责拼接；tests/test_autotile.py 15 条红。要四邻域 bitmask、边界按空地、矩形和 0/1 校验、规则缺失拒绝、输出稳定，非法输入抛 ValueError。

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
