---
layout: post
author: Kyo
title:  "Fix Python on Git Bash"
image: 
featured: false
categories: TechNotes Troubleshoot
---

在使用 gcould cli 指令取得 credential 的時候碰到了下面的問題
``` bash
gcloud container clusters get-credentials {cluster} --region {region} --project {project}
```
```
/c/Program Files (x86)/Google/Cloud SDK/google-cloud-sdk/bin/gcloud: line 41: /c/Users/me/AppData/Local/Microsoft/WindowsApps/python3: Permission denied
```

嘗試了幾種解法，無論是移除安裝啦，加上python3 alias之類的都無效，且只有 git bash 出了問題。

問題就從 python 的問題轉換到 git bash 的問題了。

解法如下
1. 移除 python
2. win key 搜尋 App execution aliases
3. toggle off app Installer for python.exe & python3.exe
![python_gitbash](/assets/images/troubleshoot/python_gitbash.jpg){:class="img-responsive"}
4. re-install python 
5. 重開 git bash 就完成了