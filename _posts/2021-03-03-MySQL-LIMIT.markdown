---
layout: post
author: Kyo
title:  "LIMIT Clause in MySQL"
image: 
featured: false
categories: TechNotes
---

我們都知道 LIMIT 這個關鍵字是可以限制查詢數量，例如下面查詢語法可以限制查詢前三筆資料

``` sql
SELECT *
FROM customers
LIMIT 3
```

但是你知道可以透過 LIMIT 來跳過前面多少筆資料嗎?

``` sql
SELECT *
FROM customers
LIMIT 3, 4
```

上面語法可以抓第 4, 5, 6, 7 這四筆資料，跳過前三筆  
最近剛學到的，分享一下 :)

