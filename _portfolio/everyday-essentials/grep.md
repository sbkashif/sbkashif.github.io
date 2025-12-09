---
layout: portfolio_item
title: "Grep"
permalink: /everyday-essentials/grep/
date_created: 2023-11-17
last_modified: 2025-10-30
hidden: true
---

# grep 

grep (global regular expression print) is the classic Unix tool for searching text using patterns.

  - grep originated with Ken Thompson in early Unix (1970s). The name comes from the ed command g/re/p (global / regular expression / print).
  - Thompson's work on regular expressions and text search influenced grep's implementation. Over time grep became part of standard Unix toolchains and GNU grep added many extensions (PCRE support with -P, --include/--exclude, colorized output, etc.).
  - Today many alternatives exist (rg, ag) that are optimized for large repositories while preserving grep-like syntax.

---
## basic syntax

A typical grep invocation:

```bash
grep [OPTIONS] PATTERN [FILE...]
```

- PATTERN: a string or regular expression to search for. Put the pattern in quotes to avoid shell interpretation:
  - Prefer single quotes: 'pattern' (prevents shell expansion).
  - Use double quotes "pattern" when you need interpolation from the shell.
- FILE...: files or directories to search. If files are omitted grep reads from stdin.

Common options and flags
- -r, --recursive: read all files under each directory recursively.
- -R, --dereference-recursive: like -r but also follow symbolic links.
- -n: show line numbers for matches.
- -H: show filename for each match (default when searching multiple files).
- -h: suppress filename in output.
- -i: case-insensitive matching.
- -v: invert match (show non-matching lines).
- -c: print only a count of matching lines per file.
- -l: print only names of files with matching lines.
- -L: print only names of files without matches.
- -o: print only the matching part of a line (one match per line).
- -w: match whole words.
- -x: match whole lines.
- -F: interpret PATTERN as a list of fixed strings (fast, no regex).
- -E: use extended regular expressions (same as egrep).
- -P: use Perl-compatible regular expressions (PCRE) — GNU grep only.
- --color=auto: highlight matches in output.
- -q, --quiet, --silent: suppress output, exit code indicates match/no-match.
- --include=GLOB, --exclude=GLOB: include or exclude files by name pattern when recursing.
- -e PATTERN: use PATTERN; useful when PATTERN starts with -.
- -f FILE: take patterns from FILE (one per line).

Other useful behaviors
- Exit codes: 0 = one or more matches found; 1 = no matches; 2 = error (e.g., bad usage or unreadable file). This is useful in scripts.
- Binary files: grep may treat files as binary; use -a or --binary-files=text to force text processing.
- Null-separated search: use -z for processing input where lines are NUL-separated (useful with find -print0).
- Performance: for literal substring searches use -F. For very large trees, consider faster modern tools like ripgrep (rg) or The Silver Searcher (ag).


# my usage examples

## Searching for a particular string in all python files in a directory:

```bash
grep -r "your_search_string" --include \*.py /path/to/search/directory
```

### Explanation via <img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/GitHub_Copilot_logo.svg" class="lo    go" alt="GitHub Copilot" style="vertical-align: middle; margin: 0 3px 3px 3px; height: 20px;"/>

  - `-r`: Tells grep to recurse into directories and search files inside them.  
`"your_search_string"`: This is the PATTERN grep will look for. In this example it is a literal string; grep treats it as a regular expression by default.
  - `--include \*.py`: This option limits recursive search to files that match the given glob (here, Python files). It's applied only when recursion is in effect (`-r` or `-R`). Note the escaping: the backslash before `*` prevents the shell from expanding `*.py` before grep sees it. Alternatively, quote the glob: `--include='*.py'`.
  - `/path/to/search/directory`: The path tells grep where to start the recursive search. You can use `.` for the current directory.