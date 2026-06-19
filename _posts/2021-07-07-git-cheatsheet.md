---
layout: post
author: Kyo
title:  "CheatSheet for git"
description: "常用 git CLI 指令速查表，涵蓋 patch 產生、branch 操作、rebase 與 stash 等日常開發必備指令。"
featured: false
categories: TechNotes CheatSheet
---

平常開發時習慣使用 git cli，紀錄常用的指令方便查閱，希望也可以幫助到別人

產生 patch，方便查閱兩個版本的差異
``` git
git diff tag1..tag2 > diff.patch
```
