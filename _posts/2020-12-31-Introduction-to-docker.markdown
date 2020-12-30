---
layout: post
author: Kyo
title:  "Docker 的基本操作介紹"
image: assets/images/Docker/docker-logo.png
featured: true
categories: TechNotes Docker
---
Docker 仍然很熱門，這邊簡單介紹一下常用的指令跟觀念，這邊假設 Docker 環境已經都安裝完成，安裝的部分就略過了。

## Hello World
首先可以直接打開命令列輸入下列指令
```
docker run hello-world
```
神奇的事情發生了，你應該會看到
![cmd](/assets/images/Docker/hello-world.png){:class="img-responsive"}

如果看到以上畫面，恭喜你，你的 Docker 已經完整安裝了。解釋一下上面的指令，docker run 就是執行 docker 映像的指令。如果你的本機沒有這個映像的快取，docker 就會幫你找 Docker Hub 上面的 image 來執行。 hello-world 這個事實上是一個映像的名字。
基本的映像名稱應該是 Namespace/Repository:Tag 的型式，如果是官方的映象，可以不用指定命名空間 (Namespace)，也可以不指定標籤(Tag)這樣就會拿最新版的，一般標籤是拿來做版本區分使用。所以 hello-world 就是拿官方的最新版的 hello-world 這個映像。

這時候你可以輸入
```
docker images
```
來看有哪些映像在本機。這時候可以用下面指令
```
docker rmi hello-world
```
來移除這個已經用不到的映象。

這時候你會發現，你無法移除這個映像，這是因為剛剛的 docker run hello-world 的指令已經建立一個容器 (Container) 了而這個容器使用了那個映像。要刪除映像，必須先把容器停止。

先透過下面指令來查看容器。
```
docker ps -a
```
![ps](/assets/images/Docker/ps.png){:class="img-responsive"}

然後透過下面指令來停止容器。
```
docker stop [container_id]
``` 
停止後，就可以使用下面指令來移除容器。
```
docker rm [container_id]
```

現在可以使用 ```docker rmi hello-world``` 來移除用不到的映像了。
到這裡就知道了最基本的執行容器，查詢映像/容器，刪除映像/容器的方法了。