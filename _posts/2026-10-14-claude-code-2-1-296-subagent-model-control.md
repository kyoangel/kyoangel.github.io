---
layout: post
author: KAI
title: "Claude Code 2.1.296 的 Subagent 模型鎖定：我打算怎麼用這個功能重新規劃團隊的 AI 工作流程"
description: "Anthropic 在 2026 年 10 月 9 日發布 Claude Code 2.1.296，新增 workflow 層級的 subagent 模型控制。身為帶領工程團隊的技術經理，這次更新讓我重新評估 AI coding agent 的成本結構與工作流程設計。本文分享我對 on-call、code review 與 junior onboarding 的實際盤算。"
image: assets/images/posts/claude-code-2-1-296-subagent-model-control.jpg
categories: TechNotes AI
---

本週有兩件事同時發生，讓我在週三的下午坐下來重新翻了一遍我們團隊的 AI 工具設定。

第一件：Anthropic 在 10 月 9 日推出了 Claude Code 2.1.296，其中最讓我注意的新功能是「workflow 層級的 subagent 模型控制」——也就是說，你現在可以在 pipeline 設定裡，明確指定每個 subagent 要使用哪個模型，而不是讓整個 workflow 的所有 agent 都跑同一個預設模型。第二件：就在差不多同一時間，Anthropic 在 10 月 7 日正式發布了 Claude Haiku 5.5，定價是每百萬 input token $0.10、output token $0.50，且具備 1M token 的 context window。這兩件事放在一起，對我來說意義完全不一樣了——等於是 Anthropic 給了你一個便宜又夠快的小模型，同時又給了你控制整個 agent pipeline 的旋鈕。

以前我一直覺得「用 AI coding agent 的成本很難控」。我們現在大部分的 workflow 都是讓所有任務跑 Opus 5.5 或 Sonnet 5.5，但其實有很多中間步驟——像是「把一段 git diff 整理成 PR 描述草稿」或是「搜尋 codebase 找出哪些地方引用了某個 API」——根本不需要最強的模型。這次更新讓我覺得，是時候重新設計我們的 agent workflow 了。

---

## 一個假設情境：8 人工程團隊，每週跑 200 次 agent workflow

想像一個 8 人的工程團隊，每週大約跑 200 次 Claude Code agent workflow。這些 workflow 包含：CI/CD 觸發的自動化 code review、PR 草稿生成、bug triage 摘要、以及每天早上的 on-call 告警彙整。在 2.1.296 之前，大部分 workflow 都預設使用 Sonnet 5.5 貫串所有步驟。

假設每次 workflow 平均用掉 20K input token + 2K output token，Sonnet 5.5 的成本大約是：

- Input: 200 × 20K = 4M tokens × $0.30/M = **$1.20**
- Output: 200 × 2K = 400K tokens × $1.50/M = **$0.60**
- 每週合計約 **$1.80**，一個月約 $7.2

這個數字看起來很小，但如果我們把其中 60% 的「低複雜度步驟」改走 Haiku 5.5，同樣的 token 量只需要約 $0.12。整個 pipeline 的月成本可以壓到 $3-4 以下，而且理論上速度還更快，因為 Haiku 5.5 的 latency 比 Sonnet 5.5 低很多。

這個計算雖然粗略，但重點不在於省了多少錢，而在於：現在我有工具去做這件事了。

---

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**

我們目前的 on-call workflow 是：告警觸發 → 用 agent 撈相關 log → 生成摘要 → 傳給 on-call engineer。這個流程的「撈 log」步驟其實非常適合跑 Haiku 5.5，因為它只需要搜尋和整理，不需要深度推理。但「生成給人看的摘要」這一步，我還是傾向保留 Sonnet 5.5，因為它要能把 stack trace 和業務邏輯串起來說清楚。有了模型分層控制，我可以明確地做這個拆分，而不是被迫選一個折衷方案。讓我猶豫的是：這樣拆分之後，中間的 context 傳遞要怎麼設計？如果 Haiku 5.5 的摘要品質不夠好，Sonnet 5.5 後段能不能補救，還是會因為前段資訊已經失真而做出錯誤判斷？這需要跑一些 A/B 測試才能確認。

**對 code review 流程的影響**

我們目前讓 Claude Code 在每個 PR 開出來之後做一次初步 review，主要是找 trivial 的 bug 和 style 問題。這個任務理論上也可以走 Haiku 5.5，但我有疑慮：Haiku 5.5 在分析跨多個檔案的邏輯依賴時，表現是否還夠穩定？如果它漏掉一個 race condition，但 Sonnet 5.5 本來可以抓到，那省的成本其實是用更高的風險換來的。我的初步判斷是：PR review 的「掃描 style 和明顯錯誤」可以走 Haiku，但「跨檔案邏輯分析」還是要保留 Sonnet 或 Opus。

**對 junior 工程師 onboarding 的影響**

這次更新對 onboarding 的影響是間接的，但我覺得很有意思。以前我們讓 junior 工程師自己決定要不要用 AI agent 幫忙看 codebase，但因為成本不夠透明，有人怕用、有人亂用。現在如果我在 workflow 設定裡明確地做了「這個步驟用 Haiku，那個步驟用 Sonnet」的分層，等於是把「什麼任務需要多少 AI 能力」的判斷顯性化了。這對 junior 工程師的認知訓練反而是好事——他們可以從 workflow 設計裡學到：不是所有問題都要拿最大的槌子打。

**技術債與長期維護成本**

新增了模型分層設定之後，我擔心的是 workflow 設定檔會變得越來越複雜，難以維護。每個 workflow 現在要明確標注每個 subagent 用哪個模型、原因是什麼，這對新進的 team member 來說會是一道閱讀門檻。另外，Haiku 5.5 是新模型，如果三個月後 Anthropic 推出 Haiku 5.6 然後把 5.5 deprecated，我就要重新評估和調整所有 workflow，這個維護成本要提前算進去。

**採用時間軸建議**

我的計劃大概是這樣：

1. **POC（第 1-2 週）**：找兩個最低風險的 workflow（例如 on-call log 撈取、PR 描述草稿生成），把其中一個 subagent 改成 Haiku 5.5，跑一週，用人工比對品質差異。指標：品質降級率 < 5%（由 reviewer 標記），latency 下降 > 20%。
2. **小規模試點（第 3-6 週）**：把 style check 類的 PR review 也移到 Haiku，開始建立「模型分層矩陣」（任務複雜度對應模型選擇）。指標：junior engineer 對 AI 輔助品質的滿意度問卷分數不下降，on-call 告警回應時間縮短。
3. **全面推行（第 7 週+）**：所有 agent workflow 都套用分層模型設定，並在 CI/CD pipeline 裡加入自動化 cost tracking。指標：月 AI 成本下降幅度是否符合預估、team 整體 cycle time 是否維持或改善。

---

接下來幾週，我會持續觀察 Haiku 5.5 在我們實際 workload 上的表現，特別是那些「感覺簡單但其實有隱含上下文依賴」的任務。這種任務最容易在降模型時踩到坑。如果你的團隊也在評估類似的模型分層策略，我很想知道你們踩過什麼坑，或是有沒有比我更系統化的評估框架——歡迎交流。

---
*封面圖片由 [Daniil Komov](https://www.pexels.com/photo/close-up-of-computer-screen-with-code-and-menu-options-34804017/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
