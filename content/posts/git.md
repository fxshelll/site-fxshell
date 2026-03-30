---
title: "Git Sheet Cheat"
date: 2019-02-27T20:54:51-06:00
draft: true
tags: ["devops", "git", "ferramentas"]
---

## Local config
```sh
git config --global user.email "email@example.com"
```

## Reset last commit
```sh
git reset HEAD~1
```

## Status of all modified files
```sh
git status -u
```

## Update last commit
```sh
git commit --amend
git push origin <branch> --force
```

## Apply (wrong) changes of one branch to another
```sh
git stash
git checkout the-right-branch
git stash apply
```
