import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ---------------- CONFIG ----------------
SHEET_ID = "1K_PiQwA30oN8uOz3mc7CM191b1mrA0UzT6ar76g8jyw"
CREDENTIALS_FILE = "credentials.json"

# ---------------- API ----------------
def get_solved(username):
    if not username:
        return 0,0,0,0

    url = "https://leetcode.com/graphql"
    query = """
    query($u:String!){
      matchedUser(username:$u){
        submitStats{
          acSubmissionNum{
            difficulty
            count
          }
        }
      }
    }
    """

    try:
        r = requests.post(url, json={"query":query,"variables":{"u":username}}, timeout=20).json()
        d = r.get("data",{}).get("matchedUser")

        if not d:
            return 0,0,0,0

        c = d["submitStats"]["acSubmissionNum"]

        E = next((x["count"] for x in c if x["difficulty"]=="Easy"),0)
        M = next((x["count"] for x in c if x["difficulty"]=="Medium"),0)
        H = next((x["count"] for x in c if x["difficulty"]=="Hard"),0)

        return E,M,H,E+M+H

    except:
        return 0,0,0,0

# ---------------- SHEET ----------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

client = gspread.authorize(
    ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
)

sheet = client.open_by_key(SHEET_ID).sheet1

data = sheet.get_all_values()
header = data[0]

today = datetime.now().strftime("%Y-%m-%d")

# Add date column
if today not in header:
    header.append(today)
    sheet.update("1:1", [header])

header = sheet.row_values(1)
today_col = header.index(today)

# column indexes
idx_user = header.index("LeetCodeUsername")
idx_total = header.index("TotalSolved")
idx_prev_e = header.index("PrevEasy")
idx_prev_m = header.index("PrevMedium")
idx_prev_h = header.index("PrevHard")
idx_prev_t = header.index("PrevTotal")

# ---------------- PROCESS ----------------
updated_rows = []

for row in data[1:]:

    # Skip empty row
    if len(row) <= idx_user:
        updated_rows.append(row)
        continue

    username = row[idx_user].strip() if row[idx_user] else ""

    if username == "":
        updated_rows.append(row)
        continue

    prev_e = int(row[idx_prev_e] or 0)
    prev_m = int(row[idx_prev_m] or 0)
    prev_h = int(row[idx_prev_h] or 0)
    prev_t = int(row[idx_prev_t] or 0)

    e,m,h,t = get_solved(username)

    de = max(e - prev_e, 0)
    dm = max(m - prev_m, 0)
    dh = max(h - prev_h, 0)
    dt = max(t - prev_t, 0)

    # Ensure row length
    while len(row) <= today_col:
        row.append("")

    # 🔥 READ EXISTING TODAY VALUE
    old_cell = row[today_col] if row[today_col] else ""

    old_total = 0
    old_e = old_m = old_h = 0

    if old_cell and "(" in old_cell:
        try:
            parts = old_cell.split(" ")
            old_total = int(parts[0])
            inside = parts[1].strip("()")
            old_e, old_m, old_h = map(int, inside.split("/"))
        except:
            pass

    # 🔥 ACCUMULATE
    new_total = old_total + dt
    new_e = old_e + de
    new_m = old_m + dm
    new_h = old_h + dh

    row[today_col] = f"{new_total} ({new_e}/{new_m}/{new_h})"

    # Update prev values
    row[idx_total] = str(t)
    row[idx_prev_e] = str(e)
    row[idx_prev_m] = str(m)
    row[idx_prev_h] = str(h)
    row[idx_prev_t] = str(t)

    updated_rows.append(row)

    print(f"✔ {username} → total today: {new_total}")

# ---------------- SINGLE WRITE ----------------
sheet.update("A2", updated_rows)

print("\n🎉 DAILY UPDATE WITH ACCUMULATION SUCCESS")

# ---------------- DASHBOARD ----------------
try:
    import subprocess
    subprocess.run(['python', 'update_dashboard.py'], check=True)
    print("✅ Dashboard updated")
except Exception as e:
    print(f"⚠️ Dashboard skipped: {e}")