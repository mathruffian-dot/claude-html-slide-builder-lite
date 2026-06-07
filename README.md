# 🎨 html-slide-builder-lite — 研習簡易版

> 給定教材，自動生成完整的 **Reveal.js HTML 互動簡報**，**雙擊瀏覽器即可播放**。
> ⚙️ **研習簡易版**：fork 自 [claude-html-slide-builder](https://github.com/mathruffian-dot/claude-html-slide-builder)，**移除所有需要額外技能或 API Key 的功能**，零金鑰、零額外安裝。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 跟完整版差在哪

| 功能 | 完整版 | 研習簡易版（本 repo） |
|------|--------|----------------------|
| 背景底圖 | AI 生圖（draw 技能 / OpenAI gpt-image，**需 API Key**）| ✅ **CSS 漸層底圖**（零金鑰）|
| 圖標 | AI 生圖 + PIL 去背（**需 API Key + Pillow**）| ✅ **Emoji / 內建 SVG** |
| 即時互動 | Firebase 文字雲 / 投票（**需 Firebase 金鑰**）| ❌ 移除；要互動改用 [`clasp-gas-guide`](https://github.com/mathruffian-dot/clasp-gas-guide) 的 GAS Web App |
| 滑桿視覺化 [VIZ] | ✅ | ✅（純 CSS/JS）|
| 輸出 | 部署 GitHub Pages | ✅ **單一 index.html，瀏覽器直接開**；GitHub Pages 改為選配 |
| 安裝門檻 | OpenAI Key + Firebase + Pillow + gh | **只需 Python + git** |

---

## ✨ 功能（全部零金鑰、純 CSS/JS）

| 功能 | 說明 |
|------|------|
| 🌈 **CSS 漸層底圖** | 深暗色 + 霓虹光暈，用 `.bg-aurora` / `.bg-soft` class，不呼叫任何生圖 |
| 😀 **Emoji / SVG 圖標** | 語意 emoji 或內建線性 SVG，取代需要生圖與去背的圖標 |
| 🔀 **滑桿視覺化** | clip-path 揭露效果，適合「前後對比」「格式轉換」內容 |
| ▶️ **瀏覽器直接播放** | 產出單一 `index.html`，雙擊全螢幕上課，不必部署 |

---

## 🔧 安裝

### 需要的元件

| 元件 | 用途 | 必要？ |
|------|------|--------|
| Python 3.8+ | 安裝腳本 | ✅ 必要 |
| git | 版本控制 | ✅ 必要 |
| [GitHub CLI (gh)](https://cli.github.com/) | GitHub Pages 部署 | ⚠️ **選配**，只有想要公開網址才需要 |

> 不需要 OpenAI API Key、不需要 Firebase、不需要 draw 技能或 Pillow。

### 一鍵安裝

```bash
git clone https://github.com/mathruffian-dot/claude-html-slide-builder-lite.git
cd claude-html-slide-builder-lite
python install.py
```

安裝腳本會偵測你的 Agent 技能資料夾（Claude Code / OpenCode / Codex），把 skill 複製過去。

---

## 🚀 使用方式

安裝後，對你的 Agent（AntiGravity / OpenCode / Claude Code）說：

```
幫我把這份教材做成 HTML 互動簡報
```

Agent 會：
1. 分析教材，列出投影片大綱（含功能標記 `[BG][ICON][VIZ]`）
2. **等你確認大綱後**才開始生成
3. 產出單一 `index.html`
4. 請你用瀏覽器打開預覽（F 全螢幕、方向鍵翻頁）

要互動投票 / 文字雲？本版不含（需資料庫）。請改用 [`clasp-gas-guide`](https://github.com/mathruffian-dot/clasp-gas-guide) 做 GAS Web App，把短網址放進簡報。

### 想放到網路上？三種選擇（由簡到繁）

1. **直接用瀏覽器播放**（預設，零帳號）：雙擊 `index.html`。
2. **GAS Web App 上線**（只要 Google 帳號）：用 `HtmlService` 純當網頁伺服器，**不需要連 Google Sheets**，免 GitHub / 免 Netlify。作法見 SKILL.md 第 7 節。
3. **GitHub Pages**（需 GitHub 帳號）：要公開原始碼 + 自訂網址時才用。

---

## 📁 Skill 結構

```
html-slide-builder-lite/
├── SKILL.md                    # 主要指令（Agent 讀取）
└── references/
    └── reveal-template.md      # Reveal.js HTML 模板 + CSS 元件庫（含漸層底圖）
```

---

## 📄 授權

MIT License。fork 自 [claude-html-slide-builder](https://github.com/mathruffian-dot/claude-html-slide-builder)。

*由 [mathruffian-dot](https://github.com/mathruffian-dot) 製作*
