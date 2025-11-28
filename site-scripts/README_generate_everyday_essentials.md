# Generate Everyday Essentials Portfolio Page

This script automatically generates the Everyday Essentials portfolio page from the README.md in the everyday-essentials repository.

## Usage

```bash
python3 scripts/generate_everyday_essentials.py
```

## What it does

1. **Reads** the README.md from `/Users/sbkashif/workspace/codes/everyday-essentials/`
2. **Parses** the Table of Contents section
3. **Generates**:
   - `_portfolio/everyday-essentials.md` - main page with cards for each tool
   - `_portfolio/<subpage_name>.md`  - subpages if sub-bullet points are also a link

## Features

- **Automatic card generation**: Creates a card for each top-level item in the TOC
- **Smart linking**: 
  - Items with `.md` files link to the GitHub repository
  - Parallelization section links to internal sub-page
- **Logo integration**: Uses shields.io badges for tool icons
- **Responsive grid layout**: Cards are displayed in a responsive grid

## Updating Content

When you update the everyday-essentials repository:

1. Simply run the script again to regenerate the pages
2. The script will automatically pick up new TOC items
3. Rebuild the Jekyll site: `bundle exec jekyll build`

## Configuration

Edit the following constants in the script to customize:

- `ESSENTIALS_REPO_PATH`: Path to the everyday-essentials repository
- `GITHUB_REPO_URL`: GitHub repository URL
- `TOOL_LOGOS`: Dictionary mapping tool names to badge URLs

## Requirements

- Python 3.x
- Access to the everyday-essentials repository (locally or via git)
