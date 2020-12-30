---
layout: post
author: Kyo
title:  "GTM 的進階設定"
image: assets/images/GTM.png
featured: true
categories: TechNotes
---
雖然 GTM 已經讓追蹤成效變得很有彈性，很方便了。不過想要完整的的追蹤整個畫面，如果不做點什麼事前設計，我相信 UX 應該是會累死的。為什麼呢? 請看看下面的情境分析

![LandingPage](/assets/images/GTM/yahooLanding.png){:class="img-responsive"}

1. 你要追蹤所有的連結的點擊狀況
2. 你要追蹤網頁的捲動深度
3. 你要追蹤登入的點擊率
4. 你要追蹤使用者的停留時間

等等等等...
這些如果 UX 都要自己寫 Tag 去逐一追蹤應該會花上大半天的時間喔!
這時候就要請出 GTM 的變數了。只要網頁上的所有元件都有設定好特定的 Category 以及 Label。這樣在 GTM 設定追蹤代碼的時候就會簡單方便。