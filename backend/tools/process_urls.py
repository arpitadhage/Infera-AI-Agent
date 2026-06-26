def process_urls(state):

    urls = state.get("urls", [])

    youtube_urls = []
    other_urls = []

    for url in urls:

        if (
            "youtube.com" in url
            or
            "youtu.be" in url
        ):
            youtube_urls.append(url)

        else:
            other_urls.append(url)

    state["youtube_urls"] = youtube_urls
    state["other_urls"] = other_urls

    return state


