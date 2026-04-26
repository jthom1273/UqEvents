import json
from gallery_dl import config, job

# Load gallery-dl config (reads config.json automatically)
config.load()

# Load our own settings from config.json
with open("config.json", "r") as f:
    cfg = json.load(f)

accounts = cfg.get("accounts", [])

if not accounts:
    print("No accounts found in config.json under 'accounts'. Nothing to scrape.")
else:
    for account in accounts:
        url = f"https://www.instagram.com/{account}/"
        print(f"Scraping {url}...")
        job.DownloadJob(url).run()

print("Finished downloading posts.")
