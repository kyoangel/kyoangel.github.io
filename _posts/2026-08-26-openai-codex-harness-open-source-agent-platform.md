---
layout: post
author: KAI
title: "OpenAI Codex 開源 Harness：Harness Engineering 時代來了，我的團隊準備好了嗎？"
description: "OpenAI 於 2026 年 8 月 20 日以 Apache-2.0 授權開源 Codex Harness 框架，把 Agent 競爭主軸從模型層移向執行引擎層。身為帶領 8 人工程團隊的技術經理，我正在評估這個框架對工具鏈、code review 與 junior 工程師培育的具體衝擊與導入時機。"
image: assets/images/posts/openai-codex-harness-open-source-agent-platform.jpg
categories: TechNotes AI
---

本週最讓我停下來思考的，是 OpenAI 在 2026 年 8 月 20 日推出的一個動作：他們以 Apache-2.0 授權正式開源了 Codex Harness，也就是驅動 Codex 這個 AI coding agent 背後的執行引擎。開源的範圍包含三個核心元件：`codex exec`（CLI 工具）、Codex SDK，以及 `app-server`（核心引擎執行伺服器）。同一天，OpenAI 的 developer blog 也發了一篇「Codex as a platform」，明確宣告他們把 Codex 的定位從「工具」升格為「基礎設施平台」。

這件事之所以讓我在意，不是因為又多了一個開源專案，而是因為它正式確認了一件我最近幾個月一直在觀察的趨勢：**AI coding 的競爭主軸，正在從「模型本身有多強」移向「Harness 工程做得好不好」**。Harness 是什麼？簡單說，就是包在模型外面的那層執行系統，負責蒐集 context、呼叫工具、管理 sandbox 隔離、串流執行進度、在多輪對話之間保持工作狀態。Claude Code 有自己的 harness；Cursor 有自己的 harness；現在 OpenAI 直接把 Codex 的 harness 拆出來開源，讓任何人都可以在上面建構自己的 agent 工作流程。

---

### 假設情境：一個 8 人全端工程團隊

讓我用一個具體情境想像一下。假設我帶領一個 8 人的全端工程團隊，目前的工作節奏大約是每兩週一個 sprint，每週大約有 30 到 40 個 PR 需要 review，CI/CD 走 GitHub Actions，主要使用 Claude Code 做輔助開發。這個情境下，Codex Harness 開源帶來的最直接想像是：**我們可以自己客製化 agent loop**，比如讓 agent 在跑完測試之後自動開 PR、或是在發現 linting 錯誤時自動送修正 commit，而不用依賴任何商業平台的固定流程。

更具體的影響是 sandbox 設計。Codex Harness 這次的開源版本針對 sandbox 做了更嚴格的隔離：限制 mount point、封鎖特定 syscall，減少 agent 在自動編輯模式下的非預期 filesystem 寫入。對我們這種有 infra-as-code 的團隊來說，這是一個不小的進展——過去最讓我對「讓 agent 直接 commit」這件事猶豫的，就是不確定 agent 會不會在沙箱外動到不該動的檔案。現在有一套可審計、可自訂的 sandbox 規範，感覺踏實很多。

---

### 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**

短期來說，引入 Codex Harness 意味著我們的維運清單多了一個新物件要管：harness 本身的版本、設定檔、sandbox policy。如果 agent 在半夜跑批次任務時出現意外行為，第一線的 on-call 工程師需要知道怎麼看 harness 的 event log，而不是只看應用程式本身的 log。這個學習曲線是真實存在的，我不打算假裝它不重要。不過，如果導入得當，agent 自動處理重複性的 hotfix 流程（例如自動偵測 lint error 並送 patch），反而可以降低夜間人工介入的頻率。我的傾向是：短期維運成本會上升，但中期有機會下降，前提是一開始就認真做好 harness 的可觀測性。

**對 code review 流程的影響**

這是我最在意的面向。如果 agent 可以自己開 PR，誰來 review agent 開的 PR？我的直覺是：必須維持「人類審核最後一關」的原則，不能因為是 agent 做的就降低 review 標準。但這也意味著 code review 的性質會改變——reviewer 要看的不再只是「這段邏輯對不對」，還要看「agent 的工具呼叫序列是不是有意義」「sandbox 有沒有被正確約束」。這對 senior 工程師的要求變高了，對工具鏈的可觀測性也提出了更高要求。我認為我們需要在 review checklist 裡加入 harness 行為的審核欄位，而不是讓這件事隱形在 CI log 裡。

**對 junior 工程師 onboarding 的影響**

這讓我有點猶豫。如果 junior 工程師一入職就在一個「agent 幫你做很多事」的環境裡，他們還會不會真正理解底層發生了什麼？我的傾向是：在 onboarding 的前三個月，先讓 junior 工程師以「觀察 agent 行為」而非「讓 agent 幫自己寫 code」的方式接觸 harness，逐步建立對工具呼叫流程的直覺，再開放 agent-assisted 的工作模式。如果跳過這個階段，我擔心的是三年後我們團隊裡沒有人真正理解 agent 在做什麼，debug 的能力會大幅退化。

**技術債與長期維護成本**

Codex Harness 是 Apache-2.0，這代表我們 fork 之後可以自由修改，但也意味著必須自己承擔維護 fork 的成本。如果 upstream 快速迭代（以 OpenAI 的節奏來看，這幾乎是確定的），我們 fork 的版本很快就會跟主線脫節。我的判斷是：**不要 fork，盡量跟上 upstream，只在 sandbox policy 和工具呼叫設定做本地化客製**，這樣才能在享受開源紅利的同時控制技術債。採用開源版本還有一個隱性成本：當 OpenAI 修了一個安全漏洞，我們需要有人在第一時間追蹤並升版，這件事不會自動發生。

**採用時間軸建議**

我設想的節奏大概是這樣：

- **POC（第 1～4 週）**：找 1 到 2 位 senior 工程師，在非生產環境的測試 repo 裡跑 Codex Harness，主要觀察 sandbox 行為是否符合預期、event log 的可讀性如何、工具呼叫序列是否透明。進入下一階段的指標：sandbox 隔離驗證通過，沒有非預期的 filesystem 寫入，team 能在 30 分鐘內看懂一次完整的 agent run log。
- **小規模試點（第 5～12 週）**：選一個低風險的內部工具 repo，讓 agent 自動處理 linting fix 和測試補全，由 1 到 2 位工程師 review agent PR。進入下一階段的指標：agent PR 的 review 時間不超過人工 PR 的 1.5 倍，且 review 後需要人工修改的比例低於 20%。
- **全面推行（第 13 週起）**：逐步在主要 repo 開放 agent-assisted 工作流程，同時建立完整的 harness monitoring dashboard，並將 harness 行為審核納入正式 code review checklist。

---

這是我接下來幾個月會持續觀察的方向。Codex Harness 開源這件事，我把它看成「時間點到了」的訊號，而不是「現在就要全面導入」的指令。AI coding agent 的基礎設施正在從黑盒子變成可審計、可組合的元件，這對願意投入工程資源的團隊來說是個機會窗口。如果你的團隊也在評估類似的方向，我很想知道你們在 sandbox 設計和 code review 流程上是怎麼取捨的，特別是 junior 工程師的培育這一塊，我覺得是這波轉型裡最難拿捏的部分。

---
*封面圖片由 [Daniil Komov](https://www.pexels.com/photo/close-up-of-computer-screen-with-code-and-menu-options-34804017/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
