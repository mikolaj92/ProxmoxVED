# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.
# Add tasks below when you want the agent to check something periodically.

# QMD context caching – update index and fetch relevant snippets
- cd /Users/mini-m4-1/clawd
- qmd update 2>/dev/null || true
- qmd search "TODO" -n 5 --json > memory/qmd_cache.json
