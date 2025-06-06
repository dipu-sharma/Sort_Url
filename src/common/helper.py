from datetime import datetime
import random
base_url = "http://localhost:8000"

# 1. POST /shorten
# Input: A JSON object with the long URL (e.g., "https://www.example.com/some/very/long/path").
# Output: A shortened unique slug (e.g., "abc123"), and the full short URL (e.g., "https://short.ly/abc123").
# The system should:
# Check if the same long URL already exists; if yes, return the existing short link.
# Otherwise, generate a new slug (6-character alphanumeric).
# Save mapping between long URL and short URL with a created timestamp.
# 2. GET /{slug}
# Retrieve the original long URL using the short slug.
# Return a 404 if slug doesn’t exist.
# 3. PUT /{slug}
# Allow updating the long URL associated with an existing slug.
# Input should be a new long URL in JSON.
# Validate that the new URL is well-formed.
# Add expiration logic (e.g., expire links after 30 days).
# Add a “custom slug” option in the POST request.
# Store the number of clicks each short URL has received.

def generate_self_short_ulr(url: str) -> str:
    random_slug = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
    return f"{base_url}/short.ly/{random_slug}"

def generate_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")