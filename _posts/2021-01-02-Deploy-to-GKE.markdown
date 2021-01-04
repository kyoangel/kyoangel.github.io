---
layout: post
author: Kyo
title:  "透過 GCP CLI 發佈你的網站"
image: assets/images/GCP/google-cloud-platform.jpg
featured: true
categories: TechNotes Docker K8s
---
要發佈建置好的映像到 Google 的 K8s Engine 服務上的話，
首先要登入你的 gcloud，這樣就可以用 CLI 來執行下面指令輕鬆發佈!

登入 gloud 後請輸入下面指令來建立一個 zone，這個關係到你的服務要部署在哪一個區域
這裡以 asia-east1-a 為例子
```
gcloud config set compute/zone asia-east1-a
```
接下來輸入下面指令建立一個叢集，例如 命名成 tw-no-1，這邊要等待幾分鐘時間。
```
gcloud container clusters create tw-no-1
```
建立好叢集之後，你必須要驗證身分憑證之後才可以跟它互動
```
gcloud container clusters get-credentials tw-no-1
```

接著，你可以使用任何你存放到 GCR 裡面的映象來部署，例如我使用 hello-world 這個映像 
```
kubectl create deployment hello-server --image=gcr.io/feisty-current-292804/hello-world:1.0
```

建立完成後，我們可以設定負載平衡並打開指定 Port 給外面連接
```
kubectl expose deployment hello-server --type=LoadBalancer --port 8080
```

你可以透過 `kubectl get service` 這個指令來看你的服務狀態，特別是要看對外 IP (EXTERNAL-IP) 這項。
如果看到是 pending 可以稍後再執行一次上面指令來查看。

看到對外 IP 之後，你已經可以透過 `http://[EXTERNAL-IP]:8080` 來查看你的服務瞜!!

有始有終最後提供刪除的指令，來清除剛剛練習的叢集。
```
gcloud container clusters delete tw-no-1
```

happy learning!