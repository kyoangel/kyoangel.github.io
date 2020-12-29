---
layout: post
author: Kyo
title:  "GTM 的簡單介紹"
image: assets/images/GTM.png
featured: true
categories: TechNotes
---
最近開發不少網站的登陸頁面，開始接觸到大量的資料追蹤需求。終於花時間(~~有權限~~)去了解什麼是 GTM，還有他運作的方式。在此之前我自己過往的經驗是埋 GA 代碼去追蹤特定的點擊或是操作。

當時當然也聽過 GTM (Google Tag Manager) 這個玩意兒。 不過只知道他就是一段 Code，埋進去網站之後，就不用再去特別設定 GA 的追蹤代碼了，UX 可以自己在 GTM 中設定取得想要追蹤的資料。GTM 真是一個省工程師時間的好工具阿!

那我們就來看看 GTM 是怎麼運作的吧! GTM 是透過 Javascript 安裝在目標網站上，然後在後台管理裡面設定代碼(Tag)以及觸發(Trigger)時機，就可以完成簡單的追蹤。如下圖追蹤了主影片撥放，設定的點擊，或是推薦影片撥放。

![track](/assets/images/GTM/track.png){:class="img-responsive"}

這三個追蹤都是透過設定代碼與觸發，然後送到 GA 去分析。

下面來個簡單的例子說明。首先你可以透過下面的說明去安裝 GTM 到網頁上。

![GTMInstall](/assets/images/GTM/GTMInstall.png){:class="img-responsive"}

安裝完後，可以到 GTM 管理介面新增一個代碼

![tag](/assets/images/GTM/tag.png){:class="img-responsive"}

且新增一個 Trigger，並指定特定的點擊

![tag](/assets/images/GTM/trigger.png){:class="img-responsive"}

這樣當使用者點擊特定 ID 的網頁元件時就會觸發 GTM 的追蹤代碼，把追蹤資料送往 GA。

Happy Data Analysis and Optimize!