"""Save a full-page screenshot of a URL.

Usage: SNAPRENDER_API_KEY=sk_live_... python examples/screenshot.py https://example.com
"""
import os
import sys

from snaprender import SnapRender

url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
client = SnapRender(api_key=os.environ["SNAPRENDER_API_KEY"])
image = client.capture(url, full_page=True, format="png")
with open("screenshot.png", "wb") as f:
    f.write(image)
print("Saved screenshot.png")
