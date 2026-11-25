# One-off script used to create the first set of people files. Kept for reference.
import os, re, unicodedata
out = os.path.join(os.path.dirname(__file__), "..", "src", "content", "people")
EYE = "https://drug.ku.dk/research-sections/translational-and-clinical-pharmacology/eyetru/"
people = [
 # name, role, category, order, projects, extras
 ("Miriam Kolko", "Professor in Translational Eye Research and Senior Consultant (Glaucoma Specialist). Group leader and FOREVER project lead.", "lead", 1, ["forever"], dict(email="miriamk@sund.ku.dk", orcid="0000-0001-8697-0734", profile_url="https://drug.ku.dk/staff/?pure=en/persons/81581", linkedin="", body="Miriam Kolko leads EyeTRU and Project FOREVER. Her research spans the pathophysiology of glaucoma, ocular surface disease and glaucoma treatment, clinical trials, and large-scale epidemiology. She is a senior consultant and glaucoma specialist at Rigshospitalet.")),
 ("Jens Rovelt", "Senior researcher", "senior", 10, ["forever"], dict(orcid="0000-0002-4114-0267", profile_url=EYE+"?pure=en/persons/246221")),
 ("Christina Eckmann-Hansen", "Researcher", "senior", 11, ["forever"], dict(orcid="0000-0002-0272-2192")),
 ("Josefine Freiberg", "Researcher", "senior", 12, ["forever"], dict(orcid="0000-0003-1520-7226", profile_url=EYE+"?pure=en/persons/464169")),
 ("Marcel Reimann", "PhD fellow (UCPH and DTU)", "phd", 20, ["forever"], dict(orcid="0009-0002-9240-7213", profile_url="https://forskning.ku.dk/soeg/result/?pure=da%2Fpersons%2Fmarcel-reimann(7122495c-5f86-4c8c-9a3e-d8c9837893b9).html")),
 ("Arevak Saruhanian", "PhD fellow", "phd", 20, ["forever"], dict(orcid="0009-0004-0958-2470")),
 ("Hande Coskun", "PhD fellow", "phd", 20, ["forever"], dict()),
 ("Kasper Jørgensen", "PhD fellow (UCPH and DTU)", "phd", 20, ["forever"], dict()),
 ("Alexander von Spreckelsen", "PhD fellow", "phd", 20, [], dict(profile_url="https://research.ku.dk/search/result/?pure=en/persons/533964")),
 ("Mariana Yolotzin Garcia Bermudez", "PhD fellow", "phd", 20, [], dict(profile_url=EYE+"?pure=en/persons/707953")),
 ("Pernille May Hansen", "PhD fellow", "phd", 20, ["forever"], dict(profile_url="https://forskning.ku.dk/soeg/result/?pure=da%2Fpersons%2Fpernille-may-hansen(4499e894-2715-48b4-a91a-e336a5a1ff5f).html")),
 ("Sarkis Saruhanian", "PhD fellow", "phd", 20, [], dict(profile_url="https://forskning.ku.dk/soeg/result/?pure=da%2Fpersons%2Fsarkis-saruhanian(2c805ac6-ddb1-463a-af3d-8f008ae3f67d).html")),
 ("Umalbaninn Mokdad Kazem Alnoor", "PhD fellow", "phd", 20, [], dict(profile_url=EYE+"?pure=en/persons/630395")),
 ("Zaynab Ahmad Mouhammad", "PhD fellow", "phd", 20, [], dict(profile_url=EYE+"?pure=en/persons/497387")),
 ("Jeppe Nygård Samuelsen", "Data manager", "staff", 30, ["forever"], dict()),
 ("Charlotte Taul", "Project coordinator", "staff", 31, ["forever"], dict(profile_url=EYE+"?pure=en/persons/312977")),
 ("Conny Irene Graae", "Study nurse", "staff", 32, ["forever"], dict(profile_url=EYE+"?id=745035&vis=medarbejder")),
 ("Emilie Gug Møller-Kongshaug", "Administrative officer and outreach coordinator", "staff", 33, ["forever"], dict(profile_url=EYE+"?id=770603&vis=medarbejder")),
 ("Christian Eggers Ø. Rasmussen", "Medical student", "student", 40, ["forever"], dict(orcid="0009-0003-3386-8607", profile_url=EYE+"?pure=en/persons/701095")),
 ("Katrine Najah Mikha", "Medical student", "student", 40, ["forever"], dict(orcid="0009-0005-2403-9027", profile_url=EYE+"?id=700427&vis=medarbejder")),
 ("Anne Hedengran Nagstrup", "Senior guest researcher", "guest", 50, [], dict(profile_url="https://research.ku.dk/search/result/?pure=en%2Fpersons%2Fanne-hedengran-nagstrup(6b5085d9-b96c-4e20-8f20-9bd6180f79a6).html")),
 ("Mia Langbøl Hjerrild", "Senior guest researcher", "guest", 50, [], dict(profile_url=EYE+"?pure=en/persons/447483")),
 ("Anna-Sophie Aagaard Thein", "Guest researcher", "guest", 51, [], dict(profile_url="https://forskning.ku.dk/soeg/result/?pure=da%2Fpersons%2Fannasophie-aagaard-thein(c12a8fde-3181-4276-bad9-d776d8f1778a).html")),
 ("Jens Riis Møller", "Guest researcher", "guest", 51, ["forever"], dict(profile_url=EYE+"?id=590975&vis=medarbejder")),
 ("Rubin Hadad", "Guest researcher", "guest", 51, [], dict()),
 ("Rupali Vohra", "Guest researcher", "guest", 51, [], dict(profile_url=EYE+"?pure=en/persons/331753")),
 ("Simone Nordqvist Graver Ahrensberg", "Guest researcher", "guest", 51, [], dict(profile_url=EYE+"?id=596955&vis=medarbejder")),
]
def slug(s):
    s = s.replace("ø","oe").replace("Ø","Oe").replace("æ","ae").replace("å","aa")
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode()
    return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
def q(v): return '"' + str(v).replace('"','\\"') + '"'
for name, role, cat, order, projects, ex in people:
    body = ex.pop("body", "")
    lines = ["---", f"name: {q(name)}", f"role: {q(role)}", f"category: {cat}", f"order: {order}",
             f"projects: [{', '.join(projects)}]", f"photo: {q(ex.get('photo',''))}", f"email: {q(ex.get('email',''))}",
             f"orcid: {q(ex.get('orcid',''))}", f"profile_url: {q(ex.get('profile_url',''))}", f"linkedin: {q(ex.get('linkedin',''))}", "---", body, ""]
    open(os.path.join(out, slug(name)+".md"), "w").write("\n".join(lines))
print(len(people))
