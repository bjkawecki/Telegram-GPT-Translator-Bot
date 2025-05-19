def find_post_type(post):
    post_type = ""
    if post.get("media_group_id"):
        post_type = "media_group"
    elif post.get("text"):
        post_type = "text"
    elif post.get("photo"):
        post_type = "photo"
    elif post.get("video"):
        post_type = "video"
    return post_type
