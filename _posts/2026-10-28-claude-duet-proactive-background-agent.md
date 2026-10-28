---
layout: post
author: KAI
title: "Claude Duet 發布了，我開始認真想：AI 主動盯著我們的工作，是好事還是風險？"
description: "Anthropic 於 2026 年 10 月 21 日推出 Claude Duet 研究預覽版，這款主動型背景 Agent 會持續監看使用者連結的應用程式並在重要操作前徵求許可，讓技術經理不得不重新評估 AI 工具在工程團隊日常流程中的角色與邊界。"
image: assets/images/posts/claude-duet-proactive-background-agent.jpg
categories: TechNotes AI
---

本週最讓我停下來多想一下的消息，不是某個模型跑分又創新高，而是 Anthropic 在 2026 年 10 月 21 日悄悄發布了一個叫做 **Claude Duet** 的新產品——一個以 waitlist 方式開放給美國 Pro 和 Max 訂閱者的研究預覽版應用程式（iOS、Android 及 claude.ai）。官方的說法是：「Claude 以主動型 Agent 的方式在背景運作，持續監看你連接的應用程式，並在執行重要操作前徵求你的許可。」

這句話裡有三個詞讓我盯著看了很久：**主動型（proactive）**、**背景運作（background）**、**連結的應用程式（connected apps）**。過去我們討論 AI 工具，談的都是「我下指令、AI 回應」——一來一回、人在主動位置。但 Duet 這個設計翻轉了這個關係：AI 開始盯著你的環境，在它認為需要的時候主動跳出來問你要不要做某件事。這個轉變對我這種帶著工程團隊的 EM 來說，意味著很不一樣的導入評估邏輯。

---

## 假設我們團隊現在是這樣的

假設是一個 8 人工程團隊，平均每天會在 Slack、GitHub、Jira、Google Meet 這四個工具之間切換超過 40 次。我們目前有一套半自動的 on-call 通報流程：監控系統觸發警報 → 工程師手動在 Slack 建立 incident channel → 拉相關人員進來 → 手動更新 Jira 狀態。整個流程跑下來，從警報到 channel 建立平均要 4-6 分鐘，這段時間有時候就是關鍵。

如果 Claude Duet 真的接上了 Slack 和 GitHub，它在理論上可以做到：監測到 GitHub 上某個 commit 觸發了測試失敗 → 主動問我「要不要現在在 Slack 建立一個 incident channel 並 tag 這份 PR 的 reviewer？」這類的流程自動化。不需要我先想到、先開口，Claude 在背景看到了，主動來敲門。

這對一個還在靠人工協調的小團隊來說，聽起來很有吸引力。但這也是讓我開始認真思考「邊界在哪裡」的起點。

---

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**

主動型 Agent 的最大潛力，恰好在 on-call 場景。如果 Duet 能接上我們的 PagerDuty 或監控工具，在半夜的告警出現時主動整理 context、建立 channel、草擬初步診斷，那對 on-call 工程師的認知負擔會有明顯幫助。但這裡的風險是：**Agent 主動採取錯誤動作的代價**。一個 chatbot 給出錯誤答案，工程師可以忽略；但一個主動型 Agent 在錯誤時機通知了錯誤的人、或在 incident 期間製造了額外雜訊，可能會讓已經緊繃的 on-call 局面更混亂。我的態度是：維運場景可以是 Duet 的第一個實驗點，但「徵求許可」的機制必須被認真檢視——現階段我不會讓它有任何不需要確認就執行的權限。

**對 code review 流程的影響**

這個面向讓我比較保留。如果 Duet 接上 GitHub，它理論上可以在 PR 開出後主動問「要不要我先跑一輪 code review 摘要？」聽起來省時，但我們團隊目前的 code review 文化建立在「reviewer 自己讀 diff、自己形成判斷」這個前提上。如果工程師習慣了「先看 AI 摘要再看 code」，我擔心這會讓 review 的深度下降——特別是對 junior 工程師來說，他們需要透過讀 diff 訓練自己的 code sense，這個過程不應該被 AI 的摘要「跳過」。這是我目前最猶豫的地方。

**對 junior 工程師 onboarding 的影響**

從 onboarding 的角度看，Duet 的主動性可能是雙面刃。好的一面是：新人進來不熟悉流程，Duet 在背景觀察到「這個人似乎卡在某個工具」時主動提示，可以降低「不知道該問誰」的焦慮。壞的一面是：如果 Duet 太積極，新人可能根本不需要自己探索環境、問問題、犯錯——而這些過程恰好是 onboarding 最有價值的學習時刻。我會先限制 Duet 在 onboarding 期間只能提示、不能操作，讓新人決定要不要採納建議，而不是讓 Agent 幫他們做決定。

**技術債與長期維護成本**

主動型 Agent 的技術債，主要藏在「permission model 的設計」裡。如果一開始沒有想清楚哪些 app 連接、哪些操作需要確認、哪些絕對不能自動執行，隨著接入的工具越來越多，這個邊界會越來越模糊。我傾向從一開始就把 Duet 的「許可清單」版本控制起來，就像對待 infra config 一樣：任何擴展 Duet 權限的變更，都需要 PR + review，而不是某個工程師自己在設定頁面勾了一個選項。

**採用時間軸建議**

- **POC（第 1-3 週）**：個人帳號試用，只連結 Slack 一個工具，觀察 Duet 在正常工作日觸發了哪些主動提示、頻率如何、有沒有明顯的誤判。進入下一階段的指標：一週內誤觸發（Agent 在不適當時機跳出來）次數 < 3，且「觸發 → 工程師選擇採納建議」的比例 > 50%。

- **小規模試點（第 4-8 週）**：邀請 2 位志願工程師一起試用，接入 GitHub + Slack，聚焦在 incident 通報流程。進入下一階段的指標：incident channel 建立時間縮短 > 30%，且試點工程師對 Duet 的主動性評分（1-5 分）平均 > 3.5（「有幫助」而不是「很煩」）。

- **全面推行（第 9 週後評估）**：根據試點結果決定是否向全團隊開放。全面推行前必須要有正式的 permission policy 文件和 rollback 計劃；如果試點結果顯示誤觸發率仍高，或工程師普遍覺得 Duet 的主動性干擾了工作節奏，我會暫停評估，等 Anthropic 把這個功能做得更成熟。

---

Claude Duet 現在還是 research preview，waitlist 都還沒全開，我目前並沒有辦法直接拿來跑。但這並不妨礙我現在就開始想「如果它進了我們團隊，我會怎麼管它」。主動型 AI 工具和過去的 AI 工具之間有一道概念上的邊界：過去我們在控制 AI，從現在開始 AI 開始主動影響我們的工作節奏。這個關係的轉變比任何技術細節都更值得認真思考。

接下來幾週我會持續觀察 Duet 的 waitlist 開放進度，以及早期使用者的實測回報，特別是「false positive 觸發」的情況。如果你的團隊也在評估主動型 AI 工具，我很想知道你們對「Agent 主動採取行動的邊界」這個問題的判斷是什麼。

---
*封面圖片由 [Matheus Bertelli](https://www.pexels.com/photo/ai-chat-interface-on-computer-screen-30530407/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
