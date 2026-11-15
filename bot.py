"""Send a daily Discord DM with Kyber's Corner Eververse store link."""
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API = "https://discord.com/api/v10"
EVERVERSE_URL = "https://kyberscorner.com/destiny2/eververse/"


def request(method, endpoint, token, payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "EververseScout (personal notification bot)",
        "Content-Type": "application/json",
    }
    for attempt in range(3):
        req = Request(f"{API}{endpoint}", data=body, headers=headers, method=method)
        try:
            with urlopen(req, timeout=25) as response:
                return json.load(response)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:700]
            if exc.code == 429 and attempt < 2:
                try:
                    delay = min(float(json.loads(detail).get("retry_after", 1)), 15)
                except (ValueError, KeyError, TypeError):
                    delay = 2
                time.sleep(delay)
                continue
            if exc.code in (401, 403, 404):
                raise RuntimeError(
                    f"Discord API HTTP {exc.code}: {detail}. Verify bot token, user ID, "
                    "mutual server and DM privacy settings."
                ) from exc
            raise RuntimeError(f"Discord API HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Network error connecting to Discord: {exc.reason}") from exc
    raise RuntimeError("Discord API rate limit retries exhausted")


def make_message(now=None):
    now = now or datetime.now(timezone.utc)
    date = f"{now:%A, %B} {now.day}, {now.year}"
    return (
        f"🛍️ **Destiny 2 — Daily Eververse** | {date}\n"
        "Daily reset has passed! See today's Bright Dust and Silver offerings at Kyber's Corner:\n"
        f"🔗 {EVERVERSE_URL}\n"
        "*Note: Kyber's Corner may need some time to refresh its inventory.*"
    )


def main():
    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    user_id = os.getenv("DISCORD_USER_ID", "").strip()
    if not token or not user_id:
        raise ValueError("Set the DISCORD_BOT_TOKEN and DISCORD_USER_ID repository secrets.")
    if not user_id.isdecimal():
        raise ValueError("DISCORD_USER_ID must contain only digits.")
    dm = request("POST", "/users/@me/channels", token, {"recipient_id": user_id})
    request("POST", f"/channels/{dm['id']}/messages", token, {
        "content": make_message(), "allowed_mentions": {"parse": []},
    })
    print("Successfully sent Eververse link via Discord DM.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
