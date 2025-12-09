---
layout: portfolio_item
title: "Tmux"
permalink: /everyday-essentials/tmux/
date_created: 2025-09-09
last_modified: 2025-09-29
hidden: true
---

# tmux

## start a session

```bash
tmux new -s <session_name>
```
observe a green strip at the bottom of the terminal with the session name printed over it

once the session begins, run the shell script that you would otherwise submit in a regular terminal


### Exit the session (while keeping it running in the background)

ctrl+b --> release the keys --> d. a message regarding detachment will be printed on screen

## Monitor runs/progress in an active session

```bash
tmux attach -t <session_name>
```
similarly, you can create multiple sessions, and see the list of all the sessions from `tmux ls`

### Killing a session

terminate a run in between by killing the session: 

```bash
tmux kill-session -t <session-name>
```