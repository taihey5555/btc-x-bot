"""
BTC分析ダッシュボード X自動投稿Bot
- ダッシュボードのスクショを取得
- データを分析してコメント生成
- Xに自動投稿
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# ダッシュボードURL
DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "https://bitcoin-bunseki.onrender.com")
API_URL = f"{DASHBOARD_URL}/api/data"

# X API認証情報
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")


def take_screenshot():
    """Playwrightでダッシュボードのスクリーンショットを取得"""
    try:
        from playwright.sync_api import sync_playwright

        screenshot_path = Path("dashboard_screenshot.png")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1200, "height": 900})

            print(f"Opening {DASHBOARD_URL}...")
            page.goto(DASHBOARD_URL)
            page.wait_for_timeout(5000)  # データ読み込み待ち

            # スクリーンショット取得
            page.screenshot(path=str(screenshot_path), full_page=False)
            browser.close()

        print(f"Screenshot saved: {screenshot_path}")
        return screenshot_path

    except Exception as e:
        print(f"Screenshot error: {e}")
        return None


def fetch_dashboard_data():
    """ダッシュボードAPIからデータを取得"""
    try:
        response = requests.get(API_URL, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"API error: {e}")
    return None


def generate_analysis_text(data):
    """データから分析テキストを生成"""
    if not data:
        return None

    btc_price = data.get("btcPrice", 0)
    score = data.get("score", 0)
    signals = data.get("signals", [])

    # スコアに応じた判定
    if score > 30:
        sentiment = "強気"
        emoji = "🟢"
    elif score > 10:
        sentiment = "やや強気"
        emoji = "🟡"
    elif score < -30:
        sentiment = "弱気"
        emoji = "🔴"
    elif score < -10:
        sentiment = "やや弱気"
        emoji = "🟠"
    else:
        sentiment = "中立"
        emoji = "⚪"

    # シグナル一覧
    signal_lines = []
    for sig in signals:
        status_emoji = {"bullish": "🟢", "bearish": "🔴", "neutral": "🟡"}.get(sig["status"], "⚪")
        signal_lines.append(f"{status_emoji} {sig['name']}: {sig['value']}")

    signals_text = "\n".join(signal_lines[:5])  # 上位5つ

    # 投稿テキスト作成
    text = f"""📊 BTC市場分析レポート
{datetime.now().strftime('%Y/%m/%d %H:%M')}

💰 BTC: ${btc_price:,.0f}
{emoji} 総合スコア: {score:+d} ({sentiment})

【シグナル】
{signals_text}

#Bitcoin #BTC #仮想通貨 #投資"""

    return text


def post_to_x(text, image_path=None):
    """Xに投稿"""
    try:
        import tweepy

        if not all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET]):
            print("X API credentials not set")
            return False

        # OAuth 1.0a認証
        auth = tweepy.OAuthHandler(X_API_KEY, X_API_SECRET)
        auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_SECRET)
        api = tweepy.API(auth)

        # 画像アップロード（v1.1 API）
        media_id = None
        if image_path and image_path.exists():
            media = api.media_upload(str(image_path))
            media_id = media.media_id
            print(f"Image uploaded: {media_id}")

        # ツイート投稿（v1.1 API）
        if media_id:
            response = api.update_status(status=text, media_ids=[media_id])
        else:
            response = api.update_status(status=text)

        print(f"Posted successfully! Tweet ID: {response.id}")
        return True

    except Exception as e:
        print(f"Post error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 50)
    print("BTC Analysis X Bot")
    print("=" * 50)

    # 1. ダッシュボードデータ取得
    print("\n1. Fetching dashboard data...")
    data = fetch_dashboard_data()
    if not data:
        print("Failed to fetch data")
        return

    print(f"   BTC: ${data.get('btcPrice', 0):,.0f}")
    print(f"   Score: {data.get('score', 0)}")

    # 2. スクリーンショット取得
    print("\n2. Taking screenshot...")
    screenshot = take_screenshot()

    # 3. 分析テキスト生成
    print("\n3. Generating analysis text...")
    text = generate_analysis_text(data)
    if not text:
        print("Failed to generate text")
        return

    print("--- Post Preview ---")
    print(text)
    print("--------------------")

    # 4. Xに投稿
    print("\n4. Posting to X...")
    success = post_to_x(text, screenshot)

    if success:
        print("\n✅ Bot completed successfully!")
    else:
        print("\n❌ Bot failed to post")


if __name__ == "__main__":
    main()
