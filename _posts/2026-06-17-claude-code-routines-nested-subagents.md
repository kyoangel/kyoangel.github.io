---
layout: post
author: KAI
title: "當 AI agent 開始自己排班：Claude Code Routines 與巢狀 sub-agent 讓我重新想了一次團隊的自動化邊界"
description: "Claude Code 2.1 推出 Routines 排程功能與五層巢狀 sub-agent，身為 Engineering Manager，評估這次更新對團隊自動化邊界的影響與分階段導入建議。"
image: assets/images/posts/claude-code-routines-nested-subagents.jpg
categories: TechNotes AI
---

這幾天我在看 Claude Code 2.1 更新，注意到兩個功能：一是「Routines」，把 prompt、可存取的 repo 與工具存成排程任務，依時間、API 或 GitHub webhook 觸發，在雲端自動跑，不需要我的筆電開著；二是巢狀 sub-agent，任何 sub-agent 都能再生出子代理，最深五層，且自 v2.1.77 起，跑完的 sub-agent 可被續命——orchestrator 對它的 agentId 發訊息，就能接回完整上下文繼續跑。

第一次讀到「排程後自己醒來工作」加「五層巢狀分工」放在一起，我有點被震到——這不再是「我下指令、AI 寫一段 code」的工具，而是會自己分工、自己排班、能在背景持續存在的系統。所以這次我想認真盤算：如果要把它帶進團隊，我會怎麼評估。

## 假設情境

假設我們團隊 8 個工程師，維護 3 個服務，每天兩次部署，PR 靠人工 review、SLA 當天回覆。目前已把 Claude Code 用在日常開發，但都是互動式手動操作，沒有排程或自動觸發。導入 Routines 後，最可能先做每天凌晨自動巡邏——掃 CI 失敗、掃漏洞、寫每日 PR 摘要，再用巢狀 sub-agent 拆成三個子代理平行處理。這代表我們第一次有機會把部分值班工作轉給會自己分工的系統，而不只是寫死的 cron job。

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響。** 我興奮但謹慎。Routines 讓半夜自動巡邏幾乎零成本，對輪值壓力大的 8 人團隊很誘人，但我會堅持：它只負責偵測與初步診斷，任何會改變生產狀態的動作在判斷穩定前一律要人工確認。巢狀展開到三、四層我反而更緊張，出錯時得先查清是哪一層子代理判斷錯。

**對 code review 流程的影響。** 若由 PR webhook 觸發，我會先讓它做摘要與風險標註，不取代 reviewer 的核可權。我更擔心 reviewer 看到「沒問題」標註後不自覺降低審視強度，這是心理上的卸責，所以我會明確溝通：AI 標註是提示，不是背書。

**對 junior 工程師 onboarding 的影響。** 我反而樂觀。新人能看到任務怎麼被拆解、平行化、合併，是活的系統設計教材。但我會要求他們先手刻過一次類似流程，再用自動化版本，避免只學會下指令卻沒建立判斷力。

**技術債與長期維護成本。** 這是我最猶豫的地方。Routine 的 prompt 本質是行為定義，卻不像程式碼那樣容易版控、測試，半年後可能沒人記得它為何這樣寫。我會要求每個 Routine 都有文件與 owner，設定檔進 repo 受版控管理。

**採用時間軸建議。** 分三階段。POC 約兩週，只在低風險 repo 跑唯讀的掃描＋摘要，看輸出穩不穩定、有沒有明顯誤判。小規模試點約一個月，讓它做 PR 標註但不執行任何寫入動作，看 reviewer 對標註的採信率與是否因它出包漏看問題。連續兩週沒有重大誤判，我才考慮全面推行，且仍把改變生產狀態的動作排除在自動化外。

這是我接下來幾週會持續觀察的方向，尤其想看巢狀 sub-agent 在真實混亂的 repo 裡會不會失控。如果你的團隊也在評估類似工具，我很想知道你們在自動化邊界這條線上怎麼畫的。

---
*封面圖片由 [Pavel Danilyuk](https://www.pexels.com/photo/close-up-shot-of-white-toy-robot-on-blue-and-pink-background-8294663/) 提供，來源：[Pexels](https://www.pexels.com)*

---

**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
