---
title: "Git Sheet Cheat"
date: 2019-02-27T20:54:51-06:00
draft: false
---

## Local config
```
>> git config --global user.email "email@example.com"
```

## Reset last commit
```
>> git reset HEAD~1
```

## Status of all modified files
```
>> git status -u
```

## Update last commit
```
>> git commit --amend
>> git push origin <branch> --force
```

## Apply (wrong) changes of one branch to another
```
>> git stash
>> git checkout the-right-branch
>> git stash apply
```
