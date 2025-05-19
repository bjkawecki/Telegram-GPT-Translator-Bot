from src.app.config.constants import TARGET_CHAT_ID


def process_media_group_payload(posts):
    """Erstellt das Payload für Telegrams sendMediaGroup-Methode."""
    if not posts:
        print("Leere MediaGroup – überspringe.")
        return None

    media_group_id = posts[0].get("media_group_id")
    if not media_group_id:
        print("Fehlende media_group_id – überspringe.")
        return None

    sorted_posts = sorted(posts, key=lambda x: int(x["message_id"]))
    media = []

    for i, p in enumerate(sorted_posts):
        media_item = {}

        if "photo" in p:
            photo_list = p.get("photo", [])
            if not photo_list:
                continue
            # Robusteste Version: größtes Bild nehmen
            largest_photo = max(photo_list, key=lambda ph: ph.get("file_size", 0))
            media_item = {
                "type": "photo",
                "media": largest_photo["file_id"],
            }

        elif "video" in p:
            media_item = {
                "type": "video",
                "media": p["video"]["file_id"],
            }

        else:
            print("Nicht unterstützter Medientyp – überspringe:", p)
            continue

        if i == 0 and p.get("caption"):
            media_item["caption"] = p["caption"]
            if p.get("caption_entities"):
                media_item["caption_entities"] = p["caption_entities"]

        media.append(media_item)

    return {"chat_id": TARGET_CHAT_ID, "media": media}
