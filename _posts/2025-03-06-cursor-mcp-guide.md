---
layout: post
author: Kyo
title: "在 Cursor IDE 中使用 Model Context Protocol (MCP)"
image: 
featured: false
categories: TechNotes Tools
---

## 什麼是 MCP 以及為什麼要使用它？

Model Context Protocol (MCP) 是 Cursor IDE 提供的一個開放協議，允許開發者為 AI 助手提供自定義工具。透過 MCP，我們可以：

1. **擴展 AI 能力**：讓 AI 助手能夠使用自定義工具處理特定任務
2. **整合外部系統**：與現有的開發工具和系統進行互動
3. **自動化工作流程**：提升開發效率

需要注意的是，MCP 工具目前僅在 Composer 的 Agent 功能中可用，且可能不是所有模型都支援。

## 如何使用 MCP

### 1. 新增 MCP 伺服器

在 Cursor 中設定 MCP 伺服器有兩種方式：

#### 方式一：透過設定介面

1. 打開 Cursor 設定 (Command + ,)
2. 進入 `Features` > `MCP`
3. 點擊 `+ Add New MCP Server`
4. 選擇傳輸類型（Transport Type）：
   - `stdio`：執行本地命令
   - `sse`：連接 SSE 端點

#### 方式二：專案配置文件

在專案根目錄建立 `.cursor/mcp.json` 文件：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/directory1",
        "/path/to/directory2"
      ]
    }
  }
}
```

或是 SSE 伺服器配置：

```json
{
  "mcpServers": {
    "sample-project-server": {
      "url": "http://localhost:3000/sse"
    }
  }
}
```

### 2. 使用 MCP 工具

Composer 的 Agent 會自動識別可用的 MCP 工具。當 AI 助手要使用工具時，預設會顯示確認訊息：

1. **工具核准**
   - 系統會顯示工具呼叫的詳細資訊
   - 使用者可以選擇允許或拒絕

2. **Yolo 模式**
   - 可以啟用 Yolo 模式讓工具自動執行
   - 類似於終端機命令的執行方式

### 3. 使用限制和注意事項

1. **功能限制**
   - 僅在 Composer 的 Agent 功能中可用
   - 需要確認模型是否支援 MCP

2. **安全性考量**
   - 謹慎處理系統資源存取
   - 建議實作適當的權限控制

3. **效能考量**
   - 控制 MCP 伺服器數量
   - 只註冊必要的工具

### 4. 最佳實踐

1. **配置管理**
   - 使用專案級別的 `mcp.json` 配置
   - 妥善管理環境變數

2. **錯誤處理**
   - 提供清楚的錯誤訊息
   - 實作適當的錯誤處理機制

3. **版本控制**
   - 將 MCP 配置納入版本控制
   - 維護配置變更記錄

透過正確設定和使用 MCP，我們可以大幅提升 Cursor IDE 的 AI 助手功能。記得遵循最佳實踐，確保工具的可靠性和安全性!!