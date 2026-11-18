---
layout: post
author: KAI
title: "Claude Code v2.1.323 的 Code Mode：當 AI 開始用 JavaScript 呼叫自己的工具"
description: "Claude Code v2.1.323 推出實驗性 Code Mode，讓 Claude 以 JavaScript 動態呼叫工具，改變 agent loop 的執行方式。身為技術經理，我正在評估這項更新對團隊維運、code review 與 junior onboarding 的潛在影響與導入時機。"
image: assets/images/posts/claude-code-code-mode-javascript-agent-loop.jpg
categories: TechNotes AI
---

這週在追蹤 Claude Code 的更新日誌時，我注意到一個讓我重新思考的細節：v2.1.323 在 2026 年 11 月 15 日這週靜悄悄地加入了一個實驗性的 opt-in 功能，名字叫做 **Code Mode**。描述很簡短——「Claude 以 JavaScript 呼叫自己的工具」——但我盯著這句話看了很久，因為這句話背後的意涵遠比版本號更大。

在這之前，Claude Code 的 agent loop 是透過一套固定的 tool-calling schema 在運作的：Claude 生成一個結構化的 JSON 請求，harness 解析後執行對應的工具，然後把結果送回去。這套模式穩定、可預測，也正因為如此，它的天花板是固定的。Code Mode 打破的就是這個假設：讓 Claude 自己寫 JavaScript 來動態組合工具呼叫。這等於把「怎麼呼叫工具」這層邏輯的控制權還給了模型本身。

同一個版本週期，v2.1.321 也修補了幾個 permission 和 sandbox 的缺口。把這兩件事放在一起看，我覺得 Anthropic 在為一個更有彈性的 agent execution 層做準備——先把安全圍欄補好，再開放更高自由度的執行模式。這個先後順序讓我對這次更新多了幾分信心。

---

**假設一個具體的情境**

我們團隊有八個人：五個後端工程師、兩個全端、一個 SRE。我們目前用 Claude Code 的頻率大概是每天 30-40 次 agent 任務，主要集中在寫測試、做 code review 輔助、還有一些 boilerplate 生成。部署節奏是每週兩次，CI pipeline 大約跑 15 分鐘。

在這個情境下，Code Mode 最直接的影響是：某些現在需要我們手動串接多個工具的任務（例如「讀這個 API spec，然後生成測試，再把測試跑起來，失敗的話調整」），理論上可以讓模型自己用 JavaScript 把整個 pipeline 組起來，不再需要人在中間當膠水。

聽起來很美。但「理論上」這個詞讓我停頓了一下。

---

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**

Code Mode 是 opt-in，所以不會影響現有的 agent 任務——除非有人主動去開。這一點讓我稍微放心，因為我最怕的是「更新後原本穩定的 workflow 突然行為改變」。但這也帶出另一個問題：一旦有人開始在正式環境的 agent 任務裡使用 Code Mode，debug 的難度會上升。現在出問題，你可以看 JSON tool call 知道 Claude 想做什麼；Code Mode 下，你需要讀 Claude 生成的 JavaScript，而那段 JavaScript 可能每次都不一樣。on-call 工程師需要額外的除錯能力。我現在的傾向是：在正式環境的 CI/CD agent 任務裡，先不開 Code Mode，把它限制在開發環境的探索性任務。

**對 code review 流程的影響**

如果 Code Mode 開始用於生成測試或修 bug，PR 的 diff 裡可能會出現更複雜的程式碼——因為模型有更大的自由度去做「跳步」的組合。這對 reviewer 來說是個挑戰：你不只要審最終的程式碼，還需要思考「這段邏輯是怎麼被生成的，有沒有走了捷徑但跳過了某個重要的中間驗證」。我打算在試點期間要求 PR description 裡加一行「是否使用 Code Mode」，讓 reviewer 有心理準備。

**對 junior 工程師 onboarding 的影響**

這一點讓我比較猶豫。我們目前用 Claude Code 輔助 junior onboarding 的方式是：讓他們先看 Claude 的 tool call JSON，理解 agent 在做什麼決策，再對照自己寫的程式碼。這套方式有個隱含的前提：agent 的思考過程是「可讀的結構」。Code Mode 下，這個可讀性可能會降低，因為 JavaScript 的自由度更高，junior 可能更難從中學習「agent 為什麼這樣決策」。短期內我不打算讓 junior 在 onboarding 階段使用 Code Mode。

**技術債與長期維護成本**

這是我最不確定的面向。Code Mode 生成的 JavaScript 是否會被存下來？是每次 session 重新生成？如果是後者，那維護成本相對低；如果前者，我們就需要一套新的版本控制策略。目前文件還不夠清楚，我打算在 POC 階段把這個問題搞清楚再說。另外，JavaScript 生成的 tool orchestration 邏輯如果和業務邏輯耦合太深，可能會製造難以追蹤的技術債。

**採用時間軸建議**

我會分三個階段走：

第一階段（**POC，2-3 週**）：讓兩個資深工程師在開發機上用 Code Mode 做五個不同類型的任務，記錄 token 消耗、執行時間、錯誤率，以及和 standard mode 的輸出差異。進入下一階段的指標：錯誤率低於 standard mode 的 1.5 倍，且有至少一個任務類型呈現明顯的效率提升（例如把三個連續 tool call 合併成一個流程，節省 30% 以上的時間）。

第二階段（**小規模試點，4-6 週**）：在開發環境的 CI pipeline 中，針對測試生成任務開放 Code Mode，監控 flaky test 比率與 CI 時間。進入下一階段的指標：flaky test 比率未上升，工程師對 PR diff 可讀性的滿意度（簡單問卷）維持在基線以上。

第三階段（**全面推行評估**）：根據前兩階段的數據，決定是否在正式環境的 agent 任務中也開放 Code Mode，以及是否需要訂定使用規範或訓練材料。

---

這是我接下來幾週會持續觀察的方向。Code Mode 本質上是把 agent 的執行層往上推了一層——從「執行指令」到「自己設計執行路徑」，這個轉變如果做得好，可以大幅提升 agent 在複雜任務上的能力；但如果沒有配套的可觀測性工具和使用規範，它也可能成為一個難以追蹤的黑盒子。如果你的團隊也在評估 Claude Code 的 Code Mode，我很想知道你們打算怎麼處理「generated JavaScript 的可審計性」這個問題——這是我目前最不確定的部分。

---
*封面圖片由 [Daniil Komov](https://www.pexels.com/photo/close-up-of-computer-screen-with-code-and-menu-options-34804017/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
