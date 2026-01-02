---
layout: portfolio_item
title: "Conda environments"
permalink: /portfolio/conda/
keywords: [conda, python, environments, dependency management]
thumbnail: "https://cdn.simpleicons.org/anaconda/43B02A"
thumbnail_alt: "Conda Environments Thumbnail"
thumbnail_credit: "simple icons"
thumbnail_credit_url: "https://cdn.simpleicons.org/"
languages: ["Conda", "Python"]
date_created: 2025-04-10
last_modified: 2025-11-27
---

Managing dependencies is one of the most challenging aspects of any software project. Individual dependencies often come with their own requirements, which can conflict with other projects or even with the operating system itself.

<!--more-->

Conda environments address this problem by creating isolated spaces where each project maintains its own dedicated set of dependencies. This isolation ensures that projects do not interfere with one another, allowing you to work across multiple workflows without worrying about version conflicts or breaking system tools.

Why is this isolation so critical? What actually goes wrong when environments are not managed properly? To answer these questions, let’s examine a common real-world failure mode.

---

## The Perils of System Python: Why Isolation Is Critical

Most Linux distributions ship with a system Python installation (for example, `/usr/bin/python3`) that is tightly coupled to core system utilities such as `yum`, `dnf`, and `apt`. Modifying this system Python—by installing or upgrading libraries globally—can destabilize essential tools.

Consider a project that requires a newer version of the `cryptography` library. Installing it globally with `pip` may seem reasonable:

```bash
# Installing a newer cryptography library globally
$ pip install cryptography==42.0 --user
````

The problem surfaces when a system tool relying on an older OpenSSL stack is invoked:

```bash
$ ssh-keygen -t rsa
ImportError: /lib/x86_64-linux-gnu/libcrypto.so.1.1: version `OPENSSL_1_1_1' not found
```

At this point, a core security utility is broken. The root cause is not `ssh-keygen` itself, but a global dependency upgrade that violated system-level assumptions. Recovering from this state can be tedious and error-prone.

Conda environments prevent this entire class of problems by isolating project dependencies from the system Python:

```bash
# Safe installation in an isolated environment
$ conda create -n safe_env python=3.10 cryptography=42.0
$ conda activate safe_env
```

The system remains untouched, SSH continues to function, and the project still receives the required library version.

---

## Conda’s Storage Architecture: Where Files Live

The isolation provided by Conda is implemented through a well-defined storage layout.

### Key Conda Directories

When Conda is installed (via Miniconda or Anaconda), several important directories are created:

* **Base environment**
  The core Conda installation, typically located at `~/miniconda3/` or `~/anaconda3/`.

* **Named environments**
  Each environment lives in its own directory under `~/miniconda3/envs/`.
  For example, an environment named `data_science` resides at:

  ```
  ~/miniconda3/envs/data_science/
  ```

* **Package cache**
  Downloaded package archives are stored in `~/.conda/pkgs/` or `~/miniconda3/pkgs/`.
  This cache allows Conda to reuse binaries across environments, reducing both installation time and disk usage.

* **Configuration**
  Global configuration options are stored in `~/.condarc`.

Creating a new environment for data analysis:

```bash
$ conda create -n data_analysis python=3.9 numpy pandas matplotlib
```

This produces a self-contained directory that includes:

* A Python 3.9 interpreter
* Environment-specific libraries in `site-packages/`
* Dedicated binaries and metadata

Activating the environment:

```bash
$ conda activate data_analysis
```

updates shell environment variables—most notably `PATH`—so that binaries from this environment take precedence.

---

## A Practical Example: Building a Custom Package (`simple_math`)

To make the discussion concrete, let’s build a minimal custom package and explore how it behaves inside Conda environments.

### Package Structure

```text
simple_math/
├── setup.py
└── simple_math/
    └── operations.py
```

**`operations.py`**

```python
def add(a, b):
    return a + b

def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)
```

**`setup.py`**

```python
from setuptools import setup

setup(
    name="simple_math",
    version="0.1",
    packages=["simple_math"],
)
```

### Package Installation Methods

#### Local Installation (Non-Editable)

**Use case:** Installing a stable snapshot of the package.

```bash
$ python setup.py sdist bdist_wheel
$ pip install dist/simple_math-0.1-py3-none-any.whl
```

**Behavior:**

* Files are copied into the environment’s `site-packages/`
* Source code changes require reinstallation

#### Editable Installation (`pip install -e`)

**Use case:** Active development with rapid iteration.

```bash
$ pip install -e .
```

**Behavior:**

* A symbolic link to the source directory is created in `site-packages/`
* Code changes take effect immediately

This workflow is ideal for GitHub-hosted projects and research codebases under continuous development.

Example workflow:

```bash
$ git clone https://github.com/you/simple_math
$ conda create -n dev_env python=3.9
$ conda activate dev_env
$ pip install -e .
```

```python
>>> import simple_math
>>> simple_math.add(5, 3)
8
```

### Publishing Your Package 

There are several platforms that enable you to publish Python packages for others to use. These platforms—such as Conda-Forge and PyPI—each follow their own protocols for package submission, review, and deployment. Package publishing will be covered in detail in a future blog post.

---

## No Free Lunch: Managing Disk Usage

While Conda environments provide the flexibility to work on multiple projects without breaking each other’s dependencies, over time both environments and cached packages can consume significant disk space.

It is therefore important to understand the common sources of storage bloat and how to keep your environments lean.


**Common sources of bloat:**

* Orphaned packages in `~/.conda/pkgs/`
* Unused environments in `~/miniconda3/envs/`
* Temporary build artifacts

**Useful commands:**

```bash
# Identify largest environments
$ du -sh ~/miniconda3/envs/* | sort -hr

# Aggressive cleanup (often frees 5–15 GB)
$ conda clean --all --yes
```
---

## Conclusion

Conda environments form the backbone of reliable, reproducible Python workflows. They enable:

* Safe isolation from system-level dependencies
* Rapid iteration through editable installs
* Scalable package distribution via private channels or Conda-Forge
* Predictable reproduction of computational environments

Whether you are debugging dependency conflicts, developing research software, or distributing tools across teams, Conda provides a robust foundation for maintaining clean and scalable projects.

