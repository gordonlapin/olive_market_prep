import os
import json
import logging
import requests
from datetime import datetime
from pathlib import Path

# ── ログ設定 ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ── 設定（ここを変更してください） ───────────────────
API_URL = "https://api.example.com/data"   # ← 対象 API の URL
API_KEY = os.environ["API_KEY"]            # GitHub Secrets から自動取得
OUTPUT_DIR = Path("output")


def fetch_data() -> dict:
    """API からデータを取得する"""
    headers = {"X-Api-Key": API_KEY}       # ← ヘッダー名は API に合わせて変更
    response = requests.get(API_URL, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def save_output(data: dict) -> Path:
    """取得データを日付付き JSON ファイルに保存する"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = OUTPUT_DIR / f"{today}.json"
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return filepath


def main():
    log.info("バッチ処理を開始します")
    try:
        data = fetch_data()
        log.info(f"取得成功: {len(data) if isinstance(data, list) else '(object)'} 件")

        path = save_output(data)
        log.info(f"保存完了: {path}")

    except requests.HTTPError as e:
        log.error(f"API エラー: {e.response.status_code} {e.response.text}")
        raise
    except Exception as e:
        log.error(f"予期しないエラー: {e}")
        raise

    log.info("バッチ処理が完了しました")


if __name__ == "__main__":
    main()
