# 🤖 pyconjpbot2

Slack bot for PyCon JP Slack

## ▶️ Commands

### [calc.py](/plugins/calc.py)

- 数式を計算する / Calculate formulas

```
takanory: 1 + 1
pyconjpbot: 2
takanory: sqrt(2)
pyconjpbot: 1.4142135623730951
```

### [greeting.py](/plugins/greeting.py)

- あいさつを返す / Return a greeting message

```
takanory: おはよう
pyconjpbot: @takanory おはようございます
```

### [translate.py](/plugins/trasnlate.py)

- テキストを翻訳する / Translate text
- `$translate python`: 指定した文字列を日本語に翻訳する
- `$translate へび`: 指定した文字列を英語に翻訳する
- `$translate -DE へび` : 指定した言語(DE等)に翻訳する
- `$translate list`: 指定できる言語の一覧を返す

### [plusplus.py](/plugins/plusplus.py)

- 指定された名前の++をカウントする / Count ++ for a given name
- `name1 name2++`: 指定された名前に +1 カウントする
- `name1 name2--`: 指定された名前に -1 カウントする
- `$plusplus search (keyword)`: 名前にkeywordを含む一覧を返す
- `$plusplus delete (name)`: 指定されたnameのカウントを削除する(カウント10未満のみ)
- `$plusplus rename (old) (new)`: カウントする名前をnewに変更する
- `$plusplus merge (old) (new)`: 2つの名前のカウントをnewにまとめ、oldを削除する

### [misc.py](/plugins/misc.py)

- `$choice spam ham eggs`: 指定された単語から1つをランダムに選んで返す
- `$shuffle spam ham eggs`: 指定された単語をシャッフルした結果を返す
- `$ping`: 応答(pong)を返す
- `$version`: バージョン情報を返す
- `$random`: チャンネルにいるメンバーからランダムに一人を選ぶ
- `$random active`: チャンネルにいるactiveなメンバーからランダムに一人を選ぶ

### [wikipedia.py](/plugins/wikipedia.py)

- 指定されたキーワードに関連するWikipediaのページを返す / Return Wikipedia page for specified keywords and language
- `$wikipedia keywords`: Wikipediaで指定されたキーワードに関連するページを返す
- `$wikipedia -en keywords`: Wikipediaで指定された言語(en等)のページを返す

### [reaction.py](/plugins/reaction.py)

- 任意のキーワードでemojiリアクションを追加する / Add emoji reactions for any keywords

## 🔧 How to build

```bash
$ python3.10 -m venv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ cp example.env .env
(env) $ vi .env
(env) $ python app.py
```

## ✨ Lint, Mypy

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

## 📚 References

* [Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)
  * [slack_bolt API documentation](https://slack.dev/bolt-python/api-docs/slack_bolt/)
* [Python Slack SDK](https://slack.dev/python-slack-sdk/)
  * [slack_sdk API documentation](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/)
* [Intro to Socket Mode](https://api.slack.com/apis/connections/socket)
* [Web API methods](https://api.slack.com/methods)
