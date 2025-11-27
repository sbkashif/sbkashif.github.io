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

# Configuration
ESSENTIALS_REPO_PATH = Path("/Users/sbkashif/workspace/codes/everyday-essentials")
README_PATH = ESSENTIALS_REPO_PATH / "README.md"
OUTPUT_PATH = Path("/Users/sbkashif/workspace/codes/sbkashif.github.io/_portfolio/everyday-essentials.md")
SUBPAGES_DIR = Path("/Users/sbkashif/workspace/codes/sbkashif.github.io/_portfolio/subpages")
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


def validate_github_file(filepath):
    """Check if a file exists in the local repo."""
    local_path = ESSENTIALS_REPO_PATH / filepath
    return local_path.exists()


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


def generate_subpage(item, parent_name="everyday-essentials"):
    """Generate a sub-page for items with children but no direct link."""
    slug = slugify(item['name'])
    permalink = f"/{parent_name}/{slug}/"
    output_path = SUBPAGES_DIR / f"{parent_name}-{slug}.md"
    
    # Validate all child links before creating the page
    valid_children = []
    for child in item['children']:
        if child['link'] and validate_github_file(child['link']):
            valid_children.append(child)
    
    # If no valid children after validation, skip this page
    if not valid_children:
        print(f"  ⚠ Skipping {item['name']}: no valid child links found")
        return None
    
    # Generate front matter
    content = f"""---
layout: portfolio_item
title: "{item['name'].title()}"
permalink: {permalink}
date: {datetime.now().strftime('%Y-%m-%d')}
page_modified: {datetime.now().strftime('%Y-%m-%d')}
hidden: true
---

## {item['name'].title()}

<div class="essentials-grid">
"""
    
    # Generate cards for children
    for idx, child in enumerate(valid_children):
        github_link = f"{GITHUB_REPO_URL}/blob/main/{child['link']}"
        badge_url = generate_badge_url(child['name'], idx)
        content += generate_card_html(child['name'], github_link, badge_url, is_external=True)
    
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
    
    # Front matter
    content = f"""---
layout: portfolio_item
title: "Everyday Essentials"
permalink: /portfolio/everyday-essentials/
keywords: command-line, terminal, productivity, cheatsheet, reference
thumbnail: "/assets/images/everyday-essentials-thumbnail.png"
thumbnail_alt: "Everyday Essentials Thumbnail"
thumbnail_credit: "Generated by AI"
languages: ["Shell", "Git", "Terminal"]
date: {datetime.now().strftime('%Y-%m-%d')}
page_modified: {datetime.now().strftime('%Y-%m-%d')}
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
        if item['link'] and validate_github_file(item['link']):
            github_link = f"{GITHUB_REPO_URL}/blob/main/{item['link']}"
            content += generate_card_html(item['name'], github_link, badge_url, is_external=True)
        
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
    
    # Write main page
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        f.write(content)
    print(f"✓ Created {OUTPUT_PATH}")
    
    print("\n✓ Done! Pages generated successfully.")
    print(f"\nVisit: /portfolio/everyday-essentials/")


if __name__ == "__main__":
    main()
