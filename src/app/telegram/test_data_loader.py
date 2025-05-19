import json


def load_test_body(flag: str):
    filename_map = {
        "text": "res_text.json",
        "photo": "res_photo.json",
        "video": "res_video.json",
        "photos-group": "res_media_group.json",
        "mixed-group": "res_group_photos.json",
    }

    filename = filename_map.get(flag)
    if not filename:
        raise ValueError(f"Unbekannte Flagge: {flag}")

    with open(f"json/{filename}", "r", encoding="utf-8") as f:
        return json.load(f)
