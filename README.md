# sbkashif.github.io — site content and editing guide

This repository contains the source for a personal website built with Jekyll using the Minima theme. The README below is focused on end-user tasks: installing, previewing the site locally, and adding new content (portfolio, research, posts).

For more details, refer to the original `Minima` theme documentation:
> https://github.com/jekyll/minima

Or the Jekyll documentation:
> https://jekyllrb.com/docs/

## Installation (quick)

Requirements: Ruby (>= 2.7), Bundler, Git.

1. Install gems:

```bash
bundle install
```

2. Update [config file](_config.yml) for site settings (optional)
```yaml
# Minima date format
# refer to https://shopify.github.io/liquid/filters/date/ if you want to customize this
minima:
  date_format: "%b %-d, %Y"
  # generate social links in footer
  social_links:
    twitter: salman_kashif21
    github:  sbkashif
    linkedin: salmanbinkashif

# If you want to link only specific pages in your header, uncomment
# this and add the path to the pages in order as they should show up
header_pages:
 - about.md
 - research.md
 - portfolio.md
 - posts.md
```
More details on styling options are in the [CSS guide](docs/CSS_GUIDE.md).
 
3. Preview locally:

```bash
bundle exec jekyll serve
# then open http://127.0.0.1:4000
```

That's it — you need to cthe site will regenerate automatically as you edit files.

## Where content lives

- **Portfolio items:** `_portfolio/` (each item is a markdown file)
- **Research pages:** `_research/` (each item is a markdown file)
- **Blog posts:** `_posts/` (standard Jekyll posts)
- **Global includes and layouts:** `_includes/` and `_layouts/`
- **Assets (images, css):** `assets/`

## Adding or updating an item (end-user steps)

1. Create a new markdown file in the appropriate folder:
  - Portfolio: `_portfolio/my-project.md`
  - Research: `_research/my-paper.md`
  - Post: `_posts/YYYY-MM-DD-my-post.md`

2. Add frontmatter (YAML at the top) — minimal example for a portfolio item:

```yaml
---
layout: portfolio_item
title: "My Project Title"
permalink: /portfolio/my-project/
page_modified: 2025-10-20   # optional: shows "Last modified"
date: 2025-06-01           # optional: shows "Published" when no modified date
keywords: ml, simulation   # optional, used for metadata
thumbnail: assets/images/thumb.png  # optional image path or external URL
codes:
  - url: "https://github.com/username/repo"
   title: "repo-name"
   thumbnail: assets/images/github-logo.svg
---

Project description goes here...
```

Notes about dates:
- If `page_modified` is present in the front matter, the page will display "Last modified: ...".
- If no modified date is provided but `date` exists, the page will display just the date.
- If neither is present the page shows no date.

3. Save the file and preview locally (`bundle exec jekyll serve`). When satisfied, commit and push.

## Frontmatter reference (common keys)

- `layout` — which layout to use (e.g., `portfolio_item`, `research_item`, `post`).
- `title` — page title.
- `permalink` — optional, custom URL.
- `page_modified` or `modified_date` — optional, a date shown as "Last modified".
- `date` — publication date; shown as "Published" when no modified date is present.
- `keywords` — comma-separated or YAML array for metadata.
- `thumbnail` — URL or path to an image for the card.
- `thumbnail_credit` / `thumbnail_credit_url` — optional attribution.
- `codes` / `preprints` — arrays used by the "Relevant links" component; each item can include `url`, `title`, `thumbnail`, and `description`.

Example `codes` block (in frontmatter):

```yaml
codes:
  - url: "https://github.com/username/repo"
   title: "repo
    thumbnail: assets/images/github-logo.svg
    description: "C++ implementation"
```

## Thumbnails and images

- You can reference images stored in `assets/images/` or use an external URL.
- For SVG logos, reference the file (example above). For other images, use a reasonable size (images are displayed responsively).

## Preview & build

- Local preview: `bundle exec jekyll serve` and visit `http://127.0.0.1:4000`.
- Static build: `bundle exec jekyll build` produces the site in `_site/`.

## Quick checklist before publishing

- Add `title` and `layout` in frontmatter.
- If you want a visible last-modified stamp, add `page_modified`.
- Provide `thumbnail` if you want a card image.
- Preview locally, then commit and push.

> For any questions or help, feel free to reach out or open an issue!