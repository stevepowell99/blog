#!/usr/bin/env python3
"""Build the public projects-and-clients page for pogol.net (Quartz).

Reads the three canonical project lists held in the JobCat repo and produces a
single grouped, searchable Quartz markdown page. Regenerate whenever the source
lists change.

Sources (single source of truth, do not invent projects):
  - steve_powell_projects.csv   Steve's personal / pre-2019 consultancy record
  - causal_map_projects.csv     Causal Map Ltd company projects (2019 on)
  - promenteprojectsSteve.xlsx  proMENTE-era work before Causal Map

The source directory defaults to the JobCat project_lists folder but can be
overridden with --source-dir (or the JOBCAT_PROJECT_LISTS env var) so the script
is not hard-tied to one machine.

Output: content/projects.md (published; draft:false). It is a public page at
pogol.net/projects.

Usage:
  python scripts/build_project_list.py
  python scripts/build_project_list.py --source-dir "D:/path/to/project_lists"
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl")

DEFAULT_SOURCE_DIR = os.environ.get(
    "JOBCAT_PROJECT_LISTS",
    r"C:\Users\Zoom\My Drive (hello@causalmap.app)\Causal Map"
    r"\20-29 Platforms and Documentation\20 all platforms\JobCat\project_lists",
)

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "content" / "projects.md"

# --- Source bucket labels -------------------------------------------------
BUCKET_PROMENTE = "proMENTE"
BUCKET_INDEP = "Independent consultancy"
BUCKET_CM = "Causal Map Ltd"

# --- Client canonicalisation ---------------------------------------------
# Map raw client-name variants to one canonical, acronyms spelled out except
# household names and names that are just names (PAX, SoCha, proMENTE, BBC...).
# Joint clients ("A / B") are split, each part mapped, then rejoined.

CANON = {
    # Red Cross / Red Crescent family
    "ifrc": "International Federation of Red Cross and Red Crescent Societies",
    "ifrc east africa": "International Federation of Red Cross and Red Crescent Societies",
    "ifrc, geneva": "International Federation of Red Cross and Red Crescent Societies",
    "icrc": "International Committee of the Red Cross",
    "international committee for the red cross": "International Committee of the Red Cross",
    "international committee for the": "International Committee of the Red Cross",
    "arc": "American Red Cross",
    "arc, s & se asia": "American Red Cross",
    # UN family
    "unicef": "United Nations Children's Fund",
    "unicef b&h": "United Nations Children's Fund",
    "unicef innocenti": "UNICEF Innocenti",
    "unicef office of research": "UNICEF Innocenti",
    "un women": "UN Women",
    "unv": "United Nations Volunteers",
    "united nations volunteers (unv)": "United Nations Volunteers",
    "united nations volunteers": "United Nations Volunteers",
    "unep": "United Nations Environment Programme",
    "undp chile": "United Nations Development Programme Chile",
    # Governance / rights
    "ndi": "National Democratic Institute",
    "icmp": "International Commission on Missing Persons",
    "international commission for missing persons": "International Commission on Missing Persons",
    "international commission for mis": "International Commission on Missing Persons",
    "international commission on missing persons": "International Commission on Missing Persons",
    "osce mission": "Organization for Security and Co-operation in Europe",
    "osce mission in bosnia and herze": "Organization for Security and Co-operation in Europe",
    "osce mission in bosnia and herzegovina": "Organization for Security and Co-operation in Europe",
    # Open Society family
    "osi": "Open Society Foundations",
    "open society institute": "Open Society Foundations",
    "open society fund bosnia": "Open Society Foundations",
    "open society foundations": "Open Society Foundations",
    "open society foundations - educa": "Open Society Foundations",
    "open society foundations - education support programme": "Open Society Foundations",
    # Catholic Relief Services family
    "crs": "Catholic Relief Services",
    "crs b&h": "Catholic Relief Services",
    "crs serbia": "Catholic Relief Services",
    "catholic relief services (crs)": "Catholic Relief Services",
    "catholic relief services (crs) b&h": "Catholic Relief Services",
    "catholic relief services (crs) b": "Catholic Relief Services",
    # Save the Children family
    "save the children": "Save the Children",
    "save the children uk": "Save the Children",
    "save the children norway": "Save the Children",
    "save the children norway and sav": "Save the Children",
    "save the children zimbabwe": "Save the Children",
    # German development agency
    "giz": "Deutsche Gesellschaft fur Internationale Zusammenarbeit (GIZ)",
    "gtz": "Deutsche Gesellschaft fur Internationale Zusammenarbeit (GIZ)",
    "deutsche gesellschaft fur internationale zusammenarbeit": "Deutsche Gesellschaft fur Internationale Zusammenarbeit (GIZ)",
    "deutsche gesellschaft für internationale zusammenarbeit": "Deutsche Gesellschaft fur Internationale Zusammenarbeit (GIZ)",
    # Bilateral donors
    "sida": "Swedish International Development Cooperation Agency (Sida)",
    "usaid": "United States Agency for International Development",
    "fco": "UK Foreign, Commonwealth and Development Office",
    "grant from uk fco": "UK Foreign, Commonwealth and Development Office",
    "uk fco": "UK Foreign, Commonwealth and Development Office",
    "grant from eu-cards": "EU CARDS programme",
    # Conservation / agriculture
    "iucn": "International Union for Conservation of Nature",
    "ifad": "International Fund for Agricultural Development",
    # NGO training
    "intrac": "International NGO Training and Research Centre",
    "opm": "Oxford Policy Management",
    # Universities
    "university of bath": "University of Bath",
    "university of bath (sps)": "University of Bath",
    "university of bath (ipr)": "University of Bath",
    "the universities of bath": "University of Bath",
    "universities of bath": "University of Bath",
    "university of munich": "University of Munich (LMU)",
    "lmu munich": "University of Munich (LMU)",
    "london school of economics": "London School of Economics",
    "kings college": "King's College London",
    "cardiff": "Cardiff University",
    "notre dame": "University of Notre Dame",
    # Balkans NGOs
    "mozaik community development": "Mozaik Foundation",
    "fondacija za razvoj zajednica \"mozaik\"": "Mozaik Foundation",
    "fondacija za razvoj zajednica \"m": "Mozaik Foundation",
    "seeyn": "South-East European Youth Network",
    "south-east european youth network (seeyn)": "South-East European Youth Network",
    "south-east european youth networ": "South-East European Youth Network",
    "tpo": "Transcultural Psychosocial Organisation (TPO)",
    "transkulturna psihosocijalna obr": "Transcultural Psychosocial Organisation (TPO)",
    "rgdts": "Roma-Gadje Dialogue Through Service",
    "roma-gadje dialogue through serv": "Roma-Gadje Dialogue Through Service",
    "nepc": "Network of Education Policy Centres",
    "network of education policy cent": "Network of Education Policy Centres",
    "network of education policy centres (nepc)": "Network of Education Policy Centres",
    "bihpep": "BIH Pension and Employment Project (BIHPEP)",
    "avso": "Association of Voluntary Service Organisations (AVSO)",
    "unv/see": "United Nations Volunteers",
    # Firms / partners kept close to source
    "tear fund": "Tearfund",
    "tearfund": "Tearfund",
    "socha llc": "SoCha",
    "60 decibels": "60 Decibels",
    "expertise france": "Expertise France",
    "bsdr": "Bath Social Development Research",
    "bath sdr": "Bath Social Development Research",
    "sgain/bathsdr": "Bath Social Development Research",
    "church of jesus christ": "Church of Jesus Christ",
    "agency for clinical innovation": "Agency for Clinical Innovation",
    "agency for clinical innovation (20": "Agency for Clinical Innovation",
    "chartered management institute": "Chartered Management Institute",
    "the chartered management institute": "Chartered Management Institute",
    "cmi": "Chartered Management Institute",
    "abt associates": "Abt Global",
    "world vision russian federation": "World Vision",
    "world vision netherlands": "World Vision",
    "medica zenica": "Medica Zenica",
    "unicef / medica": "United Nations Children's Fund / Medica",
    "handicap international": "Handicap International",
    "council of europe": "Council of Europe",
    "federal employment institute": "Federal Employment Institute, B&H",
    "federal employment institute, bo": "Federal Employment Institute, B&H",
    "federal administration for geode": "Federal Administration for Geodetic and Real Property Affairs (RERP)",
    "federal administration for geodetic and real property affairs  (rerp)": "Federal Administration for Geodetic and Real Property Affairs (RERP)",
    "dogs trust bh": "Dogs Trust",
    "dogs trust": "Dogs Trust",
}

# Household acronyms / names left as-is (never expanded).
KEEP_ASIS = {"bbc", "pax", "socha", "promente", "sage", "aims-einstein", "unesco"}


def _strip_junk(s: str) -> str:
    """Remove extraction artifacts: control/replacement chars, [](url) fragments."""
    s = (s or "").replace("\x9e", "").replace("�", "").replace("\xa0", " ")
    s = LINK_RE.sub(lambda m: m.group(1), s)      # [label](url) -> label
    s = re.sub(r"\[\]\([^)]*\)", "", s)           # []() -> ""
    s = re.sub(r"\[[^\]]*$", "", s)               # dangling "[..." with no close
    return re.sub(r"\s{2,}", " ", s).strip()


def canon_client(raw: str) -> str:
    raw = _strip_junk(raw).strip()
    if not raw:
        return ""
    # a client field that is really a leading date is a mis-parse: drop it
    if re.match(r"^((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?"
                r"(19|20)\d{2}\b", raw, re.I):
        return ""
    # split joint clients on ' / '
    parts = re.split(r"\s*/\s*", raw)
    out = []
    for p in parts:
        p = p.strip().rstrip(".,")
        key = p.lower()
        if key in CANON:
            out.append(CANON[key])
        else:
            out.append(p)
    # dedupe while preserving order
    seen = []
    for o in out:
        if o and o not in seen:
            seen.append(o)
    return " / ".join(seen)


# --- Noise detection ------------------------------------------------------
NOISE_CLIENTS = {
    "", "consultant", "global", "internal", "xy",
    "projects conducted by staff members",
    "mayors for children", "quality & usability of result",
    "grants for conservation, w&c a",
    "impact of academic support",
    "education in bosnia and herzeg",
}
DATE_RE = re.compile(
    r"^\s*((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*)?"
    r"(\d{4}|\d{1,2})",
    re.I,
)
MONTH_ONLY_RE = re.compile(
    r"^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b", re.I
)


def is_noise_client(raw: str) -> bool:
    c = (raw or "").strip().lower().rstrip(".")
    if c in NOISE_CLIENTS:
        return True
    if MONTH_ONLY_RE.match(c):  # "feb 2020", "mar-apr 2017"
        return True
    if re.fullmatch(r"[\d\s\-–—]+", c):  # pure numbers/dashes
        return True
    return False


# --- Title / work cleaning ------------------------------------------------
LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+|//[^)\s]+)\)")
LEADING_DATE_RE = re.compile(
    r"^\s*((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?[\s\-–—]*)?"
    r"\d{4}[a-z\s\-–—]*?(\d{4})?[\.\-–—]\s*",
    re.I,
)


def extract_url(*texts: str) -> str:
    for t in texts:
        if not t:
            continue
        m = re.search(r"https?://[^\s)\]\x9e�]+", t)
        if m:
            url = m.group(0).rstrip(".,;�\x9e")
            # reject obviously truncated fragments
            if len(url) > 15 and " " not in url:
                return url
    return ""


def clean_work(title: str, client_raw: str, location: str) -> str:
    w = _strip_junk(title or "")
    w = re.sub(r"https?://[^\s)\]]+", "", w)      # drop bare URLs from visible text; link is added separately
    w = w.replace("$$", "").replace("–", "-").replace("—", "-").strip()  # house style: no en/em dashes
    # strip leading "Month Year - Month Year." date prefixes
    prev = None
    while prev != w:
        prev = w
        w = LEADING_DATE_RE.sub("", w).strip()
    # strip a leading "Client, Loc." or "Client." prefix
    segs = re.split(r"\.\s+", w, maxsplit=3)
    lead_tokens = set()
    for tok in re.split(r"[,/]", (client_raw or "")):
        lead_tokens.add(tok.strip().lower())
    for tok in re.split(r"[,/]", (location or "")):
        lead_tokens.add(tok.strip().lower())
    lead_tokens.discard("")
    while segs:
        first = segs[0].strip().lower().rstrip(".")
        first_norm = re.sub(r"\s*\([^)]*\)", "", first).strip()
        matched = (
            first in lead_tokens
            or first_norm in lead_tokens
            or any(first.startswith(t) and len(t) > 3 for t in lead_tokens)
            or re.fullmatch(r"[a-z&\s]{1,18}", first) and first in lead_tokens
        )
        # also drop a bare location word
        if matched and len(segs) > 1:
            segs = segs[1:]
        else:
            break
    w = ". ".join(s for s in segs).strip()
    w = re.sub(r"\s{2,}", " ", w).strip(" .;,-–—")
    # tidy quotes
    w = w.replace("“", '"').replace("”", '"').replace("’", "'")
    if w:
        w = w[0].upper() + w[1:]
    return w


# --- Theme assignment -----------------------------------------------------
SECTOR_THEMES = [
    ("Humanitarian and Red Cross", [
        "red cross", "red crescent", "ifrc", "icrc", "american red cross",
        "disaster", "tsunami", "earthquake", "ebola", "cholera", "haiti",
        "resilience", "early warning", "everyone counts", "humanitarian",
        "mine risk", "collective centers", "collective centre", "relief",
        "emergency", "fdrs", "covid",
    ]),
    ("Peacebuilding and governance", [
        "peace", "reconcil", "governance", "democracy", "democratic",
        "political party", "trafficking", "human rights", "justice",
        "missing persons", "missing family", "osce", "civil society",
        "election", "anti-narcotic", "intelligence", "legal", "citizen",
        "ombuds", "activism",
    ]),
    ("Education", [
        "education", "teacher", "school", "student", "careers advice",
        "learning experience", "doctoral", "academic support", "literacy",
        "step-by-step", "teach our children", "higher education",
    ]),
    ("Health and psychosocial", [
        "health", "psychosocial", "ptsd", "hiv", "aids", "trauma",
        "gynaecolog", "gynecolog", "clinical", "mental", "war-trauma",
        "post-traumatic",
    ]),
    ("Conservation and environment", [
        "conservation", "iucn", "nature", "climate", "environment",
        "forest", "wildlife", "biodiversity", "polycrisis",
    ]),
    ("Social and community development", [
        "community development", "community empowerment", "youth", "philanthropy",
        "disabilit", "social capital", "women", "gender", "employment",
        "livelihood", "volunteer", "voluntary service", "giving for change",
        "roma", "poverty",
    ]),
    ("Research and academia", [
        "research", "survey", "study", "follow-up", "meta-analysis",
        "statistical report", "baseline", "feasibility", "validation",
    ]),
]
METHOD_THEMES = [
    ("evaluation", ["evaluat", "meta-evaluation", "review", "assessment", "impact evaluation"]),
    ("causal mapping", ["causal map", "causal pathway", "causal analysis", "causal qda"]),
    ("AI and LLM", ["ai-assist", "ai assist", "ai to", "ai interview", "qualia", " llm", "using ai"]),
    ("training and facilitation", ["training", "trainer", "facilitat", "workshop", "masterclass", "teambuilding", "coaching"]),
    ("survey and statistics", ["survey", "statistic", "questionnaire", "kap", "baseline", "endline", "data analysis", "focus group", "sms"]),
]


def assign_themes(text: str):
    t = text.lower()
    sectors = [name for name, kws in SECTOR_THEMES if any(k in t for k in kws)]
    methods = [name for name, kws in METHOD_THEMES if any(k in t for k in kws)]
    return sectors, methods


# --- Loading --------------------------------------------------------------
class Project:
    __slots__ = ("client", "work", "years", "source", "sectors", "methods", "url")

    def __init__(self, client, work, years, source, sectors, methods, url):
        self.client = client
        self.work = work
        self.years = years
        self.source = source
        self.sectors = sectors
        self.methods = methods
        self.url = url


def year_str(start, end):
    s = (str(start).strip() if start else "").split(".")[0]
    e = (str(end).strip() if end else "").split(".")[0]
    if s and e and e != s:
        return f"{s}-{e}"
    return s or e or ""


def dedupe_key(client, work):
    w = re.sub(r"[^a-z0-9 ]", "", (work or "").lower())
    w = " ".join(w.split()[:6])
    return (client.lower(), w)


def load_steve(path):
    promente, indep = [], []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            typ = row.get("type", "")
            if typ == "CausalMap_recent_contract":
                continue  # handled with the CM bucket
            client_raw = row.get("client", "")
            if is_noise_client(client_raw):
                continue
            client = canon_client(client_raw)
            if not client:
                continue
            work = clean_work(row.get("title", ""), client_raw, row.get("location", ""))
            if len(work) < 4:
                continue
            years = year_str(row.get("start_year"), row.get("end_year"))
            url = extract_url(row.get("urls", ""), row.get("title", ""), row.get("raw_text", ""))
            sectors, methods = assign_themes(f"{client} {work} {row.get('location','')}")
            bucket = BUCKET_PROMENTE if typ == "project" else BUCKET_INDEP
            proj = Project(client, work, years, bucket, sectors, methods, url)
            (promente if typ == "project" else indep).append(proj)
    return promente, indep


def load_promente_xlsx(path):
    out = []
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    if ws is None:
        return out
    for row in list(ws.iter_rows(values_only=True))[1:]:
        year, client_raw, title, location = row[2], row[4], row[5], row[7]
        if is_noise_client(str(client_raw or "")):
            continue
        client = canon_client(str(client_raw or ""))
        if not client:
            continue
        work = clean_work(str(title or ""), str(client_raw or ""), str(location or ""))
        if len(work) < 4:
            continue
        years = year_str(year, None)
        sectors, methods = assign_themes(f"{client} {work} {location or ''}")
        out.append(Project(client, work, years, BUCKET_PROMENTE, sectors, methods, ""))
    return out


def load_cm(path):
    out = []
    seen_clients = set()
    talks = []
    talk_clients = {
        "ees", "aea 2024 (indianapolis): introduct", "causal pathways initiative",
        "uk evaluation society webinars", "uk development studies association",
    }
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            client_raw = (row.get("client") or "").strip()
            title = (row.get("title") or "").strip()
            desc = (row.get("description") or "").strip()
            if not client_raw and not title:
                continue
            low = client_raw.lower()
            if low in ("internal",):
                continue  # in-house R&D, not client work
            work = clean_work(title or desc, client_raw, "")
            if not work:
                work = "Causal mapping"
            years = year_str(row.get("start_year"), row.get("end_year"))
            blob = f"{client_raw} {title} {desc}"
            sectors, methods = assign_themes(blob)
            if "causal mapping" not in methods:
                methods.append("causal mapping")
            if low in talk_clients:
                talks.append(Project(canon_client(client_raw) or client_raw, work, years,
                                     BUCKET_CM, sectors, methods, extract_url(desc, title)))
                continue
            client = canon_client(client_raw)
            if not client:
                continue
            seen_clients.add(client.lower())
            out.append(Project(client, work, years, BUCKET_CM, sectors, methods,
                               extract_url(desc, title, row.get("urls", ""))))
    return out, seen_clients, talks


def load_cm_recent(path, cm_seen):
    """recent-contract client list from steve CSV: add only clients that have
    no titled Causal Map project already."""
    out = []
    added = set()
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("type") != "CausalMap_recent_contract":
                continue
            client_raw = row.get("client", "")
            client = canon_client(client_raw)
            if not client:
                continue
            k = client.lower()
            if k in cm_seen or k in added:
                continue
            added.add(k)
            sectors, methods = assign_themes(client)
            if "causal mapping" not in methods:
                methods.append("causal mapping")
            out.append(Project(client, "Causal mapping", "2020", BUCKET_CM, sectors, methods, ""))
    return out


def dedupe(projects):
    seen = {}
    out = []
    for p in projects:
        k = dedupe_key(p.client, p.work)
        if k in seen:
            # keep the one with a URL / longer work
            prev = seen[k]
            if (len(p.work) > len(prev.work)) or (p.url and not prev.url):
                idx = out.index(prev)
                out[idx] = p
                seen[k] = p
            continue
        seen[k] = p
        out.append(p)
    return out


# Same project worded differently across the CSV and the xlsx: exact-key dedupe
# misses these, so collapse by client plus content-word overlap.
_FUZZY_STOP = set(
    "the a an of for and to in on with by at from into within evaluation "
    "evaluations project projects programme program report review training "
    "external final impact assessment consultant work".split()
)


def _content_tokens(work, client):
    toks = re.findall(r"[a-z0-9]+", (work or "").lower())
    ctoks = set(re.findall(r"[a-z0-9]+", (client or "").lower()))
    return {t for t in toks if len(t) > 2 and t not in _FUZZY_STOP and t not in ctoks}


def _better(a, b):
    """pick the richer of two near-duplicate projects."""
    if (a.url and not b.url):
        return a
    if (b.url and not a.url):
        return b
    return a if len(a.work) >= len(b.work) else b


def fuzzy_dedupe(projects, threshold=0.5):
    kept = []
    tokens = []
    for p in projects:
        pt = _content_tokens(p.work, p.client)
        merged = False
        for i, q in enumerate(kept):
            if q.client.lower() != p.client.lower():
                continue
            qt = tokens[i]
            if not pt or not qt:
                continue
            inter = len(pt & qt)
            union = len(pt | qt)
            smaller = pt if len(pt) <= len(qt) else qt
            subset_dupe = len(smaller) >= 2 and smaller <= (pt | qt) and (pt <= qt or qt <= pt)
            if (union and inter / union >= threshold) or subset_dupe:
                best = _better(p, q)
                kept[i] = best
                tokens[i] = _content_tokens(best.work, best.client)
                merged = True
                break
        if not merged:
            kept.append(p)
            tokens.append(pt)
    return kept


# --- Rendering ------------------------------------------------------------
CM_METHOD_SECTOR = "Causal mapping consultancy"
SECTOR_ORDER = [name for name, _ in SECTOR_THEMES] + [CM_METHOD_SECTOR, "Other work"]


def primary_sector(p):
    if p.sectors:
        return p.sectors[0]
    # cross-sector Causal Map Ltd contracts whose work is causal mapping itself
    if p.source == BUCKET_CM and "causal mapping" in p.methods:
        return CM_METHOD_SECTOR
    return "Other work"


def sort_year_desc(p):
    m = re.search(r"(\d{4})", p.years or "")
    return -(int(m.group(1)) if m else 0)


def esc(s):
    return (s or "").replace("|", "\\|")


def render(all_projects, talks):
    by_sector = defaultdict(list)
    for p in all_projects:
        by_sector[primary_sector(p)].append(p)

    n_projects = len(all_projects)
    n_clients = len({p.client for p in all_projects})

    lines = []
    lines.append("---")
    lines.append("title: Projects and clients")
    lines.append("draft: false")
    lines.append("date: 2026-07-09")
    lines.append("description: >-")
    lines.append("  A browsable list of evaluation and research projects across proMENTE, Steve")
    lines.append("  Powell's independent consultancy and Causal Map Ltd.")
    lines.append("---")
    lines.append("")
    lines.append(
        "<!-- GENERATED FILE. Do not edit by hand. Rebuild with: "
        "python scripts/build_project_list.py\n"
        "     Source of truth (JobCat repo, project_lists/): steve_powell_projects.csv, "
        "causal_map_projects.csv, promenteprojectsSteve.xlsx.\n"
        "     To change a project, edit the source CSV/xlsx in JobCat and re-run the script; "
        "do not edit this page. -->"
    )
    lines.append("")
    lines.append(
        "Over about 30 years I have worked on evaluation and applied social research in "
        "some 35 countries, first with proMENTE social research in Sarajevo, then in my own "
        "independent consultancy, and since 2019 through Causal Map Ltd. This page lists that "
        "work so it can be browsed by theme and searched by client, country or topic. Use the "
        "search box (press the key at the top of the page, or Ctrl+K) to find any client or keyword."
    )
    lines.append("")
    lines.append(
        "Work before 2019, and the IFRC Everyone Counts reports, was carried out by Steve "
        "personally. Projects marked Causal Map Ltd are company contracts from 2019 onward."
    )
    lines.append("")

    for sector in SECTOR_ORDER:
        rows = by_sector.get(sector)
        if not rows:
            continue
        rows.sort(key=sort_year_desc)
        lines.append(f"## {sector}")
        lines.append("")
        lines.append("| Client | Work | Years | Source |")
        lines.append("| --- | --- | --- | --- |")
        for p in rows:
            work = esc(p.work)
            if p.url:
                work = f"[{work}]({p.url})"
            tags = ", ".join(p.methods)
            if tags:
                work = f"{work} <br><small>{esc(tags)}</small>"
            lines.append(f"| {esc(p.client)} | {work} | {p.years} | {p.source} |")
        lines.append("")

    if talks:
        lines.append("## Selected talks, training and conference sessions")
        lines.append("")
        lines.append("| Event | Contribution | Years |")
        lines.append("| --- | --- | --- |")
        for p in sorted(talks, key=sort_year_desc):
            work = esc(p.work)
            if p.url:
                work = f"[{work}]({p.url})"
            lines.append(f"| {esc(p.client)} | {work} | {p.years} |")
        lines.append("")

    return "\n".join(lines) + "\n", n_projects, n_clients, by_sector


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR)
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()

    src = Path(args.source_dir)
    steve_csv = src / "steve_powell_projects.csv"
    cm_csv = src / "causal_map_projects.csv"
    xlsx = src / "promenteprojectsSteve.xlsx"
    for p in (steve_csv, cm_csv, xlsx):
        if not p.exists():
            sys.exit(f"Source file missing: {p}")

    promente_a, indep = load_steve(steve_csv)
    promente_b = load_promente_xlsx(xlsx)
    cm, cm_seen, talks = load_cm(cm_csv)
    cm += load_cm_recent(steve_csv, cm_seen)

    promente = fuzzy_dedupe(dedupe(promente_a + promente_b))
    indep = fuzzy_dedupe(dedupe(indep))
    cm = dedupe(cm)

    all_projects = promente + indep + cm
    text, n_projects, n_clients, by_sector = render(all_projects, talks)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    # summary to stderr
    print(f"Wrote {out}", file=sys.stderr)
    print(f"Projects: {n_projects}  Unique clients: {n_clients}", file=sys.stderr)
    print(f"  proMENTE: {len(promente)}  Independent: {len(indep)}  Causal Map Ltd: {len(cm)}", file=sys.stderr)
    print(f"  Talks: {len(talks)}", file=sys.stderr)
    print("Theme (primary sector) breakdown:", file=sys.stderr)
    for s in SECTOR_ORDER:
        if by_sector.get(s):
            print(f"  {len(by_sector[s]):3d}  {s}", file=sys.stderr)


if __name__ == "__main__":
    main()
