name: Update aggregated RSS feed

on:
  schedule:
    # Runs daily at 03:00 UTC (~08:30 IST/Colombo time). Adjust as needed.
    - cron: "0 3 * * *"
  workflow_dispatch: {}   # lets you trigger it manually from the Actions tab

permissions:
  contents: write

jobs:
  build-feed:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run aggregator
        run: python aggregate.py --out feed.xml --per-source 20 --workers 10

      - name: Commit updated feed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add feed.xml
          git diff --cached --quiet || git commit -m "Update aggregated feed.xml"
          git push
