import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- CONFIG ----------------
SHEET_ID = "1K_PiQwA30oN8uOz3mc7CM191b1mrA0UzT6ar76g8jyw"
CREDENTIALS_FILE = "credentials.json"

# ---------------- TEAM ----------------
team_members = [

    # PRIYAA
    ["Mentor","PRIYAA RAVI","Priyaa Ravi","Priyaa_16"],
    ["Mentee","PRIYAA RAVI","Harsika S","harsika07"],
    ["Mentee","PRIYAA RAVI","Mohamed Hasan A","Abu_hasan2006"],
    ["Mentee","PRIYAA RAVI","Nikshitha S","Nikshitha-S"],
    ["Mentee","PRIYAA RAVI","Sakthi Shriram K","sakthi_shriram"],

    # APARNAA
    ["Mentor","APARNAA K S","Aparnaa","Aparnaa27"],
    ["Mentee","APARNAA K S","Asifa Begum M","Asifa18"],
    ["Mentee","APARNAA K S","Hariharan N N","Hari_Haran_2589"],
    ["Mentee","APARNAA K S","Mirudhula M","mirudhu_12"],
    ["Mentee","APARNAA K S","Sarmila R","sarmila_Rajarajan"],
    ["Mentee","APARNAA K S","Rasin Ahmed F","Rasin_ahmed_F"],

    # JEYA
    ["Mentor","JEYA KARTIKA G","Jeyakarthika","jeykagovind"],
    ["Mentee","JEYA KARTIKA G","Subhashini S S","subaa27"],
    ["Mentee","JEYA KARTIKA G","Joshua Jenisus R","Jenisusjr"],
    ["Mentee","JEYA KARTIKA G","Vijay R S","Vijay10"],
    ["Mentee","JEYA KARTIKA G","Vahies Vishwanathan P V",""],
    ["Mentee","JEYA KARTIKA G","Hishaam M",""],

    # SRINATH
    ["Mentor","SRINATH T","SRINATH T","Srinath__27"],
    ["Mentee","SRINATH T","Tharunraj R","Tharunraj007"],
    ["Mentee","SRINATH T","Adithya R","Adithyar001"],
    ["Mentee","SRINATH T","Abimanyu M","M_Abimanyu"],
    ["Mentee","SRINATH T","Kamalesh S","S_Kamlesh"],
    ["Mentee","SRINATH T","Mohamed Haaris S","MohamedHaaris"],

    # GEETHA
    ["Mentor","GEETHAVARSHINI R","Geethavarshini","geeth_18"],
    ["Mentee","GEETHAVARSHINI R","Balasubasri A","balasubasri"],
    ["Mentee","GEETHAVARSHINI R","Deepan Raj R","Deepan_Raj_R"],
    ["Mentee","GEETHAVARSHINI R","Kowsalya M","kows_26"],
    ["Mentee","GEETHAVARSHINI R","Gocegin Sanjay N","Gocegin_sanjay"],

    # PONAR
    ["Mentor","PONARUNKUMAR","Ponarunkumar","Ponarunkumar"],
    ["Mentee","PONARUNKUMAR","Janarthan A","Janarthanajana"],
    ["Mentee","PONARUNKUMAR","Muthukumar S","Muthukumar-Leet"],
    ["Mentee","PONARUNKUMAR","Balaji T","BALAJITAMILSELVAN"],
    ["Mentee","PONARUNKUMAR","Jagath P","jagath_0711"],
    ["Mentee","PONARUNKUMAR","Mohamed Nifrasdeen H","nifras786"],

    # ARVINDH
    ["Mentor","ARVINDH BABU","Arvindh Babu V","arvindhbabu23"],
    ["Mentee","ARVINDH BABU","Ramani Jayandren G","Ramani_JayandrenG"],
    ["Mentee","ARVINDH BABU","Krishnaji S","Skrishnaji"],
    ["Mentee","ARVINDH BABU","Manikandan M","qk29BICfmQ"],
    ["Mentee","ARVINDH BABU","Balaji V M","_balaji_vm"],
    ["Mentee","ARVINDH BABU","Yukesh S","rjtBAYLWVn"],

    # KARUPPANAN
    ["Mentor","KARUPPANAN","Karuppanan","Karuppanan_Thandapani"],
    ["Mentee","KARUPPANAN","Mohamed Idris","MohamedIdris"],
    ["Mentee","KARUPPANAN","Navadeep S","Navadeep7"],
    ["Mentee","KARUPPANAN","Kishore A",""],
    ["Mentee","KARUPPANAN","Nowfil A","Nowfil25"],
    ["Mentee","KARUPPANAN","Nagul Inban S","NagulInban"],

    # JAYAPRIYA
    ["Mentor","JAYAPRIYA","Jayapriya S","Priyasakthivel"],
    ["Mentee","JAYAPRIYA","Oviya M","Oviyamuruganantham"],
    ["Mentee","JAYAPRIYA","Srija S","Srija_019"],
    ["Mentee","JAYAPRIYA","Sachin R","rsachin_006"],
    ["Mentee","JAYAPRIYA","Visveshwaran M","VisveshvaranM"],
    ["Mentee","JAYAPRIYA","Yogapriya V","Yogapriya_2004"],

    # KIRUTHIKA
    ["Mentor","KIRUTHIKA","Kiruthika","kiruthika_0511"],
    ["Mentee","KIRUTHIKA","Tharun R","tL1eFZ6alJ"],
    ["Mentee","KIRUTHIKA","Pooja J","pooja_jayaprakash27"],
    ["Mentee","KIRUTHIKA","Subitha M","Subitha12"],
    ["Mentee","KIRUTHIKA","Nivetha R","Nive_20"],
]

# ---------------- API ----------------
def get_solved(username):
    if not username:
        return 0,0,0,0

    url = "https://leetcode.com/graphql"
    query = """query($u:String!){matchedUser(username:$u){submitStats{acSubmissionNum{difficulty count}}}}"""

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

# CLEAR
sheet.clear()

# HEADER
rows = [[
    "Role","Name","LeetCodeUsername",
    "InitialTotalSolved","TotalSolved",
    "PrevEasy","PrevMedium","PrevHard","PrevTotal"
]]

prev_mentor = None

# BUILD DATA
for role, mentor, name, user in team_members:

    if role == "Mentor" and prev_mentor is not None:
        rows.append(["","","","","","","","",""])

    prev_mentor = mentor

    E,M,H,T = get_solved(user)

    rows.append([
        role,name,user,
        T,T,E,M,H,T
    ])

    print(f"✔ {name} → {T}")

# SINGLE WRITE
sheet.update("A1", rows)

print("\n🎉 FINAL BASELINE CREATED SUCCESSFULLY")