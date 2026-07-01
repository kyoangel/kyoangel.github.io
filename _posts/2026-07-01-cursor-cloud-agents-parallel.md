---
layout: post
author: KAI
title: "Cursor 3.7 雲端平行代理上線：我開始認真重新審視團隊的 CI 與 Review 工作流"
description: "Cursor 3.7 推出 /in-cloud 雲端子代理，Composer 2.5 讓 Bugbot review 壓縮至 90 秒。身為帶領 8 人後端團隊的技術經理，我從 on-call、code review 到 junior onboarding 逐一評估這次更新的導入價值與取捨。"
image: assets/images/posts/cursor-cloud-agents-parallel.jpg
categories: TechNotes AI
---

這週讓我停下來認真研究的，是 Cursor 在六月悄悄推進的一個指令：`/in-cloud`。

隨著 **Cursor 3.7** 與 **Composer 2.5** 的正式釋出（2026 年 6 月），工程師現在可以在 Cursor 裡輸入 `/in-cloud`，啟動一個跑在獨立 VM 上的雲端子代理，讓它去處理耗時的任務——修 CI、探索陌生 repo、或者跑一輪長時間重構。代理有自己的 branch，完全不干擾本機工作區，而且可以同時開多個並行。配合 Composer 2.5 的效能提升，Cursor 內建的 Bugbot 自動 code review 平均時間從原本的約 **5 分鐘壓縮到 90 秒**，每次 run 的 bug 發現率從 0.56 提升到 **0.62**，執行成本還降了 **22%**。

數字本身不算震撼，但組合在一起代表一件事：AI 代理的執行模式，已從「在你機器上跑」移到「在雲端替你跑、你繼續做你的事」，而且可以並行。這讓我開始認真重新盤算，我們團隊的幾個日常工作流程，是不是該跟著調整了。

## 假設情境

假設我的團隊有 8 位後端工程師，每天平均 6–8 個 PR 等待 review，CI pipeline 跑一次約 12 分鐘，每週有 3–4 次因為「CI 紅了但沒人及時修」導致 main branch 卡住。我們目前靠人工輪流 review 加 GitHub Actions + Slack 通知，一個 PR 有時要等 4–6 小時才有第一個 reviewer 回應。

如果 `/in-cloud` 穩定可用，工程師提完 PR 後可以立刻把「診斷這次 CI 失敗」或「初步探索這個 issue 的根因」丟給雲端代理，本機不需要掛著等結果，而是繼續做主線開發。對每週 3–4 次的 CI 卡關問題，這有非常實際的緩解潛力。

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響。** 雲端代理最吸引我的應用場景是 off-hours 的初步診斷：CI 紅了自動觸發代理診斷，再把結果貼到 Slack，on-call 工程師不需要半夜起來判斷「這是真的出事了，還是 flaky test？」但讓我猶豫的是錯誤處理——代理如果誤判並推了半成品 fix，on-call 反而要花更多時間清理。我的傾向是：目前只讓代理做診斷與建議，不做任何自動推送，等判斷品質穩定後再考慮鬆綁。

**對 code review 流程的影響。** Bugbot 90 秒出初稿，我想把它定位成「第一輪篩選器」——先抓樣板性錯誤（沒處理 null、忘記關 connection），讓人工 reviewer 聚焦在架構和業務邏輯。但這需要先在團隊訂好 convention：哪些 Bugbot comment 必須 resolve、哪些可以 dismiss。沒有明確規則，PR 的噪音只會增加而不是減少，reviewer 也容易因看到「AI 已掃過」就降低警覺。

**對 junior 工程師 onboarding 的影響。** `/in-cloud` 有一個用途讓我很喜歡：讓 junior 用雲端代理安全地探索陌生 repo，不怕弄壞本機環境，也不占用 senior 的帶人時間。代理可以幫他們回答「這個函式有哪些 caller？」「這個 API endpoint 的完整呼叫鏈是什麼？」之類的問題。我需要注意的是：onboarding 計畫要刻意設計「必須自己理解才能過的關卡」，避免 junior 依賴代理給答案、跳過建立系統認知的過程。

**技術債與長期維護成本。** 代理產生的 branch 和 PR 是有代價的：版本控制歷史變複雜，代理產生的 code 需要有人負責長期維護。我的傾向是從一開始就訂好清理 policy：探索 branch 超過 48 小時未合併自動關閉，代理產生的 PR 必須有人工 co-author 才能被 merge。

**採用時間軸建議。** 分三階段。POC 約 2–3 週，讓 1–2 位對工具有興趣的工程師在側線專案試跑 `/in-cloud`，驗證穩定性；指標是 VM 啟動失敗率 < 5%、代理任務完成率 > 70%。小規模試點約 4–6 週，選一個非關鍵服務，讓整組把 Bugbot 和雲端代理都跑起來；指標是 PR review 等待時間縮短超過 30%、每週 CI 卡關次數下降。小規模試點指標達標、且沒有出現代理產生的壞 code 溜進 main 的狀況，我才會把全面推行提上議程，並在那之前先把 team convention 文件整理好。

這是我接下來幾週會持續追蹤的方向，尤其想看 `/in-cloud` 在較大型 monorepo 上的實際穩定性，以及 Bugbot 在複雜業務邏輯面前的誤判率。如果你的團隊也在評估雲端平行代理，我很想知道你們的考量點和踩過的坑——這種真實使用經驗，往往比官方 changelog 更能幫助判斷要不要踩這個油門。

---
*封面圖片由 [Daniil Komov](https://www.pexels.com/photo/close-up-of-computer-screen-with-code-and-menu-options-34804017/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
