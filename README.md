# pyconjpbot2

PyCon JP Slackワークスペース用のチャットボット。slack-machineフレームワークを使用して構築。

## 概要

pyconjpbot2は、既存のpyconjpbotをslack-machine（最新のSlack Pythonフレームワーク）に移植したものです。以下の機能を提供します：

- 🤖 **基本コマンド**: ping, help, version, thx
- ➕ **感謝カウント**: `名前++` / `名前--` で感謝を記録、ランキング表示
- 📖 **カスタム用語辞書**: よく使う用語や情報を登録・検索
- 🌐 **翻訳**: DeepL APIを使用した多言語翻訳
- 🔍 **検索**: Wikipedia、Google検索
- 🔢 **計算**: 数式評価
- 👋 **挨拶・リアクション**: キーワードベースの自動応答
- 🎫 **JIRA統合**: issue検索・表示

## 必要要件

- Python 3.13
- uv (パッケージマネージャー)
- Slack Workspace（Bot Token必須）

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/pyconjp/pyconjpbot2.git
cd pyconjpbot2
```

### 2. Python環境のセットアップ

```bash
# uvをインストール（未インストールの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係をインストール
uv sync --all-extras
```

### 3. 設定ファイルの作成

```bash
# サンプル設定ファイルをコピー
cp local_settings.py.sample local_settings.py

# local_settings.pyを編集して実際の値を設定
# 最低限必要: SLACK_APP_TOKEN, SLACK_BOT_TOKEN
```

### 4. Slack Appの作成

1. [Slack API](https://api.slack.com/apps)にアクセス
2. "Create New App" → "From scratch"
3. App NameとWorkspaceを選択
4. 以下のURLにあるmanifest.yamlを設定してアプリを作成
   - https://dondebonair.github.io/slack-machine/user/usage/
5. Basic Information→App-Level Tokensで"Install to Workspace"で `connections:write` のトークン(`xapp-xxx`)を作成し、local_settings.pyのSLACK_APP_TOKENに設定
6. Botをワークスペースにインストール
7. OAuth & PermissionsのBot User OAuth Token(`xoxb-xxx`)をコピーしてlocal_settings.pyのSLACK_BOT_TOKENに設定

### 5. ボットの起動

```bash
# 開発環境
uv run slack-machine

# 本番環境（バックグラウンド実行）
nohup uv run slack-machine > logs/bot.log 2>&1 &
```

## 使用方法

### 基本コマンド

```
@pyconjpbot ping          # ボット応答確認
@pyconjpbot help          # ヘルプ表示
@pyconjpbot version       # バージョン情報
@pyconjpbot thx           # 使用技術クレジット
```

### 感謝カウント

```
takanory++                # takanoryに+1
Python--                  # Pythonに-1
$plusplus ranking         # ランキング表示
$plusplus search 検索語   # 検索
$plusplus delete 名前     # 削除（count < 10のみ）
$plusplus rename 旧 新    # リネーム
$plusplus merge 元 先     # マージ
```

### カスタム用語辞書

```
$term create 酒           # 「酒」コマンドを作成
$酒 add ビール             # 応答を追加
$酒                       # ランダムに応答を表示
$酒 list                  # すべての応答を表示
$term drop 酒             # 「酒」コマンドを削除
$term search 検索語       # 用語検索
```

### 翻訳

```
$translate python                  # 自動検出 → 日本語
$translate -en こんにちは         # 日本語 → 英語
```

### 検索

```
$wikipedia Python         # Wikipedia検索
$google PyCon JP          # Google検索
```

### 計算

```
1 + 1                     # 2
sqrt(2)                   # 1.4142135623730951
```

### JIRA統合

```
SAR-123                   # issue情報を表示
$jira search キーワード   # Open issueを検索
$jira allsearch 検索語    # すべてのissueを検索
$jira assignee ユーザー名 # 担当issue一覧
```

## 開発

### テスト実行

```bash
# すべてのテストを実行
uv run pytest

# カバレッジレポート生成
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### コード品質チェック

```bash
# Lintチェック
uv run ruff check src

# フォーマット
uv run ruff format src

# 型チェック
uv run mypy src
```

### テストファースト開発

このプロジェクトはテストファースト原則に従います：

1. **Red**: テストを書く（失敗する）
2. **Green**: 最小限の実装でテストをパス
3. **Refactor**: コードを改善

詳細は[specs/001-slack-bot-migration/tasks.md](specs/001-slack-bot-migration/tasks.md)を参照。

## プロジェクト構造

```
pyconjpbot2/
├── src/
│   └── plugins/         # slack-machineプラグイン
├── tests/
│   ├── unit/            # ユニットテスト
│   ├── integration/     # 統合テスト
│   └── contract/        # コントラクトテスト
├── data/                # データベース
├── specs/               # 仕様書・設計ドキュメント
├── pyproject.toml       # プロジェクト設定
└── local_settings.py.sample   # 設定ファイルサンプル
```

## ライセンス

MIT License - 詳細は[LICENSE](LICENSE)を参照

## クレジット

- slack-machine: Slack bot framework
- SQLModel: Database ORM
- DeepL API: Translation service
- pytest: Testing framework

---

**PyCon JP Team** | https://www.pycon.jp/
