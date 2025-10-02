import json
import csv

with open("thread_get_stats.txt") as f:
    data = json.load(f)

rows = []
for t in data["threads"]:
    busy = t["busy"]
    idle = t["idle"]
    util = busy / (busy + idle) if (busy + idle) > 0 else 0
    rows.append({
        "name": t["name"],
        "id": t["id"],
        "cpumask": t["cpumask"],
        "busy": busy,
        "idle": idle,
        "util": round(util, 6)
    })

# 存成 CSV
fieldnames = ["name", "id", "cpumask", "busy", "idle", "util"]
with open("thread_stats.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 螢幕印出 (tab 分隔)
print("\t".join(fieldnames))
for r in rows:
    print("\t".join(str(r[k]) for k in fieldnames))
