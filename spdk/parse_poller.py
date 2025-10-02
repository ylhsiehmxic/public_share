import json
import csv

with open("thread_get_pollers.txt") as f:
    data = json.load(f)

rows = []
for t in data["threads"]:
    total_run = 0
    total_busy = 0

    for p in t["active_pollers"] + t["timed_pollers"] + t["paused_pollers"]:
        total_run += p.get("run_count", 0)
        total_busy += p.get("busy_count", 0)

    util = total_busy / total_run if total_run > 0 else 0
    rows.append({
        "name": t["name"],
        "id": t["id"],
        "run_count": total_run,
        "busy_count": total_busy,
        "util": round(util, 6) if total_run > 0 else ""
    })

# 存成 CSV
fieldnames = ["name", "id", "run_count", "busy_count", "util"]
with open("poller_stats.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 螢幕印出 (tab 分隔)
print("\t".join(fieldnames))
for r in rows:
    print("\t".join(str(r[k]) for k in fieldnames))
