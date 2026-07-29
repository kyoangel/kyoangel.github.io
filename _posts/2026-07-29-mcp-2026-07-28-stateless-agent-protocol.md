---
layout: post
author: KAI
title: "MCP 2026-07-28 無狀態規格正式亮相：我的工程團隊該怎麼應對這次架構轉變？"
description: "MCP 2026-07-28 規格於 7 月 28 日發布，從有狀態雙向連線改為無狀態請求回應模型，強化 OAuth/OIDC 授權並引入版本化擴充框架。本文為技術經理 KAI 評估 AI agent 協定升級對工程團隊維運、code review、onboarding 與技術債的具體影響與導入時間軸。"
image: assets/images/posts/mcp-2026-07-28-stateless-agent-protocol.jpg
categories: TechNotes AI
---

這週讓我頻繁刷新頁面的，是 Model Context Protocol（MCP）在 7 月 28 日正式推出的 **2026-07-28 規格版本**。這不是小改版——整個 MCP 核心從原本的「有狀態雙向連線」改成「無狀態請求/回應」模型，徹底改變了 AI agent 與工具之間的通訊方式。同一天，Anthropic 也宣布 Claude 將率先支援這個新規格，而根據 MCP 官方部落格的數據，MCP 的月度 SDK 下載量已突破 4 億次，是今年年初的 4 倍。這個數字讓我意識到，這個協定已經不再是一個可以觀望的邊緣規格，而是整個 AI agent 生態正在收斂的基礎建設。

我在看到這則消息的第一反應是：**我們團隊目前的 agent 架構，有幾個假設會在這個版本下失效？** 這半年來，我們陸續把幾個內部工具接上 MCP，靠的正是那個有狀態的 session 機制——每次 initialize handshake，靠 `Mcp-Session-Id` 追蹤對話狀態。新規格把這個 handshake 完全移除了，每個 request 必須自帶 protocol version、client identity 與 capabilities，全部放在 `_meta` 裡傳遞。這意味著我們現有的 MCP server 實作要改，而且不是小修小補。

## 假設一個具體的情境

設想一支我比較熟悉的規模：8 人工程團隊，維護 3 個微服務，每週大約產生 20-30 個 PR，目前用 Claude Code 搭配自建的 MCP server 做程式碼審查輔助和部署前合規檢查。MCP server 部署在單一 EC2 實例上，靠 session state 記住 PR 的對話歷史，讓 agent 在多輪溝通中持續追蹤同一個 PR 的修改脈絡。

在 2026-07-28 規格下，這整套架構的前提改變了：session state 的責任從 server 端移到 client（也就是 agent loop 本身）或完全消解（每個 request 攜帶完整 context）。短期痛點很清楚——需要重構 server，或把 session state 抽到外部快取（比如 Redis）。但長遠來說，stateless server 可以部署在 serverless 或 edge 環境，冷啟動快、橫向擴展容易，對我們的 on-call 輪班負擔其實是好事。

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**

舊架構的 stateful MCP server 是個典型的單點問題：server 掛掉，所有進行中的 agent session 就一起斷了，on-call 要重啟 server、手動觸發 session 重建，非常折磨人。新的 stateless 設計讓每個 request 獨立，任何一個 instance 都能服務任何一個 request，水平擴展幾乎不需要協調。我的判斷是：**長期維運成本會明顯下降，但遷移期間的 on-call 風險會短暫升高**。我會特別要求在遷移前補足 integration test，確認 `_meta` 傳遞的 capability 欄位沒有被任何 middleware 或 API gateway 悄悄過濾掉。

**對 code review 流程的影響**

我們的 code review 輔助 agent 目前依賴 session state 來記住「這個 PR 第 3 輪對話前已確認過哪些 issue」。換成 stateless 之後，要不就在每個 request 附上完整的 review history，要不就把 history 存到外部系統再讓 agent 查詢。前者讓 context 體積變大、token 成本上升；後者增加了一個外部依賴。**讓我猶豫的是**：如果我們選擇攜帶完整 context，在 Claude Opus 5（同週 7 月 24 日發布，支援 1M token context window）的配合下，理論上是可行的，但 token 費用的試算得先做清楚。

**對 junior 工程師 onboarding 的影響**

MCP 2026-07-28 的 OAuth/OIDC 授權強化，對我來說是這次更新最讓人開心的部分。過去新人要接一個新 MCP server，常常在 OAuth flow 這邊卡上半天，因為我們的 MCP server 授權設計和企業 IdP（我們用 Microsoft Entra）契合度不佳，要寫一堆 workaround。新規格正式對齊標準的 OAuth 2.0 和 OIDC，接企業 identity 系統理論上會順很多。如果是我們團隊，**我會先用這塊做 POC 指標**：如果新人設置環境的時間從原本的半天縮短到 30 分鐘以內，這個升級就值得加速推行。

**技術債與長期維護成本**

這次規格附帶了一個正式的 **12 個月棄用政策**，這是我很想看到的東西。過去 MCP 改版時，常常不知道舊版 server 還能撐多久，讓技術債的排程很難做。現在有明確的棄用時間軸，我可以把「舊版 MCP 遷移」排進下一個季度的 backlog，不再讓它懸在那邊壓著團隊。另外，versioned extensions framework 讓 MCP Apps 和 Tasks 有正式的擴充路徑，未來在 MCP 上疊加更多 agent 功能時，不用擔心每次大改破壞既有實作，這對技術債的管控很重要。

**採用時間軸建議**

我會建議三個階段，每個階段都要有明確的指標才進下一步：

- **POC（2-3 週）**：挑一個非關鍵的內部工具，把 MCP server 改成 stateless，同時測試 OAuth/OIDC 對接 Entra 的完整流程。進入下一階段的門檻：request 成功率 ≥ 99%、p95 latency 不超過舊版的 1.2 倍、新人環境設置時間縮短 50% 以上。
- **小規模試點（4-6 週）**：挑一個有真實使用量的工具（例如 PR review agent），讓 2-3 位工程師在真實工作中使用新架構。衡量指標：agent 任務完成率、工程師對 context 連貫性的主觀評分（每週一次 5 分量表問卷）。
- **全面推行（試點後視結果決定）**：若試點指標達標，制定全團隊遷移計畫，配合 12 個月棄用期限留有充裕餘裕，不用趕在 deadline 前衝刺。

這個規格更新是今年 MCP 生態最大的一次架構調整，我接下來幾週會密切追蹤 Claude Code 和各家 community MCP server 對 2026-07-28 的支援進度，特別是我們依賴的幾個第三方 server 有沒有跟上。如果你的團隊也在用 MCP 接 AI agent、而且有 stateful server 的實作，我很想知道你們打算怎麼安排遷移的節奏——是選擇攜帶完整 context，還是引入外部 session store？

---
*封面圖片由 [Christina Morillo](https://www.pexels.com/photo/engineer-holding-laptop-1181316/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
