---
layout: post
author: Kyo
title: "Cursor 編輯器使用技巧"
image: assets/images/cursor-editor-tips.png
featured: true
categories: TechNotes,Tools
---

Cursor 是一個基於 VS Code 的 AI 輔助程式編輯器，今天來分享一些實用的小技巧。

## Chat 功能使用技巧

### 1. 智能程式碼解釋
直接選取程式碼後按下 `Cmd/Ctrl + L`，可以快速向 AI 詢問選中程式碼的功能說明。

### 2. 自動 Debug
當遇到錯誤時，可以將錯誤訊息複製到 Chat 中，AI 會協助分析問題並提供解決方案。

### 3. 上下文理解
Chat 會自動理解當前檔案的上下文，所以問題不需要重複說明程式碼的背景。

## Composer 功能技巧

### 1. 快速生成程式碼
使用 `/` 指令可以快速呼叫 Composer：
- `/fix` - 修復程式碼問題
- `/test` - 生成測試程式碼
- `/doc` - 產生文件註解

### 2. 程式碼重構
選取需要重構的程式碼，使用 Composer 可以：
- 優化程式碼結構
- 提升程式碼可讀性
- 改善效能

### 3. 自動完成
Composer 會根據上下文提供更智能的程式碼建議，比傳統的自動完成更準確。

## 實用快捷鍵

- `Cmd/Ctrl + L` - 開啟 Chat
- `Cmd/Ctrl + K` - 開啟 Composer
- `Cmd/Ctrl + I` - 插入程式碼建議

## 使用小提醒

1. 善用 Chat 歷史記錄，可以快速回顧之前的對話
2. 定期更新 Cursor 以獲得最新功能
3. 可以自訂 AI 模型的行為，讓回答更符合個人需求

Cursor 結合了 VS Code 的強大功能和 AI 的智能輔助，善用這些功能可以大幅提升開發效率。不過要記住，AI 只是輔助工具，最終還是要依靠開發者的判斷和經驗。 