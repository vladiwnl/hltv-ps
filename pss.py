#       HLTV.ORG
    #Plyaer-stats-scraper
#       Overall stats - Round stats - Opening stats - Weapon stats
#

from bs4 import BeautifulSoup
import requests
import sqlite3
import re

stats = sqlite3.connect("ps.db")
stts = stats.cursor()

def setdb():
    stts.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, COUNTRY VARCHAR(20), NICKNAME VARCHAR(20), MAPS VARCHAR(20), KDDIFF VARCHAR(20), KD VARCHAR(20), RATING1 VARCHAR(20))")
    stts.execute("CREATE TABLE IF NOT EXISTS pstats (id INTEGER PRIMARY KEY AUTOINCREMENT, TOTALKILLS VARCHAR(20), HEADSHOT VARCHAR(20), TOTALDEATHS VARCHAR(20), KDRATIO VARCHAR(20), DAMAGEROUND VARCHAR(20), GRENADEDMGROUND VARCHAR(20), MAPSPLAYED VARCHAR(20), ROUNDSPLAYED VARCHAR(20), KILLSROUND VARCHAR(20), ASSISTSROUND VARCHAR(20), DEATHSROUND VARCHAR(20), SAVEDBYTEAMMATEROUND VARCHAR(20), SAVEDTEAMMATESROUND VARCHAR(20), RATING10 VARCHAR(20))")
    stts.execute("CREATE TABLE IF NOT EXISTS pindividualstats (id INTEGER PRIMARY KEY AUTOINCREMENT, KILLS VARCHAR(20), DEATHS VARCHAR(20), KILLDEATH VARCHAR(20), KILLROUND VARCHAR(20), ROUNDSWITHKILLS VARCHAR(20), KILLDEATHDIFFERENCE VARCHAR(20), a0KILLROUND VARCHAR(20), b1KILLROUND VARCHAR(20), c2KILLROUND VARCHAR(20), d3KILLROUND VARCHAR(20), e4KILLROUND VARCHAR(20), f5KILLROUND VARCHAR(20), TOTALOPENINGKILLS VARCHAR(20), TOTALOPENINGDEATHS VARCHAR(20), OPENINGKILLRATIO VARCHAR(20), OPENINGKILLRATING VARCHAR(20), TEAMWINPERCENTAFTERFIRSTKILL VARCHAR(20), FIRSTKILLINWONROUNDS VARCHAR(20), RIFLEKILLS VARCHAR(20), SNIPERKILLS VARCHAR(20), SMGKILLS VARCHAR(20), PISTONKILLS VARCHAR(20), GRENADE VARCHAR(20), OTHER VARCHAR(20))")
    stats.commit()
def insertplayer(country, nickname, maps, kddiff, kd, rating1):
    stats.execute("INSERT INTO players (COUNTRY, NICKNAME, MAPS, KDDIFF, KD, RATING1) VALUES ('" + country + "', '" + nickname + "', '" + maps + "', '" + kddiff + "', '" + kd + "', '" + rating1 + "')")
    print("Processing: " + "'" + country + "', '" + nickname + "', '" + maps + "', '" + kddiff + "', '" + kd + "', '" + rating1 + "'")
    stats.commit()
def insertstats(tk, hs, td, kdr, dr, gdmgr, mp, rp, kr, ar, dthr, sbtr, str, rt1):
    stts.execute("INSERT INTO pstats (TOTALKILLS, HEADSHOT, TOTALDEATHS, KDRATIO, DAMAGEROUND, GRENADEDMGROUND, MAPSPLAYED, ROUNDSPLAYED, KILLSROUND, ASSISTSROUND, DEATHSROUND, SAVEDBYTEAMMATEROUND, SAVEDTEAMMATESROUND, RATING10) VALUES ('" + tk + "', '" + hs + "', '" + td + "', '" + kdr + "', '" + dr + "', '" + gdmgr + "', '" + mp + "', '" + rp + "', '" + kr + "', '" + ar + "', '" + dthr + "', '" + sbtr + "', '" + str + "', '" + rt1 + "')")
    print("Processing: " + "'" + tk + "', '" + hs + "', '" + td + "', '" + kdr + "', '" + dr + "', '" + gdmgr + "', '" + mp + "', '" + rp + "', '" + kr + "', '" + ar + "', '" + dthr + "', '" + sbtr + "', '" + rt1 + "'")
    stats.commit()
def insertindividual(k, d, kd, kr, rwk, kdd, a0, b1, c2, d3, e4, f5, tok, tod, okr1, okr2, twpafk, fkiwr, rk, sk, smgk, pk, g, o):
    stts.execute("INSERT INTO pindividualstats (KILLS, DEATHS, KILLDEATH, KILLROUND, ROUNDSWITHKILLS, KILLDEATHDIFFERENCE, a0KILLROUND, b1KILLROUND, c2KILLROUND, d3KILLROUND, e4KILLROUND, f5KILLROUND, TOTALOPENINGKILLS, TOTALOPENINGDEATHS, OPENINGKILLRATIO, OPENINGKILLRATING, TEAMWINPERCENTAFTERFIRSTKILL, FIRSTKILLINWONROUNDS, RIFLEKILLS, SNIPERKILLS, SMGKILLS, PISTONKILLS, GRENADE, OTHER) VALUES ('" + k + "', '" + d + "', '" + kd + "', '" + kr + "', '" + rwk + "', '" + kdd + "', '" + a0 + "', '" + b1 + "', '" + c2 + "', '" + d3 + "', '" + e4 + "', '" + f5 + "', '" + tok + "', '" + tod + "', '" + okr1 + "', '" + okr2 + "', '" + twpafk + "', '" + fkiwr + "', '" + rk + "', '" + sk + "', '" + smgk + "', '" + pk + "', '" + g + "', '" + o + "')")
    print("Processing: '" + k + "', '" + d + "', '" + kd + "', '" + kr + "', '" + rwk + "', '" + kdd + "', '" + a0 + "', '" + b1 + "', '" + c2 + "', '" + d3 + "', '" + e4 + "', '" + f5 + "', '" + tok + "', '" + tod + "', '" + okr1 + "', '" + okr2 + "', '" + twpafk + "', '" + fkiwr + "', '" + rk + "', '" + sk + "', '" + smgk + "', '" + pk + "', '" + g + "', '" + o + "'")
    stats.commit()

def processplayer(linktoplayer):
    player = requests.get(linktoplayer)
    soup = BeautifulSoup(player.text, "html.parser")
    rows = soup.find_all("div", {"class": "stats-row"})
    if len(rows) < 14:
        empty = "-empty-"
        insertstats(empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty)
        return
    uprow = []
    for row in rows:
        uprow.extend([row.find_all("span")[1].text])
    insertstats(uprow[0], uprow[1], uprow[2], uprow[3], uprow[4], uprow[5], uprow[6], uprow[7], uprow[8], uprow[9], uprow[10], uprow[11], uprow[12], uprow[13])
def processindividualstats(linktoplayer):
    player = requests.get(linktoplayer)
    soup = BeautifulSoup(player.text, "html.parser")
    rows = soup.find_all("div", {"class": "stats-row"})
    uprow = []
    for row in rows:
        if row.find_all("span")[1].text == "K / D diff.":
            uprow.extend([row.find_all("span")[2].text])
        else:
            uprow.extend([row.find_all("span")[1].text])
    insertindividual(uprow[0], uprow[1], uprow[2], uprow[3], uprow[4], uprow[5], uprow[6], uprow[7], uprow[8], uprow[9], uprow[10], uprow[11], uprow[12], uprow[13], uprow[14], uprow[15], uprow[16], uprow[17], uprow[18], uprow[19], uprow[20], uprow[21], uprow[22], uprow[23])

req = requests.get("https://www.hltv.org/stats/players")
soup = BeautifulSoup(req.text, 'html.parser')

def statsplayers():
    alltrs = soup.find_all("tr", {"class": ""})
    for tr in alltrs:
        td = tr.findChildren("td")
        insertplayer(td[0].find("img")["alt"], td[0].text.replace("'", ""), td[2].text, td[3].text, td[4].text, td[5].text)
def otherstats():
    aes = soup.find_all("a", {"class": "", "href": re.compile("^/stats/players/")})
    preurl = "https://www.hltv.org"
    for a in aes:
        currenturl = preurl + a["href"]
        processplayer(currenturl)
        newa = "/stats/players/individual/" + a["href"][14:]
        currenturl = preurl + newa
        processindividualstats(currenturl)

setdb()
statsplayers()
otherstats()

stats.close()