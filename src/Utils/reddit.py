import urllib.request
import re

def grab_img(sub: str) -> list[str]:
    """
    sub : str = name of a subreddit

    Returns a list containing images from top posts of the subreddit
    at the time it's called, sorted by popular.

    Must not be used too much to avoid HTTPError 429
    """
    url = f"https://reddit.com/r/{sub}.json"
    regex = r'https:\/\/i\.redd\.it\/[a-z,A-Z,0-9]+\.(jpg|png|gif)'
    page = urllib.request.urlopen(url).read().decode()
    imgs = re.finditer(regex, page)
    return [g.group(0) for g in imgs]