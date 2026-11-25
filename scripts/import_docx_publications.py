"""Import the publication list from the group's Word document into one file per item.

Usage:  python3 scripts/import_docx_publications.py path/to/list.docx
Creates src/content/publications/<year>-<slug>.md. Existing files are left untouched,
so it is safe to re-run after adding new items to the document (needs python-docx).
"""
import os, re, sys, unicodedata
import docx

OUT = os.path.join(os.path.dirname(__file__), "..", "src", "content", "publications")
SECTION_STATUS = {
    "Peer-reviewed published": "published",
    "Under review / Submitted": "submitted",
    "Ready for submission": "ready",
    "In preparation": "in-preparation",
    "Other publications": "published",
}

def slug(s, n=60):
    s = s.replace("ø", "oe").replace("æ", "ae").replace("å", "aa")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n].strip("-")

def q(v):
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'

def parse(text):
    text = re.sub(r"^\d+\.\s+", "", text.strip())
    note = ""
    m = re.search(r"\s*\[([^\]]+)\]\s*$", text)
    if m:
        note, text = m.group(1), text[: m.start()]
    doi = ""
    m = re.search(r"doi:\s*(10\.\S+?)\.?(?=\s|$)", text, re.I)
    if m:
        doi = m.group(1).rstrip(".")
        text = (text[: m.start()] + text[m.end():]).strip()
    m = re.match(r"^(.*?)\s*\((\d{4})\)\.?\s*(.*)$", text)
    if not m:
        return dict(authors="", year="", title=text, rest="", doi=doi, note=note)
    authors, year, rest = m.groups()
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z0-9])", rest, maxsplit=1)
    title = parts[0].rstrip(".")
    rest = parts[1].strip() if len(parts) > 1 else ""
    return dict(authors=authors.strip().rstrip(","), year=year, title=title, rest=rest.rstrip(". "), doi=doi, note=note)

def classify(section, sub, rest, title):
    r = rest.lower()
    award = ""
    m = re.search(r"(best [a-z ]+award)", rest, re.I)
    if m:
        award = m.group(1)
    if section == "Other publications":
        return "popular", "published", rest, award
    if section.startswith("Conference"):
        if "acta ophthalmologica" in r and "(s" in r:
            return "abstract", "published", rest, award
        if "gunderslevholm" in r:
            return "seminar", "published", "Gunderslevholm Research Seminar", award
        typ = "poster" if "poster" in r else "presentation"
        venue = re.sub(r"\.\s*(Poster|Presentation|Best .*|Programme lead.*|Poster & Rapid fire presentation)\.?$", "", rest, flags=re.I).strip(" .")
        return typ, "published", venue, award
    status = SECTION_STATUS.get(section, "published")
    if section.startswith("Under review"):
        status = "in-review" if "under review" in r else "submitted"
    if "lecture notes" in r or "(eds.)" in r:
        return "book-chapter", status, rest, award
    typ = "review" if re.search(r"review|overview|now and beyond|novel approaches|potential|game changers|promising or not|girl power|is fat the future", title, re.I) and status == "published" else "article"
    return typ, status, rest, award

def split_venue(rest):
    # "Acta Ophthalmologica, 103(1), 33–42" -> venue "Acta Ophthalmologica", details "103(1), 33–42"
    rest = re.sub(r"\.?\s*(Submitted|Under review.*|Ready for submission|In preparation|Advance online publication|Epub ahead of print)\.?.*$", "", rest, flags=re.I).strip(" .")
    rest = re.sub(r"^Intended for\s+", "", rest)
    m = re.match(r"^(.*?),\s*(\d.*)$", rest)
    if m and not rest.lower().startswith("in "):
        return m.group(1), m.group(2)
    return rest, ""

FOREVER = re.compile(r"forever|danish eye and vision cohort|high street optician|questionnaire responses|community optometry|glaucoma screening|oct representations|wide-field oct|ai som klinisk|deep learning", re.I)

def main(path):
    d = docx.Document(path)
    section = sub = ""
    made = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if p.style.name == "Heading 1":
            section, sub = t, ""
            continue
        if p.style.name == "Heading 2":
            sub = t
            continue
        if p.style.name != "Reference Entry" or not section:
            continue
        e = parse(t)
        if not e["year"]:
            e["year"] = "2026"
        typ, status, rest, award = classify(section, sub, e["rest"], e["title"])
        if typ in ("article", "review", "book-chapter", "popular"):
            venue, details = split_venue(rest)
        else:
            venue, details = rest, ""
        if "http" in e["title"]:
            continue  # bare links (e.g. LinkedIn posts) are not publications
        projects = ["forever"] if FOREVER.search(t) else []
        name = f"{e['year']}-{slug(e['title'])}.md"
        fp = os.path.join(OUT, name)
        if os.path.exists(fp):
            name = f"{e['year']}-{slug(e['title'], 50)}-{typ}-{slug(venue, 20)}.md"
            fp = os.path.join(OUT, name)
        if os.path.exists(fp):
            continue
        fm = ["---", f"title: {q(e['title'])}", f"authors: {q(e['authors'])}", f"year: {e['year']}",
              f"type: {typ}", f"status: {status}", f"venue: {q(venue)}", f"details: {q(details)}",
              f"doi: {q(e['doi'])}", "url: \"\"", f"award: {q(award.capitalize() if award else '')}",
              f"projects: [{', '.join(projects)}]"]
        if e["note"]:
            fm.append(f"note: {q(e['note'])}")
        fm += ["---", ""]
        open(fp, "w").write("\n".join(fm))
        made += 1
    print(f"created {made} files in {os.path.normpath(OUT)}")

if __name__ == "__main__":
    main(sys.argv[1])
