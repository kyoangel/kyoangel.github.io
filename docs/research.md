# Research: GitHub Pages 路由分群 + Harness Engineering 持續更新

> 研究日期：2026-06-11（Part 1 + 首頁 Hub）／2026-06-13 更新（Part 2：Wealth_Kyo 第二專案 + Harness）
> 範圍：純研究，不涉及程式碼修改

## 1. Project Context（現況技術棧）

- **框架**：Jekyll 4.3.4（`Gemfile`/`Gemfile.lock` 使用 `github-pages` gem，標準 GitHub Pages 自動建置，`vendor/bundle`）
- **Repo 性質**：`kyoangel/kyoangel.github.io`（SSH remote: `git@github.com:kyoangel/kyoangel.github.io.git`）— user page，部署在網域根目錄 `kyoangel.github.io`
- **現況（2026-06-13，Part 1 + 首頁 Hub 已上線後）**：
  - `/` — 全新「Project Hub」首頁（`_layouts/home.html` + `assets/css/home.css`），由 `_data/projects.yml` 驅動專案卡片網格。目前 1 張 active（Coder_Kyo Blog → `/coder_kyo/`）+ 2 張「Coming Soon」佔位卡。
  - `/coder_kyo/` — 既有部落格，Mediumish 主題（`_layouts/default.html` + `_layouts/post.html`），文章在 `_posts/*.md`，全站 `permalink: /coder_kyo/:title/`（`jekyll-archives` category 同樣加上 `/coder_kyo/` 前綴，`_pages/{about,categories,tags}.md` permalink 也都加上 `/coder_kyo` 前綴）。
  - 模板（`_layouts/*`、`_includes/postbox.html`、`feed.xml`）連結幾乎都用 `{{ site.baseurl }}{{ post.url }}` 或 `{{ site.baseurl }}/assets/...`，沒有寫死絕對路徑——`_layouts/post.html` 的分類/標籤連結是例外（見 §3.2）。

## 2. Part 1：路由分群（決策 = 同一 repo，改 permalink 前綴）— ✅ 已完成

> 已於 2026-06-12 完成並上線，實作記錄見 `docs/plans/2026-06-12-coder-kyo-routing-split.md`（含各 Task 執行時發現的修正/Correction 註記）。以下保留原始研究內容作為決策紀錄。

### 結論

GitHub Pages 是純靜態 hosting，沒有 server-side routing/反向代理；「路徑」就是輸出檔案在 `_site/` 裡的實際路徑。因為這個 repo 沒有設定 `baseurl`，且模板全部透過 `{{ site.baseurl }}` 引用資源，可以只調整 **permalink**（網址結構），不動 `baseurl`，達成「文章區搬到 `/coder_kyo/`、根目錄留給新首頁」。

### 需要調整的設定點（實作時的調整對照）

| 項目 | 原狀（2026-06-11） | 改為 |
|---|---|---|
| `_config.yml` → `permalink` | `/:title/` | `/coder_kyo/:title/` |
| `_pages/about.md` permalink | `/about` | `/coder_kyo/about` |
| `_pages/categories.md` permalink | `/categories` | `/coder_kyo/categories` |
| `_pages/tags.md` permalink | `/tags` | `/coder_kyo/tags` |
| `jekyll-archives.permalinks.category` | `/category/:name/` | `/coder_kyo/category/:name/` |
| `paginate_path` | `/page:num/` | 移除（`/coder_kyo/` 改為列出所有文章，不分頁） |
| 根目錄 `index.html` | 文章列表（首頁） | 先放佔位頁面，後續迭代為 Hub（見下） |
| 新增文章列表頁 | 無 | `coder_kyo/index.html`（列出所有文章） |
| `assets/`、`_layouts`、`_includes` | 用 `{{ site.baseurl }}/assets/...` | 不變 |
| `404.html` | 通用 404 | 加入 JS catch-all 轉址 |

### 轉址策略（決策 = 重要，需要做轉址）

GitHub Pages 沒有真 301，只能用靜態 meta-refresh / JS 轉址：

1. **舊文章網址**：新舊路徑是 1:1 規律映射（`/<slug>/` → `/coder_kyo/<slug>/`），已在 `404.html` 加入 JS catch-all：偵測目前路徑，自動轉址到 `/coder_kyo/<原路徑>`。
2. **Disqus 留言**：`_includes/disqus.html` 沒有設定 `disqus_identifier`，留言串預設綁定 `window.location.href`。網址改變後舊留言需透過 Disqus 後台「URL Mapper / Migrate Threads」工具手動對應新舊網址（手動、部署後執行，記錄於 routing-split plan 的「Manual Post-Deploy Steps」）。
3. **SEO**：`jekyll-sitemap` 已依新 permalink 重新產生 `sitemap.xml`，需在 Google Search Console 重新提交（同上，手動步驟）。

## 2.5 首頁 Hub（2026-06-12 完成）

根目錄 `/` 已從 Part 1 的暫時佔位頁，迭代為「多專案 Hub」——`_data/projects.yml` 驅動的卡片網格 + `_layouts/home.html`（全新極簡 layout，與 Mediumish 完全分離，無 Bootstrap/jQuery）+ `assets/css/home.css`。實作記錄見 `docs/plans/2026-06-12-new-homepage-hub.md`（已標記 Complete）。

目前 `_data/projects.yml`：

```yaml
- title: "Coder_Kyo Blog"
  description: "分享程式開發技巧、學習筆記與技術心得"
  url: /coder_kyo/
  status: active

- title: "Coming Soon"
  description: "新專案籌備中，敬請期待"
  url: ""
  status: placeholder

- title: "Coming Soon"
  description: "新專案籌備中，敬請期待"
  url: ""
  status: placeholder
```

未來新增專案只需編輯這份 YAML（`status: active` + 真實 `url`），網格樣式會自動重新排列。**Part 2（Wealth_Kyo）就是要把其中一張佔位卡換成真實專案。**

## 3. Part 2：Wealth_Kyo 第二專案 + Harness 自動發文（2026-06-13 確定範圍）

> 2026-06-11 的原始研究僅將 Part 2 定位為「Harness Engineering 持續更新」，方向未定（HN 主題 vs. 個人專案主題、`/schedule` vs. GitHub Actions、頻率未定）。2026-06-13 透過 AskUserQuestion 與使用者確認了完整範圍，記錄如下。

### 3.0 背景：2026-06-11 原始研究摘要

**現有自動化盤點（`generate_blog.py`）**：流程為 HN 首頁爬蟲 → 呼叫本機 LM Studio（`http://localhost:1234/v1`，模型 `llama-3-8b-gpt-4o-ru1.0`）→ 寫入 `_posts/*.md`（`layout: post`、`author: KAI`、`categories: TechNotes News`、繁中、文末附 AI 撰文警語）→ `git add/commit/push` 到 `origin master`。repo 內**完全沒有 `.github/workflows`**，也沒有任何排程設定（過去靠人工/本機 cron）。依賴 `localhost:1234` 的本機 LM Studio——任何雲端方向都需要換掉 LLM 來源，且目前**沒有 build 驗證步驟**就直接 push。

**核心概念**：Agent = Model + Harness。Harness 是模型以外所有的東西：排程、context 注入、工具執行、驗證/回饋迴圈、權限控管。

**當時整理的兩個方向**：
- **方向 A：Claude Code `/schedule`（雲端 scheduled agent）**——排程任務、雲端 agent checkout repo、用 WebSearch 找主題、依現有 front-matter 慣例寫 Markdown、跑 `bundle exec jekyll build` 驗證、commit & push。
- **方向 B：GitHub Actions + 雲端 LLM**——新增 `.github/workflows/auto-post.yml`（`on: schedule: cron`），把 LLM 呼叫換成雲端 API（repo secret），加入 build 驗證 gate。

2026-06-13 已確認採用**方向 A**。

### 3.1 範圍與決策摘要（2026-06-13）

| 問題 | 決定 |
|---|---|
| 第二個專案範圍 | 同 repo 內新分區 `/wealth_kyo/`（填入 `_data/projects.yml` 的一張「Coming Soon」佔位卡） |
| 內容主題 | 美股 / 台股投資趨勢觀察，專案命名 **Wealth_Kyo** |
| Harness 機制 | Claude Code `/schedule`（雲端 routine） |
| 發文頻率 | 每週一次，且**需可由使用者自行調整** |
| 視覺設計 | 沿用 Mediumish 主題（與 `/coder_kyo/` 一致的版型/樣式） |

### 3.2 現況盤點與關鍵發現（2026-06-13）

**可重用模式**
- **Hub 卡片模式**：`_data/projects.yml` 新增一筆 `status: active`、`url: /wealth_kyo/` 即可在首頁出現新卡片，無需改 HTML/CSS。
- **`/coder_kyo/` 路由分群模式**（`docs/plans/2026-06-12-coder-kyo-routing-split.md`）：permalink 前綴 + 專屬 index 頁 + nav 連結調整 + 404 redirect，是 `/wealth_kyo/` 分區建立的直接範本。
- **AI 產文慣例**（`_posts/2025-06-16-ai-cursor-dev-experience.md`、`generate_blog.py`）：`layout: post`、`author: KAI`、`categories: ...`、繁體中文、文末附 AI 撰文警語。`_config.yml` `authors:` 已有 `Kyo`（站長）與 `KAI`（Coder_Kyo 的 AI persona，含 avatar/description）。

**技術限制（影響 /plan 架構）**
1. **內容資料架構**：`_includes/postbox.html`/`featuredbox.html` 依賴 `post.url/title/excerpt/author/date/image`。`_posts/` 的 `date` 會自動從檔名推導，但**自訂 Jekyll collection 不會**——若採用新 collection（如 `_wealth_posts/`），每篇文章 front matter 須明確帶 `date:`。
2. **`_layouts/post.html` 硬編碼分區連結**：第 103/116 行寫死 `/coder_kyo/categories`、`/coder_kyo/tags`。Wealth_Kyo 文章若沿用此 layout（已決定沿用 Mediumish），這兩個連結需改為依分區動態產生（例如依 `page.collection` 或新增的 front-matter 欄位判斷前綴），否則會誤指向 Coder_Kyo 分區。
3. **jekyll-archives 單一全域 permalink**：`_config.yml` 的 `jekyll-archives.permalinks.category` 只能設定一個全站模式（目前是 `/coder_kyo/category/:name/`）。若 Wealth_Kyo 文章也用 `categories:`，分類彙整頁仍會落在 `/coder_kyo/category/...`。需在 /plan 決定：共用同一個 category 命名空間（可接受），或 Wealth_Kyo 文章不提供分類彙整頁。
4. **`/schedule` 雲端 routine 的 repo push 權限**：`origin` 為 SSH remote。`/schedule` 雲端 routine 的 repo 存取通常在**建立 routine 時**透過連結的 GitHub 帳號/App 設定，與本機 SSH key 無關——這是 /plan 執行前/中需驗證的前置條件。
5. **發文頻率可調整**：使用者要求頻率（目前定為每週）之後要能自行調整。`/schedule` routine 的 cron 排程本身即可透過 `/schedule` 指令更新既有 routine，/plan 應確保排程設定有清楚記錄、易於修改，不需改動 repo 程式碼。

**新增需求**
- **新 Author Persona**：需在 `_config.yml` `authors:` 新增 Wealth_Kyo 的 AI persona（名稱、`avatar` 圖片資產、`description`），對應 Coder_Kyo 的 `KAI`。
- **投資內容警語**：建議延用 Coder_Kyo AI 文章「警語提醒是AI撰文」慣例，並加上投資相關警語（如「本文僅為市場資訊整理與個人觀察，不構成投資建議」）。

### 3.3 待 /plan 確認/設計的項目
1. 內容資料架構：新 collection（`_wealth_posts/` + `permalink: /wealth_kyo/:title/`）vs. `_posts/` + 每篇 front matter `permalink` 覆寫——研究建議採用新 collection。
2. `_layouts/post.html` 分類/標籤連結的分區感知化做法。
3. `/wealth_kyo/` index 頁（仿 `coder_kyo/index.html`）。
4. `/schedule` routine 的 prompt 設計：趨勢來源（WebSearch 關鍵字）、文章 front-matter 範本、AI/投資警語文案、build 驗證步驟、commit & push 流程、push 權限確認。
5. 排程頻率的可調整機制（如何讓使用者之後自行改變頻率）。

## 4. 使用者決策摘要（累積）

| 問題 | 決定 | 階段 |
|---|---|---|
| 路由分群方案 | 同一 repo，改 permalink 前綴 | Part 1（已完成） |
| 舊網址/SEO/Disqus | 重要，需要做轉址 | Part 1（已完成） |
| 首頁定位 | 多專案 Hub（卡片網格），與 Mediumish 視覺分離 | Hub（已完成） |
| 第二個專案範圍 | 同 repo 新分區 `/wealth_kyo/` | Part 2 |
| 第二個專案主題 | 美股/台股投資趨勢觀察，命名 Wealth_Kyo | Part 2 |
| Harness 機制 | Claude Code `/schedule` 雲端 routine | Part 2 |
| 發文頻率 | 每週一次，且需可調整 | Part 2 |
| Wealth_Kyo 視覺設計 | 沿用 Mediumish（與 Coder_Kyo 一致） | Part 2 |

## 5. 後續
- ~~`/plan` — Part 1：路由分群~~ ✅ 已完成
- ~~`/plan` — 新首頁 Hub~~ ✅ 已完成
- `/plan` — Wealth_Kyo 第二專案 + `/schedule` harness routine（下一步，本次執行）
