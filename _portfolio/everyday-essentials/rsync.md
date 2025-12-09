---
layout: portfolio_item
title: "Rsync"
permalink: /everyday-essentials/rsync/
date_created: 2025-11-28
last_modified: 2025-11-28
hidden: true
---

# rsync

`rsync` (remote sync) is a powerful file-copying and synchronization utility commonly used on Unix systems. It efficiently transfers only changed data, making it ideal for backups, mirroring directories, and incremental updates.

* Originally developed by Andrew Tridgell and Paul Mackerras in the mid-1990s.
* Introduced the **rsync algorithm**, which sends checksums to avoid re-transferring unchanged blocks of large files.
* Became a standard tool for incremental backups, local directory sync, remote sync over SSH, and file-based deployments.
* Today it’s heavily used in DevOps, HPC clusters, local workstation syncing, filesystem backups, and mirroring GitHub repos or website content.

---

## basic syntax
```bash
rsync [OPTIONS] SOURCE DESTINATION
```

general rules:

* `SOURCE` and `DESTINATION` may be:

  * paths (`/path/to/folder`)
  * remote locations (`user@host:/path`)
  * local directories (`.` for current directory)
* The **trailing slash** on SOURCE or DESTINATION changes behavior:

  * `src/` → copy *contents*
  * `src` → copy the *folder itself*

This distinction is fundamental to using `rsync` safely.

## Common options and flags

### Core options

* `-a` — archive mode (recursive + preserve permissions, timestamps, symlinks, etc.)
* `-v` — verbose output
* `-r` — recursive (included inside `-a`)
* `-n`, `--dry-run` — show what would happen without making changes
* `--delete` — delete extraneous files from destination that are not in source
* `-i`, `--itemize-changes` — detailed report of what is updated, added, or deleted
* `--progress` — show progress during transfer
* `-h` — human-readable numbers

### file-selection and filtering

* `--exclude=PATTERN` — skip files matching pattern
* `--include=PATTERN` — explicitly include files
* `--exclude-from=FILE` — read exclude patterns from file
* `--include-from=FILE` — read include patterns from file

### Copy behavior

* `--update` — skip files that are newer on destination
* `--checksum` — detect changes using checksums instead of mod-time/size
* `--ignore-existing` — don't overwrite existing files at destination
* `--remove-source-files` — delete source files after successful transfer

### Remote sync options

* `-e "ssh"` — specify remote shell (usually required for remote rsync)
* `--rsync-path` — specify rsync path on remote server

### safety / debugging

* `--dry-run` — preview only
* `--itemize-changes` — show how each file would change
* `--backup --backup-dir=DIR` — keep backups of overwritten files
* `--log-file=FILE` — log all actions


## trailing slash semantics (extremely important)

Given a folder named `src`:

| Command                                | Result                                        |
| -------------------------------------- | --------------------------------------------- |
| `rsync -a src/ dest/`                  | Copies *contents of src* into `dest/`         |
| `rsync -a src dest/`                   | Copies `src` folder *itself* into `dest/src/` |
| `rsync -a src/ .` (inside dest folder) | Syncs contents into current directory         |
| `rsync -a src .`                       | Creates `./src`                               |


**RULE:**

> Use **trailing slash on source** (`src/`) when you want the destination to be an *exact mirror* of source contents.

## exit codes

* `0` → success
* `1` → minor issues (some files skipped)
* `2` → serious errors (permissions, network, etc.)

Useful for scripts and CI pipelines.

---

# my usage examples

## safely mirror one directory into another (local → local)

```bash
rsync -av --delete source_dir/ destination_dir/
```

* `source_dir/` → copy contents
* `--delete` → remove extra files from destination
* this makes `destination_dir` an exact replica of `source_dir`.

## preview what changes would be made

```bash
rsync -av --delete --dry-run source/ dest/
```

Shows adds, updates, and deletions **without modifying anything**.

## show exactly what will be added/updated/deleted

```bash
rsync -av --delete -i --dry-run source/ dest/
```

example output:

```
>f+++++++++ newfile.py     (new file)
>f.st...... config.yaml    (updated)
*deleting   old.log        (deleted)
```
## sync a folder into the current directory

if you're already inside the destination folder:

```bash
rsync -av --delete ../source_dir/ .
```

`.` means “the current directory.”

## sync over ssh

```bash
rsync -av -e "ssh" local_dir/ user@hostname:/remote/path/
```
Useful for server deployments or backups.

## pull from a remote server into local machine

```bash
rsync -av -e "ssh" user@hostname:/remote/path/ ./local_copy/
```

## exclude temporary or generated files

```bash
rsync -av --exclude='*.log' --exclude='__pycache__/' src/ dest/
```

## copy only certain file types

```bash
rsync -av --include='*.py' --exclude='*' src/ dest/
```

copies only `.py` files, ignores everything else.

## backup files that would be overwritten

```bash
rsync -av --backup --backup-dir=old_versions/ src/ dest/
```

creates backup copies of overwritten files.

## synchronize two folders on external drives

Example you used:

```bash
rsync -av --delete --dry-run \
    source/ \
    .
```
perfect for keeping exact mirrors of project subfolders.