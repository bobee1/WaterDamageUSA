"""State hub pages for DryFlare.

Combines three inputs into one page per state (and DC) at /locations/<state>/:
  research/06-state-data.json   Census ACS housing data, top places, FEMA declarations
  src/states/meta.json          names, slugs, neighbors, insurance regulator, contractor board, mold licensing
  src/states/content/<AB>.json  hand-written copy: lead, risks, why, problems, tips, insurance note, FAQ
Templates below only stitch the facts together; every page's narrative comes from its own content file.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "research" / "06-state-data.json").read_text())
META = json.loads((ROOT / "src" / "states" / "meta.json").read_text())
CONTENT_DIR = ROOT / "src" / "states" / "content"

WIKI = {"GA": "Georgia_(U.S._state)", "WA": "Washington_(state)", "NY": "New_York_(state)", "DC": "Washington,_D.C."}

IMAGES = {
    "storm": ("/img/storm-damaged-roof-and-window-800.webp", 800, 1200, True),
    "flood": ("/img/flooded-neighborhood-flood-barrier-800.webp", 800, 534, False),
    "floodroom": ("/img/flooded-room-standing-water-800.webp", 800, 1203, True),
    "floodyard": ("/img/flooded-home-yard-after-heavy-rain-800.webp", 800, 534, False),
    "stairs": ("/img/floodwater-inside-building-stairs-800.webp", 800, 1066, True),
    "pipe": ("/img/leaking-pipe-dripping-water-800.webp", 800, 1200, True),
    "ceiling": ("/img/collapsed-ceiling-after-water-leak-800.webp", 800, 1422, True),
    "mold": ("/img/mold-spots-on-wall-after-leak-800.webp", 800, 534, False),
    "drywall": ("/img/drywall-repair-after-water-damage-800.webp", 800, 1200, True),
    "commercial": ("/img/commercial-office-floor-800.webp", 800, 534, False),
}

TYPE_WORDS = {"Severe Storm": "severe storms", "Hurricane": "hurricanes", "Flood": "floods", "Tornado": "tornadoes",
              "Severe Ice Storm": "ice storms", "Snowstorm": "snowstorms", "Winter Storm": "winter storms",
              "Coastal Storm": "coastal storms", "Tropical Storm": "tropical storms", "Mud/Landslide": "landslides",
              "Dam/Levee Break": "dam or levee breaks", "Typhoon": "typhoons"}


def pick(ab, options, salt=""):
    """Deterministic choice so each state keeps the same wording between builds."""
    h = int(hashlib.md5((ab + salt).encode()).hexdigest(), 16)
    return options[h % len(options)]


def join_list(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def fmt(n):
    return f"{n:,}"


def state_path(ab):
    return f"/locations/{META[ab]['slug']}/"


def link(ab, text=None):
    return f'<a href="{state_path(ab)}">{text or META[ab]["name"]}</a>'


def the(ab):
    return "the District of Columbia" if ab == "DC" else META[ab]["name"]


def load_content(ab):
    f = CONTENT_DIR / f"{ab}.json"
    return json.loads(f.read_text()) if f.exists() else None


def glance_table(ab):
    pop, med, own, pre80, pre40, mobile, units = DATA["acs"][ab]
    total, water, types, recent = DATA["fema"][ab]
    top = sorted(types.items(), key=lambda kv: -kv[1])[:2]
    top_txt = join_list(f"{TYPE_WORDS.get(k, k.lower())} ({v})" for k, v in top)
    rec = "; ".join(f"{name} ({yr})" for yr, name in recent)
    rows = [
        ("Population", fmt(pop)),
        ("Housing units", fmt(units)),
        ("Median year homes were built", str(med)),
        ("Homes built before 1980", f"{pre80}%"),
        ("Homes built before 1940", f"{pre40}%"),
        ("Owner-occupied homes", f"{own}%"),
        ("Mobile homes", f"{mobile}% of housing units"),
        ("FEMA major disasters since 2000", f"{total} in all, {water} from storms, floods and other water events"),
        ("Most frequent water-related types", top_txt),
        ("Latest water-related declarations", rec),
    ]
    trs = "".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in rows)
    return f'<div class="table-scroll"><table class="facts"><tbody>{trs}</tbody></table></div>'


def housing_sentence(ab):
    pop, med, own, pre80, pre40, mobile, units = DATA["acs"][ab]
    name = the(ab)
    if pre80 >= 60:
        s = pick(ab, [
            f"{pre80}% of homes in {name} were built before 1980. Old supply lines, cast-iron drains and worn water heaters cause many leaks.",
            f"Older housing is the norm here. {pre80}% of {name} homes went up before 1980, and old pipes and drains cause many calls.",
        ], "h")
    elif pre80 >= 45:
        s = pick(ab, [
            f"About {pre80}% of homes in {name} were built before 1980. Original pipes and roofs matter as much as the weather.",
            f"Roughly half the homes in {name} ({pre80}%) went up before 1980. Many still have their first pipes, drains and roofs.",
        ], "h")
    else:
        s = pick(ab, [
            f"Most homes in {name} are newer, with a median build year of {med}. New homes still leak from supply lines, appliances and storms.",
            f"Homes in {name} skew newer, with a median build year of {med}. Leaks from fittings, washers and water heaters still happen daily.",
        ], "h")
    if mobile >= 10:
        s += f" Mobile homes make up {mobile}% of housing. Their floors soak up water fast."
    return s


def quick_answer(ab, c):
    total, water, types, recent = DATA["fema"][ab]
    name = the(ab)
    lead = pick(ab, [
        f"Water damage restoration in {name} covers water removal, structural drying, mold prevention and repairs.",
        f"In {name}, water damage restoration means getting water out, drying the building and fixing what got wet.",
        f"Water damage restoration in {name} starts with stopping the water, then extraction, drying and repair.",
    ], "q")
    fact = pick(ab, [
        f"FEMA has declared {water} major disasters for storms, floods and similar events here since 2000.",
        f"Since 2000, FEMA has issued {water} major disaster declarations for water-related events in {name}.",
    ], "f")
    return f"{lead} The biggest local risks are {c['risk']}. {fact}"


def insurance_section(ab, c):
    m = META[ab]
    name = the(ab)
    doi, doiu = m["doi"]
    p1 = pick(ab, [
        f'The <a href="{doiu}">{doi}</a> regulates home insurance in {name}. It takes complaints if a claim stalls.',
        f'The <a href="{doiu}">{doi}</a> oversees home insurance in {name}. It can help with claim problems.',
    ], "i") + " " + c["insurance"]
    p2 = pick(ab, [
        f"Most home policies exclude flood. In {name}, flood cover comes from FEMA's flood program (NFIP) or a private insurer. NFIP policies usually take 30 days to start.",
        f"Flood needs its own policy. Owners in {name} can buy one from the NFIP or a private carrier. NFIP cover starts after a 30-day wait.",
        f"Most home policies in {name} leave out rising water. A flood policy from the NFIP or a private insurer fills the gap. NFIP policies have a 30-day wait.",
    ], "fl")
    if c.get("licensing"):
        p3 = c["licensing"]
    elif m.get("contractor"):
        cb, cbu = m["contractor"]
        p3 = pick(ab, [
            f'The <a href="{cbu}">{cb}</a> licenses or registers contractors. Ask for the number and look it up before rebuild work starts.',
            f'For repairs, check the contractor with the <a href="{cbu}">{cb}</a>. It licenses or registers builders in {name}.',
        ], "c")
    else:
        p3 = pick(ab, [
            f"{name} has no statewide general contractor license. Cities and counties set the rules for building work. Plumbers and electricians need their own licenses.",
            f"There is no statewide general contractor license in {name}. Local building offices handle permits. Plumbers and electricians hold trade licenses.",
        ], "c")
    if m.get("mold"):
        ma, mau = m["mold"]
        p3 += f' {name} also licenses mold work through the <a href="{mau}">{ma}</a>. If mold is part of the job, ask for that license too.'
    return f"<p>{p1}</p>\n<p>{p2}</p>\n<p>{p3}</p>"


def faq(ab, c):
    m = META[ab]
    name = the(ab)
    cities = DATA["cities"][ab]
    if ab == "DC":
        cover = ("Yes. DryFlare takes calls from every ward of the District, from Capitol Hill and Georgetown to Anacostia, "
                 "and from nearby Maryland and Virginia suburbs.")
    else:
        cover = (f"Yes. DryFlare takes calls from all of {name}, including {join_list(cities[:5])}. "
                 f"Small towns and rural areas in every county are covered too.")
    flood_a = (f"Usually not. Most home policies in {name} exclude rising water. They often cover sudden leaks, like a burst pipe. "
               f"Flood needs a separate NFIP or private policy. For claim help, contact the {m['doi'][0]}.")
    if c.get("licensing_faq"):
        lic_a = c["licensing_faq"]
    elif m.get("contractor"):
        lic_a = f"Rules depend on the work. Check builders with the {m['contractor'][0]}. Plumbing and electrical work need trade licenses."
    else:
        lic_a = f"{name} has no statewide general contractor license, so local rules apply. Plumbing and electrical work still need licensed trades, and your city may require permits for rebuilds."
    if m.get("mold"):
        lic_a += f" Mold assessment and remediation are licensed separately through the {m['mold'][0]}."
    return [
        {"q": f"Do you cover all of {name}?", "a": cover},
        {"q": f"Does homeowners insurance cover flood damage in {name}?", "a": flood_a},
        {"q": f"Does a water damage company need a license in {name}?", "a": lic_a},
        c["faq"],
    ]


def problems_table(c, name):
    rows = "".join(f"<tr><td>{p}</td><td>{w}</td><td>{h}</td></tr>" for p, w, h in c["problems"])
    return ('<div class="table-scroll"><table><thead><tr><th>Problem</th><th>Where it shows up</th>'
            f'<th>What helps</th></tr></thead><tbody>{rows}</tbody></table></div>')


def figure(ab, c):
    src, w, h, portrait = IMAGES[c["image"]]
    cls = ' class="portrait"' if portrait else ""
    return (f'<figure class="figure"><img src="{src}" width="{w}" height="{h}" loading="lazy" decoding="async" '
            f'alt="{c["image_alt"]}"{cls}><figcaption>{c["image_caption"]}</figcaption></figure>')


def nearby(ab):
    pills = "".join(f'<li><a href="{state_path(n)}">Water damage restoration in {the(n)}</a></li>' for n in META[ab]["neighbors"])
    pills += '<li><a href="/locations/">All states</a></li><li><a href="/">DryFlare home</a></li>'
    return f'<ul class="pills">{pills}</ul>'


def state_page(ab):
    c = load_content(ab)
    if not c:
        return None
    m = META[ab]
    name = the(ab)
    short = m["name"] if ab != "DC" else "Washington, DC"
    cities = DATA["cities"][ab]
    disp = "Washington, DC" if ab == "DC" else m["name"]
    h1 = f"Water Damage Restoration in {disp}"
    title = f"Water Damage Restoration in {disp} | DryFlare"
    if len(title) > 60:
        title = f"Water Damage Restoration {disp} | DryFlare"
    desc = f"Water damage restoration in {disp}: {c['risk_short']}. Water removal, drying, mold and repairs. Call 1-800-555-0199."
    if len(desc) > 155:
        desc = f"Water damage restoration in {disp}: {c['risk_short']}. Call 1-800-555-0199."
    tips_h = pick(ab, [f"Tips for {short} homeowners", f"Tips for property owners in {short}", f"Practical tips for {short} homes"], "t")
    cta1 = pick(ab, [f"Water inside a {short} home or business? Call DryFlare {{{{availability}}}}.",
                     f"Need water out fast in {short}? Call DryFlare at {{{{phone}}}}."], "cta")
    cta2 = f"Call DryFlare for water damage help anywhere in {short}: {{{{phone}}}}."
    areas_h = f"Areas served in {short}" if ab != "DC" else "Neighborhoods served in Washington, DC"
    nb = [link(n, the(n)) for n in m["neighbors"]]
    nb_line = pick(ab, [f" Calls from neighboring {join_list(nb)} are covered too.",
                        f" DryFlare also helps owners next door in {join_list(nb)}.",
                        f" Water damage help is also available across the line in {join_list(nb)}."], "nb")
    if ab == "DC":
        areas_p = c["areas"] + nb_line
    else:
        import metros as _M
        mm = _M.metros_in_state(ab)
        metro_line = (" Local pages: " + join_list([_M.mlink(x) for x in mm]) + ".") if mm else ""
        areas_p = (f"DryFlare handles water damage calls across {name}. The largest communities are "
                   f"{join_list(cities)}. " + c.get("areas", "") + metro_line + nb_line)
    body = f"""<p class="quick"><strong>Quick answer:</strong> {quick_answer(ab, c)}</p>

<h2>{short} water damage at a glance</h2>
{glance_table(ab)}
<p class="small-note">{short} figures: Census ACS 2020–2024 estimates and FEMA declarations from 2000 to November 2026.</p>
<p>{housing_sentence(ab)}</p>

<h2>Why water damage in {short} is different</h2>
{''.join(f'<p>{p}</p>' for p in c['why'])}
{figure(ab, c)}

<h2>Common water damage problems in {short}</h2>
{problems_table(c, name)}
{{{{cta:{cta1}}}}}

<h2>{tips_h}</h2>
<ul>{''.join(f'<li>{t}</li>' for t in c['tips'])}</ul>

<h2>Insurance and licensing in {short}</h2>
{insurance_section(ab, c)}
{{{{cta:{cta2}}}}}

<h2>{areas_h}</h2>
<p>{areas_p}</p>

{{{{faq}}}}

<h2>Water damage restoration services in {short}</h2>
{{{{services_grid}}}}

<h2>Water damage help in nearby states</h2>
{nearby(ab)}

{{{{sources}}}}
"""
    wiki = "https://en.wikipedia.org/wiki/" + WIKI.get(ab, m["name"].replace(" ", "_"))
    sources = [
        ["FEMA: Disaster declarations", "https://www.fema.gov/disaster/declarations"],
        ["U.S. Census Bureau: American Community Survey", "https://www.census.gov/programs-surveys/acs"],
        [m["doi"][0], m["doi"][1]],
        ["FloodSmart (NFIP): Flood insurance basics", "https://www.floodsmart.gov/"],
    ]
    if m.get("contractor"):
        sources.append([m["contractor"][0], m["contractor"][1]])
    if m.get("mold"):
        sources.append([m["mold"][0], m["mold"][1]])
    sources += c.get("sources", [])
    return {
        "path": state_path(ab), "type": "state", "parents": [["Locations", "/locations/"]],
        "title": title, "description": desc, "h1": h1, "crumb": disp, "priority": "0.8",
        "lead": c["lead"],
        "chips": [f"All of {short}" if ab != "DC" else "Every DC ward", "Homes, rentals & businesses", "24/7 water damage calls"],
        "service": {"name": f"Water damage restoration in {disp}", "serviceType": "Water damage restoration",
                    "areaServed": {"@type": "State" if ab != "DC" else "City", "name": disp, "sameAs": wiki}},
        "about": [[disp, wiki]],
        "mentions": [["Water damage", "https://en.wikipedia.org/wiki/Water_damage"], ["Flood", "https://en.wikipedia.org/wiki/Flood"]],
        "faq_title": f"Water damage questions in {short}",
        "faq": faq(ab, c), "sources": sources, "reviewed": "November 19, 2026",
        "body": body, "source": f"src/states/content/{ab}.json", "state": ab,
    }


def all_state_pages():
    return [p for p in (state_page(ab) for ab in sorted(META, key=lambda a: META[a]["name"])) if p]


def states_grid():
    """Cards for the locations hub, grouped by Census region."""
    regions = {
        "Northeast": ["CT", "ME", "MA", "NH", "NJ", "NY", "PA", "RI", "VT"],
        "Midwest": ["IL", "IN", "IA", "KS", "MI", "MN", "MO", "NE", "ND", "OH", "SD", "WI"],
        "South": ["AL", "AR", "DE", "DC", "FL", "GA", "KY", "LA", "MD", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "WV"],
        "West": ["AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NV", "NM", "OR", "UT", "WA", "WY"],
    }
    out = []
    for reg, abs_ in regions.items():
        cards = "".join(
            f'<li><a class="state-card" href="{state_path(a)}"><span class="state-name">{"Washington, DC" if a == "DC" else META[a]["name"]}</span>'
            f'<span class="state-cities">{", ".join(DATA["cities"][a][:3]) if a != "DC" else "All eight wards"}</span></a></li>'
            for a in sorted(abs_, key=lambda x: META[x]["name"]))
        out.append(f'<h3>{reg}</h3><ul class="state-grid">{cards}</ul>')
    return "\n".join(out)


def state_pills():
    pills = "".join(f'<li><a href="{state_path(a)}">{"Washington, DC" if a == "DC" else META[a]["name"]}</a></li>'
                    for a in sorted(META, key=lambda x: META[x]["name"]))
    return f'<ul class="pills pills-sm">{pills}</ul>'
