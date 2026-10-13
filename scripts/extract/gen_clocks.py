import json, re, html, sys

V2 = r"C:\Users\bradl\OneDrive\Desktop\GitHubClone\OPHIS-Pattern-Recognition-Event-Prediction_files\Chronicon_Engine_v2.html"
OUT = r"C:\Users\bradl\AppData\Local\Temp\claude\C--Users-bradl-OneDrive-Desktop-GitHubClone\f0d3fe13-8807-43e7-9da7-1e81488401ba\scratchpad\clocks.json"
TXT = "chronicon-clocks-calendrics.txt"
V2N = "Chronicon_Engine_v2.html"
MAN = "natorion/MANUAL.md"

lines = open(V2, encoding="utf-8").read().split("\n")
ledger = []
for i in range(666, 735):  # file lines 667..735
    m = re.match(r"\s*\[(-?\d+),'(\w+)','(.*)'\],?\s*$", lines[i])
    assert m, lines[i]
    ledger.append((int(m.group(1)), m.group(2), html.unescape(m.group(3)), i + 1))
assert len(ledger) == 69

def ep(y, m=None, d=None):
    return {"year": y, "month": m, "day": d}

def clock(id, name, py, pd, epoch, formula, units, desc, src):
    assert len(desc) <= 200, (id, len(desc))
    return {"id": id, "name": name, "periodYears": py, "periodDays": pd, "epoch": epoch,
            "formula": formula, "unitLabels": units, "description": desc, "source": src}

clocks = [
 clock("annus-mundi", "Annus Mundi", None, None, ep(-3894),
  "Era count, years elapsed since 3895 BC. JS: am = astro + 3894 (astro = astronomical year, 1 BC = 0). Source comment also: AM = 3895 - (BC year). Anchors: 2022 CE -> 5916; 2239 BC -> 1656; 2026 -> 5920; AM 6000 = 2106 CE. Flag: isPalindrome(am).",
  ["AM"], "The Ancient-World count from the 3895 BC poleshift - the calendar's Year One. Flood node AM 1656; AM 6000 in 2106 CE.",
  f"{TXT}:485,634,648-649 (srcdoc TIME MODEL, render 'Annus Mundi'); {V2N}:640,790,806-807"),
 clock("cataclysm-era", "Cataclysm Era", None, None, ep(-5238),
  "Years since the Nemesis Cataclysm of 5239 BC. JS: cat = astro + 5238. Meta note: 7-cycle Nemesis frame = 5544 yr (792x7).",
  ["yr"], "Years since the Nemesis Cataclysm of 5239 BC, when the binary broke apart.",
  f"{TXT}:371,634,652-653; {V2N}:396,790,810-811"),
 clock("phoenix-138", "Phoenix · Sky Dragon", 138, None, ep(-4308),
  "Strict 138-yr lattice; node where mod(astro,138) === 108; node #1 = 4309 BC (PHX = {mod:108, step:138, base:-4308}). JS: pPrev = astro - mod(astro-108,138); pNext = pPrev + 138; pInto = astro - pPrev; pTo = pNext - astro; pIdx = Math.round((pPrev - PHX.base)/138) + 1; bar = pInto/138*100. mod(n,m) = ((n%m)+m)%m. Multiples: 138x3=414 'cursed time', 138x4=552 'Phoenix cycles', 138x46=6348 (4309 BC -> 2040 CE).",
  ["node", "yr to node"], "The 138-year reset cycle - the recurring destroyer Breshears named; due 15 May 2040. Node #1 = 4309 BC; nodes 1902, 2040, 2178.",
  f"{TXT}:503,642,656-662,463; {V2N}:369,659,799,814-820,615"),
 clock("nemesis-x-792", "Nemesis X Object", 792, None, ep(462),
  "792-yr orbit: enters inner system when mod(astro-462,792) === 0, inside for 60 yr, outside 732 yr (NEM_ENTER = {mod:462, step:792}). JS: offset = mod(astro-462,792); inner = offset < 60; enterPrev = astro - offset; enterNext = enterPrev + 792; exit = enterPrev + 60; if inner: yrsLeft = 60 - offset, bar = offset/60*100; else: yrsToReturn = enterNext - astro, bar = (astro - (enterPrev+60))/732*100. Ledger marker: txt uses offset<60, v2 uses offset<=60.",
  ["yr inside", "yr to return"], "The 792-year orbit of the dark companion - 60 yr inside Sol, 732 without; returns 2046.",
  f"{TXT}:504,664-680,606; {V2N}:376,660,822-838,762"),
 clock("ner-600", "Anunnaki NER", 600, None, ep(-5238),
  "600-yr epochs phased on astro 162 (NER = {mod:162, step:600, base:-5238}; 5239 BC start). JS: nerOff = mod(astro-162,600); nerStart = astro - nerOff; nerNum = Math.floor((astro - NER.base)/600) + 1; next = nerStart + 600; bar = nerOff/600*100. Each 600-yr NER = ten 60-yr decans. 762 CE = 6000th NER year.",
  ["PERIOD", "decan"], "The 600-year regnal epochs of the Anunna kings - ten 60-year decans apiece. 762 CE falls on the 6000th NER year.",
  f"{TXT}:505,682-688,951; {V2N}:383,661,840-846"),
 clock("mayan-long-count", "Mayan Long-Count", 5158, 1872000, ep(-3112),
  "Hard-coded baktun boundaries MAY_NODES = [-3112,-2712,-2312,-1912,-1512,-1112,-712,-318,76,470,864,1258,1652,2046] (six 400-yr spans, then seven 394-yr spans after -712). Find bi with MAY_NODES[bi] <= astro < MAY_NODES[bi+1]; label 'BAKTUN '+(bi+1)+'/13'; span = bEnd - bStart; into = astro - bStart; yrsToNext = bEnd - astro; before -3112 = PRE-COUNT; v2: astro >= 2046 -> '13.0.0.0.0 complete'. Long-Count year: lc = astro + 3112 (2026 -> 5138; 2046 -> 5158). Sigil flag (v2): lc > 0 && String(lc).indexOf('138') >= 0.",
  ["baktun", "13.0.0.0.0", "LC year"], "Thirteen baktuns of 144,000 days from 3113 BC, closing at 13.0.0.0.0 in 2046. 2026 = LC 5138.",
  f"{TXT}:506,690-700,1045-1049; {V2N}:402,662,793,803,848-859,1252-1279"),
 clock("metonic-19", "Lunar Clock · Metonic recursion", 19, None, ep(2026, 5, 30),
  "19 yr = 235 lunations (235/19 = 12.368 moons/yr). Flag: mod(REF - astro, 19) === 0 where REF = 2026 (txt) or TODAY.y (v2). Cycle count: yd = REF - astro; yd >= 0 ? Math.floor(yd/19)+' back' : Math.abs(Math.floor(yd/19))+' ahead'.",
  ["Metonic cycle", "lunation"], "The 19-year Metonic gear - after 235 lunations the moon returns to the same phase on the same date.",
  f"{TXT}:426,467,643,726,862-863; {V2N}:428-429,800,885-886,936-937"),
 clock("lunar-synodic", "Moon phase (continuous synodic model)", None, 29.530588853, ep(2000, 1, 6),
  "SYN = 29.530588853; NEWMOON_J2000 = 2451550.1 (2000-01-06 18:14 UT). J = jdn(astro,m,d) (proleptic Gregorian: a=floor((14-m)/12); y=astro+4800-a; mm=m+12a-3; J = d+floor((153mm+2)/5)+365y+floor(y/4)-floor(y/100)+floor(y/400)-32045). age = mod(J - NEWMOON_J2000, SYN); frac = age/SYN; illum = (1-cos(2*PI*frac))/2; phaseIdx = floor(mod(frac+1/16,1)*8)%8 over [New, Waxing Crescent, First Quarter, Waxing Gibbous, Full, Waning Gibbous, Last Quarter, Waning Crescent]; lunation (txt) = Math.round((J-2423436.40347)/SYN), (v2) = Math.floor((J-2423436.40347)/SYN)+1; moonsFromToday = Math.round((TODAY_JD - J)/SYN).",
  ["d", "lunation #"], "Moon age, illumination and lunation number from a J2000 new-moon epoch; deep-past phases are cycle-true rather than historically observed.",
  f"{TXT}:487-498,711-727,849-865; {V2N}:642-654,870-889,923-939"),
 clock("anunna-turnings", "Anunna Reckoning · šar = a turning of the stars", None, None, ep(-3894, 1, 1),
  "šar = one day (a turning). JS: AM_EPOCH = jdn(-3894,1,1); turns = J - AM_EPOCH; T = |turns|; Draconian yr = T/360; NER = T/216000; baktun = T/144000; nodes: T===432000 'antediluvian total', T===864000 'Foundation of Time', T%144000===0 'n x baktun'. 432,000 = 3 baktuns = 1,200 Draconian yr; 864,000 = 6 baktuns = 2,400 Draconian yr; Enoch 300 yr = 108,000 turnings.",
  ["turnings", "Draconian yr", "NER", "baktun"], "Counts turnings (days) since AM Year One, 3895 BC, read in Draconian measures: 360 = 1 Draconian yr, 216,000 = 1 NER, 144,000 = 1 baktun.",
  f"{V2N}:361-362,994,1003-1012,1334-1344,623-625 (v2 only)"),
 clock("phoenix-countdown", "Phoenix Countdown · 15 May 2040", None, None, ep(2040, 5, 15),
  "Live: ms = Date.UTC(2040,4,15,0,0,0) - now; days = floor(ms/86400000); flags days%138===0 '÷138 today', days%19===0 '÷19 today'; also yrsTo(y) = ((Date.UTC(y,0,1)-Date.now())/3.15576e10).toFixed(1) for 2046 and 2178. After target: 'ARRIVED'.",
  ["d", "hh:mm:ss"], "Live count to the 2040 reset - calls it out whenever the days remaining fall on a multiple of 19 or 138.",
  f"{V2N}:470-473,1095,1116-1124; {TXT}:888-893 (liveTick, unused)"),
 clock("giza-apparent-solar", "Giza Apparent Solar · the true sun", None, None, None,
  "lon = 31.1342; utcH = h + m/60 + s/3600; B = 2*PI*(dayOfYear-81)/364; EoT = 9.87*sin(2B) - 7.53*cos(B) - 1.5*sin(B) (minutes); solarH = ((utcH + lon/15 + EoT/60) % 24 + 24) % 24.",
  ["hh:mm:ss", "EoT min"], "Sundial time over the pyramid's own meridian, corrected by the equation of time.",
  f"{V2N}:452-455,1110-1115"),
 clock("cairo-civil", "Cairo · Giza Plateau", None, None, None,
  "Intl.DateTimeFormat timeZone 'Africa/Cairo'; offset read from shortOffset (default 2); label EEST if UTC+3 else EET. Meta: 30.0°N 31.1°E.",
  ["hh:mm:ss"], "Civil time where the Great Pyramid stands - the stone this whole instrument reads.",
  f"{V2N}:446-449,1100-1104"),
 clock("utc", "UTC · Zulu", None, None, None, "now.getUTCHours/Minutes/Seconds.", ["hh:mm:ss"],
  "Coordinated Universal Time - the world's reference clock.", f"{V2N}:458-461,1106-1107"),
 clock("local-meridian", "Your meridian · local", None, None, None, "now.getHours/Minutes/Seconds; zone from Intl resolvedOptions().timeZone.", ["hh:mm:ss"],
  "This device's own time zone, wherever you are reading from.", f"{V2N}:464-467,1108-1109"),
 clock("solar-year-length", "Solar Year · day-length", None, None, None,
  "leap = (astro%4===0) && (astro%100!==0 || astro%400===0); days = leap ? 366 : 365. Note: the Draconian/Anunna year was 360 turnings.",
  ["days"], "Length of the dialed year - 365 or 366; the Anunna/Draconian year was 360.", f"{V2N}:482-485,1014-1016"),
 clock("hebrew-anno-mundi", "Hebrew · Anno Mundi", None, None, ep(-3760),
  "hy = Intl year (calendar 'hebrew'); metonicYr = mod(hy,19) || 19; leap13 = mod(7*hy+1,19) < 7; hgap = (astro+3894) - hy (Archaix AM minus Hebrew AM; flagged when hgap%19===0). Epoch stated as 3761 BC, 134 yr after Year One (133 after Rosh Hashanah).",
  ["AM", "Metonic yr /19"], "Rabbinic world-era, built on the same 19-year Metonic gear as the moon.", f"{V2N}:488-491,1018-1022"),
 clock("coptic", "Coptic · Church of Egypt", None, None, ep(284),
  "Intl calendar 'coptic' (year = first digit-run). Year of the Martyrs from 284 CE.", ["Year of the Martyrs"],
  "The Egyptian church's count from the Year of the Martyrs, 284 CE.", f"{V2N}:494-497,1024-1025"),
 clock("egyptian-civil-nabonassar", "Egyptian Civil · Nabonassar", None, 365, None,
  "ed = J - 1448638; year = floor(ed/365)+1; doy = mod(ed,365); month = floor(doy/30) (Thoth..Mesore, 12 x 30) else epagomenae; day = mod(doy,30)+1.",
  ["Nabonassar yr", "Thoth..Mesore", "epagomenae"], "The ancient 365-day wandering year that drifts a full turn every Sothic 1460.", f"{V2N}:500-503,1027-1030"),
 clock("sothic", "Sothic cycle", 1460, None, ep(139),
  "v2: sothicPos = mod(astro - 139, 1460) + '/1460'. MANUAL constant OPH_SOTHIC = 1461 (years), no position formula.",
  ["/1460"], "The Egyptian civil year drifts a full turn every Sothic 1460 (v2). MANUAL lists OPH_SOTHIC = 1461 years.", f"{V2N}:501,1030,1346; {MAN}:331"),
 clock("mayan-calendar-round", "Mayan Calendar Round", 52, 18980, None,
  "ld = J - 584283; tzolkin = (mod(ld+3,13)+1) + ' ' + tzNm[mod(ld+19,20)]; hp = mod(ld+348,365); haabMonth = floor(hp/20) (Pop..Kumku, 18) else Wayeb; haabDay = mod(hp,20). Round 52 yr / 18,980 d (260-day Tzolkin x 365-day Haab).",
  ["Tzolkin", "Haab", "Wayeb"], "The 52-year meshing of the 260-day Tzolkin and 365-day Haab.", f"{V2N}:506-509,1032-1037"),
 clock("julian-calendar", "Julian Calendar · Old Style", None, None, None,
  "fromJDJulian(J): c=J+32082; d=floor((4c+3)/1461); e=c-floor(1461d/4); m=floor((5e+2)/153); day=e-floor((153m+2)/5)+1; month=m+3-12*floor(m/10); year=d-4800+floor(m/10). gap = J - jdn(julian y,m,d) days behind Gregorian.",
  ["Old Style"], "Caesar's calendar - now 13 days behind Gregorian.", f"{V2N}:512-515,989,1039-1041"),
 clock("julian-day", "Julian Day · raw count", None, None, None,
  "J = jdn(astro,m,d) (proleptic Gregorian JDN, see lunar-synodic). Flags palindromic day; next palindrome JDN.", ["JDN"],
  "The astronomer's continuous day-number since 4713 BC.", f"{V2N}:518-521,1043-1045"),
 clock("islamic-hijri", "Islamic · Hijri", None, None, ep(622), "Intl calendar 'islamic'.", ["AH"],
  "The Muslim lunar year, ~354 days, from 622 CE.", f"{V2N}:524-527,1047-1048"),
 clock("persian-solar-hijri", "Persian · Solar Hijri", None, None, ep(622), "Intl calendar 'persian'. Meta: 'from 622 CE'.", ["Solar Hijri"],
  "The most astronomically accurate solar calendar in use.", f"{V2N}:530-533,1050-1051"),
 clock("indian-saka", "Indian National · Saka", None, None, ep(78), "Intl calendar 'indian'.", ["Saka"],
  "India's civil calendar, epoch 78 CE.", f"{V2N}:536-539,1053-1054"),
 clock("buddhist-era", "Buddhist Era", None, None, None, "be = astro + 543.", ["BE"], "Theravada count - CE + 543.", f"{V2N}:542-545,1056-1057"),
 clock("ethiopic", "Ethiopic", None, None, None, "Intl calendar 'ethiopic' (Amete Mihret).", ["Amete Mihret"],
  "Thirteen months, ~7-8 years behind Gregorian.", f"{V2N}:548-551,1059-1060"),
 clock("chinese-sexagenary", "Chinese · sexagenary", 60, None, None,
  "ci = mod(astro-4,60); stem = st[mod(ci,10)] (Jia..Gui); branch = br[mod(ci,12)] (Zi..Hai); element = el[mod(ci,10)]; animal = an[mod(ci,12)]; yr = ci+1 of 60; 'approx at Jan'.",
  ["stem", "branch", "element", "animal"], "The 60-year cycle of stem, branch, element and zodiac animal.", f"{V2N}:554-557,1062-1068"),
 clock("byzantine-world-era", "Byzantine · Old Russian", None, None, ep(-5508, 9, 1), "year = m >= 9 ? astro + 5509 : astro + 5508.", ["AM"],
  "The creation world-era from 1 Sept 5509 BC.", f"{V2N}:560-563,1070-1071"),
 clock("kali-yuga", "Kali Yuga · Vedic", None, None, ep(-3101), "ky = astro + 3101.", ["Kali Yuga yr"],
  "The Hindu dark age, begun 3102 BC.", f"{V2N}:566-569,1073-1075; ledger -3102"),
 clock("holocene", "Holocene · Human Era", None, None, None, "he = astro + 10000.", ["HE"],
  "CE + 10,000 - counting from the dawn of settlement.", f"{V2N}:572-575,1077-1079"),
 clock("french-republican", "French Republican", None, None, ep(1792, 9, 22),
  "fJD = J - 2375839; if fJD < 1 'pre-Republic'; fy = floor((fJD-1)/365.2422)+1; fdoy = floor(fJD-1-(fy-1)*365.2422); month = floor(fdoy/30) (Vendemiaire..Fructidor) else Sansculottides; day = mod(fdoy,30)+1. Approximate.",
  ["An", "month"], "The Revolution's decimal calendar of 1793 (approximate).", f"{V2N}:578-581,1081-1088"),
 clock("unix", "Unix · machine time", None, None, ep(1970, 1, 1), "ux = Math.round(dt.getTime()/1000).", ["s"],
  "Seconds elapsed since 1 Jan 1970.", f"{V2N}:584-587,1090-1092"),
 clock("saros", "Saros eclipse cycle", 18.03, 6585.3211, None,
  "Constant only: OPH_SAROS = 6585.3211 days (18.03 years). No epoch or position formula in the sources.", ["d"],
  "The Saros eclipse cycle, in days (18.03 years). Natorion equation constant.", f"{MAN}:324"),
 clock("inex", "Inex eclipse cycle", 28.94, 10571.95, None,
  "Constant only: OPH_INEX = 10571.95 days (28.94 years). No epoch or position formula.", ["d"],
  "The Inex eclipse cycle, in days (28.94 years). Natorion equation constant.", f"{MAN}:325"),
 clock("precession", "Precession of the equinoxes", 25772, None, None,
  "Constant only: OPH_PRECESSION = 25772 years. v2 prose: '72 years - one precessional degree'. No epoch or position formula.", ["yr"],
  "One precession of the equinoxes, in years (MANUAL). v2 prose calls 72 years one precessional degree.", f"{MAN}:332; {V2N}:1342"),
 clock("jupiter-saturn", "Jupiter-Saturn great conjunction", 19.86, None, None, "Constant only: OPH_JUPSAT = 19.86 years.", ["yr"],
  "Jupiter-Saturn great conjunction, in years. Natorion equation constant.", f"{MAN}:333"),
 clock("jupiter-return", "Jupiter return", 11.862, None, None, "Constant only: OPH_JUPITER = 11.862 years.", ["yr"],
  "Jupiter return, in years. Natorion equation constant.", f"{MAN}:335"),
 clock("saturn-return", "Saturn return", 29.4571, None, None, "Constant only: OPH_SATURN = 29.4571 years.", ["yr"],
  "Saturn return, in years. Natorion equation constant.", f"{MAN}:334"),
 clock("uranus-return", "Uranus return", 84.0205, None, None, "Constant only: OPH_URANUS = 84.0205 years.", ["yr"],
  "Uranus return, in years. Natorion equation constant.", f"{MAN}:336"),
 clock("chiron-return", "Chiron return", 50.42, None, None, "Constant only: OPH_CHIRON = 50.42 years.", ["yr"],
  "Chiron return, in years. Natorion equation constant.", f"{MAN}:337"),
 clock("year-lengths", "Year lengths (tropical / sidereal / anomalistic / ideal)", None, 365.24219, None,
  "Constants only: OPH_YEAR_TROPICAL = 365.24219 d; OPH_YEAR_SIDEREAL = 365.256363 d; OPH_YEAR_ANOMALISTIC = 365.259636 d; OPH_YEAR_IDEAL = 360 d ('the ideal year of the thesis'). periodDays holds the tropical value.",
  ["d"], "Year-length constants; OPH_YEAR_IDEAL = 360 is the ideal year of the thesis (the Draconian year of 360 turnings in v2).", f"{MAN}:327-330"),
]

clockIdsByKind = {"phx": ["phoenix-138"], "nem": ["nemesis-x-792"], "ner": ["ner-600"], "may": ["mayan-long-count"], "note": []}
keyIds = {-5238: ["cataclysm-era", "ner-600"], -4038: [], -2838: ["annus-mundi"], -2238: ["annus-mundi", "phoenix-138"],
          2040: ["phoenix-138", "phoenix-countdown"], 2046: ["nemesis-x-792", "mayan-long-count"], 2178: ["phoenix-138"]}
special_md = {-2238: (5, None), 2040: (5, 15), -582: (5, None)}

def fmt(a):
    return f"{1-a} BC" if a <= 0 else f"{a} CE"

cd = []
for a, kind, txt, ln in ledger:
    ids = keyIds[a] if kind == "key" else clockIdsByKind[kind]
    if kind == "note" and a == -3102: ids = ["kali-yuga"]
    m, d = special_md.get(a, (None, None))
    cd.append({"year": a, "month": m, "day": d, "title": txt, "clockIds": ids,
               "note": f"{fmt(a)} · AM {a+3894} · ledger kind '{kind}'",
               "source": f"{TXT}:{ln-156} / {V2N}:{ln} (event ledger E)"})

extra = [
 (-2904, None, None, "Great Pyramid first stone set (AM 990)", ["annus-mundi"], "2905 BC; 666 years before the Flood; 90-year raising", f"{TXT}:964,970,1127"),
 (-2814, None, None, "Great Pyramid capstone set (AM 1080)", ["annus-mundi"], "2815 BC; also ledger row -2814; stands 576 years", f"{TXT}:963-964,1128"),
 (-1898, None, None, "Great Pyramid re-emerges (AM 1996)", ["annus-mundi"], "1899 BC; after 340 years beneath the waters; year of Babel & founding of Akkad", f"{TXT}:964,1130"),
 (1882, None, None, "Petrie completes Giza survey (AM 5776)", ["annus-mundi"], "1882 + 3894 = 5776 = 76²; height 5776 in", f"{TXT}:985-987"),
 (2026, 5, 30, "You Are Here: AM 5920 · LC 5138 · 7264 yr after the Cataclysm", ["annus-mundi", "mayan-long-count", "cataclysm-era", "metonic-19"], "txt reference date; moon near-full", f"{TXT}:478,955,1094"),
 (2106, None, None, "AM 6000", ["annus-mundi", "nemesis-x-792"], "same year as ledger 'Nemesis X exits'", f"{TXT}:649"),
 (2045, None, None, "LC 5157 - the count's final whole year", ["mayan-long-count", "metonic-19"], "2026 + one Metonic 19", f"{V2N}:1261"),
 (-2974, None, None, "Long-Count sigil rung LC 138 (AM 920)", ["mayan-long-count"], "2975 BC; seventy years before the first stone of Giza", f"{V2N}:1270"),
 (-1974, None, None, "Long-Count sigil rung LC 1138 (AM 1920)", ["mayan-long-count"], "1975 BC; the Stone lies beneath the Flood waters", f"{V2N}:1271"),
 (-974, None, None, "Long-Count sigil rung LC 2138 (AM 2920)", ["mayan-long-count"], "975 BC; sixty-four years after the ledger's birth of David", f"{V2N}:1272"),
 (26, None, None, "Long-Count sigil rung LC 3138 (AM 3920)", ["mayan-long-count"], "26 CE; the only rung of the early Common Era", f"{V2N}:1273"),
 (1026, None, None, "Long-Count sigil rung LC 4138 (AM 4920)", ["mayan-long-count"], "1026 CE; deep in the quiet of baktun 11", f"{V2N}:1274"),
 (2026, None, None, "Long-Count sigil rung LC 5138 (AM 5920)", ["mayan-long-count"], "the last 138-faced year the count will ever show", f"{V2N}:1275"),
]
for y, m, d, t, ids, n, s in extra:
    cd.append({"year": y, "month": m, "day": d, "title": t, "clockIds": ids, "note": n, "source": s})
cd.sort(key=lambda r: (r["year"], r["month"] or 0))

def passages(kind_rows):
    return kind_rows

nem_rows = [(a, t) for a, k, t, _ in ledger if (k == "nem" or a in (2046,)) ]
phx_rows = [(a, t) for a, k, t, _ in ledger if (k == "phx" or a in (-2238, 1488, 2040, 2178))]

def body(id, name, aliases, py, rows, desc, src):
    assert len(desc) <= 200
    last = [{"year": a, "note": t} for a, t in rows if a <= 2026]
    nxt = [{"year": a, "note": t} for a, t in rows if a > 2026]
    return {"id": id, "name": name, "aliases": aliases, "periodYears": py, "lastPassages": last, "nextPassages": nxt,
            "description": desc, "source": src}

bodies = [
 body("nemesis-x", "Nemesis X Object", ["Nemesis X", "the dark companion", "intruder world", "Tiamat (ledger -1914: 'Tiamat passes')"], 792,
      nem_rows, "792-year orbit: 60 years inside Sol, 732 without. Enters the inner system when mod(astro-462,792)=0; returns 2046, exits 2106.",
      f"{TXT}:384,504,664-680 + ledger; {V2N}:375-376,660,822-838; 14-domain-and-style.md:144"),
 body("phoenix", "Phoenix", ["Sky Dragon", "Fenris (ledger 2040)"], 138,
      phx_rows, "The recurring planetary destroyer Breshears named, on a strict 138-year lattice (node: mod(astro,138)=108). Next visitation 15 May 2040.",
      f"{TXT}:377,503,949,1080 + ledger; {V2N}:368-369,1318"),
 body("nemesis", "Nemesis", ["the binary", "dead Nemesis system"], None,
      [(-5238, "Nemesis Cataclysm — Nemesis implodes; Earth, Luna, Phoenix, Nemesis X & Electra hurled toward Sol")],
      "The companion whose implosion in 5239 BC (the Nemesis Cataclysm) starts the Cataclysm Era; Luna is said to arrive from the dead Nemesis system.",
      f"{TXT}:511,514; {V2N}:396"),
 body("electra", "Electra", [], None,
      [(-5238, "Nemesis Cataclysm — ... Electra hurled toward Sol")],
      "Fifth body hurled toward Sol at the Cataclysm. No period or further passages given in the sources.", f"{TXT}:511"),
 {"id": "nibiru", "name": "Nibiru", "aliases": [], "periodYears": None, "lastPassages": [], "nextPassages": [],
  "description": "Not defined in any assigned source file. See openQuestions for where the name does appear.",
  "source": "none of the assigned files (grep: chronicon-clocks-calendrics.txt, Chronicon_Engine_v2.html, chronicon.html, DOMAIN.md, 20-chronicon-source.md, WHITEPAPER.md, 14-domain-and-style.md, MANUAL.md)"},
]

openQ = [
 "YEAR CONVENTION: all 'year' fields are ASTRONOMICAL years exactly as the sources' JS uses them: 1 BC = 0, 2 BC = -1, so BC year B -> 1 - B (e.g. 5239 BC = -5238, 3113 BC = -3112, 2239 BC = -2238). Source: TIME MODEL comment, chronicon-clocks-calendrics.txt:484 / Chronicon_Engine_v2.html:639. fmtYear(a) = a<=0 ? (1-a)+' BC' : a+' CE'.",
 "'YEAR ONE' (3895 BC, astro -3894) evaluates to AM 0 under AM = astro + 3894; ledger rows before it have negative AM (-5238 -> AM -1344). Source labels it Year One; 20-chronicon-source.md §7.7 reads AM as years elapsed.",
 "Nibiru: absent from all assigned files. Outside them it appears in chronicon-desk/package.json (description only), Chronotecture-Charts/redesign/vid.html:111-112 ('Anunnaki planet Nibiru passes over ecliptic, entering' 1254; 'Nibiru seen from Earth as it exits the system' 1314) and iic.html:131 (1314 'Nibiru passed close to Earth'). 1254 and 1314 are Nemesis X ledger years; no source states Nibiru = Nemesis X. Not imported.",
 "Sothic: v2 uses 1460 (mod(astro-139,1460), epoch astro 139); MANUAL OPH_SOTHIC = 1461. 20-chronicon-source.md §2.7 says Sothic/Saros/Inex/Jupiter-Saturn are absent from the clocks txt and have no Chronicon provenance (they are Natorion equation constants).",
 "Precession: MANUAL OPH_PRECESSION = 25772 yr; v2 prose says '72 years — one precessional degree' (which x360 would be 25920). No precession clock/epoch in any source.",
 "Saros, Inex, Jupiter-Saturn, planetary returns and year-length constants have no epoch, so no position/next-date can be computed from the sources alone.",
 "Nemesis inner arc: render test is offset < 60 in both files, but v2's ledger marker uses offset <= 60 ('0 = entry … 60 = exit'). Six nem rows sit at offset 60 (-3438, -2646, -1854, -270, 1314, 2106); the '60th year of transit' rows (-1854, 1314) test as outside under < 60.",
 "Ledger 522 CE says 'ONLY year Phoenix & Nemesis X are in the inner system together', but mod(522-462,792) = 60 (not inner); years satisfying both tests are -3480, -2652, -306 (20-chronicon-source.md §7.2).",
 "Baktun: labelled 144,000 days, but MAY_NODES spans are 400 yr x6 then 394 yr x7 (pivot -712, the '360→365.25 d' reset row); 6x400+7x394 = 5158. Full count 1,872,000 d (v2).",
 "Mayan Calendar Round epoch JD 584283 is, by the sources' own jdn(), 11 Aug of astro -3113 (3114 BC), one year before the Long-Count epoch astro -3112 (3113 BC) used by MAY_NODES and LC = astro + 3112.",
 "Lunation number: txt Math.round((J-2423436.40347)/SYN); v2 Math.floor(...)+1. Metonic reference year: txt hard-codes 2026; v2 uses the current year.",
 "Mayan wheel past 2046: txt shows 'BAKTUN 14/13' (span 0); v2 adds a '13.0.0.0.0 complete' branch.",
 "NER: 600 years (clock) vs v2 Anunna reckoning 1 NER = 216,000 turnings = 600 Draconian (360-day) years (~591.4 Julian years). Anunna turnings epoch jdn(-3894,1,1) is what v2 code uses; the source prose gives no zero point (20-chronicon-source.md §10.7).",
 "2040 Phoenix date: ledger says '15/16 MAY'; the countdown targets 15 May 2040 00:00 UTC.",
 "Hebrew gap note says the rabbinic epoch (3761 BC) is 134 yr after Year One, '133 after Rosh Hashanah'; Persian Solar Hijri meta says 'from 622 CE'.",
 "Ledger heading says 'The 300-Event Ledger' but both files ship 69 identical rows (txt escapes ’ as \\u2019). Only year-level dates; month given only for 2040 (15 May), the Flood (May) and Thales (May).",
 "Phoenix appears both as a clock (phoenix-138) and a body; ledger rows of other kinds also land on Phoenix nodes (-2238 key, 1488 note) and were included as Phoenix passages. 2178 'Simulation Collapse' is a node (138 yr after 2040) and is included as a next passage.",
]

data = {"clocks": clocks, "bodies": bodies, "calendricDates": cd, "openQuestions": openQ}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(clocks), len(bodies), len(cd), len(openQ))
for b in bodies:
    print(b["id"], b["periodYears"], [p["year"] for p in b["lastPassages"]], [p["year"] for p in b["nextPassages"]])
