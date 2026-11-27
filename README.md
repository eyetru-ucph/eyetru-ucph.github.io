# EyeTRU website

Website for the Eye Translational Research Unit (EyeTRU), University of Copenhagen, with
sub-sites for its projects (currently Project FOREVER at `/forever/`).

- **Hosting:** GitHub Pages, rebuilt automatically on every change to `main` (`.github/workflows/deploy.yml`).
- **Editing for staff:** [Pages CMS](https://app.pagescms.org). Staff without GitHub accounts are invited by email
  (Pages CMS → this repository → Settings → Collaborators). The forms are defined in `.pages.yml`.
- **Site generator:** [Eleventy 3](https://www.11ty.dev/), no other runtime dependencies.

Live site: https://eyetru-ucph.github.io/

## Updating content in the editor (no coding)

News, publications, people, funders, partners, datasets, project pages, the front page and the menu
can all be edited in a web form.

**First, the person needs access.** Someone who already has access must add them once:

- **Staff without a GitHub account:** sign in at [app.pagescms.org](https://app.pagescms.org), open
  `eyetru-ucph / eyetru-ucph.github.io`, go to **Settings → Collaborators** and invite their email address.
  They receive an email with a sign-in link and never need GitHub.
- **People with a GitHub account** (e.g. the data manager): add them on GitHub under
  **eyetru-ucph → People → Invite member** (or the repository's **Settings → Collaborators**).
  They then sign in at [app.pagescms.org](https://app.pagescms.org) with GitHub.

**Then, to edit:**

1. Go to [app.pagescms.org](https://app.pagescms.org) and sign in (email link or GitHub).
2. Choose `eyetru-ucph.github.io`.
3. Pick a section in the left menu (e.g. **News**), then click an item to edit it or **Add an entry** to create one.
4. Fill in the form and click **Save**.
5. The live site updates by itself about a minute later. To follow progress or see an error, check
   the [Actions tab](https://github.com/eyetru-ucph/eyetru-ucph.github.io/actions).

Tips:
- To link a news item, person, publication etc. to FOREVER, choose it under **Related projects**. It then
  also appears on the FOREVER page.
- To take something off the site without deleting it, tick **Hide from website** (or **Hide (draft)** for news).
- Images and PDFs uploaded in the editor are stored in `src/assets/img/uploads/`.
- Every save is a commit on `main`, so the full history is in Git and any change can be undone.

## Changing the layout, design or code (developers)

Template, style and code changes are made locally on a branch and merged through a pull request,
so the live site is never broken by an unfinished change.

**One-time setup:** install [Git](https://git-scm.com/) and [Node.js](https://nodejs.org/) 20 or newer.
On Windows, WSL works well. One tested setup is Node installed with conda:
`conda install -c conda-forge nodejs`.

```bash
git clone https://github.com/eyetru-ucph/eyetru-ucph.github.io.git
cd eyetru-ucph.github.io
npm install
```

**Each change:**

```bash
git checkout main
git pull                       # staff edit main through the editor, so always pull first
git checkout -b my-change      # a short name for what you're doing, e.g. new-footer
npm start                      # preview at http://localhost:8080, reloads when you save a file
# ...edit files in src/_includes/ (templates) or src/assets/css/style.css (design)...
npm run build                  # optional: check the full build has no errors
git add -A
git commit -m "Describe the change"
git push -u origin my-change
```

Then open a pull request on GitHub (a **Compare & pull request** button appears on the repository page),
check the changes, and click **Merge**. The live site rebuilds from `main` about a minute after the merge.

If `git pull` or the merge reports a conflict, someone edited the same file in the editor meanwhile:
keep both changes, commit, and push again.

## Where things live

| What | Where | One file per |
|---|---|---|
| News | `src/content/news/` | news item (`YYYY-MM-DD-title.md`) |
| Publications, talks, posters | `src/content/publications/` | item |
| People | `src/content/people/` | person |
| Funders / grants | `src/content/grants/` | funder or grant |
| Partners & collaborators | `src/content/partners/` | organisation |
| Datasets | `src/content/datasets/` | dataset |
| Project sub-sites (FOREVER, …) | `src/content/projects/` | project → becomes `/<file-name>/` |
| Front page, contact details, footer links | `src/_data/site.yml` | – |
| Main menu | `src/_data/navigation.yml` | – |
| Labels for codes (publication types, people groups) | `src/_data/labels.yml` | – |
| Research page text and themes | `src/pages/research.md` | – |
| Uploaded images and PDFs | `src/assets/img/uploads/` | – |
| Templates and design | `src/_includes/`, `src/assets/css/style.css` | – |

Every content file has a `projects:` list, e.g. `projects: [forever]`. A project page automatically
shows the people, publications, datasets, partners, funders and news tagged with its file name.

## Adding a new subproject

1. Copy `src/content/projects/forever.md` to `src/content/projects/<short-name>.md` and edit it.
   The page appears at `/<short-name>/`.
2. In `.pages.yml`, add `{ value: <short-name>, label: <Name> }` to every `projects` field
   (search for `forever`) so editors can tag content with it.
3. Optionally add it to the menu in `src/_data/navigation.yml`.

## Importing publications from the Word list

`scripts/import_docx_publications.py` turns the group's publication document into one file per item
(needs `pip install python-docx`). Existing files are never overwritten, so new items can be imported
again later. Check the result, since citations in free text are parsed on a best-effort basis.

## Handing over

The repository belongs to the group's GitHub organisation, not a person. When someone leaves,
remove them from the organisation and from Pages CMS collaborators. Make sure at least two people
are organisation owners at all times.
