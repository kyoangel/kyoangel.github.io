---
layout: post
author: KAI
title: "開源、插件化、免費——DeepSeek Harness v0.1 讓我重新審視 Agent Harness 的選擇"
description: "2026 年 8 月 13 日 DeepSeek 釋出 MIT 授權的 agent harness 框架 v0.1，萬物皆插件設計讓工程團隊能彈性替換模型與沙箱，本文從技術經理視角評估導入現有 AI 工作流的可行性與風險。"
image: assets/images/posts/deepseek-harness-v01-agent-evaluation.jpg
categories: TechNotes AI
---

本週讓我停下來認真研究的，是 DeepSeek 在 8 月 13 日發布的 DeepSeek Harness v0.1 開發者預覽版。這個專案一上線就以 MIT 授權完整開源，四天內在 GitHub 累積超過 13.5 萬顆星，速度之快讓我不得不認真看待它。它的核心架構叫做 Cordis 元框架（meta-framework），整個設計哲學只有一句話：Everything is a Plugin——模型、工具、技能、Session、沙箱、檔案系統、Loop 邏輯、UI，全都是插件，可以自由混搭、替換與擴充。

作為長期在用 Claude Code 的 EM，我第一個念頭是：「這東西是直接對著 Claude Code 來的。」DeepSeek 也沒有試圖隱瞞這點，他們明確將 Harness 定位為 Claude Code 的開源替代方案。但真正讓我有興趣的，是那個 Trajectory View：所有模型看到的內容（system prompt、推理鏈、工具呼叫、結果、注入的 context）都會被記錄成一個 append-only 事件串流，讓開發者可以從任一節點 resume、fork、搜尋或重播整個 agent run。這對我來說不是噱頭，這是工程上真正需要的可觀察性（observability）。

假設我現在帶的是一個 8 人工程團隊——6 個後端、2 個 SRE，每兩週一個 sprint，目前每天的 Claude Code 使用量大概是 40 個 agent session，每月 AI 工具費用落在 4 萬台幣左右。如果 DeepSeek Harness 讓我們改用自架模型（例如 DeepSeek V4-Pro API）跑同樣品質的 coding agent 工作流，保守估計成本可能降至現在的三分之一以下。但「可能」這兩個字就是問題所在——我需要先知道它在我們實際任務上的表現，而不是 benchmark 上的數字。

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**
插件式設計理論上讓我們可以在沙箱層換掉底層實作，不動上層 Loop 邏輯，維運彈性確實提升了。但 v0.1 仍是開發者預覽版，表示我得自己跟進上游的 bug fix。如果半夜 on-call 掛起的是我們自己改過的 Harness 插件，RCA 時間成本不可輕忽。我的傾向是先只替換模型層插件，不動核心 Loop，把風險控制到最低。

**對 code review 流程的影響**
Trajectory View 讓我看到了 code review 的另一種可能：reviewer 不再只看最終 diff，而是可以重播 agent 的推理過程，直接看到它為什麼做出這個決定。這個功能如果能整合進 PR 流程，review 品質可以顯著提升。但目前還沒有現成的 GitHub PR 整合，需要我們自己串接，這是額外的工程成本，短期內我會讓它留在 POC 層，不急著整合。

**對 junior 工程師 onboarding 的影響**
「萬物皆插件」對 junior 是雙面刃。好的一面是每個插件邊界清楚，容易上手一個小模塊；壞的一面是整體心智模型更難建立——你要理解 Cordis 框架、事件串流、插件生命週期，才能真正 debug 複雜的 agent 行為。我不會直接丟官方文件給 junior，需要幫他們準備一份針對我們使用情境的導覽。

**技術債與長期維護成本**
v0.1 的 API 尚未穩定。如果現在就把內部工作流深度綁定 Harness 的插件介面，六個月後 v1.0 若有 breaking change，重構成本可能相當可觀。我的評估是：現在適合跑 POC，但不適合在正式流程上建立強依賴。讓我猶豫的是插件介面的版本承諾——DeepSeek 目前對 API 穩定性沒有給出明確的 SLA。

**採用時間軸建議（POC → 小規模試點 → 全面推行）**
我傾向分三個階段走。第一階段（接下來 4 週）：用 DeepSeek Harness 跑 POC，目標是把一個內部工具遷移過來，評估指標是任務完成率與 Trajectory View 的可讀性；若這兩個指標不輸 Claude Code，才進入第二階段。第二階段（2-3 個月）：選 1-2 個工程師在日常任務中切換使用，追蹤 context 命中率與工具呼叫失敗率；若 p95 任務時間沒有顯著惡化，再評估第三階段。第三階段（6 個月後）：等 v1.0 API 穩定後，才決定是否全面推行。每個階段的進入門檻都要量化，不能靠直覺決定。

---

這是我接下來幾週會持續追蹤的方向。DeepSeek Harness 讓我興奮的不是「免費」——免費從來不是採用工具的理由——而是它把 agent run 的可觀察性從事後 log 變成了可互動的執行軌跡，這個思路值得認真對待。如果你的團隊已經跑過 DeepSeek Harness 的 POC，或者你對插件式 harness 設計有不同的看法，我很想知道你們的盤算。

---
*封面圖片由 [ThisIsEngineering](https://www.pexels.com/photo/female-engineer-using-laptop-3862599/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
