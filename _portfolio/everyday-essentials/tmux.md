---
layout: portfolio_item
title: "Tmux"
permalink: /everyday-essentials/tmux/
date: 2025-11-28
page_modified: 2025-11-28
hidden: true
---

# tmux

## Start a session

```bash
tmux new -s <session_name>
```
Observe a green strip at the bottom of the terminal with the session name printed over it

Once the session begins, run the shell script that you would otherwise submit in a regular terminal


### Exit the session (while keeping it running in the background)

Ctrl+B --> Release the keys --> D. A message regarding detachment will be printed on screen.

## Monitor runs/progress in an active session

```bash
tmux attach -t <session_name>
```
Similarly, you can create multiple sessions, and see the list of all the sessions from `tmux ls`

### Killing a session

Terminate a run in between by killing the session: `tmux kill-session -t <session-name>`
