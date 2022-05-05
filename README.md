# 🤖pyconjpbot2

Slack bot for PyCon JP Slack

## ▶️Commands

### [misc.py](/plugins/misc.py)

- `$shuffle spam ham eggs`: 指定された単語をシャッフルした結果を返す
- `$choice spam ham eggs`: 指定された単語から1つをランダムに選んで返す
- `$ping`: 応答(pong)を返す
- `$random`: チャンネルにいるメンバーからランダムに一人を選ぶ
- `$random active`: チャンネルにいるactiveなメンバーからランダムに一人を選ぶ

## 🔧How to build

```bash
$ python3.10 -m venv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ cp example.env .env
(env) $ vi .env
(env) $ python app.py
```

## ✨Lint, Mypy

* `tox -e lintcheck`: check black, isort and flake8
* `tox -e mypy`: check mypy

```bash
$ python3.10 -m venv env
$ . env/bin/activate
(env) $ pip install -r requirements-dev.txt
(env) $ tox -e lintcheck
...
lintcheck run-test: commands[0] | isort -c --diff app.py
lintcheck run-test: commands[1] | black --check app.py
...
lintcheck run-test: commands[2] | flake8 app.py
___________________________________ summary ____________________________________
  lintcheck: commands succeeded
  congratulations :)
(env) $ tox-e mypy 
...
mypy run-test: commands[0] | mypy app.py
...
___________________________________ summary ____________________________________
  mypy: commands succeeded
  congratulations :)
```

## 📚References

* [Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)
  * [slack_bolt API documentation](https://slack.dev/bolt-python/api-docs/slack_bolt/)
* [Python Slack SDK](https://slack.dev/python-slack-sdk/)
  * [slack_sdk API documentation](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/)
* [Intro to Socket Mode](https://api.slack.com/apis/connections/socket)
* [Web API methods](https://api.slack.com/methods)
