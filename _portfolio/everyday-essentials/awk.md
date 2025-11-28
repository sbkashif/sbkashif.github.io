---
layout: portfolio_item
title: "Awk"
permalink: /everyday-essentials/awk/
date: 2025-11-28
page_modified: 2025-11-28
hidden: true
---

# basic syntax of awk

A typical AWK command looks like this:

```bash
awk 'pattern { action }' filename
```

- **pattern**: The condition that each line (or record) is tested against. Examples include matching text, line numbers, or expressions.[^2][^4][^5]
- **{ action }**: Actions to perform on each line that matches the pattern. These are enclosed in curly braces `{...}` and can include printing columns, doing math, or assigning variables.
- **filename**: The text file or input stream being processed.

If no pattern is specified, the action applies to every line.

Special blocks:

- **END { ... }**: Runs only once, after all lines have been processed. Commonly used for post-processing tasks, like printing totals or averages.[^7]
- **BEGIN { ... }**: Runs once before any lines are processed, often used for initializing variables.



# usage examples

## finding the average of a particular column in the OpenMM output file

```bash
awk 'NR>10000 {sum += \$6; count++} END {if (count > 0) print sum/count}' prod_out.txt
```
### explanation via <img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:32px;margin-right:16px"/>

- `NR > 10000`: filters lines by line number. `NR` is AWK's built-in variable, representing the current line number. this block applies the following logic only for lines **after** line 10,000.
- `{sum += $6; count++}`: accumulates the sum and count. `sum += $6`: adds the value in the 6th column of the current line to the running total `sum`. `count++`: increments `count` for each line processed after line 10,000.
- `END {if (count > 0) print sum/count}`: calculates and prints the average. the `END` block is executed after all lines have been processed. `if (count > 0)`: Prevents division by zero if no lines matched. `print sum/count`: Calculates and prints the average of the 6th column values from lines after 10,000.
- `prod_out.txt`: is the input file name that will be read by awk line by line

**summary**: The command skips the first 10,000 lines, then computes the average of the values in the 6th column over all following lines in `prod_out.txt`. This is often used for analyzing simulation or production logs, where only a subset of data is relevant for statistics.
