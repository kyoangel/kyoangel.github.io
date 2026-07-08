---
layout: post
author: KAI
title: "Claude Code Dynamic Workflows 讓我重新思考：AI Agent 的 orchestration 層，才是真正的護城河"
description: "Anthropic 於 2026 年 6 月 30 日發布 Claude Sonnet 5，並同步推出 Claude Code Dynamic Workflows 平行代理協調功能。身為技術經理，我從 on-call 維運、code review、junior onboarding 與技術債等面向評估是否導入，並提出 POC 到全面推行的具體時間軸建議。"
image: assets/images/posts/claude-code-dynamic-workflows-sonnet5.jpg
categories: TechNotes AI
---

六月底的一週，我的通知欄裡同時跳出兩件事：Anthropic 在 6 月 30 日正式發布 **Claude Sonnet 5**，然後幾乎同一時間，Claude Code 也悄悄上線了 **Dynamic Workflows** 功能——一個可以讓 AI 自己決定何時拆解任務、動態產生 orchestration 腳本、讓多個子代理平行執行的機制。說悄悄，是因為公告的措辭很低調，但工程社群的反應完全不低調。

Sonnet 5 的幾個數字讓我注意到它不只是版本號遞增：它在 agentic search 和 computer use 任務上已逼近 Opus 4.8 的表現，且 introductory 定價到 8 月底之前是每百萬 input token 2 美元、output 10 美元，比 Sonnet 4.6 的同等使用情境便宜不少。更關鍵的是，它原生支援 **1M token 的 context window**，這個數字對我們這種 monorepo 體質的團隊意義重大。Dynamic Workflows 本身則是在研究預覽（research preview）階段就開放給 Max、Team、Enterprise 方案，以及透過 API 接入的使用者，它不需要手動寫 orchestration 腳本——Claude 自己讀懂你的目標，拆出子任務，平行跑，然後比對結果再迭代，中斷了還能從上次進度續跑。

這兩件事合在一起，讓我覺得不太對勁——不是壞的不對勁，而是「這個組合如果真的可以這樣運作，我們現在的工作方式可能要調整一些假設」那種感覺。

## 假設一個具體情境

我們團隊目前 8 人，後端用 TypeScript + NestJS，部署在 AWS ECS，PR review 流程平均一個 PR 從開出到 merge 要 1.5 天，主要卡在 reviewer 檔期和 context-switching。CI pipeline 跑完大約 18 分鐘。junior 工程師平均需要三週才能獨立送出第一個不需要大改的 PR。

現在想像把 Dynamic Workflows 接進來：一個資深工程師描述「幫我 migrate 這個 auth module，保留現有的 test coverage，列出所有我們目前不符合 OWASP TOP 10 的地方，然後出一個分段計畫」，Claude Code 自己拆成三個並行子代理，一個讀現有 codebase、一個跑 AST 分析、一個參照安全規範，最後整合結果。這整件事如果以前要手動做，資深工程師大概要花半天，現在可能壓縮到 15-30 分鐘的監督時間。

問題是：節省下來的時間要去哪裡？這才是我真正想弄清楚的。

## 身為技術經理，我會怎麼評估這次更新

**a. 對 on-call / 維運的影響**

Dynamic Workflows 最直觀的想像用途是「深夜的 incident triage」，但我現在不會這樣用。原因很簡單：它消耗的 token 量遠高於一般 Claude Code 工作階段，Anthropic 自己也提醒要從小的、範圍明確的任務開始。深夜 on-call 的時間壓力和 token 成本疊在一起，不是好的組合。我傾向把它用在預防性的維運工作——例如週期性地讓它掃 dependency 更新、找潛在的 breaking change，而不是緊急修復。

**b. 對 code review 流程的影響**

這裡讓我最感興趣，也最讓我猶豫。Dynamic Workflows 可以讓 AI 在送出 PR 之前就自己做一輪 review——不是 linter，而是語意層次的「這段邏輯有沒有跟其他模組的假設衝突」。如果這真的可靠，我們的 review 時間應該會縮短，reviewer 可以聚焦在架構決策而不是低階的 bug hunting。但我擔心的是「reviewer 越來越不讀 code」的長期效應，這個我需要在試點階段特別設計指標來追蹤，例如 reviewer 給出實質性意見的比率有沒有下降。

**c. 對 junior 工程師 onboarding 的影響**

Sonnet 5 的 1M context 加上 Dynamic Workflows，理論上可以讓 junior 工程師更快理解一個陌生的 codebase：「幫我解釋這個 repository 的架構，從資料流的角度，用我這個背景（給一份自我介紹）能理解的方式」。但我更擔心的是相反的方向——如果 junior 工程師從一開始就習慣讓 AI 幫他讀 code，他自己建立的 mental model 夠不夠扎實？這件事我沒有答案，但我會在試點階段設計一個「AI 關掉後的能力評估」，確保工具是加速器而不是替代品。

**d. 技術債與長期維護成本**

Dynamic Workflows 產出的 code 或 plan，有一個我目前還沒完全想清楚的風險：**orchestration 層本身會不會變成技術債？** 當它動態產生的腳本越來越多，這些腳本的可讀性、可稽核性、以及日後要 debug 的成本是什麼？Anthropic 說進度可以斷點續跑，但我想知道當六個月後一個新人要回頭看「這個 workflow 當初為什麼這樣設計」，他能找到答案嗎？目前我的直覺是，要對 AI 產生的 workflow 設計一套命名規範和 changelog 機制，就像我們對 migration script 做的事一樣。

**e. 採用時間軸建議**

- **POC（第 1-3 週）**：找一個已經結束、結果已知的歷史任務，讓 Dynamic Workflows 重新跑一遍，比對輸出品質。進入下一階段的指標：AI 的輸出在沒有額外 prompt tuning 的情況下，被資深工程師評為「可直接參考」的比率 ≥ 60%。
- **小規模試點（第 4-8 週）**：選 1-2 個資深工程師，在實際的功能開發或技術債清理任務中使用，每週做 15 分鐘回顧。進入下一階段的指標：任務完成速度提升 ≥ 20%，且 reviewer 在 PR 上的實質性意見數沒有明顯下降（代表 review 品質沒被侵蝕）。
- **全面推行（第 9 週起）**：配套措施——內部使用規範文件、token 預算監控 dashboard、至少一次「AI 關掉的應變演練」。

---

接下來幾週，我會特別盯著 token 消耗的實際數字，以及社群裡關於「Dynamic Workflows 的 orchestration 腳本可讀性」的討論。這個功能的技術邊界還沒有被充分探索，而邊界在哪裡，往往是在真實生產情境裡踩過幾次才會清楚。如果你的團隊也在評估類似的導入路徑，或是已經在用 Dynamic Workflows，我非常想聽聽你們碰到的實際障礙——特別是 token 成本控制這塊。

---
*封面圖片由 [Magda Ehlers](https://www.pexels.com/photo/robotic-arm-in-modern-industrial-setting-35280311/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
