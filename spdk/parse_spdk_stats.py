import json
import csv

# 假設 thread_get_stats.json 與 thread_get_pollers.json 分開存
with open("thread_get_stats.txt") as f:
    stats = json.load(f)

with open("thread_get_pollers.txt") as f:
    pollers = json.load(f)

# 建立 thread 資料字典
threads = {}
for t in stats["threads"]:
    threads[t["id"]] = {
        "name": t["name"],
        "id": t["id"],
        "cpumask": t["cpumask"],
        "busy": t["busy"],
        "idle": t["idle"],
        "run_count": 0,
        "busy_count": 0,
        "util_busy_idle": round(t["busy"] / (t["busy"] + t["idle"]), 6) if (t["busy"] + t["idle"]) > 0 else 0,
        "util_busycount_run": None
    }

# 合併 poller 的 run_count/busy_count
for t in pollers["threads"]:
    tid = t["id"]
    total_run = 0
    total_busycount = 0

    for p in t["active_pollers"] + t["timed_pollers"]:
        total_run += p.get("run_count", 0)
        total_busycount += p.get("busy_count", 0)

    if tid in threads:
        threads[tid]["run_count"] = total_run
        threads[tid]["busy_count"] = total_busycount
        if total_run > 0:
            threads[tid]["util_busycount_run"] = round(total_busycount / total_run, 6)
        else:
            threads[tid]["util_busycount_run"] = None

# 輸出到 CSV
fieldnames = ["name", "id", "cpumask", "busy", "idle", "run_count", "busy_count", "util_busy_idle", "util_busycount_run"]
with open("threads.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for t in threads.values():
        writer.writerow(t)

# 在螢幕印出 (tab 分隔)
print("\t".join(fieldnames))
for t in threads.values():
    row = [str(t.get(k, "")) if t.get(k, "") is not None else "" for k in fieldnames]
    print("\t".join(row))
