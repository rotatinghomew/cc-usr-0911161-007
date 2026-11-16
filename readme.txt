人工智能治理政策版本影响评估平台

运行验收：
python3 -m policy_impact run --fixture fixtures/acceptance.json --database /tmp/policy_impact.sqlite3 --output /tmp/policy_impact-output

核验：
python3 -m policy_impact verify --database /tmp/policy_impact.sqlite3 --output /tmp/policy_impact-output

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.impact_signal.test_policy_signal -v

构建检查：
python3 -m compileall -q policy_impact tests

业务口径：实施前后均记录同一风险指标，后风险低于前风险表示改善；证据可靠性不足时效果不能按确定改善处理。报告和政策采用判断应采用一致的风险方向。
