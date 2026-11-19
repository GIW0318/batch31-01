# GSB Bugfix Task
## 题面
音频声部一多，抢占策略就乱：超过上限不抢占，最新声部直接丢，保护声部被抢，同优先级不按最早开始，limit 为 0 还保留声部。audio_voice_steal.py 的 select 负责选声部；tests/test_audio_voice_steal.py 15 条红。要按优先级和开始时间保留、保护声部优先、keep/steal 不重叠、limit 边界，非法输入抛 ValueError。

## 运行方式
```bash
python -m pytest tests -q
```

## 平台字段

所属领域：安全
子方向：音视频处理
任务类型：Bugfix
语言 / 框架：Python 3, pytest
环境可复现等级：有外部依赖，未容器化
