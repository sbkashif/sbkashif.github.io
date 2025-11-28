---
layout: portfolio_item
title: "Git"
permalink: /everyday-essentials/git/
date: 2025-11-28
page_modified: 2025-11-28
hidden: true
---

# git
git is a **distributed version control system**. it helps you track changes to files, collaborate with others, and experiment safely without losing your work.  


## basic terms

| term | definition | notes / example |
|------|-----------|----------------|
| **Repository (repo)** | a folder that contains your project and git history | `git init` creates a new repo |
| **Working Tree** | Your actual files on disk that you edit | Files like `main.py` or `README.md` |
| **Index / Staging Area** | Temporary area for changes you plan to commit | `git add <file>` stages a file |
| **HEAD** | Pointer to your current commit/branch | `git commit` updates HEAD to the new commit |
| **Branch** | A movable pointer to a series of commits | `main`, `feature-x` |
| **Commit** | A snapshot of your project at a point in time | `git commit -m "message"` |
| **Remote** | A copy of your repository hosted elsewhere | `origin` is the default remote |
| **Upstream Branch** | Remote branch your local branch tracks | Usually `origin/main` |
| **Merge Base** | Most recent common ancestor of two branches | Used for merges |
| **Conflict Markers** | Sections Git inserts when a file has conflicting changes | code below |
```
<<<<<<< HEAD
your code
=======
their code
>>>>>>> branch
```

## common commands
```bash
git init
````

* creates a new git repository in your project folder.
* adds a hidden `.git` folder to track changes.

```bash
git status
```

* shows modified files, staged files, and untracked files.
* always run before committing to see the current state.

```bash
git add <file>
git add .
```

* adds changes to the **staging area** in preparation for commit.

```bash
git commit -m "Describe your changes"
```

* saves a snapshot of your staged changes to the repository.
* updates `HEAD` to point to this new commit.

```bash
git log --oneline
```

* Shows a concise history of commits.
* Example:
```
f3a2b1c Add login feature
e4d5f6a Fix README typo
a1b2c3d Initial commit
```
```bash
git branch feature-x      # Create branch
git checkout feature-x    # Switch to branch
# or combine
git switch -c feature-x
```
* branches let you experiment independently of `main`.

```bash
git remote add origin <repo-url>
git push -u origin main
```
* sends your commits to a remote repository (like GitHub).
* `-u` sets the upstream so you can later just run `git push`.

```bash
git pull
```

* fetches and merges changes from the upstream branch.
* ensures your branch is up-to-date with collaborators.

## visualizing a simple git history

```
# Initial commit on main
A --- B --- C  (main / HEAD)

# Create feature branch
        \
         D --- E  (feature-x)

# Merge back to main
A --- B --- C --- F  (main)
        \       /
         D --- E  (feature-x)
```

* each letter represents a **commit**.
* branches allow parallel work.
* merge combines changes.

---

# my usage examples

## automatically git rm the deleted files

### command
```bash
git ls-files --deleted | xargs git rm
```

### explanation
to be added later

## disable file mode changes from git tracking
```bash
git config --global core.fileMode false
```
## preview before merging

oo **preview conflicts safely** without modifying your working tree, we can write and use the following **zsh function** with color highlighting.

### command
```bash
git-conflicts-color
````
this will show all **potential conflicts** with colors:

* **ted background** → your local changes (HEAD)
* **yellow background** → separator between changes
* **green background** → incoming changes from upstream

## underlying function
```zsh
git-conflicts-color() {
  # Check if inside a Git repository
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "Not inside a Git repository."
    return 1
  }

  # Identify the upstream branch
  upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null)
  if [[ -z "$upstream" ]]; then
    echo "No upstream branch set for this branch."
    echo "Set it using: git branch -u origin/<branch>"
    return 1
  }

  # Fetch latest remote commits
  echo "Fetching latest changes..."
  git fetch >/dev/null

  # Show which branches are being compared
  echo "Checking for merge conflicts between:"
  echo "  LOCAL:    HEAD ($(git rev-parse --abbrev-ref HEAD))"
  echo "  REMOTE:   $upstream"
  echo

  # Find the common ancestor (merge base)
  base=$(git merge-base HEAD "$upstream")

  # Simulate the merge in memory
  output=$(git merge-tree "$base" HEAD "$upstream")

  # Check if there are conflict markers
  if ! echo "$output" | grep -q "<<<<<<<"; then
    echo "✅ No merge conflicts. Merge should be clean."
    return 0
  fi

  echo "⚠️  Potential merge conflicts detected:"
  echo "--------------------------------------"

  # Colorize the output
  echo "$output" | sed \
    -e 's/^<<<<<<< .*/\x1b[41;97m&\x1b[0m/' \   # Red background for HEAD
    -e 's/^=======/\x1b[43;30m&\x1b[0m/' \     # Yellow background for separator
    -e 's/^>>>>>>> .*/\x1b[42;97m&\x1b[0m/' \  # Green background for incoming
    -e 's/^+/\x1b[32m&\x1b[0m/' \               # Green text for additions
    -e 's/^-/\x1b[31m&\x1b[0m/'                 # Red text for deletions

  echo "--------------------------------------"
}
```
### step-by-step explanation
#### check git repository
```zsh
git rev-parse --is-inside-work-tree
```
* verifies that you are inside a Git repository.
* if not, the function exits safely.

#### identify upstream branch
```zsh
upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream})
```
* finds the remote branch your current branch is tracking.
* needed to know which branch to compare against.

#### fetch latest remote changes
```zsh
git fetch
```
* updates remote references locally without modifying files.
* safe: your working tree stays unchanged.

#### find merge base
```zsh
base=$(git merge-base HEAD "$upstream")
```
* determines the **common ancestor commit** of your branch and upstream.
* used for a **three-way merge simulation**.

#### simulate the merge
```zsh
output=$(git merge-tree "$base" HEAD "$upstream")
```
* performs an **in-memory merge**.
* does **not modify working tree or index**.
* produces conflict markers where changes overlap.

---

#### detect conflicts
```zsh
if ! echo "$output" | grep -q "<<<<<<<"; then
  echo "✅ No merge conflicts. Merge should be clean."
  return 0
fi
```
* checks if any conflict markers exist in the simulated merge.
* if none, the merge is safe and clean.

#### colorize conflict output
```zsh
echo "$output" | sed \
  -e 's/^<<<<<<< .*/\x1b[41;97m&\x1b[0m/' \
  -e 's/^=======/\x1b[43;30m&\x1b[0m/' \
  -e 's/^>>>>>>> .*/\x1b[42;97m&\x1b[0m/' \
  -e 's/^+/\x1b[32m&\x1b[0m/' \
  -e 's/^-/\x1b[31m&\x1b[0m/'
```

* adds **ANSI color codes** for easier reading:

  * Red background → HEAD (local)
  * Yellow background → separator
  * Green background → upstream changes
  * Red/Green text → deletions/additions

#### end output
```zsh
echo "--------------------------------------"
```
* Adds a visual divider for clarity.

### ✅ summary

* The function **simulates a merge** without touching your files.
* Conflicts are clearly highlighted in **color**.
* You can review which files and lines would conflict **before performing an actual merge**.
* It is completely safe to run on any branch with an upstream set.
