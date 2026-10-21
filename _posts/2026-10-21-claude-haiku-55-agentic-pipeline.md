---
layout: post
author: KAI
title: "Claude Haiku 5.5 上線後，我重新盤算了團隊的 Agentic Pipeline 成本結構"
description: "Anthropic 於 2026 年 10 月 7 日發布 Claude Haiku 5.5，定位為高吞吐、低成本的子代理模型，搭配可調整的 effort 設定，讓技術經理重新思考多代理工作流程中的模型路由與成本分配策略。"
image: assets/images/posts/claude-haiku-55-agentic-pipeline.jpg
categories: TechNotes AI
---

上週五我在看 Anthropic 的 changelog 時，看到一條乍看不起眼的更新：Claude Haiku 5.5 於 2026 年 10 月 7 日正式發布，是 Claude 5.5 系列的最後一個成員。官方的定位很清楚——「高吞吐、低成本，適合摘要、資料庫查詢、分類，以及 coding subagent 工作」，而且新增了一個可調整的 effort 設定（adjustable effort setting）。

看到「coding subagent」這四個字，我馬上放下手邊的 PR review，打開了我們的 agent pipeline 架構圖。

這件事讓我開始重新盤算的原因，不是因為 Haiku 5.5 本身有多驚人，而是因為它的出現讓我們目前的模型路由策略變得可重新討論了。我們現在用的是 Claude Opus 5.5 跑所有子代理任務，理由是「能力夠、不用多想」，但代價是每個月的 API 費用讓我有點說不出口。Haiku 5.5 的到來，逼我認真想一件事：**什麼工作值得用旗艦模型，什麼工作其實用輕量模型就夠了？**

---

## 假設我們團隊現在是這樣的

假設是一個 7 人工程團隊，每天跑 3-5 個 CI pipeline，其中有兩個 pipeline 會啟動 agentic task：一個是 code review bot（會逐檔讀 diff、產出評論），另一個是測試報告分析（會讀 log、歸納失敗原因、建議修復方向）。

用 Opus 5.5 跑這兩個 pipeline，大概每週燒掉 X tokens 在「讀 diff 確認語法規範」這種其實不太需要 frontier 模型的事情上。如果把 code review bot 裡的「語法檢查」、「命名慣例確認」這類子任務切出來改走 Haiku 5.5，搭配 effort 設定調到 low，理論上可以讓這部分的成本降到原本的 1/5 甚至更少，而品質差異幾乎感受不到。

更有意思的是 effort 設定這個旋鈕。如果 Haiku 5.5 讓我可以在執行時動態告訴模型「這個子任務很重要，請認真一點」或「這個只是 pre-check，快速過就好」，那就等於我可以在同一個模型上得到不同的「速度/品質」曲線，不用在不同模型之間切換。這對 harness 的設計來說是一個很有吸引力的訊號。

---

## 身為技術經理，我會怎麼評估這次更新

**對 on-call / 維運的影響**

引入一個新的模型節點，意味著 harness 裡要多一個 fallback 路徑。如果 Haiku 5.5 服務降級，子代理是要繼續用 Haiku 排隊，還是自動升級到 Opus？這個決策路徑需要在 on-call runbook 裡寫清楚。我傾向先把降級策略定義好再導入，不然半夜出事的時候會有人不知道該怎麼辦。維運負擔的增加是真實的，但不是無法管理的。

**對 code review 流程的影響**

我們的 code review bot 現在是「Opus 5.5 全程主導」，如果要切成「Haiku 5.5 做第一輪 pre-screening，Opus 5.5 做最終深度分析」，這需要重新設計 prompt chaining 和任務分配邏輯。短期內會增加 harness 複雜度；但中長期來說，能力分層的架構會讓整個 pipeline 更好維護，因為每個節點的責任邊界更清楚。讓我猶豫的是這段過渡期的 QA 成本——我們必須跑一批 A/B test 確認 Haiku 5.5 在我們的 codebase 上表現沒有顯著退步，這需要時間。

**對 junior 工程師 onboarding 的影響**

這反而可能是意外的好消息。如果 Haiku 5.5 的速度夠快、成本夠低，我們可以考慮在 junior 工程師的開發環境裡開放更多「隨時問 agent」的互動，不用擔心每次觸發都燒掉昂貴的 token。降低成本焦慮，可以讓我們更大膽地把 AI agent 作為學習工具，而不只是生產工具。這是我比較看好的面向。

**技術債與長期維護成本**

能力分層架構的技術債風險，主要在於「什麼任務應該走 Haiku、什麼任務應該走 Opus」這個分類邏輯本身。如果這個邏輯寫死在 config 裡，未來模型迭代時就會需要人工重新審視。我的想法是把路由規則做成 policy-as-code，讓它可以被版本控制和 review，而不是散落在各個 pipeline 的 hardcoded 條件裡。這樣雖然初期多了一點設計成本，但長期維護起來會輕鬆很多。

**採用時間軸建議**

- **POC（第 1-2 週）**：在一個非關鍵的子任務（例如 commit message lint）上把 Haiku 5.5 接進來，跑 effort=low 和 effort=high 的對比測試。進入下一階段的指標：品質分數（人工評估）不低於 Opus 5.5 的 90%，速度提升 > 30%，成本下降 > 40%。

- **小規模試點（第 3-6 週）**：把 code review bot 的 pre-screening 階段切換到 Haiku 5.5，在兩個非主幹 pipeline 上實驗。進入下一階段的指標：工程師對 review 品質的抱怨率沒有顯著上升，pipeline 總執行時間縮短，月費用降低符合預期。

- **全面推行（第 7 週之後）**：根據試點結果，決定是否在所有適合的子任務上切換。這個時間點我會要求一份正式的 migration doc，包含 rollback 計劃和效能基準。

---

接下來幾週，我打算先動手做 POC，特別是想摸清楚 adjustable effort 設定的邊界——到底 low、medium、high 在實務上代表什麼差異，文件現在還太薄，需要自己跑實驗才知道。

如果你的團隊也在評估用輕量模型替換部分子代理任務，或者你已經有 Haiku 5.5 的實測數據，我很想知道你們的發現。這種模型路由的取捨，我相信每個團隊的答案都不一樣，但互相交換觀察應該對大家都有幫助。

---
*封面圖片由 [Daniil Komov](https://www.pexels.com/photo/close-up-of-computer-screen-with-code-and-menu-options-34804017/) 提供，來源：[Pexels](https://www.pexels.com)*

---
**警語：本文由 AI 自動生成，僅為技術趨勢整理與個人觀察，內容可能與實際發布資訊有出入，實際導入前請自行查證官方文件並評估團隊狀況。**
