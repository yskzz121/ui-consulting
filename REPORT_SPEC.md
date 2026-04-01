# U&Iコンサルティング レポート仕様書

> 本書はクライアント向け財務分析レポート（HTMLインフォグラフィック）の統一仕様を定める。
> 全レポートは本仕様に準拠して作成すること。

---

## 1. リポジトリ構造

```
ui-consulting/
├── index.html              # クライアント選択ポータル
├── assets/                 # 共有アセット
│   ├── ui_logo_white.png   # U&I ロゴ（白・フッター用）
│   └── ui_logo.png         # U&I ロゴ（通常）
├── {client-id}/            # クライアントフォルダ（例: f-ryukyu, mco-japan）
│   ├── index.html          # クライアントポータル or 単一レポート
│   ├── {report}.html       # 各レポートファイル
│   └── {assets}            # クライアント固有のロゴ・画像等
├── REPORT_SPEC.md          # 本仕様書
└── .nojekyll               # GitHub Pages用
```

### 命名規則
| 項目 | 規則 | 例 |
|------|------|-----|
| クライアントフォルダ | 英字小文字・ハイフン区切り | `f-ryukyu`, `mco-japan` |
| レポートファイル | 内容を示す英字小文字 | `financial-report.html`, `cross-analysis.html` |
| 単一レポートの場合 | `index.html` | `mco-japan/index.html` |

---

## 2. デザインシステム（Atlas VI）

### 2.1 カラーパレット

| トークン | HEX | 用途 |
|----------|-----|------|
| `--navy` | `#1A2540` | 見出し・ヘッダー背景・テーブルヘッダー |
| `--navy-light` | `#243352` | セカンダリ背景 |
| `--navy-dark` | `#0F1829` | フッター背景・最暗部 |
| `--gold` | `#B8912A` | アクセント・セクション下線・バッジ |
| `--gold-light` | `#D4A843` | ホバー・ハイライト |
| `--gold-pale` | `rgba(184,145,42,0.08)` | テーブル行ホバー |
| `--paper` | `#F5F2EC` | ページ背景 |
| `--paper-dark` | `#EDE8DF` | カード内背景 |
| `--text` | `#2C2C2C` | 本文テキスト |
| `--text-sub` | `#6B6B6B` | 補足テキスト |
| `--text-light` | `#999` | 注釈 |
| `--positive` | `#1B7A3D` | 改善・ポジティブ指標 |
| `--positive-bg` | `#E8F5E9` | ポジティブ背景 |
| `--negative` | `#8B2020` | 悪化・ネガティブ指標 |
| `--negative-bg` | `#FFEBEE` | ネガティブ背景 |
| `--neutral` | `#E65100` | 注意・中立 |
| `--neutral-bg` | `#FFF3E0` | 注意背景 |

### 2.2 タイポグラフィ

| 用途 | フォント | ウェイト |
|------|----------|----------|
| 見出し | `Noto Serif JP` | 700 |
| UI・本文 | `Noto Sans JP` | 300〜900 |
| 英文・数値 | `Inter` | 400〜800 |

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@400;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

### 2.3 基本スタイル

```css
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: 'Noto Sans JP', sans-serif;
  background: var(--paper);
  color: var(--text);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px 60px; }
```

---

## 3. ヘッダー仕様

### 構造
```
┌─────────────────────────────────────────┐
│         [U&Iロゴ] Consulting              │
│            [企業名バッジ]                   │
│           レポートタイトル（h1）              │
│          [N期]  [YYYY年M月度]               │
└─────────────────────────────────────────┘
```

### HTML
```html
<div class="header">
  <div class="header-content">
    <div class="header-ui-logo">
      <img src="../assets/ui_logo_white.png" alt="U&amp;I Consulting">
      <span>Consulting</span>
    </div>
    <div class="header-client-row">
      <div class="ticker-badge">{企業名}</div>
    </div>
    <h1>{レポートタイトル}</h1>
    <div class="header-period">
      <span class="period-fiscal">{N}期</span>
      <span class="period-month">{YYYY年M月度}</span>
    </div>
  </div>
</div>
```

### CSS
```css
.header {
  background: linear-gradient(135deg, #1a2332 0%, #1A2540 50%, #0F1829 100%);
  color: #fff;
  border-bottom: 1px solid rgba(184,145,42,0.15);
  padding: 48px 24px 36px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.header::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse at 30% 50%, rgba(184,145,42,0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 50%, rgba(184,145,42,0.06) 0%, transparent 60%);
}
.header-content { position: relative; z-index: 1; }
.header-logo-row { display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:12px; }
.ticker-badge {
  display: inline-block;
  background: rgba(184,145,42,0.15);
  border: 1px solid rgba(184,145,42,0.3);
  border-radius: 8px;
  padding: 6px 16px;
  font-size: 14px;
  color: var(--gold-light);
  letter-spacing: 1px;
}
.header h1 {
  font-family: 'Noto Serif JP', serif;
  font-size: 1.9rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 4px;
  letter-spacing: 2px;
}
.header .subtitle { color: rgba(255,255,255,0.7); font-size: 0.92rem; }
.header .date { color: rgba(255,255,255,0.5); font-size: 0.78rem; margin-top: 8px; }
```

### ルール
- ヘッダー最上部にU&Iロゴ + 「Consulting」を必ず表示
- 年度（N期）と月度を `header-period` で明確に分離表示
- **分析日は表示しない**
- グラデーション背景は全クライアント共通（変更しない）

---

## 4. フッター仕様

### 構造
```
┌─────────────────────────────────────────┐
│          [U&Iロゴ] Consulting             │
│          {企業名} {レポート名}               │
│         最重要機密（CONFIDENTIAL）          │
└─────────────────────────────────────────┘
```

### HTML
```html
<div class="footer">
  <div class="footer-content">
    <div class="footer-logo">
      <img src="{path}/ui_logo_white.png" alt="U&I">
      <span>Consulting</span>
    </div>
    <div class="footer-info">
      {企業名} {レポート名} ｜ 分析日: {YYYY年M月D日}
    </div>
    <div class="footer-confidential">最重要機密（CONFIDENTIAL）</div>
  </div>
</div>
```

### CSS
```css
.footer {
  background: var(--navy-dark);
  color: rgba(255,255,255,0.5);
  padding: 28px 20px;
  text-align: center;
}
.footer-logo { display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:14px; }
.footer-logo img { height:28px;opacity:0.85;flex-shrink:0; }
.footer-logo span { color:var(--gold-light);font-family:'Inter',sans-serif;font-weight:600;font-size:0.85rem;line-height:1;letter-spacing:1.5px; }
.footer-info { font-size: 0.72rem; margin-bottom: 10px; }
.footer-confidential {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--gold);
  letter-spacing: 3px;
  border: 1px solid rgba(184,145,42,0.3);
  display: inline-block;
  padding: 4px 16px;
  border-radius: 4px;
}
```

### ルール
- フッターは `container` の**外**に配置
- U&Iロゴは `assets/ui_logo_white.png` を参照（相対パスはフォルダ階層に合わせる）
- 「最重要機密（CONFIDENTIAL）」バッジは全レポート必須

---

## 5. セクション仕様

### 基本セクション
```html
<div class="section">
  <div class="section-title"><span class="icon">{emoji}</span> {セクションタイトル}</div>
  <!-- コンテンツ -->
</div>
```

```css
.section {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 28px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border: 1px solid var(--border);
}
.section-title {
  font-family: 'Noto Serif JP', serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--navy);
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--gold);
  display: flex;
  align-items: center;
  gap: 10px;
}
```

### Executive Summary（ダークボックス）
```html
<div class="summary-box">
  <h3>{タイトル}</h3>
  <p>{本文 — <span class="highlight">ハイライト</span>で強調}</p>
</div>
```

```css
.summary-box {
  background: linear-gradient(135deg, var(--navy) 0%, var(--navy-dark) 100%);
  color: #fff;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 28px;
}
.summary-box h3 { color: var(--gold-light); font-family: 'Noto Serif JP', serif; }
.summary-box .highlight { color: var(--gold-light); font-weight: 700; }
```

---

## 6. コンポーネント仕様

### 6.1 スコアカード（Key Metrics）
```html
<div class="score-row"> <!-- grid: repeat(5, 1fr) -->
  <div class="score-card {positive|negative|neutral}">
    <div class="sc-label">{指標名}</div>
    <div class="sc-value {up|down}">{値}</div>
    <div class="sc-change {up|down}">{変化}</div>
    <div class="sc-sub">{補足}</div>
  </div>
</div>
```

### 6.2 比較テーブル
```html
<table class="comp-table">
  <thead><tr><th>...</th></tr></thead>
  <tbody>
    <tr class="highlight-row"><!-- 強調行 --></tr>
    <tr><td class="up">改善</td><td class="down">悪化</td></tr>
  </tbody>
</table>
```

### 6.3 メトリクスカード
```html
<div class="metrics-grid"> <!-- grid: repeat(3, 1fr) -->
  <div class="metric-card">
    <div class="mc-header">
      <div class="mc-label">{指標名}</div>
      <div class="mc-badge {good|bad|warn}">{評価}</div>
    </div>
    <div class="mc-values">
      <div class="mc-current">{現在値}</div>
      <div class="mc-prev">{比較値}</div>
    </div>
    <div class="mc-bar"><div class="mc-bar-fill {good|bad|warn|gold}" style="width:{pct}%"></div></div>
  </div>
</div>
```

### 6.4 ゲージカード
```html
<div class="gauge-row"> <!-- grid: repeat(4, 1fr) -->
  <div class="gauge-card">
    <div class="gc-label">{指標名}</div>
    <div class="gc-value" style="color:var(--{color})">{値}</div>
    <div class="gc-unit">{単位}</div>
    <div class="gc-note">{補足}</div>
  </div>
</div>
```

### 6.5 提案カード
```html
<div class="proposal-grid"> <!-- grid: 1fr 1fr -->
  <div class="proposal-card {critical|important|suggest|info}">
    <div class="pc-priority">{優先度ラベル}</div>
    <div class="pc-title">{提案タイトル}</div>
    <div class="pc-body">{本文}</div>
    <div class="pc-impact">想定効果: {効果}</div>
  </div>
</div>
```

| クラス | 用途 | ボーダー色 |
|--------|------|-----------|
| `critical` | 最重要・即時対応 | `--negative` |
| `important` | 重要・中期 | `--neutral` |
| `suggest` | 推奨・中長期 | `--positive` |
| `info` | 参考・継続 | `#1976D2` |

### 6.6 アラートボックス
```html
<div class="alert-box {warning|danger|success}">
  <strong>{見出し}</strong>{本文}
</div>
```

---

## 7. チャート仕様

### ライブラリ
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### グローバル設定
```javascript
Chart.defaults.font.family = "'Inter', 'Noto Sans JP', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = '#6B6B6B';
```

### カラー使用ルール
| データ種別 | 色 |
|-----------|-----|
| 主要データ（売上等） | `#1A2540`（navy） |
| アクセント（利益等） | `#B8912A`（gold） |
| ポジティブ | `#1B7A3D` |
| ネガティブ | `#8B2020` |
| セカンダリ | `#243352`, `#D4A843`, `#8B7355` |

### チャートコンテナ
```html
<div class="chart-container" style="height:{height}px">
  <canvas id="{chartId}"></canvas>
</div>
```

---

## 8. パスワードロック仕様

全クライアントレポートにはパスワード認証を実装する。

### 方式
- SHA-256ハッシュによるクライアント側認証
- `sessionStorage` でセッション中の再入力不要
- パスワードはクライアントごとに個別設定

### ロック画面構造
```
┌──────────────────────────────┐
│           🔒                  │
│      {企業名 or ロゴ}          │
│   閲覧にはパスワードが必要です    │
│     [_________________]       │
│       [  閲覧する  ]           │
│                              │
│    U&Iコンサルティング          │
└──────────────────────────────┘
```

### パスワード管理
| クライアント | パスワード | ハッシュ生成方法 |
|------------|-----------|----------------|
| 各クライアント | 個別設定 | `echo -n "{pw}" \| shasum -a 256` |

### sessionStorageキー命名
- `{client-id}_auth` （例: `mco_auth`, `fr_auth`）

---

## 9. レスポンシブ対応

### ブレークポイント
- `768px` — タブレット以下
- `600px` — スマートフォン（ポータル用）

### 768px以下の必須ルール
```css
@media(max-width:768px){
  .score-row { grid-template-columns: repeat(2, 1fr); }
  .metrics-grid { grid-template-columns: 1fr; }
  .chart-row { grid-template-columns: 1fr; }
  .proposal-grid { grid-template-columns: 1fr; }
  .two-col { grid-template-columns: 1fr; }
  .gauge-row { grid-template-columns: repeat(2, 1fr); }
  .overview-grid { grid-template-columns: 1fr; }
  .header h1 { font-size: 1.4rem; }
  .header-logo-row { flex-direction:column;gap:8px; }
  .ticker-badge { font-size:12px;padding:4px 12px; }
  .section { padding: 20px 16px; }
  .comp-table { font-size: 0.75rem; }
  .comp-table thead th, .comp-table tbody td { padding: 8px 10px; }
}
```

---

## 10. レポート種別と必須セクション

### 月次P/L分析（前年同月比較）
1. Executive Summary
2. Key Metrics（スコアカード5枚）
3. KPIカード（営業日数・客数・客単価・日販等）
4. 前年同月比P/Lテーブル（7列: 科目 / 前年 / 構成比 / 当年 / 構成比 / 増減額 / YoY）
5. 売上構成分析（チャネル別ドーナツチャート）
6. FL比率分析（F+L構成バー・シミュレーション）
7. 原価構造詳細
8. B/S分析（該当月がある場合）
9. 損益分岐点分析
10. コンサルティング提案（提案カード）
11. 総合評価（ダークボックス）

### 財務分析レポート（期間累計）
1. Executive Summary
2. Key Metrics
3. 収益性分析（テーブル + チャート）
4. 資本効率性分析（ROA・ROE・DuPont分解）
5. 安全性分析（流動比率・自己資本比率等）
6. 在庫回転分析
7. CCC分析
8. 改善提案

### 直接原価計算クロス分析
1. Executive Summary
2. 変動費・固定費分解
3. 損益分岐点分析
4. 安全余裕率
5. 感度分析
6. 期間比較

---

## 11. 新規クライアント追加手順

1. `{client-id}/` フォルダを作成
2. クライアントロゴを配置
3. レポートHTMLを本仕様に準拠して作成
4. パスワードを設定しハッシュを生成
5. ルートの `index.html` にクライアントカードを追加
6. コミット & プッシュ

---

## 12. 禁止事項

- ヘッダー/フッターのデザインをクライアントごとに変更しない
- `--navy`, `--gold`, `--paper` のカラーを変更しない
- U&Iロゴを省略しない
- CONFIDENTIAL バッジを省略しない
- `container` 内にフッターを配置しない（必ず外に出す）
- インラインスタイルで `grid-template-columns` を指定しない（メディアクエリが効かなくなるため）
