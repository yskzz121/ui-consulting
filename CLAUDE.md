# U&Iコンサルティング レポート仕様

> このリポジトリで作業する際は、以下の仕様に必ず準拠すること。
> 全てのコミュニケーション・出力は日本語で行う。

---

## リポジトリ構造

```
ui-consulting/
├── index.html              # クライアント選択ポータル
├── assets/                 # 共有アセット
│   ├── ui_logo_white.png   # U&I ロゴ（白・フッター用）
│   └── ui_logo.png         # U&I ロゴ（通常）
├── {client-id}/            # クライアントフォルダ
│   ├── index.html          # クライアントポータル or 単一レポート
│   ├── {report}.html       # 各レポートファイル
│   └── {assets}            # クライアント固有のロゴ・画像等
├── CLAUDE.md               # 本仕様書
├── REPORT_SPEC.md          # 詳細仕様（リファレンス）
└── .nojekyll
```

### 命名規則
- クライアントフォルダ: 英字小文字・ハイフン区切り（例: `f-ryukyu`, `mco-japan`）
- レポートファイル: 英字小文字（例: `financial-report.html`）
- 単一レポートの場合: `index.html`
- HTMLの `&` は必ず `&amp;` にエスケープする

---

## デザインシステム（Atlas VI）

### カラーパレット（CSS変数）
```css
:root {
  --navy: #1A2540;        /* 見出し・ヘッダー背景・テーブルヘッダー */
  --navy-light: #243352;  /* セカンダリ背景 */
  --navy-dark: #0F1829;   /* フッター背景・最暗部 */
  --gold: #B8912A;        /* アクセント・セクション下線・バッジ */
  --gold-light: #D4A843;  /* ホバー・ハイライト */
  --gold-pale: rgba(184,145,42,0.08); /* テーブル行ホバー */
  --paper: #F5F2EC;       /* ページ背景 */
  --paper-dark: #EDE8DF;  /* カード内背景 */
  --text: #2C2C2C;        /* 本文 */
  --text-sub: #6B6B6B;    /* 補足 */
  --text-light: #999;     /* 注釈 */
  --positive: #1B7A3D;    /* 改善・ポジティブ */
  --positive-bg: #E8F5E9;
  --negative: #8B2020;    /* 悪化・ネガティブ */
  --negative-bg: #FFEBEE;
  --neutral: #E65100;     /* 注意・中立 */
  --neutral-bg: #FFF3E0;
  --border: #E0DCD4;
  --card-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
```

### タイポグラフィ
| 用途 | フォント | ウェイト |
|------|----------|----------|
| 見出し | `Noto Serif JP` | 700 |
| UI・本文 | `Noto Sans JP` | 300〜900 |
| 英文・数値 | `Inter` | 400〜800 |

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@400;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

---

## ヘッダー仕様（全レポート共通）

```html
<div class="header">
  <div class="header-content">
    <div class="header-logo-row">
      <!-- ロゴがある場合のみ。PNGにはborder-radius:8pxを追加 -->
      <img src="{client-logo}" alt="{client}" style="height:56px;width:auto;border-radius:8px;">
      <div class="ticker-badge">{企業名}</div>
    </div>
    <h1>{レポートタイトル}</h1>
    <div class="subtitle">{サブタイトル}</div>
    <div class="date">分析日: {YYYY年M月D日} ｜ 作成: U&amp;Iコンサルティング</div>
  </div>
</div>
```

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
.header h1 { font-family:'Noto Serif JP',serif; font-size:1.9rem; font-weight:700; color:#fff; margin-bottom:4px; letter-spacing:2px; }
.header .subtitle { color: rgba(255,255,255,0.7); font-size: 0.92rem; }
.header .date { color: rgba(255,255,255,0.5); font-size: 0.78rem; margin-top: 8px; }
```

**ルール:**
- グラデーション背景は全クライアント共通（変更しない）
- ロゴがない場合は `ticker-badge` のみで構成
- 「作成: U&Iコンサルティング」は必ず日付行に含める

---

## フッター仕様（全レポート共通）

**配置: `container` の外**

```html
<div class="footer">
  <div class="footer-content">
    <div class="footer-logo">
      <img src="{相対パス}/ui_logo_white.png" alt="U&amp;I">
      <span>Consulting</span>
    </div>
    <div class="footer-info">
      {企業名} {レポート名} ｜ 分析日: {YYYY年M月D日}
    </div>
    <div class="footer-confidential">最重要機密（CONFIDENTIAL）</div>
  </div>
</div>
```

```css
.footer { background:var(--navy-dark); color:rgba(255,255,255,0.5); padding:28px 20px; text-align:center; }
.footer-logo { display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:14px; }
.footer-logo img { height:28px;opacity:0.85;flex-shrink:0; }
.footer-logo span { color:var(--gold-light);font-family:'Inter',sans-serif;font-weight:600;font-size:0.85rem;line-height:1;letter-spacing:1.5px; }
.footer-info { font-size:0.72rem; margin-bottom:10px; }
.footer-confidential { font-size:0.7rem; font-weight:700; color:var(--gold); letter-spacing:3px; border:1px solid rgba(184,145,42,0.3); display:inline-block; padding:4px 16px; border-radius:4px; }
```

---

## コンポーネント一覧

### セクション
```html
<div class="section">
  <div class="section-title"><span class="icon">{emoji}</span> {タイトル}</div>
  <!-- コンテンツ -->
</div>
```
- 白背景・角丸16px・ゴールド下線

### Executive Summary
```html
<div class="summary-box">
  <h3>{タイトル}</h3>
  <p>{本文 — <span class="highlight">強調</span>}</p>
</div>
```
- navy→navy-darkグラデーション背景・ゴールドハイライト

### スコアカード（Key Metrics）
- `.score-row` — grid: repeat(5, 1fr)
- `.score-card {positive|negative|neutral}` — 上部4px色バー
- 子要素: `.sc-label` `.sc-value {up|down}` `.sc-change {up|down}` `.sc-sub`

### 比較テーブル
- `.comp-table` — navyヘッダー・ゴールドホバー
- `.highlight-row` — 強調行
- `.up` / `.down` — 色付きテキスト

### メトリクスカード
- `.metrics-grid` — grid: repeat(3, 1fr)
- `.metric-card` → `.mc-header` `.mc-label` `.mc-badge {good|bad|warn}` `.mc-values` `.mc-bar` `.mc-bar-fill`

### ゲージカード
- `.gauge-row` — grid: repeat(4, 1fr)
- `.gauge-card` → `.gc-label` `.gc-value` `.gc-unit` `.gc-note`

### 提案カード
- `.proposal-grid` — grid: 1fr 1fr
- `.proposal-card {critical|important|suggest|info}`
- 子要素: `.pc-priority` `.pc-title` `.pc-body` `.pc-impact`

| クラス | 用途 | ボーダー色 |
|--------|------|-----------|
| `critical` | 最重要・即時対応 | `--negative` |
| `important` | 重要・中期 | `--neutral` |
| `suggest` | 推奨・中長期 | `--positive` |
| `info` | 参考・継続 | `#1976D2` |

### アラートボックス
- `.alert-box {warning|danger|success}`

---

## チャート仕様

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

```javascript
Chart.defaults.font.family = "'Inter', 'Noto Sans JP', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = '#6B6B6B';
```

| データ種別 | 色 |
|-----------|-----|
| 主要データ | `#1A2540`（navy） |
| アクセント | `#B8912A`（gold） |
| ポジティブ | `#1B7A3D` |
| ネガティブ | `#8B2020` |
| セカンダリ | `#243352`, `#D4A843`, `#8B7355` |

---

## パスワードロック

- SHA-256ハッシュによるクライアント側認証
- `sessionStorage` でセッション中の再入力不要
- パスワードはクライアントごとに個別設定
- ハッシュ生成: `echo -n "{password}" | shasum -a 256`
- sessionStorageキー: `{client-id}_auth`

---

## レスポンシブ対応

ブレークポイント: `768px`（タブレット以下）、`600px`（スマホ・ポータル）

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

## レポート種別と必須セクション

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

## 新規クライアント追加手順

1. `{client-id}/` フォルダを作成
2. クライアントロゴを配置
3. レポートHTMLを本仕様に準拠して作成
4. パスワードを設定しハッシュを生成
5. ルートの `index.html` にクライアントカードを追加
6. コミット & プッシュ

---

## 禁止事項

- ヘッダー/フッターのデザインをクライアントごとに変更しない
- `--navy`, `--gold`, `--paper` のカラーを変更しない
- U&Iロゴを省略しない
- CONFIDENTIALバッジを省略しない
- `container` 内にフッターを配置しない（必ず外に出す）
- インラインスタイルで `grid-template-columns` を指定しない（メディアクエリが効かなくなる）
- HTMLの `&` をエスケープし忘れない（`&amp;` を使う）
