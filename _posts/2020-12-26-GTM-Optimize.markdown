---
layout: post
author: Kyo
title:  "Integrate Google Optimize into GTM"
image: assets/images/Optimize.png
featured: false
categories: TechNotes
---
最近在嘗試使用 Google Optimize 最佳化工具在網站上做實驗，由於原本網站上已經使用了 GTM (Google Tag Manager) 在管理追蹤成效了。
因為不想直接把 Optimize 的追蹤代碼又加到專案的 \<head> 裡面，就查一下文件發現可以直接透過 GTM 把 Google Optimize 加進去並觸發。

怎麼做呢? 先進到 GTM 的管理系統，一般來說應該會有一個 AllPageView 的標籤來追蹤所有的網頁瀏覽!

![AllPageView](/assets/images/GTM/allpageview.png){:class="img-responsive"}

這時候要做的事情很簡單，就是新增一個 Google Optimize 的代碼，並設定成每個頁面發動一次即可，不需要設定觸發條件。

![addOptimize](/assets/images/GTM/addOptimize.png){:class="img-responsive"}

![optimizeTagSetting](/assets/images/GTM/optimizeTagSetting.png){:class="img-responsive"}

新增並設定 Google Optimize 代碼後，就去編輯 AllPageView 的代碼，去進階設定代碼觸法順序，並指定在 AllPageView 觸發前先觸發 Optimize 的代碼。

![triggerBeforeView](/assets/images/GTM/triggerBeforeView.png){:class="img-responsive"}

完成! 這樣就順利完成將 Google Optimize 的代碼整合到 GTM 裡面了。

Happy Data Analysis and Optimize!