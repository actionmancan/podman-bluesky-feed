"""
Configuration for the Podman Community Bluesky Feed
"""

# Feed metadata
FEED_NAME = "Podman Community"
FEED_DESCRIPTION = "A curated feed for the Podman containerization community"
FEED_URI = "at://did:plc:oe2nzi6rjpijm5o2w2gp7jzo/app.bsky.feed.generator/3m5p5ammzgh2s"

# Keywords to search for in posts
PODMAN_KEYWORDS = [
    "podman",
    "containers",
    "containerization",
    "rootless",
    "cri-o",
    "buildah",
    "skopeo",
    "libpod",
]

# Hashtags to include
PODMAN_HASHTAGS = [
    "podman",
    "podmancontainers",
    "containerization",
    "linuxcontainers",
    "rootlesscontainers",
    "buildah",
    "skopeo",
]

# Bluesky handles/DIDs of key Podman community accounts
PODMAN_ACCOUNTS = [
    "podman.io",  # Official Podman account (if exists)
    # Add more Podman community accounts here
]

# Minimum post quality filters
MIN_REPLY_COUNT = 0  # Minimum number of replies
MIN_REPOST_COUNT = 0  # Minimum number of reposts
MIN_LIKE_COUNT = 0  # Minimum number of likes

# Language filter (empty list = all languages)
LANGUAGES = []  # e.g., ["en"] for English only

