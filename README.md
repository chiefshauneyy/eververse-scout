# Eververse Scout

A simple Discord bot that privately sends the Kyber's Corner Destiny 2 Eververse link after each daily reset.

## Set up Discord

1. At https://discord.com/developers/applications create an application called **Eververse Scout**.
2. Open **Bot** and copy the bot token. Keep it secret; never commit it to GitHub.
3. Under **OAuth2 > URL Generator**, choose the **bot** scope and invite the bot to a server you share with it. No special server permissions or privileged intents are needed.
4. In Discord **User Settings > Advanced**, enable Developer Mode and copy your numeric user ID.
5. Allow DMs from members of the shared server.

## Add GitHub Actions secrets

In the repository, visit **Settings > Secrets and variables > Actions** and add these two *repository secrets*:

- `DISCORD_BOT_TOKEN`: Discord bot token.
- `DISCORD_USER_ID`: your numeric Discord account ID.

Never put these values in source files or chat.

## Test

Open **Actions > Daily Eververse Discord DM > Run workflow**. Check your Discord DMs, then check the Actions log if it fails. You can also run `python -m unittest discover -s tests -v` locally.

## Timing

The workflow runs daily at **17:15 UTC**, 15 minutes after the 17:00 UTC Destiny 2 reset. That is **11:15 AM CST** or **12:15 PM CDT** in San Antonio. GitHub scheduled actions are not guaranteed to run exactly on time.

The bot sends a permanent link, not scraped inventory, and cannot confirm Kyber's Corner has refreshed its page. GitHub may disable scheduled workflows in public repositories after 60 days without activity. Manual runs send an extra message.

https://kyberscorner.com/destiny2/eververse/
