import time
import argparse
import json
from src.handlers.telegram_event_handler import handler
from src.telegram.test_data_loader import load_test_body

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram Payload Tester")
    parser.add_argument(
        "--flag",
        choices=["text", "photo", "video", "photos-group", "mixed-group"],
        help="Art der Testdaten",
        required=False,
    )
    args = parser.parse_args()

    if args.flag:
        test_body = load_test_body(args.flag)
        print(f"==> Sende Payload für Flag '{args.flag}'")
        handler(test_body, context=None)
    else:
        # fallback auf statische Testdateien
        for testfile in ["test_1", "test_2"]:
            with open(f"json/{testfile}.json", "r", encoding="utf-8") as f:
                test_body = json.load(f)
            print(f"==> Sende {testfile}")
            handler(test_body, context=None)
            time.sleep(1)
