---
layout: portfolio_item
title: "Git"
permalink: /everyday-essentials/git/
date: 2025-11-28
page_modified: 2025-12-06
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

---
## disable file mode changes from git tracking
### command
```bash
git config --global core.fileMode false
```
### explanation
to be added later

---

## preview conflicts before merging

* the function **simulates a merge** without touching your files.
* conflicts are clearly highlighted in **color**.
* you can review which files and lines would conflict **before performing an actual merge**.
* it is completely safe to run on any branch with an upstream set.


### command
```bash
git-conflicts-color
````
### example output

* **ted background** → your local changes (HEAD)
* **yellow background** → separator between changes
* **green background** → incoming changes from upstream

### underlying function

#### function defition
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
#### step-by-step explanation

##### check git repository
```zsh
git rev-parse --is-inside-work-tree
```
* verifies that you are inside a Git repository.
* if not, the function exits safely.

##### identify upstream branch
```zsh
upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{upstream})
```
* finds the remote branch your current branch is tracking.
* needed to know which branch to compare against.

##### fetch latest remote changes
```zsh
git fetch
```
* updates remote references locally without modifying files.
* safe: your working tree stays unchanged.

##### find merge base
```zsh
base=$(git merge-base HEAD "$upstream")
```
* determines the **common ancestor commit** of your branch and upstream.
* used for a **three-way merge simulation**.

##### simulate the merge
```zsh
output=$(git merge-tree "$base" HEAD "$upstream")
```
* performs an **in-memory merge**
* does **not modify working tree or index**
* produces conflict markers where changes overlap

##### detect conflicts
```zsh
if ! echo "$output" | grep -q "<<<<<<<"; then
  echo "✅ No merge conflicts. Merge should be clean."
  return 0
fi
```
* checks if any conflict markers exist in the simulated merge.
* if none, the merge is safe and clean.

##### colorize conflict output
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
---

## combined preview of merge conflicts and uncommitted changes that would block `git pull`

A custom shell function to **check whether a Git branch is safe to pull**. It provides:

* Local branch **ahead/behind status** relative to its upstream.
* Warnings for **uncommitted or modified tracked files** that could block a pull.
* Warnings for **untracked files** (`??`) that may block a merge if the remote has files with the same name.
* Optional detection of **potential merge conflicts** if the branch has diverged.

This function is designed as a **safety check before running `git pull`**, giving you a clear picture of any issues that might prevent a clean merge.

### command
```zsh
git_pull_check
```

### example output
```shell
⚠️  Local changes that may block pull:
 M file1.py
 M file2.py
ℹ️  Untracked files (safe for pull unless remote has same path):
 ?? new_file.txt

Local branch:  feature-xyz
Tracking:      origin/feature-xyz
Ahead:         2 commits
Behind:        1 commit
⚠️  Branch has diverged. Checking potential merge conflicts...
⚠️  Potential merge conflicts detected:
--------------------------------------
<<<<<<< HEAD
some local line
=======
some remote line
>>>>>>> origin/feature-xyz
--------------------------------------
❌ Cannot safely pull: local changes may block merge.
```


### underlying function

#### function definition

```bash
git_pull_check() {
    # Ensure inside Git repo
    git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
        echo "Not inside a Git repository."
        return 1
    }

    # Check upstream
    UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
    if [ -z "$UPSTREAM" ]; then
        echo "No upstream branch set. Use: git branch -u origin/<branch>"
        return 1
    fi

    # Fetch remote
    git fetch >/dev/null

    # Check working directory
    STATUS=$(git status --porcelain)
    MODIFIED=$(echo "$STATUS" | grep -E '^[ MADRC]')
    UNTRACKED=$(echo "$STATUS" | grep '^??')

    if [ -n "$MODIFIED" ]; then
        echo "⚠️  Local changes that may block pull:"
        echo "$MODIFIED"
        BLOCK_FLAG=1
    else
        BLOCK_FLAG=0
    fi

    if [ -n "$UNTRACKED" ]; then
        echo "ℹ️  Untracked files (safe for pull unless remote has same path):"
        echo "$UNTRACKED"
    fi

    # Ahead / behind
    AHEAD=$(git rev-list --count @{u}..HEAD)
    BEHIND=$(git rev-list --count HEAD..@{u})

    echo "Local branch:  $(git branch --show-current)"
    echo "Tracking:      $UPSTREAM"
    echo "Ahead:         $AHEAD commits"
    echo "Behind:        $BEHIND commits"

    # Determine pull status
    if [ "$BLOCK_FLAG" -eq 1 ]; then
        echo "❌ Cannot safely pull: local changes may block merge."
        return 1
    fi

    if [ "$BEHIND" -gt 0 ] && [ "$AHEAD" -eq 0 ]; then
        echo "✅ Safe to pull: remote has new commits, fast-forward possible."
        return 0
    elif [ "$BEHIND" -eq 0 ] && [ "$AHEAD" -gt 0 ]; then
        echo "⚠️  You have local commits not pushed. Pull not needed."
        return 0
    elif [ "$BEHIND" -gt 0 ] && [ "$AHEAD" -gt 0 ]; then
        echo "⚠️  Branch has diverged. Checking potential merge conflicts..."
        BASE=$(git merge-base HEAD "$UPSTREAM")
        OUTPUT=$(git merge-tree "$BASE" HEAD "$UPSTREAM")
        if ! echo "$OUTPUT" | grep -q "<<<<<<<"; then
            echo "✅ No merge conflicts detected. Merge should be clean."
        else
            echo "⚠️  Potential merge conflicts detected:"
            echo "--------------------------------------"
            echo "$OUTPUT" | sed \
                -e 's/^<<<<<<< .*/\x1b[41;97m&\x1b[0m/' \
                -e 's/^=======/\x1b[43;30m&\x1b[0m/' \
                -e 's/^>>>>>>> .*/\x1b[42;97m&\x1b[0m/' \
                -e 's/^+/\x1b[32m&\x1b[0m/' \
                -e 's/^-/\x1b[31m&\x1b[0m/'
            echo "--------------------------------------"
        fi
        return 1
    else
        echo "✔ Up-to-date with remote."
        return 0
    fi
}
```
#### line-by-line function explanation

##### verify you’re in a Git repository
```bash
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "Not inside a Git repository."
    return 1
}
```
* Checks if the current directory is inside a Git repository.
* If not, prints an error and exits.

##### determine the upstream branch
```bash
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
if [ -z "$UPSTREAM" ]; then
    echo "No upstream branch set. Use: git branch -u origin/<branch>"
    return 1
fi
```
* gets the name of the upstream branch (tracking branch).
* if there’s no upstream set, prints instructions and exits.

##### fetch the latest remote changes
```bash
git fetch >/dev/null
```
* fetches the latest remote changes quietly (without printing output).

##### identify **modified tracked files** (which block pull).
```bash
STATUS=$(git status --porcelain)
MODIFIED=$(echo "$STATUS" | grep -E '^[ MADRC]')
UNTRACKED=$(echo "$STATUS" | grep '^??')
```
* `git status --porcelain` gives a **machine-readable status** of the working directory.
* `MODIFIED` → lines indicating **modified/staged files** that can block a pull (`M`, `A`, `D`, etc.).
* `UNTRACKED` → lines starting with `??`, which are untracked files (informational).

#### identify **untracked files** (informational only).
```bash
if [ -n "$MODIFIED" ]; then
    echo "⚠️  Local changes that may block pull:"
    echo "$MODIFIED"
    BLOCK_FLAG=1
else
    BLOCK_FLAG=0
fi
```
* if there are modified/staged files, print a warning and mark `BLOCK_FLAG`.
* yhese files **can block a pull** if a remote merge would overwrite them.

##### Calculate **ahead/behind commit counts** relative to upstream.
```bash
if [ -n "$UNTRACKED" ]; then
    echo "ℹ️  Untracked files (safe for pull unless remote has same path):"
    echo "$UNTRACKED"
fi
```
* prints untracked files separately for information.
* normally, untracked files **do not block a pull** unless remote has a file with the same name.

##### check for **divergence** and potential merge conflicts.
```bash
AHEAD=$(git rev-list --count @{u}..HEAD)
BEHIND=$(git rev-list --count HEAD..@{u})
```
* counts commits **ahead** (local commits not in remote) and **behind** (remote commits not in local).
* helps determine if the branch can be fast-forwarded or has diverged.

##### output a **clear summary** of pull safety.
```bash
echo "Local branch:  $(git branch --show-current)"
echo "Tracking:      $UPSTREAM"
echo "Ahead:         $AHEAD commits"
echo "Behind:        $BEHIND commits"
```
* prints a summary of the branch and its relationship to upstream.

```bash
if [ "$BLOCK_FLAG" -eq 1 ]; then
    echo "❌ Cannot safely pull: local changes may block merge."
    return 1
fi
```

* Stops the function if **local modified files exist**, since pull could fail.

```bash
if [ "$BEHIND" -gt 0 ] && [ "$AHEAD" -eq 0 ]; then
    echo "✅ Safe to pull: remote has new commits, fast-forward possible."
    return 0
elif [ "$BEHIND" -eq 0 ] && [ "$AHEAD" -gt 0 ]; then
    echo "⚠️  You have local commits not pushed. Pull not needed."
    return 0
elif [ "$BEHIND" -gt 0 ] && [ "$AHEAD" -gt 0 ]; then
    echo "⚠️  Branch has diverged. Checking potential merge conflicts..."
    BASE=$(git merge-base HEAD "$UPSTREAM")
    OUTPUT=$(git merge-tree "$BASE" HEAD "$UPSTREAM")
    if ! echo "$OUTPUT" | grep -q "<<<<<<<"; then
        echo "✅ No merge conflicts detected. Merge should be clean."
    else
        echo "⚠️  Potential merge conflicts detected:"
        echo "--------------------------------------"
        echo "$OUTPUT" | sed \
            -e 's/^<<<<<<< .*/\x1b[41;97m&\x1b[0m/' \
            -e 's/^=======/\x1b[43;30m&\x1b[0m/' \
            -e 's/^>>>>>>> .*/\x1b[42;97m&\x1b[0m/' \
            -e 's/^+/\x1b[32m&\x1b[0m/' \
            -e 's/^-/\x1b[31m&\x1b[0m/'
        echo "--------------------------------------"
    fi
    return 1
else
    echo "✔ Up-to-date with remote."
    return 0
fi
```

* **Branch behind, ahead=0** → safe to fast-forward.
* **Branch ahead, behind=0** → no pull needed.
* **Branch ahead & behind** → diverged, potential merge conflicts detected using `git merge-tree`.
* Conflicts are highlighted in color:

  * `<<<<<<< HEAD` → local changes
  * `=======` → separator
  * `>>>>>>> remote` → remote changes
  * `+` → added lines (green)
  * `-` → removed lines (red)
* If no divergence → prints “Up-to-date.”

---

## get git commits from a specific author

### basic
```bash
git log --all --author="$AUTHOR_GITHUB_ID" --pretty=format:"%h %an %ad %s"
```
Here:
 - `%h`: short hash
 - `%an`: author name
 - `%ad`: author date
 - `%s`: subject (commit message)

### search across branches
#### as is
```bash
git for-each-ref --format="%(refname:short)" refs/heads/ | while read branch
do
    echo "== $branch =="
    git log "$branch" --author="Salman" --pretty=format:"%h %s"
    echo
done
```

#### in a table
```bash
git-author-commits() {
    if [ -z "$1" ]; then
        echo "Usage: git-author-commits <author name or email>"
        return 1
    fi

    for c in $(git log --all --author="$1" --pretty=format:"%H"); do
        echo "---------"
        echo "Commit: $c"
        
        git show -s --pretty=format:"Author: %an <%ae>%nDate:   %ad%nMessage:%n  %s" "$c"
        
        echo "Branches:"
        git branch --all --contains "$c" | sed 's/^/  /'
        echo
    done
}
```