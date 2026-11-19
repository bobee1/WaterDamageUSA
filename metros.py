"""Metro hub pages: /locations/<state>/<city>/ for the Phase 1 metro list (Build 6).

Inputs:
  research/09-metro-acs.json         Census ACS housing data for each principal city
  src/metros/meta.json               city name, state, county, ZIP codes, neighborhoods, nearby metros, Semrush figures
  src/metros/content/<slug>.json     hand-written copy: lead, risks, why, problems, tips, FAQ, image
"""
import json
from pathlib import Path

import states as S

ROOT = Path(__file__).parent
ACS = json.loads((ROOT / "research" / "09-metro-acs.json").read_text())["places"]
MMETA = json.loads((ROOT / "src" / "metros" / "meta.json").read_text())
CDIR = ROOT / "src" / "metros" / "content"



def mpath(slug):
    m = MMETA[slug]
    return f"/locations/{S.META[m['st']]['slug']}/{m['url']}/"


def mlink(slug, text=None):
    return f'<a href="{mpath(slug)}">{text or MMETA[slug]["city"]}</a>'


def metros_in_state(ab):
    return sorted([k for k, v in MMETA.items() if v["st"] == ab and (CDIR / f"{k}.json").exists()],
                  key=lambda k: MMETA[k]["city"])


def glance(slug):
    m = MMETA[slug]
    pop, units, med, pre80, pre40, own, mobile = ACS[m["acs"]]
    rows = [("Population", S.fmt(pop)), ("Housing units", S.fmt(units)), ("Median year homes were built", str(med)),
            ("Homes built before 1980", f"{pre80}%"), ("Homes built before 1940", f"{pre40}%"),
            ("Owner-occupied homes", f"{own}%"), ("County", m["county"]),
            ("Sample ZIP codes", ", ".join(m["zips"]))]
    trs = "".join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows)
    return f'<div class="table-scroll"><table class="facts"><tbody>{trs}</tbody></table></div>'


def housing_line(slug):
    m = MMETA[slug]
    pop, units, med, pre80, pre40, own, mobile = ACS[m["acs"]]
    c = m["city"]
    if pre40 >= 30:
        return S.pick(slug, [f"{pre40}% of homes in {c} were built before 1940. Old drain lines, plaster walls and stone or brick basements are common.",
                             f"{c} is an old city: {pre40}% of its homes predate 1940, so cast-iron drains and century-old basements show up on many jobs."], "hl")
    if pre80 >= 50:
        return S.pick(slug, [f"About {pre80}% of {c} homes were built before 1980. Original plumbing and aging roofs cause many leaks.",
                             f"More than half of {c}'s housing ({pre80}%) went up before 1980, so many homes still have their first pipes."], "hl")
    return S.pick(slug, [f"Housing in {c} is newer, with a median build year of {med}. Supply lines, water heaters and appliances cause most indoor leaks.",
                         f"With a median build year of {med}, most {c} homes are newer. Failed fittings, washers and AC drains still cause daily calls."], "hl")


def page(slug):
    f = CDIR / f"{slug}.json"
    if not f.exists():
        return None
    c = json.loads(f.read_text())
    m = MMETA[slug]
    st = S.META[m["st"]]
    city, ab = m["city"], m["st"]
    disp = f"{city}, {ab}"
    sp = S.state_path(ab)
    title = f"Water Damage Restoration {city}, {ab} | DryFlare"
    if len(title) > 60:
        title = f"Water Damage Restoration {city} | DryFlare"
    desc = f"Water damage restoration in {disp}: {c['risk_short']}. Water removal, drying, mold and repairs. Call 1-800-555-0199."
    if len(desc) > 155:
        desc = f"Water damage restoration in {disp}: {c['risk_short']}. Call 1-800-555-0199."
    near = [n for n in m["nearby"] if (CDIR / f"{n}.json").exists()]
    nb = S.pick(slug, [f"DryFlare also covers nearby {S.join_list([mlink(n) for n in near])}.",
                       f"Crews also work in {S.join_list([mlink(n) for n in near])}.",
                       f"Help is also available in {S.join_list([mlink(n) for n in near])}."], "nb") if near else ""
    quick = S.pick(slug, [f"Water damage restoration in {disp} means fast water removal, structural drying and repairs.",
                          f"In {city}, water damage restoration covers extraction, drying, mold prevention and rebuild work.",
                          f"Water damage restoration in {city} starts with stopping the water, then drying and repair."], "q")
    quick += f" The main local risks are {c['risk']}. DryFlare covers all of {m['county']}, including ZIP codes {', '.join(m['zips'][:3])}."
    doi, doiu = st["doi"]
    ins = S.pick(slug, [f'Home insurance in {city} is regulated by the <a href="{doiu}">{doi}</a>. ',
                        f'The <a href="{doiu}">{doi}</a> oversees insurance for {city} homeowners. '], "i")
    ins += c.get("insurance", "") + f" See the {S.link(ab, st['name'] if ab != 'DC' else 'Washington, DC')} page for state flood, licensing and claim notes."
    cta1 = S.pick(slug, [f"Water inside a {city} home or business? Call DryFlare {{{{availability}}}}.",
                         f"Need water out fast in {city}? Call DryFlare at {{{{phone}}}}."], "c1")
    tips_h = S.pick(slug, [f"Tips for {city} homeowners", f"Water damage tips for {city} homes", f"How {city} owners can prevent water damage"], "t")
    faq = [
        {"q": f"Do you cover all of {city}?", "a": f"Yes. DryFlare takes calls from across {city} and {m['county']}, including {S.join_list(m['hoods'][:5])}, and ZIP codes such as {', '.join(m['zips'])}."},
        {"q": f"How fast should water damage be dried in {city}?", "a": S.pick(slug, [f"Start within 24 to 48 hours. The EPA says that is the window to dry wet materials before mold grows in a {city} home. {c.get('speed_note', '')}".strip(),
                                                                             f"As soon as possible. For {city} homes, the EPA advice is to dry wet materials within 24 to 48 hours to prevent mold. {c.get('speed_note', '')}".strip()], "fq")},
        {"q": f"Does insurance cover water damage in {city}?", "a": f"For {city} homeowners, sudden events like burst pipes are usually covered. Flood from rising water needs a separate flood policy. For claim problems, contact the {doi}."},
        c["faq"],
    ]
    body = f"""<p class="quick"><strong>Quick answer:</strong> {quick}</p>

<h2>{city} water damage at a glance</h2>
{glance(slug)}
<p class="small-note">{city} housing figures: U.S. Census Bureau ACS 2020–2024 5-year estimates.</p>
<p>{housing_line(slug)}</p>

<h2>Why water damage in {city} is different</h2>
{''.join(f'<p>{p}</p>' for p in c['why'])}
{S.figure(slug, c)}

<h2>Common water damage problems in {city}</h2>
{S.problems_table(c, city)}
{{{{cta:{cta1}}}}}

<h2>{tips_h}</h2>
<ul>{''.join(f'<li>{t}</li>' for t in c['tips'])}</ul>

<h2>Neighborhoods and suburbs served in {city}</h2>
<p>{c['areas']} {nb}</p>

<h2>Insurance and licensing in {city}</h2>
<p>{ins}</p>
{{{{cta:Call DryFlare for water damage help in {city}: {{{{phone}}}}.}}}}

{{{{faq}}}}

<h2>Water damage restoration services in {city}</h2>
{{{{services_grid}}}}

<h2>More water damage help near {city}</h2>
<ul class="pills">{''.join(f'<li><a href="{mpath(n)}">Water damage restoration in {MMETA[n]["city"]}</a></li>' for n in near)}<li><a href="{sp}">All of {st['name'] if ab != 'DC' else 'DC'}</a></li><li><a href="/locations/">All locations</a></li><li><a href="/">DryFlare home</a></li></ul>

{{{{sources}}}}
"""
    wiki = c.get("wiki", "https://en.wikipedia.org/wiki/" + m["wiki"])
    sources = [["U.S. Census Bureau: American Community Survey", "https://www.census.gov/programs-surveys/acs"],
               ["EPA: A Brief Guide to Mold, Moisture and Your Home", "https://www.epa.gov/mold/brief-guide-mold-moisture-and-your-home"],
               [doi, doiu], ["FEMA: Flood insurance", "https://www.fema.gov/flood-insurance"]] + c.get("sources", [])
    return {
        "path": mpath(slug), "type": "city", "parents": [["Locations", "/locations/"], [st["name"], sp]],
        "title": title, "description": desc, "h1": f"Water Damage Restoration in {disp}", "crumb": city, "priority": "0.8",
        "lead": c["lead"], "chips": [m["county"], "Homes, rentals & businesses", "24/7 water damage calls"],
        "service": {"name": f"Water damage restoration in {disp}", "serviceType": "Water damage restoration",
                    "areaServed": {"@type": "City", "name": disp, "sameAs": wiki,
                                   "containedInPlace": {"@type": "AdministrativeArea", "name": m["county"]}}},
        "about": [[disp, wiki]], "mentions": [["Water damage", "https://en.wikipedia.org/wiki/Water_damage"]] + c.get("mentions", []),
        "faq_title": f"Water damage questions in {city}", "faq": faq, "sources": sources, "reviewed": "November 19, 2026",
        "body": body, "source": f"src/metros/content/{slug}.json",
    }


def all_pages():
    return [p for p in (page(s) for s in sorted(MMETA)) if p]
