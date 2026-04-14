# NASA APOD サンプルアプリ

NASA の [Astronomy Picture of the Day (APOD)](https://apod.nasa.gov/apod/astropix.html) APIを使って、今日の宇宙画像を取得するサンプルアプリです。

## 必要要件

- Python 3.8 以上
- 外部ライブラリ不要（標準ライブラリのみ使用）

## セットアップ

### APIキーの設定（任意）

デフォルトでは `DEMO_KEY` を使用します（レート制限: 1時間30回 / 1日50回）。  
より多く利用する場合は [api.nasa.gov](https://api.nasa.gov/) で無料APIキーを取得してください。

```bash
# Windows
set NASA_API_KEY=あなたのAPIキー

# PowerShell
$env:NASA_API_KEY = "あなたのAPIキー"
```

## 使い方

```bash
python apod_app.py
```

## 実行例

```
📡 NASA APOD を取得中: 2026-04-14

============================================================
🔭 タイトル  : The Milky Way Over Norway
📅 日付      : 2026-04-14
🖼️  メディア  : image
📝 説明      :
   ...
🔗 URL: https://apod.nasa.gov/apod/image/...
============================================================

ブラウザで画像を開きますか？ [y/N]:
```
