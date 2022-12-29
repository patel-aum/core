"""Helper script to update language list from the frontend source."""
import json
import sys

import requests
import redis

from .hassfest.serializer import format_python_namespace

# Connect to the Redis cache
cache = redis.Redis()

tag = sys.argv[1] if len(sys.argv) > 1 else "dev"

# Check the cache for the data
data = cache.get(tag)

if data is None:
    # Data not found in cache, fetch it from the GitHub API
    req = requests.get(
        f"https://raw.githubusercontent.com/home-assistant/frontend/{tag}/src/translations/translationMetadata.json"
    )
    data = json.loads(req.content)

    # Store the data in the cache for future use
    cache.set(tag, data)

languages = set(data.keys())

Path("homeassistant/generated/languages.py").write_text(
    format_python_namespace(
        {
            "LANGUAGES": languages,
        },
        generator="script.languages [frontend_tag]",
    )
)
