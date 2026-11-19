# GSB Bugfix Task
## 题面
手柄 UI 焦点一上，菜单导航就乱：按右方向跳到左边节点，禁用节点仍能获得焦点，同距节点每次选不同，当前节点缺失直接崩，方向不是四向也继续算。ui_focus.py 的 move 负责移动焦点；tests/test_ui_focus.py 15 条红。要方向筛选、最近距离、禁用跳过、无候选保持原焦点、坐标/方向/节点校验，非法输入抛 ValueError。

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
