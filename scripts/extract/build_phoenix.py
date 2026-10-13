import json, sys

OUT = sys.argv[1]
CM = "chronologists-machine/src/data/stations.json"
EW = "ere-we-were-remotion/stations.json"
CH = "films/data/AllClips_Chyrons_v1.json"
TR = "films/data/AllClips_Transcripts_v2.json"
CX = "codex/PhoenixCODEX138.txt"
PAL = "codex/PhoenixCODEX138_Palindromic.txt"
RD = "README.md"

cycle = {
    "lengthYears": 138,
    "description": "Phoenix 138-year cycle per the Archaix/Chronicon thesis (Jason Breshears) as used in the Phoenix CODEX 138 project. Phoenix years fall on multiples of 138 Anno Mundi counted from Year One (3895 BC = AM 1); 43 such passes run to 2040 (AM 5934 = 138 x 43). Every fourth Phoenix is a flood (552-year chain: 2239, 1687, 1135, 583 BC). The engine pairs it with Metonic 19, NER 600, Nemesis 792, the 144,000-day baktun and the sar.",
    "anchorYears": [-5239, -3895, -2239, 1902, 2040, 2106],
    "anchorNotes": {
        "-5239": "Chronicon count origin (Nemesis/Great Year count opens); 7,344 years to 2106",
        "-3895": "Year One, Anno Mundi 1",
        "-2239": "Great Flood, AM 1656 = 138 x 12 (the hinge/mirror centre)",
        "1902": "Last documented Phoenix, AM 5796 = 138 x 42 (Mont Pelee / Red Mud)",
        "2040": "Next Phoenix, AM 5934 = 138 x 43",
        "2106": "AM 6000 capstone year; Nemesis 792 loop from 3439 BC also lands here"
    },
    "yearNumbering": "BC years are stored as negative integers exactly as the sources' own sortYear fields do: N BC = -N, so 1 BC = -1 and there is NO year zero (1 BC is followed by AD 1). This is historical BC/AD numbering written with a minus sign, NOT astronomical numbering (astronomical year = -(N-1), i.e. 1 BC = 0). The sources state the Chronicon rule AD = AM - 3894 and do BC arithmetic as 3895 - AM; the station sheets note the Long Count zero '11 August 3114 BC ... astronomical year -3113', which Chronicon lists as 3113 BCE. Fractional sortYears in the sources (e.g. 1932.5, 2026.74) were used only for ordering and are rounded down here."
}

def P(year, label, idx, source):
    return {"year": year, "label": label, "cycleIndex": idx, "source": source}

phoenix = [
    P(-4309, "4309 BC - THE DAYSTAR GOES DARK: Chronicon calls this 'Phoenix Year 1' (start of chronoliths); 414 years (138 x 3) before Year One", None, f"{EW} C02; {CM} M02"),
    P(-4033, "4033 BCE - one Phoenix step (-138 AM) before Year One; mirror of 2377 BCE", -1, f"{EW} C18"),
    P(-3895, "AM 1 - YEAR ONE - THE BLACK FLAT (Anno Mundi count begins)", 0, f"{CH}; {CM} M03; {EW} C04"),
]
ch = [
    (1, 138, -3757, "A CALENDAR REMEMBERS", f"{EW} C05 (THE FIRST PHOENIX)"),
    (2, 276, -3620, "SALT WHERE THE SEA WAS", None),
    (3, 414, -3482, "THE QUIET ONE", None),
    (4, 552, -3344, "THE SLOW MUD", f"{EW} C07 gives 3343 BC (THE FIRST CYCLE CLOSES)"),
    (5, 690, -3206, "LIGHTS ON THE MOUNTAIN", f"{EW} C08 gives 3205 BC (ENOCH'S THIRD YEAR)"),
    (6, 828, -3068, "BUILDING THE CLOCK", f"{EW} C12 gives 3067 BC (THE MIDPOINT)"),
    (7, 966, -2930, "THE QUARRY", None),
    (8, 1104, -2792, "RED DUST", None),
    (9, 1242, -2654, "NOBODY HOME", f"{EW} C16 gives 2653 BC (THE SUMERIAN CATASTROPHE)"),
    (10, 1380, -2516, "WRONG BUILDER", None),
    (11, 1518, -2378, "A BROWN SUN", f"{EW} C18 gives 2377 BC (THE LAST PASS)"),
    (12, 1656, -2239, "THE FLOOD", f"{EW} C19, F01; {CM} M05-M08"),
    (13, 1794, -2101, "DIGGING OUT", None),
    (14, 1932, -1963, "THE GROUND REMEMBERS", None),
    (15, 2070, -1825, "A RUST MOON", None),
    (16, 2208, -1687, "THE FLOOD OF OGYGES", f"{EW} F02; {CM} M09"),
    (17, 2346, -1549, "THERA", None),
    (18, 2484, -1411, "ONE VALLEY", None),
    (19, 2622, -1273, "KADESH", f"{EW} K03"),
    (20, 2760, -1135, "THE AXIS", f"{EW} F03"),
    (21, 2898, -997, "THE SWORD", None),
    (22, 3036, -859, "ASSYRIA MARCHES", None),
    (23, 3174, -721, "TEN TRIBES", None),
    (24, 3312, -583, "THE MEDO-LYDIAN DARK", f"{EW} F04; {CM} M10"),
    (25, 3450, -445, "THE WALLS AGAIN", None),
    (26, 3588, -307, "A RUST SKY", None),
    (27, 3726, -169, "THE GOLD GOES DOWN", None),
    (28, 3864, -31, "JUDEA AND ACTIUM", None),
    (29, 4002, 107, "THE WRONG SUN", None),
    (30, 4140, 245, "CARTS AT THE GATE", None),
    (31, 4278, 383, "A TIMESTAMP", f"{EW} K03 gives 384 AD for the same pass"),
    (32, 4416, 521, "LIGHT WITHOUT BRIGHTNESS", None),
    (33, 4554, 659, "THE CAMELS KNOW", None),
    (34, 4692, 797, "DRAGONS, THEY WROTE", None),
    (35, 4830, 935, "ELDGJA", None),
    (36, 4968, 1073, "EMPTY SCAFFOLDS", None),
    (37, 5106, 1211, "SOMETIMES MEN", None),
    (38, 5244, 1349, "TWICE NINETEEN", None),
    (39, 5382, 1487, "DRUMS ON THE TEMPLE", None),
    (40, 5520, 1625, "CROSSES ON THE DOORS", None),
    (41, 5658, 1763, "NINETEEN GUNS", None),
    (42, 5796, 1902, "RED MUD", f"{CM} M11; {EW} K02"),
]
for idx, am, yr, ttl, extra in ch:
    lab = f"AM {am} - PHOENIX {idx} · 138 × {idx} - {ttl}"
    src = CH + (f"; {extra}" if extra else "")
    phoenix.append(P(yr, lab, idx, src))

def E(year, title, summary, tags, ph, source, yearEnd=None):
    assert len(summary) <= 200, (title, len(summary))
    return {"year": year, "yearEnd": yearEnd, "title": title, "summary": summary, "tags": tags, "phoenixYear": ph, "source": source}

events = [
 E(-5239, "THE FIRST FIRE / THE GREAT YEAR BEGINS", "A fire crosses the sky and the Chronicon count opens: 1,344 years before Year One, 7,344 years (3 x 2,448) to 2106; the 600-year Great Year and a binary sun with a smaller Daystar.", ["origin", "sky-fire", "Nemesis", "Great Year"], None, f"{CM} M01; {EW} C01"),
 E(-4309, "SHADOW ENTERS THE CIRCLE / THE DAYSTAR GOES DARK", "Chronoliths begin as a shadow first enters a stone circle's centre; the smaller sun collapses into a dark companion (Nemesis), the Kuiper Belt its wreckage. 930 years after 5239.", ["Nemesis", "chronolith", "sky"], None, f"{CM} M02; {EW} C02"),
 E(-4039, "THE CAPTURE OF LUNA", "After 270 frozen years Earth drifts into the Sun's system and takes up the Moon; Chronicon says Ussher's 4004 BC creation is 109 years off.", ["Moon", "cosmic"], None, f"{EW} C03"),
 E(-3895, "YEAR ONE", "Banishment from the walled garden; Anno Mundi 1, 6,000 years to 2106. Counted 1,656 years back from the 2239 BC Flood. AD = AM - 3894.", ["origin", "Anno Mundi"], -3895, f"{CM} M03; {EW} C04; {CH} THE BLACK FLAT; {TR}"),
 E(-3757, "THE FIRST PHOENIX", "Phoenix completes its first 138-year orbit after Year One; a calendar remembers what people forget. Hebrew epoch listed by Chronicon at 3760 BCE (135 AM).", ["Phoenix"], -3757, f"{EW} C05; {CH} A CALENDAR REMEMBERS; {TR}"),
 E(-3620, "SALT WHERE THE SEA WAS", "Phoenix 2: salt where the sea had been, nothing left to burn, yet the air smells of smoke.", ["Phoenix", "sea"], -3620, f"{CH}; {TR}"),
 E(-3482, "THE QUIET ONE", "Phoenix 3: red rain and nothing else; a quiet pass nobody writes down.", ["Phoenix", "red rain"], -3482, f"{CH}; {TR}"),
 E(-3439, "THE WATCHERS DESCEND / THE ARCS", "Nemesis X completes a 792-year orbit; fifty Watchers descend on Hermon; the Gihon floods a third of the earth in Enosh's days. 2239 + 1,200 = 3439; 2239 - 792 = 1447 BC.", ["Nemesis", "flood", "Watchers"], None, f"{EW} C06; {CM} M04"),
 E(-3344, "THE SLOW MUD", "Phoenix 4: the mud came slowly enough to run from, but they did not; a cook fire still burns beneath it.", ["Phoenix", "mudflow"], -3344, f"{CH}; {TR}"),
 E(-3343, "THE FIRST CYCLE CLOSES", "Four passes, 552 years; 5,448 years remain to 2106, read as the Great Pyramid's height in inches without its capstone.", ["Phoenix", "Great Pyramid"], -3343, f"{EW} C07"),
 E(-3300, "THE FIRST ACCOUNTS", "Core Claim 3: seals and proto-writing are dated 3500-3100 BC everywhere but Gobekli Tepe. Uruk IV tablets (~3350 BC) are the oldest writing known.", ["evidence", "writing"], None, f"{EW} E03"),
 E(-3206, "LIGHTS ON THE MOUNTAIN", "Phoenix 5: lights on the mountain; they came down, were called gods, and led us.", ["Phoenix", "sky"], -3206, f"{CH}; {TR}"),
 E(-3205, "ENOCH'S THIRD YEAR", "Phoenix passes in the third regnal year of Enoch, the first to write down the signs of heaven (364-day year); 'the planet of chronology and the chronologist'.", ["Phoenix", "Enoch"], -3205, f"{EW} C08"),
 E(-3200, "THE ŠAR", "Engine constant: the Sumerian sar = 3,600; Berossus's 120 sars (432,000) read as days are three baktuns. Archaix reads the sar as a day's turning of the stars.", ["cipher"], None, f"{EW} K06"),
 E(-3163, "NEWGRANGE", "The Sethites raise Carnac, Newgrange and Stonehenge I in Enoch's 45th year; Newgrange's roof-box aimed at winter-solstice sunrise c. 3150 BC.", ["megalith"], None, f"{EW} C09"),
 E(-3113, "THE LONG COUNT BEGINS", "Day zero of the Mayan Long Count (13.0.0.0.0 4 Ahau 8 Kumk'u); Chronicon reads the count in days and closes it in 2046, not 2012.", ["calendar"], None, f"{EW} C10"),
 E(-3103, "THE BLACK AGE", "Kali Yuga opens, ten years after the Long Count zero; Kali is time; the Persians remember a flood; Manetho's 36,525-year chronicle (25 Sothic cycles).", ["calendar", "flood"], None, f"{EW} C11"),
 E(-3068, "BUILDING THE CLOCK", "Phoenix 6: they lay the line with water; 828 years and six cycles in, they are building the clock.", ["Phoenix", "Great Pyramid"], -3068, f"{CH}; {TR}"),
 E(-3067, "THE MIDPOINT", "828 years after Year One and 828 before the Flood: a Phoenix pass at the exact centre of the antediluvian count (3895 - 6 x 138).", ["Phoenix", "mirror"], -3067, f"{EW} C12"),
 E(-2965, "ADAM DIES", "Adam dies at 930 AM and orders burial at the middle of the earth; Chronicon argues he had lived since 4039 BC (1,074 years).", ["patriarch"], None, f"{EW} C13"),
 E(-2930, "THE QUARRY", "Phoenix 7: they were still cutting stone the week it passed; the stone did not notice.", ["Phoenix", "quarry"], -2930, f"{CH}; {TR}"),
 E(-2905, "THE ALTAR IS BEGUN", "The Sethites begin the Great Pyramid 666 years before the Flood, four corners first then inward; slope 51°51'52\".", ["Great Pyramid"], None, f"{EW} C14"),
 E(-2905, "OPH_PI", "Engine constant OPH_PI = 3.14 ('Archaix pi'): base 440 cubits, height 280, 2 x 440 / 280 = 22/7.", ["cipher", "Great Pyramid"], None, f"{EW} K07"),
 E(-2900, "MUD BRICK", "The Great Pyramid already finished while others still build in mud brick, before the kings who claim it.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(-2815, "THE ALTAR IS FINISHED", "Great Pyramid complete after 90 years (1,080 months) in 1080 AM; perimeter 3,024 ft; 203 courses, top left off 'for later'; no body, no inscription, only numbers.", ["Great Pyramid"], None, f"{EW} C15; {CH} OFF-CYCLE TWO HUNDRED THREE COURSES (AM 1081) and ONLY NUMBERS; {TR}"),
 E(-2815, "OPH_PHI", "Engine constant OPH_PHI = 1.618: slant height over half-base at 51°52' is the golden ratio (Kepler triangle).", ["cipher", "Great Pyramid"], None, f"{EW} K08"),
 E(-2792, "RED DUST", "Phoenix 8: dust eating the monument from the top down; 1,104 years and still counting.", ["Phoenix", "dust"], -2792, f"{CH}; {TR}"),
 E(-2700, "ASWAN", "Copper and sand, they say; but the drill groove advances a tenth of an inch every turn.", ["Great Pyramid", "quarry"], None, f"{CH}; {TR}"),
 E(-2654, "NOBODY HOME", "Phoenix 9: every door open, every fire lit, nobody home; they went to the next cycle.", ["Phoenix", "disappearance"], -2654, f"{CH}; {TR}"),
 E(-2653, "THE SUMERIAN CATASTROPHE", "Phoenix pass 414 years before the Flood, matched to Sitchin's Sumerian cataclysm; sky dark at noon over Saqqara. One Cursed Earth.", ["Phoenix", "catastrophe", "darkness"], -2653, f"{EW} C16"),
 E(-2647, "THE EXODUS OF THE ANUNNA", "Nemesis X returns after 792 years; the Anunna withdraw for 732 years; the Hurrians build Urkesh.", ["Nemesis", "Anunnaki"], None, f"{EW} C17"),
 E(-2560, "KHUFU FOUND THEM", "The stela says Khufu found the monuments here, repairing the Sphinx, not carving it.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(-2516, "WRONG BUILDER", "Phoenix 10: a pharaoh walks to a monument older than his name. Wrong builder, right story.", ["Phoenix", "Great Pyramid"], -2516, f"{CH}; {TR}"),
 E(-2378, "A BROWN SUN", "Phoenix 11: noon under a brown sun; the barley ripens anyway.", ["Phoenix", "dim sun"], -2378, f"{CH}; {TR}"),
 E(-2377, "THE LAST PASS", "Phoenix's final orbit before the Flood, 138 years out; mirror of 4033 BCE, 138 years before Year One.", ["Phoenix", "mirror"], -2377, f"{EW} C18"),
 E(-2239, "THE GREAT FLOOD", "AM 1656 = 138 x 12, the twelfth Phoenix; 1,656 years after Year One and before the Medo-Lydian eclipse; first link of the 552-year flood chain; the mirror's centre.", ["flood", "Phoenix", "mirror"], -2239, f"{EW} C19, F01; {CM} M05, M06, M07, M08; {CH} THE FLOOD; {TR}"),
 E(-2101, "DIGGING OUT", "Phoenix 13: survivors dig out with their hands; every cycle someone digs out and calls it history.", ["Phoenix", "aftermath"], -2101, f"{CH}; {TR}"),
 E(-1963, "THE GROUND REMEMBERS", "Phoenix 14: no scripture keeps the date, the ground does; Jason's charts call it worldwide.", ["Phoenix", "catastrophe"], -1963, f"{CH}; {TR}"),
 E(-1825, "A RUST MOON", "Phoenix 15: the Moon turns the colour of rust, and only one man writes it down.", ["Phoenix", "Moon"], -1825, f"{CH}; {TR}"),
 E(-1687, "THE FLOOD OF OGYGES", "AM 2208 = 138 x 16; 552 years after the Flood, second link of the chain. Comet glow over a darkened sun; Attica under water; moai, Baalbek and Aswan quarries left mid-cut.", ["flood", "comet", "Phoenix", "quarry"], -1687, f"{EW} F02, E08; {CM} M09; {CH}; {TR}"),
 E(-1549, "THERA", "Phoenix 17: Thera goes up; no witness wrote it down, but someone watched.", ["Phoenix", "volcano"], -1549, f"{CH}; {TR}"),
 E(-1447, "EARLY EXODUS (ARC)", "2239 - 792 = 1447 BC, the early Exodus date, struck from AM 1656 by the 792-year arc.", ["Nemesis", "arc"], None, f"{CM} M04"),
 E(-1411, "ONE VALLEY", "Phoenix 18: it burned one valley and spared the next; ours was spared, this time.", ["Phoenix", "fire"], -1411, f"{CH}; {TR}"),
 E(-1273, "KADESH", "Phoenix 19, AM 2622 = 19 x 138 = 138 Metonic cycles; two armies with every face turned up; the year after Ramesses II fought at Kadesh.", ["Phoenix", "Metonic", "battle"], -1273, f"{EW} K03; {CH}; {TR}"),
 E(-1135, "THE AXIS", "Phoenix 20 (AM 2760), third flood-chain link and midpoint of the 43 fires; Atlantis goes under and the Bronze Age ends.", ["flood", "Phoenix", "Atlantis"], -1135, f"{EW} F03; {CH}; {TR}"),
 E(-997, "THE SWORD", "Phoenix 21: a shepherd king's tent on a hill; nothing kept but the count.", ["Phoenix"], -997, f"{CH}; {TR}"),
 E(-859, "ASSYRIA MARCHES", "Phoenix 22: Assyria marches; the dust ahead of them is not their own.", ["Phoenix", "dust", "war"], -859, f"{CH}; {TR}"),
 E(-721, "TEN TRIBES", "Phoenix 23: ten tribes walk out of the record and never walk back in.", ["Phoenix", "exile"], -721, f"{CH}; {TR}"),
 E(-583, "THE MEDO-LYDIAN DARK", "Phoenix 24, AM 3312 = 138 x 24, fourth flood-chain link: the sun goes out over the Halys and Medes and Lydians stop fighting. Thales called (remembered) it; book rounds 2 years.", ["eclipse", "Phoenix", "battle"], -583, f"{EW} F04; {CM} M10; {CH}; {TR}"),
 E(-539, "TIME, TIMES, AND HALF A TIME", "Important MSRF set (1260, 2520): Daniel's time, times and half a time = 1,260 days; Babylon falls to Cyrus.", ["cipher", "prophecy"], None, f"{EW} K13"),
 E(-450, "THE PRIESTS GUESS", "Two thousand years after the builders, a Greek asks the priests, and the priests guess.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(-445, "THE WALLS AGAIN", "Phoenix 25: one hand on the stone, one on the spear; they always build the walls again.", ["Phoenix", "rebuilding"], -445, f"{CH}; {TR}"),
 E(-432, "NINETEEN YEARS, TWO HUNDRED THIRTY-FIVE MOONS", "Engine's Metonic wheel: Meton announces the 19-year cycle on the Pnyx; 19 years hold 235 moons, drifting about two hours per round.", ["Metonic", "cipher"], None, f"{EW} K01"),
 E(-307, "A RUST SKY", "Phoenix 26: galleys under a rust sky, waiting for a wind that is not coming.", ["Phoenix", "sky"], -307, f"{CH}; {TR}"),
 E(-169, "THE GOLD GOES DOWN", "Phoenix 27: the gold is carried down the steps, taken, just like that.", ["Phoenix", "plunder"], -169, f"{CH}; {TR}"),
 E(-31, "JUDEA AND ACTIUM", "Phoenix 28: an earthquake in Judea and Actium burning on the same water, the same spring.", ["Phoenix", "earthquake", "battle"], -31, f"{CH}; {TR}"),
 E(34, "THE BENNU", "Core Claim 14: bird plus disc is the Bennu, the Phoenix. Tacitus reports a phoenix seen in Egypt in 34 AD; Herodotus says it returns every 500 years.", ["Phoenix", "evidence"], None, f"{EW} E14"),
 E(93, "THE GREAT YEAR", "Engine's NER wheel, 600 years a turn: Josephus writes that the great year completes in 600 years; 5239 to 2239 BC is five turns.", ["NER", "cipher", "Great Year"], None, f"{EW} K05"),
 E(107, "THE WRONG SUN", "Phoenix 29: every face turned up at the wrong sun; the sky counts cycles.", ["Phoenix", "sun"], 107, f"{CH}; {TR}"),
 E(139, "THE SOTHIC RETURN", "Normal MSRF set (1461): Censorinus records a new Sothic period in 139 AD when Sirius rose with the sun on 1 Thoth.", ["cipher", "Sothic"], None, f"{EW} K14"),
 E(245, "CARTS AT THE GATE", "Phoenix 30: the carts of the dead at the gate; it always follows the sky (transcript: 'Plagefolos').", ["Phoenix", "plague"], 245, f"{CH}; {TR}"),
 E(383, "A TIMESTAMP", "Phoenix 31: the northern sky burns; they will call it an omen, but it is a timestamp.", ["Phoenix", "sky-fire"], 383, f"{CH}; {TR}; {EW} K03 (384 AD)"),
 E(521, "LIGHT WITHOUT BRIGHTNESS", "Phoenix 32: a sun with light but no brightness, frosts in summer; thirty-two down, eleven left.", ["Phoenix", "dim sun", "cold"], 521, f"{CH}; {TR}"),
 E(659, "THE CAMELS KNOW", "Phoenix 33, a quiet one: the sun dim enough to look at; the camels know before we do.", ["Phoenix", "dim sun"], 659, f"{CH}; {TR}"),
 E(797, "DRAGONS, THEY WROTE", "Phoenix 34: fire in the sky over the monastery; they wrote 'dragons' instead of the date.", ["Phoenix", "sky-fire"], 797, f"{CH}; {TR}"),
 E(935, "ELDGJA", "Phoenix 35: Iceland splits open, fire for months, and the sun goes pale over Europe.", ["Phoenix", "volcano"], 935, f"{CH}; {TR}"),
 E(1050, "THE KINGFISHER", "Core Claim 15: the bird plucking a fish carries one meaning from Cyprus to Nazca to New Mexico (Mimbres bowls, c. 1000-1130 AD).", ["evidence", "motif"], None, f"{EW} E15"),
 E(1073, "EMPTY SCAFFOLDS", "Phoenix 36: a cathedral half built, scaffolds empty; they will finish it and forget why they stopped.", ["Phoenix"], 1073, f"{CH}; {TR}"),
 E(1211, "SOMETIMES MEN", "Phoenix 37: the plain is full of horsemen; sometimes the sky sends men.", ["Phoenix", "invasion"], 1211, f"{CH}; {TR}"),
 E(1314, "THE DARK ONE'S LOOP", "Engine's Nemesis wheel, 792 years: steps from 3439 BC reach 522, 1314 and 2106 AD; the Great Famine's unrelenting rains begin in spring 1315.", ["Nemesis", "famine", "rain"], None, f"{EW} K04"),
 E(1349, "TWICE NINETEEN", "Phoenix 38 (twice 19): a stinking mist out of the east, and then the dying.", ["Phoenix", "mist", "death"], 1349, f"{CH}; {TR}"),
 E(1487, "DRUMS ON THE TEMPLE", "Phoenix 39: drums on the temple; listen to the rhythm, they are counting it too.", ["Phoenix"], 1487, f"{CH}; {TR}"),
 E(1625, "CROSSES ON THE DOORS", "Phoenix 40: crosses on the doors, a lantern in the fog; three to go.", ["Phoenix"], 1625, f"{CH}; {TR}"),
 E(1722, "THE UNFINISHED", "Core Claim 8: work at the moai quarry, Baalbek and Aswan stopped at once in 1687 BC. Roggeveen sights Rapa Nui; ~400 moai remain in Rano Raraku.", ["evidence", "quarry"], None, f"{EW} E08"),
 E(1763, "NINETEEN GUNS", "Phoenix 41: cannon on the quay firing at a sky like a dying coal.", ["Phoenix", "sky"], 1763, f"{CH}; {TR}"),
 E(1837, "NO KING, NO BODY", "They called it the King's Chamber, but there was no king and no body: call it the upper chamber.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(1837, "IT RINGS", "'Sarcophagus' means flesh-eater, yet it never ate anyone: a granite coffer that rings when struck.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(1845, "THE BUCKET & THE CONE", "Core Claim 12: the 'handbag' is a bucket and the 'pine cone' the palm, badges of the apkallu's office. Layard opens Nimrud.", ["evidence", "apkallu"], None, f"{EW} E12"),
 E(1864, "THE TABLETS", "Core Claim 4: rongorongo is used to date Easter Island young. Eyraud first reports the tablets; one dated in 2024 to the 15th century.", ["evidence", "writing"], None, f"{EW} E04"),
 E(1865, "THROUGH SOLID ROCK", "345 feet at 26 degrees 31 minutes, through solid rock.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(1865, "THE MERIDIAN WINK", "The Resonance Clock's wink sits on the Giza meridian: apex at 29.9792 N echoes light's 299,792,458 m/s; Piazzi Smyth surveys the pyramid.", ["cipher", "Great Pyramid"], None, f"{EW} K16"),
 E(1881, "WHEN THE STONE STOPS BREATHING", "He measures at night when the stone stops breathing, to a thousandth of an inch, never bettered.", ["Great Pyramid", "measurement"], None, f"{CH}; {TR}"),
 E(1890, "THE VORTEX IS 1089", "The Vortex MSRF set (21.7, 32.6, 43.5...) is 1089 in disguise, the reversal constant; 1089 x 9 = 9801.", ["cipher"], None, f"{EW} K12"),
 E(1898, "THE SCORPION KING", "Core Claim 18: the scorpion is protection, never a threat (Serket, the Girtablilu). Scorpion Macehead found at Hierakonpolis.", ["evidence", "motif"], None, f"{EW} E18"),
 E(1902, "RED MUD / SHADOW LEAVES THE CIRCLE", "Phoenix 42, AM 5796, last documented step: Mont Pelee erases Saint-Pierre (8 May); red mud, 'the harvest begins'; chronoliths end. 1902 + 138 = 2040.", ["Phoenix", "volcano", "red mud", "chronolith"], 1902, f"{CM} M11; {EW} K02; {CH} RED MUD; {TR}"),
 E(1915, "THE FAT GODDESS", "Core Claim 6: Malta's Tarxien repeats Gobekli Tepe's enclosures, relief technique and goddess. Zammit excavates 1915-1919.", ["evidence"], None, f"{EW} E06"),
 E(1919, "19 · 91 · 138 · 831", "Closing sequence: 19 x 91 = 1,729 (Hardy's taxi to Ramanujan); 138 + 831 = 969, Methuselah's years.", ["cipher"], None, f"{EW} K15"),
 E(1922, "THE KING LIST", "Core Claim 13: Enki = Etana = Enoch, who left earth on a winged object leaving seven apkallu. Weld-Blundell Prism names Etana who ascended.", ["evidence", "Enoch"], None, f"{EW} E13"),
 E(1930, "THE CAGED SUN", "Core Claim 17: the Ashanti tale of the bird that brought the sun encodes the vapour-canopy sky; Rattray publishes it.", ["evidence", "sky"], None, f"{EW} E17"),
 E(1932, "THE BENNETT MONOLITH", "Core Claim 9: Tiwanaku repeats the folded-finger pose, T-face and bucket-holding figures. Bennett unearths a 7.3 m monolith.", ["evidence"], None, f"{EW} E09"),
 E(1932, "THE COMPARISON", "Core Claim 11: Hittite eyes, boustrophedon rows and rongorongo signs match Indus seals; de Hevesy's comparison read to the Academie.", ["evidence", "writing"], None, f"{EW} E11"),
 E(1952, "THE TRENCH", "Core Claim 2: Kenyon's Pre-Pottery Neolithic scheme frames all Near-Eastern dating; she digs Jericho 1952-1958.", ["evidence"], None, f"{EW} E02", 1958),
 E(1959, "OPH_CRV", "Engine constant OPH_CRV = 5.08 (curvature) = 3.14 x 1.618, also exactly two inches in cm since the inch was fixed at 25.4 mm.", ["cipher"], None, f"{EW} K09"),
 E(1961, "THE VULTURE SHRINE", "Core Claim 19: the vulture is the phoenix; Neolithic head removal is soul-rescue, not violence. Mellaart's Catalhoyuk vulture murals.", ["evidence", "Phoenix"], None, f"{EW} E19", 1965),
 E(1963, "THE DOOR IN THE WALL", "Core Claim 10: kivas, the sipapu, King Annacus and the underground cities; a wall knocked through opens Derinkuyu.", ["evidence", "underground"], None, f"{EW} E10"),
 E(1972, "THE CROW IN THE SUN", "Core Claim 16: crows and ravens are sun-darkening (three-legged crow, Hou Yi, Amaterasu). Lady Dai's banner shows a crow in the sun.", ["evidence", "sun"], None, f"{EW} E16"),
 E(1995, "THE FIRST SEASON", "Core Claim 1: the sites are underground because of cataclysm, not deliberate burial. Schmidt opens Gobekli Tepe under up to 15 m of fill.", ["evidence", "cataclysm"], None, f"{EW} E01"),
 E(2007, "THE JADE PIG", "Core Claim 7: Lingjiatan and Liangzhu repeat the boar, mouth style and animal poses, 5,000 years younger; an 88 kg jade pig over tomb 07M23.", ["evidence"], None, f"{EW} E07"),
 E(2017, "THE SEALED HOLLOW", "A sealed hollow the length of the gallery, still keeping records we cannot read yet.", ["Great Pyramid"], None, f"{CH}; {TR}"),
 E(2023, "THE SEATED MAN", "Core Claim 5: Karahan Tepe carries an apkallu supporting a winged disc. A 2.3 m seated man and a vulture statue announced September 2023.", ["evidence", "apkallu"], None, f"{EW} E05"),
 E(2023, "THIRTY-TWO YEARS TO THE DAY", "19 January 2023: entering the Great Pyramid, 'thirty-two years to the day'; start of the 1,656-day (138 x 12) span to the 2 August 2027 eclipse.", ["Great Pyramid", "personal"], None, f"{CH}; {TR}; {PAL} line 6"),
 E(2026, "THE CAST", "Manual's worked cast: X1 4 Jul 2026, X2 20 Aug, Y 47 days; operation 9 (X2 + Y x phi) lands on 4 November 2026.", ["cipher", "engine"], None, f"{EW} K10"),
 E(2026, "THE HEPTA-CYCLE", "OPH_HEP = 7.01: seven Metonics (133) fall five short of a Phoenix (138); the missing capstone is the fifth corner.", ["cipher", "Metonic", "Great Pyramid"], None, f"{EW} K11"),
 E(2026, "THE SIX WHEELS", "Resonance Clock: Metonic 19, Phoenix 138, NER 600, Nemesis 792, baktun, sar; 19 & 138 mesh at 2,622, 138 & 600 at 13,800, 138 & 792 at 18,216.", ["cipher", "Phoenix", "Nemesis"], None, f"{EW} K17"),
 E(2026, "TODAY HAS NINETEEN NAMES", "26 September 2026 in nineteen calendars, including 15 Tishri 5787, Long Count 13.0.13.17.7, and 5920 AM by Chronicon.", ["cipher", "calendar"], None, f"{EW} K19"),
]

def W(name, era, year, testimony, refs, source):
    assert len(testimony) <= 200, (name, len(testimony))
    return {"name": name, "era": era, "year": year, "testimony": testimony, "eventRefs": refs, "source": source}

witnesses = [
 W("Natori", "Narrator/walker in the films (co-author credit: Natori Saira Evren)", None, "Walks every station and speaks its date; on 2040 says 'This is the one I haven't seen.'", ["THE GREAT FLOOD", "RED MUD / SHADOW LEAVES THE CIRCLE", "THERA"], f"{CM}; {EW} (natori lines); {TR}"),
 W("Rogue", "Narrator/walker in the films (Bradley Rogue)", None, "Second voice at each station; answers on 2040 'I have.' and is told 'Someone watched. You.' at Thera.", ["THERA", "THE MEDO-LYDIAN DARK"], f"{CM}; {EW} (rogue lines); {TR}"),
 W("The Chronologist (Codex)", "Character in the Phoenix CODEX", None, "Gives the margin for the next fire: as early as 2039, as late as 2046 for the worst of it (projection, see projections 2039/2040/2046).", [], f"{CM} M12"),
 W("Bradley Rogue (addressed as 'you')", "Author; Egypt trip", 2023, "Entered the Great Pyramid the morning of 19 January 2023; returning under the 2 August 2027 Luxor eclipse, 1,656 days later.", ["THIRTY-TWO YEARS TO THE DAY"], f"{PAL} line 6"),
 W("Jason Breshears", "Archaix / Chronicon author", None, "His Chronicon and charts supply the chronology (5239 BC count, 3895 BC Year One, Phoenix 138, Nemesis 792); 'Jason's charts call it worldwide' (1963 BC).", ["THE GROUND REMEMBERS", "YEAR ONE"], f"{RD}; {CM} M01-M02, M11; {TR}"),
 W("Thales", "Ancient (Herodotus 1.74)", None, "Foretold the eclipse that stopped the Medo-Lydian battle on the Halys; the film says he did not predict it, he remembered.", ["THE MEDO-LYDIAN DARK"], f"{EW} F04; {CM} M10; {TR}"),
 W("Herodotus", "Ancient (Histories)", None, "Records day becoming night mid-battle and both sides making peace (1.74); records the phoenix returning to Heliopolis every 500 years (2.73).", ["THE MEDO-LYDIAN DARK", "THE BENNU"], f"{CM} M10; {EW} F04, E14"),
 W("Tacitus", "Ancient (Annals 6.28)", 34, "Reports a phoenix seen in Egypt in 34 AD and discusses a cycle of 1,461 years.", ["THE BENNU"], f"{EW} E14"),
 W("Josephus", "Ancient (Antiquities 1.3.9)", 93, "Says the patriarchs lived six hundred years because 'the great year is completed in that interval'.", ["THE GREAT YEAR", "THE FIRST FIRE / THE GREAT YEAR BEGINS"], f"{EW} K05, C01"),
 W("Meton of Athens", "Ancient Athens", -432, "Set up a sun-tracker on the Pnyx and announced the nineteen-year cycle: 19 years hold 235 moons.", ["NINETEEN YEARS, TWO HUNDRED THIRTY-FIVE MOONS"], f"{EW} K01"),
 W("Varro", "Ancient (quoted by Censorinus)", None, "Dates the flood of Ogyges to about 1600 BC.", ["THE FLOOD OF OGYGES"], f"{EW} F02; {CM} M09"),
 W("Julius Africanus", "Ancient chronographer", None, "Dates the flood of Ogyges c. 1796 BC.", ["THE FLOOD OF OGYGES"], f"{CM} M09 (check)"),
 W("Censorinus", "Ancient (De Die Natali 21)", 238, "Records that a new Sothic period began in 139 AD when Sirius rose with the sun on 1 Thoth; quotes Varro on Ogyges.", ["THE SOTHIC RETURN", "THE FLOOD OF OGYGES"], f"{EW} K14, F02"),
 W("Plato", "Ancient (Timaeus 25c-d)", None, "Has Atlantis sink in a single day and night.", ["THE AXIS"], f"{EW} F03"),
 W("Xenophon", "Ancient (Anabasis 4.5.25)", -401, "Described Anatolian houses dug underground.", ["THE DOOR IN THE WALL"], f"{EW} E10"),
 W("Berossus", "Ancient (via Syncellus)", None, "Gives the ten kings before the Flood 120 sars, 432,000 years.", ["THE ŠAR"], f"{EW} K06"),
 W("Manetho", "Ancient (via Syncellus)", None, "His 'Old Chronicle' spans 36,525 years, twenty-five Sothic cycles of 1,461.", ["THE BLACK AGE"], f"{EW} C11"),
 W("Aryabhata", "Ancient Indian astronomer", None, "His reckoning puts the Kali Yuga epoch at 17/18 February 3102 BC, ten years after the Long Count zero.", ["THE BLACK AGE"], f"{EW} C11"),
 W("Enoch", "Antediluvian (Jubilees 4:17; 1 Enoch 72-82)", None, "First to write down the signs of heaven by the order of their months; a 364-day year. Chronicon makes him a king whose 3rd year is a Phoenix pass.", ["ENOCH'S THIRD YEAR", "THE KING LIST"], f"{EW} C08, E13"),
 W("Khufu (per the stela)", "Old Kingdom Egypt", -2560, "The stela says Khufu found the monuments already there, repairing the Sphinx, not carving it.", ["KHUFU FOUND THEM"], f"{CH}; {TR}"),
 W("James Ussher", "Annales Veteris Testamenti (1650)", 1650, "Put creation at 4004 BC, which Chronicon calls 109 years off.", ["THE CAPTURE OF LUNA", "YEAR ONE"], f"{EW} C03, C04; {CM} M03"),
 W("Klaus Schmidt", "German Archaeological Institute", 1995, "Recognised the T-pillars in 1994 and opened excavation of Gobekli Tepe in 1995; enclosures under up to 15 m of fill.", ["THE FIRST SEASON"], f"{EW} E01"),
 W("Lee Clare", "German Archaeological Institute", 2018, "With colleagues, since 2018 questions the deliberate-backfill reading of Gobekli Tepe, proposing slope-slide and natural infill.", ["THE FIRST SEASON"], f"{EW} E01"),
 W("Kathleen Kenyon", "Archaeologist, Jericho", 1952, "Dug Tell es-Sultan 1952-1958 and defined the Pre-Pottery Neolithic A and B phases.", ["THE TRENCH"], f"{EW} E02"),
 W("Brother Eugène Eyraud", "Missionary, Rapa Nui", 1864, "His December 1864 letter is the first report of the rongorongo tablets.", ["THE TABLETS"], f"{EW} E04"),
 W("Necmi Karul", "Archaeologist, Karahan Tepe", 2023, "Leads excavation since 2019; team announced a 2.3 m seated man and life-size vulture statue in September 2023.", ["THE SEATED MAN"], f"{EW} E05"),
 W("Themistocles Zammit", "Archaeologist, Malta", 1915, "Excavated the Tarxien temples 1915-1919 after farmers struck the stones in 1913.", ["THE FAT GODDESS"], f"{EW} E06"),
 W("Jacob Roggeveen", "Dutch navigator", 1722, "Sighted Rapa Nui on Easter Sunday, 5 April 1722, a hill full of half-cut giants.", ["THE UNFINISHED"], f"{EW} E08"),
 W("Wendell C. Bennett", "Archaeologist, Tiwanaku", 1932, "Unearthed the 7.3 m monolith holding a kero beaker and snuff tablet in the semi-subterranean temple.", ["THE BENNETT MONOLITH"], f"{EW} E09"),
 W("Guillaume de Hevesy", "Scholar, Paris", 1932, "Compared rongorongo signs with Indus Valley seal signs; read to the Academie by Paul Pelliot; later rejected but on record.", ["THE COMPARISON"], f"{EW} E11"),
 W("Paul Pelliot", "Scholar, Paris", 1932, "Read de Hevesy's rongorongo-Indus paper to the Academie des Inscriptions in September 1932.", ["THE COMPARISON"], f"{EW} E11"),
 W("Austen Henry Layard", "Excavator, Nimrud", 1845, "Began digging Nimrud in November 1845, uncovering apkallu reliefs carrying the bucket and cone.", ["THE BUCKET & THE CONE"], f"{EW} E12"),
 W("Langdon", "Oxford Assyriologist", 1923, "Published the Weld-Blundell Prism naming Etana of Kish, 'who ascended to heaven'.", ["THE KING LIST"], f"{EW} E13"),
 W("R. S. Rattray", "Government anthropologist, Gold Coast", 1930, "Published Akan-Ashanti Folk-Tales with the tale of the bird that brought the sun.", ["THE CAGED SUN"], f"{EW} E17"),
 W("Quibell and Green", "Excavators, Hierakonpolis", 1898, "Found the Scorpion Macehead in the Main Deposit in 1897-98.", ["THE SCORPION KING"], f"{EW} E18"),
 W("James Mellaart", "Excavator, Catalhoyuk", 1961, "Exposed vulture wall paintings over headless figures in Level VII, 1961-65.", ["THE VULTURE SHRINE"], f"{EW} E19"),
 W("Tom Ray", "Nature 337 (1989)", 1989, "Showed Newgrange's roof-box aimed at winter-solstice sunrise as it stood c. 3150 BC.", ["NEWGRANGE"], f"{EW} C09"),
 W("Zecharia Sitchin", "The 12th Planet (1976)", 1976, "Found a cataclysm in Sumerian records that Chronicon matches to the 2653 BC Phoenix pass.", ["THE SUMERIAN CATASTROPHE"], f"{EW} C16"),
 W("Richard Muller (with Davis and Hut)", "Nature 308 (1984); Nemesis (1988)", 1984, "Proposed Nemesis, a dark solar companion, which Chronicon cites by page.", ["SHADOW ENTERS THE CIRCLE / THE DAYSTAR GOES DARK"], f"{EW} C02"),
 W("Flinders Petrie", "Survey of Giza (1883)", 1883, "Measured the slope at 51 deg 52' +/- 2', mean side 9,068.8 in, design height 5,776 in.", ["THE ALTAR IS BEGUN", "THE ALTAR IS FINISHED", "OPH_PI", "OPH_PHI"], f"{EW} C14, C15, K07, K08"),
 W("Charles Piazzi Smyth", "Surveyor of the Great Pyramid", 1865, "Surveyed the pyramid January-April 1865 and argued for a prime meridian through Giza; his school gave ~5,449 in height without apex.", ["THE MERIDIAN WINK", "THE FIRST CYCLE CLOSES"], f"{EW} K16, C07"),
 W("Graham Hancock", "Fingerprints of the Gods (1995)", 1995, "Quotes the pyramid's base perimeter as 3,023.16 feet.", ["THE ALTAR IS FINISHED"], f"{EW} C15"),
 W("G. H. Hardy and Srinivasa Ramanujan", "Putney, 1919", 1919, "Hardy's taxi 1,729 (= 19 x 91), the smallest number that is two sums of two cubes.", ["19 · 91 · 138 · 831"], f"{EW} K15"),
]

def PR(year, label, idx, source, note):
    return {"year": year, "label": label, "cycleIndex": idx, "source": source, "note": note}

projections = [
 PR(2027, "Total solar eclipse over Luxor, 2 August 2027", None, f"{PAL} line 6", "1,656 days (138 x 12) after entering the Great Pyramid on 19 January 2023; 'the third return'. Not a Phoenix year."),
 PR(2039, "Earliest margin for the next fire", None, f"{CM} M12", "The Codex's Chronologist: 'as early as 2039'."),
 PR(2040, "AM 5934 - PHOENIX 43 · 138 × 43 - THE ONE SHE HASN'T SEEN / FIRE AGAIN", 43, f"{CH}; {CM} M12; {EW} K02, K18; {CX} line 1140-1144; {TR}", "1902 + 138. Site countdown targets 2040-05-16T00:00:00Z; film transcript says 'May 17th, 2040'. Pyramid chyron for 2040: IT DOESN'T EXPLAIN IT."),
 PR(2046, "Latest margin / Long Count closure", None, f"{CM} M12; {EW} C10, K18", "'as late as 2046 for the worst of it'; Chronicon's count-closure year for the Long Count read in days."),
 PR(2106, "AM 6000 - THE CAPSTONE", None, f"{CH}; {EW} K18, K04, C01, C04; {CM} M01; {TR}", "6000 AM by AD = AM - 3894; 7,344 years from 5239 BC; Nemesis 792 loop from 3439 BC lands here; 'Year one. Again.' Not a 138-multiple."),
 PR(2178, "2040 + 138 - Sky Dragon endpoint", 44, f"{EW} K18", "PSYFR page's Sky Dragon endpoint; cycleIndex 44 is implied by 2040 + 138, not stated as 'Phoenix 44'."),
]

openq = [
 "codex/PhoenixCODEX138.txt (the named 'main source', 65 KB) is not working notes: it is the HTML of the 'Bradley Rogue Ventures' portfolio page. Its only cycle data is the Phoenix countdown to 2040-05-16. README calls it 'working notes', so the wrong file may be checked in. Nearly all data here comes from the two stations.json files and films/data chyrons/transcripts.",
 "The year-conversion rule changes between sources, giving off-by-one years. Chyrons give Phoenix 4/5/6/9/11 as 3344/3206/3068/2654/2378 BC; the station sheets give 3343/3205/3067/2653/2377 BC (3895 - AM). Phoenix 1 (3757) and 12+ BC match.",
 "On the AD side, chyrons for Phoenix 29-41 equal AM - 3895 (107, 245, 383, 521 ... 1763). The stated rule AD = AM - 3894 (which 1902/2040/2106 follow) would give 108, 246, 384, 522 ... 1764. Station K03 gives 384 AD for AM 4278, but the chyron says 383.",
 "4309 BC is called 'Phoenix Year 1' in C02, but C05 calls 3757 BC 'the first Phoenix' and chyrons number Phoenix 1 = AM 138 = 3757 BC.",
 "2815 BC (pyramid finished) is 1080 AM in C15 but AM 1081 in the chyrons ('OFF-CYCLE').",
 "Phoenix 2040 date: the site countdown targets 2040-05-16, but the film transcript says 'May 17th, 2040'.",
 "The Medo-Lydian eclipse: the chart says 583 BC, while the station notes record 585 BC astronomically. The sources call this the book rounding. Ogyges is 1687 BC; the M09 caption reads 1688.",
 "C10 equates Chronicon's 3113 BCE with astronomical year -3113 (= 3114 BC). That suggests at least some Chronicon BCE labels may be astronomical. This file stores all BC labels as -N with no year zero.",
 "Transcripts are auto-generated and garbled ('Fails' = Thales?, 'Pilea erases sampier', 'hikesos', 'Kadath', 'Acton', 'Plagefolos', 'Justiny and Sun', 'Harajan', 'A lesion'). Summaries avoid relying on the garbled words; the 245 AD 'plague' tag rests on 'Plagefolos'.",
 "Nibiru appears only in the portfolio page's word-highlighter, never with a date, so no event is tagged Nibiru.",
 "Witness scope: people quoted in the 'anchor'/'claim' text are included. Names that appear only as bibliography in 'check' fields (e.g. Hodder, Lehner, Kitchen, Jordan, Nissen) are excluded. The film's unnamed 'Greek' (450 BC) and the 1881 'He measures' figure are left unnamed.",
 "The station 'check' fields contain mainstream counterpoints (e.g. no global flood layer, dates of Gobekli/Stonehenge). Per instructions these are not used to correct the framework's dates.",
 "Some station years are nominal display years for undated items (e.g. K11 2026.5, K17 2026.7, K19 2026.74, E11 1932.5). They are rounded down to integers here.",
]

data = {"cycle": cycle, "phoenixDates": phoenix, "events": events, "witnesses": witnesses, "projections": projections, "openQuestions": openq}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print({k: len(v) for k, v in data.items() if isinstance(v, list)})
