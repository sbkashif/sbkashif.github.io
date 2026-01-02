---
layout: portfolio_item
title: "ssh"
permalink: /everyday-essentials/ssh/
date_created: 2025-12-08
last_modified: 2025-12-08
hidden: true
---

ssh (secure shell) is a protocol that allows you to securely access another computer over a network. it encrypts all communication, including your login credentials, commands, and data. common usage areas include:

* logging into remote servers
* running commands on a remote system
* secure file transfer (scp, sftp)
* tunneling or port-forwarding connections
* remote development (e.g., vs code remote ssh)

when you use ssh on a unix-like system (linux, macos), ssh stores user-specific configuration and authentication data inside your home directory: `~/.ssh`

this folder may contain several types of files:

### private and public keys

* **id_rsa**, **id_ecdsa**, **id_ed25519** – private keys that must be kept secret
* **id_rsa.pub**, **id_ed25519.pub** – public keys that you can safely share

### known hosts

* stores fingerprints of servers you've connected to, so ssh can verify you're talking to the correct machine.

### config file

* a user-specific file where you store ssh connection settings, shortcuts, and quality-of-life options like persistent connections. ssh reads this file automatically every time you run `ssh`.

---

# my usage examples

## reusable remote connection

`ssh` `config` file allows you to define reusable connection settings for any number of hosts. so, instead of typing an entire ssh command each time, you can simply type:
### command
```
ssh your.remote.host
```

### after having these settings defined in your ```~/.ssh/config``` file

```ssh
host your.remote.host
    hostname your.remote.host
    user your_username
    forwardx11 yes
    controlmaster auto
    controlpath ~/.ssh/control-%r@%h:%p
    controlpersist 2h
```

### explanation

this block tells ssh how to behave every time you connect to this host. each directive configures one aspect of your connection:

* **host** — the shortcut name you will type. ssh matches this and applies all settings under it.
* **hostname** — the actual machine name or ip address.
* **user** — the username you want to log in as.
* **forwardx11** — allows graphical programs from the remote system to appear on your local machine.
* **controlmaster auto** - ssh normally creates a *new* network connection every time you run a command (like opening another terminal or using scp). `controlmaster` changes this behavior. it allows ssh to create a **master connection** the first time you log in. future ssh commands **reuse** that same connection instead of creating new ones. think of it like opening the main door to a building once and then using internal doors to move around without leaving and re-entering the building.
* **controlpath** - this tells ssh where to store a small socket file that represents the master connection. all additional ssh sessions communicate through this socket. example:
```
~/.ssh/control-your_username@your.remote.host:22
```
* **controlpersist 2h**  - this keeps the master connection alive for 2 hours even after you close your terminal. any new ssh or scp commands during that time will reuse that stored connection
note: this does **not** mean the remote host stays busy — it's just holding a lightweight session open.

---