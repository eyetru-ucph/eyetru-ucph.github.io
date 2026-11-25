# EyeTRU website

Website for the Eye Translational Research Unit (EyeTRU), University of Copenhagen, with
sub-sites for its projects (currently Project FOREVER at `/forever/`).

- **Hosting:** GitHub Pages, rebuilt automatically on every change to `main` (`.github/workflows/deploy.yml`).
- **Editing for staff:** [Pages CMS](https://app.pagescms.org). Staff without GitHub accounts are invited by email
  (Pages CMS → this repository → Settings → Collaborators). The forms are defined in `.pages.yml`.
- **Site generator:** [Eleventy 3](https://www.11ty.dev/), no other runtime dependencies.

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

## Running it locally

```bash
npm install
npm start        # http://localhost:8080, reloads on save
npm run build    # writes the site to _site/
```

## Importing publications from the Word list

`scripts/import_docx_publications.py` turns the group's publication document into one file per item
(needs `pip install python-docx`). Existing files are never overwritten, so new items can be imported
again later. Check the result, since citations in free text are parsed on a best-effort basis.

## Handing over

The repository belongs to the group's GitHub organisation, not a person. When someone leaves,
remove them from the organisation and from Pages CMS collaborators. Make sure at least two people
are organisation owners at all times.
