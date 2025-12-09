#!/usr/bin/env python3
"""
Script to generate the Everyday Essentials portfolio page from the README.md
in the everyday-essentials repository.

This script is fully dynamic and works with any README structure:
- Parses TOC items recursively
- Validates GitHub links before creating pages
- Generates sub-pages for items without direct links
- Creates shield badges automatically based on item names
"""

import re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import subprocess

# Configuration
ESSENTIALS_REPO_PATH = Path("/Users/sbkashif/workspace/codes/everyday-essentials")
README_PATH = ESSENTIALS_REPO_PATH / "README.md"
OUTPUT_PATH = Path("/Users/sbkashif/workspace/codes/sbkashif.github.io/_portfolio/everyday-essentials.md")
SUBPAGES_DIR = Path("/Users/sbkashif/workspace/codes/sbkashif.github.io/_portfolio/everyday-essentials/subpages")
# Directory for internally rendered pages generated from README-linked markdown (specialized under portfolio)
PAGES_DIR = Path("/Users/sbkashif/workspace/codes/sbkashif.github.io/_portfolio/everyday-essentials")
GITHUB_REPO_URL = "https://github.com/sbkashif/everyday-essentials"

# Badge color palette
BADGE_COLORS = ["4B32C3", "F05032", "1BB91F", "0078D4", "FF6B6B", "4ECDC4", "45B7D1", "FFA07A"]


def parse_toc_structure(readme_path):
    """Parse the README TOC and return a hierarchical structure."""
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Find Table of Contents section
    toc_pattern = r'## Table of Contents\s+(.*?)(?=\n##|\n---|\Z)'
    toc_match = re.search(toc_pattern, content, re.DOTALL)
    
    if not toc_match:
        return []
    
    toc_content = toc_match.group(1)
    lines = toc_content.strip().split('\n')
    
    items = []
    current_parent = None
    
    for line in lines:
        if not line.strip():
            continue
        
        # Determine indentation level
        indent = len(line) - len(line.lstrip())
        
        # Parse item
        linked_match = re.match(r'-\s+\[([^\]]+)\]\(([^)]+)\)', line.strip())
        unlinked_match = re.match(r'-\s+(.+)', line.strip())
        
        if linked_match:
            name = linked_match.group(1)
            link = linked_match.group(2)
            item = {'name': name, 'link': link, 'children': []}
        elif unlinked_match:
            name = unlinked_match.group(1).strip()
            item = {'name': name, 'link': None, 'children': []}
        else:
            continue
        
        # Top-level item
        if indent == 0:
            items.append(item)
            current_parent = item
        # Child item
        elif indent >= 2 and current_parent:
            current_parent['children'].append(item)
    
    return items


def validate_local_md(filepath):
    """Check if a markdown file exists in the local repo."""
    if not filepath:
        return False
    local_path = ESSENTIALS_REPO_PATH / filepath
    return local_path.exists() and local_path.suffix.lower() in {".md", ".markdown"}


def generate_badge_url(name, index=0):
    """Generate a shields.io badge URL for any item name."""
    # Clean and format the name
    clean_name = name.replace('-', ' ').replace('_', ' ').title()
    encoded_name = quote(clean_name)
    
    # Pick a color from the palette
    color = BADGE_COLORS[index % len(BADGE_COLORS)]
    
    # Try to detect known tools for better logos
    name_lower = name.lower()
    logo_map = {
        'git': 'git',
        'tmux': 'tmux',
        'awk': 'gnu',
        'grep': 'gnu',
        'find': 'gnu',
        'sed': 'gnu',
        'bash': 'gnubash',
        'python': 'python',
        'javascript': 'javascript',
        'docker': 'docker',
        'kubernetes': 'kubernetes',
        'vasp': 'moleculer',
        'lammps': 'moleculer',
    }
    
    logo = None
    for key, value in logo_map.items():
        if key in name_lower:
            logo = value
            break
    
    if logo:
        return f"https://img.shields.io/badge/{encoded_name}-{color}?style=for-the-badge&logo={logo}&logoColor=white"
    else:
        return f"https://img.shields.io/badge/{encoded_name}-{color}?style=for-the-badge&logoColor=white"


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def generate_card_html(name, link, badge_url, is_external=True):
    """Generate HTML for a single card."""
    target = ' target="_blank" rel="noopener noreferrer"' if is_external else ''
    
    return f"""  <div class="essential-card">
    <a href="{link}"{target}>
      <div class="essential-logo">
        <img src="{badge_url}" alt="{name}">
      </div>
      <h3>{name.title()}</h3>
    </a>
  </div>
"""


def get_git_dates(filepath):
    """Return (date_created, last_modified) from git history for a file."""
    rel_path = str(filepath)
    repo_path = str(ESSENTIALS_REPO_PATH)
    try:
        # Get first commit date
        first = subprocess.check_output(
            ["git", "log", "--follow", "--format=%ad", "--date=short", rel_path],
            cwd=repo_path
        ).decode().strip().split('\n')
        if first:
            date_created = first[-1]
            last_modified = first[0]
        else:
            date_created = last_modified = datetime.now().strftime('%Y-%m-%d')
    except Exception:
        date_created = last_modified = datetime.now().strftime('%Y-%m-%d')
    return date_created, last_modified

def create_internal_page(name, source_md_relpath, parent_slug="everyday-essentials"):
    """Create an internal HTML page (Jekyll markdown) rendering the linked README markdown."""
    slug = slugify(name)
    permalink = f"/{parent_slug}/{slug}/"
    output_path = PAGES_DIR / f"{slug}.md"

    # Read source markdown content
    source_path = ESSENTIALS_REPO_PATH / source_md_relpath
    try:
        with open(source_path, "r") as sf:
            source_md = sf.read()
    except Exception as e:
        print(f"  ⚠ Failed to read source for {name}: {e}")
        return None

    # Use the markdown as-is from the source repo (no normalization, no code removal)
    # Ensure a blank line after every markdown table for correct rendering
    def add_blank_line_after_tables(md):
        lines = md.splitlines()
        out = []
        in_table = False
        for i, line in enumerate(lines):
            out.append(line)
            # Detect end of a table (a table row followed by a non-table row or end of file)
            if re.match(r'^\s*\|.*\|\s*$', line):
                in_table = True
                # If next line is not a table row, insert blank line
                if i+1 == len(lines) or not re.match(r'^\s*\|.*\|\s*$', lines[i+1]):
                    out.append('')
                    in_table = False
            else:
                in_table = False
        return '\n'.join(out)
    processed_md = add_blank_line_after_tables(source_md)

    # Get git dates for the source file
    date_created, last_modified = get_git_dates(source_path)
    fm = f"""---
layout: portfolio_item
title: "{name.title()}"
permalink: {permalink}
date_created: {date_created}
last_modified: {last_modified}
hidden: true
---
\n"""

    # Write internal page
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(fm + processed_md)

    print(f"  ✓ Created internal page: {output_path}")
    return permalink


def generate_subpage(item, parent_name="everyday-essentials"):
    """Generate a sub-page for items with children but no direct link. Cards link to internal pages."""
    slug = slugify(item['name'])
    permalink = f"/{parent_name}/{slug}/"
    output_path = SUBPAGES_DIR / f"{parent_name}-{slug}.md"

    # Validate all child links before creating the page
    valid_children = []
    for child in item['children']:
        if validate_local_md(child.get('link')):
            valid_children.append(child)

    # If no valid children after validation, skip this page
    if not valid_children:
        print(f"  ⚠ Skipping {item['name']}: no valid child links found")
        return None

    # Use git dates for the subpage file itself
    date_created, last_modified = get_git_dates(output_path)
    content = f"""---
layout: portfolio_item
title: "{item['name'].title()}"
permalink: {permalink}
date_created: {date_created}
last_modified: {last_modified}
hidden: true
---

## {item['name'].title()}

<div class="essentials-grid">
"""

    # Generate cards for children (create internal pages first)
    for idx, child in enumerate(valid_children):
        child_permalink = create_internal_page(child['name'], child['link'], parent_slug=parent_name)
        if not child_permalink:
            continue
        badge_url = generate_badge_url(child['name'], idx)
        content += generate_card_html(child['name'], child_permalink, badge_url, is_external=False)

    content += f"""</div>

[← Back to Everyday Essentials](/portfolio/everyday-essentials/)
"""

    # Write the file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"  ✓ Created sub-page: {output_path}")
    return permalink


def generate_main_page(items):
    """Generate the main portfolio page."""

    # Use git dates for the main README file
    date_created, last_modified = get_git_dates(README_PATH)
    content = f"""---
layout: portfolio_item
title: "Everyday Essentials"
permalink: /portfolio/everyday-essentials/
keywords: command-line, terminal, productivity, cheatsheet, reference
thumbnail: "/assets/images/everyday-essentials-thumbnail.png"
thumbnail_alt: "Everyday Essentials Thumbnail"
thumbnail_credit: "Generated by AI"
languages: ["Shell", "Git", "Terminal"]
date_created: {date_created}
last_modified: {last_modified}
---
A curated collection of useful information I refer to daily — from basic English grammar to terminal commands and keyboard shortcuts. This serves as a quick reference guide for common tasks and tools.

<!--more-->

This page aggregates content from my [everyday-essentials repository]({GITHUB_REPO_URL}), providing quick access to various command-line tools, shortcuts, and reference materials.

## Contents

<div class="essentials-grid">
"""

    # Process each top-level item
    for idx, item in enumerate(items):
        badge_url = generate_badge_url(item['name'], idx)

        # Item has a direct link
        if validate_local_md(item.get('link')):
            # Create an internal page rendering the linked markdown
            permalink = create_internal_page(item['name'], item['link'])
            if permalink:
                content += generate_card_html(item['name'], permalink, badge_url, is_external=False)

        # Item has children but no direct link - create a sub-page
        elif item['children']:
            permalink = generate_subpage(item)
            if permalink:  # Only add card if sub-page was created
                content += generate_card_html(item['name'], permalink, badge_url, is_external=False)

        # Item has no link and no children - skip it
        else:
            print(f"  ⚠ Skipping {item['name']}: no link or children")

    content += "</div>\n"

    return content


def main():
    """Main function."""
    
    # Check if README exists
    if not README_PATH.exists():
        print(f"Error: README not found at {README_PATH}")
        return
    
    print("Parsing README structure...")
    items = parse_toc_structure(README_PATH)
    
    if not items:
        print("Error: No TOC items found in README")
        return
    
    print(f"Found {len(items)} top-level items")
    
    # Generate main portfolio page
    print("\nGenerating everyday-essentials portfolio page...")
    content = generate_main_page(items)

    # Check if file exists and content is different (ignoring date fields)
    write_file = True
    if OUTPUT_PATH.exists():
        with open(OUTPUT_PATH, 'r') as f:
            old = f.read()
        # Remove date and page_modified lines for comparison
        import re
        def strip_dates(text):
            return re.sub(r'^(date|page_modified):.*$', '', text, flags=re.MULTILINE).strip()
        if strip_dates(content) == strip_dates(old):
            write_file = False
    if write_file:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, 'w') as f:
            f.write(content)
        print(f"✓ Created {OUTPUT_PATH}")
    else:
        print(f"No changes to {OUTPUT_PATH}; not updating date.")
    
    print("\n✓ Done! Pages generated successfully.")
    print(f"\nVisit: /portfolio/everyday-essentials/")


if __name__ == "__main__":
    main()
