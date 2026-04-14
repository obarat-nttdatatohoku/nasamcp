"""
NASA APOD (Astronomy Picture of the Day) サンプルアプリ
今日の宇宙画像を取得して表示します。

使い方:
    python apod_app.py          # NASA APIから取得（インターネット接続が必要）
    python apod_app.py --mock   # サンプルデータで動作確認
"""

import urllib.request
import urllib.error
import json
import os
import sys
import webbrowser
from datetime import date

NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")
BASE_URL = "https://api.nasa.gov/planetary/apod"

MOCK_DATA = {
    "date": str(date.today()),
    "title": "The Tarantula Nebula",
    "media_type": "image",
    "explanation": (
        "The Tarantula Nebula, also known as 30 Doradus, is a large star-forming region "
        "in the Large Magellanic Cloud, a satellite galaxy of the Milky Way. "
        "It is one of the largest known stellar nurseries and is visible to the naked eye "
        "from the Southern Hemisphere. The nebula contains some of the most massive and "
        "luminous stars known, making it a prime target for astronomers studying stellar evolution."
    ),
    "hdurl": "https://apod.nasa.gov/apod/image/2210/tarantula_jwst.jpg",
    "url": "https://apod.nasa.gov/apod/image/2210/tarantula_jwst1024.jpg",
    "copyright": "NASA, ESA, CSA, STScI",
}


def fetch_apod() -> dict:
    """NASA APOD APIから今日の宇宙画像データを取得する"""
    url = f"{BASE_URL}?api_key={NASA_API_KEY}&date={date.today()}"
    print(f"📡 NASA APOD を取得中: {date.today()}")
    print(f"🌐 エンドポイント: {BASE_URL}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"\n❌ HTTPエラー {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except (urllib.error.URLError, TimeoutError) as e:
        reason = getattr(e, "reason", str(e))
        print(f"\n❌ 接続エラー: {reason}", file=sys.stderr)
        print("💡 インターネット接続を確認するか、--mock オプションを試してください", file=sys.stderr)
        sys.exit(1)


def display_apod(data: dict) -> str:
    """APODデータをターミナルに表示する"""
    print("\n" + "=" * 60)
    print(f"🔭 タイトル  : {data.get('title', 'N/A')}")
    print(f"📅 日付      : {data.get('date', 'N/A')}")
    print(f"🖼️  メディア  : {data.get('media_type', 'N/A')}")
    print(f"\n📝 説明:\n{data.get('explanation', 'N/A')}")

    if data.get("copyright"):
        print(f"\n©️  著作権: {data['copyright'].strip()}")

    url = data.get("hdurl") or data.get("url", "")
    if url:
        print(f"\n🔗 URL: {url}")

    print("=" * 60)
    return url


def open_in_browser(url: str) -> None:
    """URLをブラウザで開く"""
    if not url:
        return
    try:
        answer = input("\nブラウザで画像を開きますか？ [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return
    if answer == "y":
        webbrowser.open(url)
        print("✅ ブラウザで開きました")


def main() -> None:
    mock_mode = "--mock" in sys.argv

    if mock_mode:
        print("🧪 モックモードで実行中（サンプルデータを使用）")
        data = MOCK_DATA
    else:
        data = fetch_apod()

    url = display_apod(data)
    open_in_browser(url)


if __name__ == "__main__":
    main()
