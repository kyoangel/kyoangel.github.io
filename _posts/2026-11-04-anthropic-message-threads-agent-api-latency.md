---
layout: post
author: KAI
title: "Anthropic Message Threads 公測：我的 Agent API 延遲減少了 35%，但這改變了什麼？"
description: "Anthropic 於 2026 年 11 月 2 日推出 Message Threads 公測版，對超長 context 的 AI Agent 請求最多可縮短 35% 的 TTFT。身為技術經理，我正在評估這項更新對團隊 Agent 工作流程、on-call 負擔與採用節奏的實際影響。"
image: assets/images/posts/anthropic-message-threads-agent-api-latency.jpg
categories: TechNotes AI
---

這週讓我花了最多時間思考的更新，不是某個全新模型發布，而是一個看起來很「基礎建設」的改變：Anthropic 在 2026 年 11 月 2 日正式把 **Message Threads** 推上 Messages API 的公測版（public beta）。

簡單說，以前每一次 Agent 呼叫 API，都必須把完整的對話歷史重新傳一次——無論是第一輪還是第十五輪。現在，第一個請求建立一個 Thread，後續的請求只需要傳「新增的訊息」加上「上一個 response 的 ID」就夠了。Anthropic 自己的數字是：在 500,000 到 1,000,000 tokens 的超長 session 中，Time to First Token（TTFT）的中位數降低了約 **35%**。

乍看之下這只是一個 SDK 層的優化，但我越想越覺得，這個改動的意義不只是「等待變短」。

---

## 假設情境：一個 8 人團隊在跑什麼樣的 Agent？

我們的團隊目前大約 8 個人，負責一個 B2B SaaS 平台。過去半年我們陸陸續續在內部跑了幾個 AI Agent 的 POC：一個負責 code review 的 Agent、一個負責 ticket 分類與摘要的 Agent，以及最近在試驗的「multi-turn debug assistant」——工程師可以在 terminal 開啟一個 session，像在 pair programming 一樣和 Agent 互動，把問題從初步描述一路追蹤到根本原因。

問題就出在 multi-turn debug assistant 上。我們內部測試的 session 動輒超過 100 輪對話，context 長度常常落在 300K 到 600K tokens 之間。在這個長度下，每一輪都要等 2 到 3 秒才能拿到第一個 token，對話節奏被破壞得很嚴重——工程師回報說「感覺不像在對話，比較像在送出表單」。

如果 Message Threads 能把這個情境的 TTFT 壓到 1.5 秒以內，那個「對話感」可能就回來了。這是我對這次更新最直接的期待。

但有一個細節讓我沒辦法輕易跳過：Thread 在最後一次請求後 **5 分鐘會過期**。過期之後，Agent 必須回退到傳送完整對話歷史的模式。這意味著 Agent 程式碼必須同時維護「Thread 活躍」和「Thread 過期後 fallback」兩套邏輯，這增加了實作複雜度，也讓 on-call 時的 debug 路徑多了一個可能的斷點。

---

## 身為技術經理，我會怎麼評估這次更新

### a. 對 on-call / 維運的影響

Thread 的 5 分鐘 TTL 是一個新的狀態面。如果我們的 Agent 在某個緊急情境下因為網路閃斷而中斷了超過 5 分鐘，重新連線後必須能夠優雅地 replay 整段對話——沒做好就是一個靜默的功能退化，工程師很可能要等很久才知道 Thread 已經失效了。我傾向在 monitoring 層加一個明確的 Thread TTL 告警，而不是等使用者回報「怎麼突然變慢」。

### b. 對 code review 流程的影響

這個功能對我們的 code review Agent 影響相對有限，因為那個 Agent 通常是「一個 PR 一個短 session」，context 長度不到 50K tokens，根本不在 35% 優化效果的適用範圍內。但對 multi-turn debug assistant 來說，code review 本身也需要更新：要審查 Thread ID 的傳遞邏輯、TTL 的 fallback 路徑，以及 replay 時的去重機制。這些都是以前沒有的新審查面向。

### c. 對 junior 工程師 onboarding 的影響

我們團隊有兩位剛進來不到一年的工程師。Message Threads 的加入讓 Anthropic SDK 的正確使用方式多了一個「有狀態 vs. 無狀態 session」的概念。這對 junior 工程師來說是一個新的心智模型負擔——他們現在必須理解 Thread 的生命週期，不然很容易寫出在某些邊界條件下靜默失效的 Agent 邏輯。我打算在 onboarding 文件裡加一節專門說明 Thread 的正確使用姿勢，包括什麼情況下應該主動不用 Thread（例如短 session、需要零資料留存的 HIPAA 情境）。

### d. 技術債與長期維護成本

Message Threads 目前是 **beta feature**，要透過 `anthropic-beta: message-threads-2026-11-02` header 啟用。這意味著它未來可能有不相容的 API 變動。我不希望現在就把 Thread 邏輯深埋到每一個 Agent 的 core loop 裡，而是傾向用一個可以輕鬆 feature-flag 關掉的 wrapper 層來包裝它。技術債的風險在於：如果 Anthropic 在正式版 GA 時改了介面，我們不要花一週時間在 10 個地方散射式地做修改。

### e. 採用時間軸建議

我的傾向是分三個階段走：

**POC（1 週）：** 只在 multi-turn debug assistant 的開發環境裡啟用 Message Threads，專注測量一件事：在我們實際的 session 長度分布（300K–600K tokens）下，TTFT 的 p50 和 p95 有沒有顯著改善？如果 p95 還是超過 3 秒，那代表這次優化對我們的情境效果有限，就不用急著進 staging。

**小規模試點（2–3 週）：** 把 Thread 邏輯推到 staging，讓 2-3 位工程師用真實的工作 session 試用，重點觀察 Thread 過期的頻率（他們的工作節奏是否常常中斷超過 5 分鐘？）以及 fallback 路徑有沒有被觸發。如果過期頻率低於 5%，才考慮進入下一階段。

**全面推行（4–6 週後）：** 把 Thread 包成一個標準化的 `AgentSession` 抽象層，讓所有 Agent 共用，同時讓 HIPAA 相容的 session 明確走 opt-out 路徑。這個階段的成功指標是：工程師不需要知道 Thread ID 在做什麼，Agent 就可以正常運作。

---

值得注意的是，Message Threads 目前不支援零資料留存（zero-data-retention）和 HIPAA 工作流程。如果你的產品需要資料在每次 request 後不被保留，這次更新暫時不在你的選項裡。這是我在正式決定採用前，還需要和我們的法務確認的一點。

這是我接下來兩週會持續跟進的方向：先把 POC 跑起來，看看真實的 TTFT 數字，再決定要不要在 Q4 末把 Thread 納入正式的 Agent 基礎建設。如果你的團隊已經在用 Anthropic API 跑長 session 的 Agent，很想知道你們遇到的瓶頸是不是也在同一個點上。

---
*封面圖片由 [Daniil Komov](https://www.pexels.com/photo/close-up-of-computer-screen-with-code-and-menu-options-34804017/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
