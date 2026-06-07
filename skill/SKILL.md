---
name: html-slide-builder-lite
description: |
  給定任何教材（文字、課程大綱、PDF、講義、口述主題），自動生成完整的 Reveal.js HTML 互動簡報。研習簡易版：不需要任何 API Key、不需要額外技能。

  自動處理三大視覺強化（全部零金鑰、純 CSS/JS）：
  1. CSS 漸層底圖（不呼叫 AI 生圖，用內建漸層 + 光暈預設）
  2. Emoji / 內建 SVG 圖標（取代需要生圖與去背的扁平化圖標）
  3. 滑桿視覺化演示（clip-path 揭露，適合前後對比內容）

  當使用者說「幫我做 HTML 簡報」「把這份教材轉成互動簡報」「做 Reveal.js 簡報」「做成投影片」「做一份課程簡報」，或提供教材並要求轉成簡報格式時，務必使用此 Skill。即使使用者未明確說「互動」或「HTML」，只要目的是從教材產出可展示的簡報，也應觸發此 Skill。
---

# HTML 智慧簡報生成器（研習簡易版）

教材 → 分析 → 確認大綱 → 生成 Reveal.js 簡報 → 強化（漸層底圖 / Emoji圖標 / 視覺化）→ 直接用瀏覽器播放（選配部署）

> ⚙️ **研習簡易版**：相較完整版 [claude-html-slide-builder](https://github.com/mathruffian-dot/claude-html-slide-builder)，本版**移除所有需要額外技能或 API Key 的功能**：
> - ❌ AI 生圖底圖（draw 技能 / OpenAI gpt-image）→ ✅ 改用 **CSS 漸層底圖**
> - ❌ AI 圖標 + PIL 去背 → ✅ 改用 **Emoji / 內建 SVG**
> - ❌ Firebase 即時互動（文字雲 / 投票，需資料庫金鑰）→ ✅ 移除；要互動改用 [`clasp-gas-guide`](https://github.com/mathruffian-dot/clasp-gas-guide) 的 GAS Web App
>
> 產出是**單一 `index.html`**，雙擊就能用瀏覽器全螢幕播放，零安裝、零金鑰。

---

## 0. 讀取教材

接受任何形式的輸入：

- **文字 / Markdown**：直接分析
- **PDF**：用 Read 工具讀取（若有多頁先讀摘要頁）
- **口述主題**：自行根據標準教學邏輯設計（引言→概念→範例→互動→結論）

若教材資訊不足，不要詢問，直接用教學慣例補充。

---

## 1. 分析大綱，等使用者確認

分析完畢後輸出大綱表格，**等使用者確認後才繼續**：

```
## 📋 簡報大綱草稿（共 N 頁）

| 頁碼 | 標題 | 內容摘要 | 功能標記 |
|------|------|----------|----------|
| 1    | 封面 | 課程名稱、講師 | [BG] |
| 2    | 三大重點 | 並列說明三個核心概念 | [ICON] |
| 3    | 前後對比 | A 方案 vs B 方案演進 | [VIZ] |
...

**功能標記說明**
- [BG] CSS 漸層底圖（深暗色 + 光暈，零生圖）
- [ICON] Emoji / 內建 SVG 圖標
- [VIZ] 滑桿視覺化演示（clip-path）

請確認大綱，或說明要調整的地方。
```

### 功能標記的決策原則

| 標記 | 觸發條件 | 每份簡報目標數量 |
|------|----------|-----------------|
| [BG] | 封面、封底、章節轉換、高衝擊結論 | 3–5 頁 |
| [ICON] | 頁面有 3–6 個並列項目（優缺點、步驟、特性） | 1–3 頁 |
| [VIZ] | 「前後對比」「格式轉換」「A 到 B 的演進」 | 0–1 頁 |

> 💡 需要「即時文字雲 / 投票」這類互動？本研習版不含（需資料庫）。請改用 [`clasp-gas-guide`](https://github.com/mathruffian-dot/clasp-gas-guide) 做一個 GAS Web App 投票頁，再把短網址放進簡報。

---

## 2. 建立專案目錄與基礎 HTML

使用者確認後：

1. 建立專案目錄：`<當前工作目錄>/<簡報英文短名>/`
2. 生成 `index.html`（完整 Reveal.js 骨架）

讀取 `references/reveal-template.md` 獲得：完整 CSS 變數、元件樣式、Reveal.js 初始化程式碼。

**命名規則：** 專案目錄用 kebab-case 英文（`ai-course`、`math-lesson`）。

**調色盤（所有簡報統一使用）：**
```
--accent:  #e8643a   橘紅（主強調）
--accent2: #4fc3f7   青（次強調）
--success: #81c784   綠（正面）
--warn:    #ffb74d   琥珀（提示）
背景：     #0d1117 ~ #1a1a2e（深暗色）
```

---

## 3. 漸層底圖 [BG]（零生圖）

不呼叫任何 AI 生圖。直接用 CSS 漸層 + 徑向光暈做出「深暗色霓虹」氛圍。在該 section 加 class，並把以下樣式放進 `<style>`：

```html
<section class="bg-aurora">
  <!-- 內容 -->
</section>
```

```css
/* 通用深色漸層底（封面 / 章節 / 封底）*/
.reveal .bg-aurora{
  background:
    radial-gradient(60% 80% at 20% 20%, rgba(79,195,247,.25), transparent 60%),
    radial-gradient(50% 70% at 80% 70%, rgba(232,100,58,.22), transparent 60%),
    linear-gradient(135deg, #0d1117, #1a1a2e);
}
/* 一般內容頁：更淡，避免干擾文字 */
.reveal .bg-soft{
  background:
    radial-gradient(50% 60% at 85% 15%, rgba(79,195,247,.12), transparent 60%),
    linear-gradient(160deg, #0d1117, #161b22);
}
```

> 想換色：改 radial-gradient 的 rgba 即可（青 `79,195,247` / 橘 `232,100,58`）。封面用 `.bg-aurora`，內容頁用 `.bg-soft`。

---

## 4. 圖標系統 [ICON]（Emoji / 內建 SVG，零生圖、零去背）

不生圖、不裝 PIL。兩種做法擇一：

### 4-1 Emoji（最快，研習預設）
直接用語意 emoji 取代圖標，配 `drop-shadow` 發光：

```html
<div class="adv-card fragment">
  <div class="adv-icon" style="font-size:2.2em;
       filter:drop-shadow(0 0 10px rgba(79,195,247,.6));">🚀</div>
  <div class="adv-title">標題 A</div>
  <div class="adv-desc">說明文字…</div>
</div>
```

常用對照：步驟①②③、優點 ✅、缺點 ⚠️、想法 💡、目標 🎯、工具 🛠️、雲端 ☁️、資料 📊、時間 ⏱️、互動 💬。

### 4-2 內建 inline SVG（要風格統一時）
用簡單線性 SVG（`stroke=currentColor`），顏色跟著主題色：

```html
<div class="adv-icon" style="color:var(--accent2)">
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>
  </svg>
</div>
```

- adv-card 統一 `border-top: 4px solid var(--accent2)` + `text-align:center`。

---

## 5. 課堂互動（用 GAS，不用 Firebase / 任何資料庫）

本版**不串接任何資料庫**。若課堂要即時投票 / 文字雲：

- 用 [`clasp-gas-guide`](https://github.com/mathruffian-dot/clasp-gas-guide) 做一個 **GAS Web App** 投票 / 提問頁（只要 Google 帳號、零金鑰）。
- 把該頁的短網址 + QR Code 放進簡報的一張 section 即可。

---

## 6. 視覺化演示 [VIZ]

clip-path 滑桿揭露效果，適合「格式轉換」「前後對比」「A→B 演進」。純 CSS/JS，零依賴。

```html
<div style="position:relative; height:390px; border-radius:12px; overflow:hidden;">
  <div id="viz-before" style="position:absolute;inset:0;"></div>
  <div id="viz-after" style="position:absolute;inset:0;clip-path:inset(0 100% 0 0);"></div>
  <div id="viz-divider" style="position:absolute;top:0;left:0;width:3px;height:100%;
    background:linear-gradient(to bottom,transparent,#4fc3f7,transparent);
    box-shadow:0 0 12px #4fc3f7;pointer-events:none;"></div>
</div>
<input id="viz-slider" type="range" min="0" max="100" value="0">
<script>
document.getElementById('viz-slider').addEventListener('input', function() {
  const v = +this.value;
  document.getElementById('viz-after').style.clipPath = `inset(0 ${100-v}% 0 0)`;
  document.getElementById('viz-divider').style.left = v + '%';
});
</script>
```

左右各加標籤（`position:absolute; top:8px`），接近邊界時用 JS 淡出。

---

## 7. 播放與部署

### 預設：直接用瀏覽器播放（零帳號）
產出的 `index.html` 是自足檔案（Reveal.js 走 CDN）。**雙擊用瀏覽器打開，按 F 全螢幕、方向鍵翻頁**即可上課。

回傳給使用者：
```
✅ 簡報完成！
📂 檔案：<專案目錄>/index.html
▶️ 用瀏覽器打開即可播放（F 全螢幕、方向鍵翻頁）
```

### 選配：用 GAS Web App 上線（免 Sheets、免 GitHub、免 Netlify）

只要 Google 帳號就能把這份 `index.html` 掛上網 —— GAS 的 `HtmlService` 可以**純當網頁伺服器，不需要連 Google Sheets**：

1. 到 [script.google.com](https://script.google.com) 新建專案。
2. 新增一個 HTML 檔（檔名例如 `index`），把產出的 `index.html` 內容整段貼進去。
3. 後端 `Code.gs` 只要一個 `doGet`（**沒有 doPost、沒有 SpreadsheetApp、不建任何試算表**）：
   ```javascript
   function doGet() {
     return HtmlService.createHtmlOutputFromFile('index')
       .addMetaTag('viewport', 'width=device-width, initial-scale=1')
       .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
   }
   ```
4. 部署 → 網頁應用程式 → 存取權選「任何人」→ 取得網址（可再用 is.gd 縮短 + 產 QR Code）。

> 注意：GAS 會把頁面包在 iframe 沙箱裡，但 Reveal.js + CDN 仍正常運作；全程不需建立或連接任何試算表。

### 選配：部署到 GitHub Pages（需 GitHub 帳號）
若使用者有 GitHub 帳號且想要公開網址才做：

```bash
cd "<專案目錄>"
git init
git add .
git commit -m "初始化：<簡報名稱>"
# 先建立並推送 repo（branch 名以實際 git 預設為準，新版多為 main）
gh repo create <帳號>/<repo-name> --public --source=. --push \
  --description "<簡報一句話描述>"
# 取得目前分支名再開 Pages，避免 master/main 不一致
BRANCH=$(git rev-parse --abbrev-ref HEAD)
gh api repos/<帳號>/<repo-name>/pages \
  --method POST -f "source[branch]=$BRANCH" -f "source[path]=/"
```

---

## 執行順序

```
Phase 0: 讀取教材
Phase 1: 輸出大綱 → 等待確認 ← 必須停在這裡
Phase 2: 生成 HTML 骨架（含漸層底圖 CSS）
Phase 3: 填內容（Emoji/SVG 圖標、VIZ 滑桿）
Phase 4: 請使用者用瀏覽器預覽
Phase 5:（選配）上線：GAS Web App（免 Sheets）或 GitHub Pages
```

---

## 參考資源

| 檔案 | 用途 |
|------|------|
| `references/reveal-template.md` | Reveal.js HTML 完整模板、CSS 元件庫 |
