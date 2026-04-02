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

```css
.header {
  background: linear-gradient(135deg, #1a2332 0%, #1A2540 50%, #0F1829 100%);
  color: #fff;
  border-bottom: 1px solid rgba(184,145,42,0.15);
  padding: 48px 24px 40px;
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
.header-ui-logo { display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:20px; }
.header-ui-logo img { height:28px;opacity:0.85;flex-shrink:0; }
.header-ui-logo span { color:var(--gold-light);font-family:'Inter',sans-serif;font-weight:600;font-size:0.8rem;letter-spacing:1.5px; }
.header-client-row { display:flex;align-items:center;justify-content:center;gap:16px;margin-bottom:12px; }
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
.header h1 { font-family:'Noto Serif JP',serif; font-size:1.9rem; font-weight:700; color:#fff; margin-bottom:8px; letter-spacing:2px; }
.header-period { display:flex;align-items:center;justify-content:center;gap:16px;margin-top:4px; }
.period-fiscal { background:rgba(184,145,42,0.2);border:1px solid rgba(184,145,42,0.4);border-radius:6px;padding:4px 14px;font-size:0.85rem;color:var(--gold-light);font-weight:700;letter-spacing:1px; }
.period-month { font-size:1.1rem;color:rgba(255,255,255,0.9);font-weight:700;letter-spacing:1px; }
```

**ルール:**
- ヘッダー最上部にU&Iロゴ + 「Consulting」を必ず表示（U&Iコンサルティングの成果物であることを明示）
- U&Iロゴは `../assets/ui_logo_white.png` を参照
- クライアントロゴがある場合は `header-client-row` 内に ticker-badge と並べて配置
- 年度（N期）と月度（YYYY年M月度）を `header-period` で明確に分離表示
- **分析日は表示しない**（不要）
- グラデーション背景は全クライアント共通（変更しない）

## ヘッダー直後の余白

ヘッダーと最初のセクション（Executive Summary等）の間に十分な余白を確保する。

```css
.container { max-width: 1200px; margin: 0 auto; padding: 40px 24px 60px; }
```

`container` の `padding-top: 40px` により、ヘッダーとコンテンツの間に余白が生まれる。

---

## フッター仕様（全レポート共通）

**配置: `container` の外**

```html
<div class="footer">
  <div class="footer-content">
    <div class="footer-logo">
      <img src="../assets/ui_logo_white.png" alt="U&amp;I">
      <span>Consulting</span>
    </div>
    <div class="footer-info">
      {企業名} {レポート名}
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
- `.score-card` — 白背景・角丸・シャドウのみ。**カラーアクセント（上部色バー等）は使用禁止**
- 子要素: `.sc-label` `.sc-value {up|down}` `.sc-change {up|down}` `.sc-sub`
- `{positive|negative|neutral}` クラスによるボーダー色変更は**廃止**

### 比較テーブル
- `.comp-table` — navyヘッダー・ゴールドホバー
- `.highlight-row` — 強調行
- `.up` / `.down` — 色付きテキスト

### メトリクスカード
- `.metrics-grid` — grid: repeat(3, 1fr)
- `.metric-card` → `.mc-header` `.mc-label` `.mc-badge {good|bad|warn}` `.mc-values` `.mc-bar` `.mc-bar-fill`
- **カラーアクセント（ボーダー色変更）は使用禁止**。バッジのテキスト色のみで状態を表現

### ゲージカード
- `.gauge-row` — grid: repeat(4, 1fr)
- `.gauge-card` → `.gc-label` `.gc-value` `.gc-unit` `.gc-note`
- **カラーアクセント（ボーダー色変更）は使用禁止**

### 提案カード
- `.proposal-grid` — grid: 1fr 1fr
- `.proposal-card` — 白背景・角丸・シャドウのみ。**カラーアクセント（左ボーダー色等）は使用禁止**
- 子要素: `.pc-priority` `.pc-title` `.pc-body` `.pc-impact`
- 優先度はテキストラベル（最重要/重要/推奨/参考）で表現。ボーダー色による区別は**廃止**

### アラートボックス
- `.alert-box {warning|danger|success}`
- **カラーアクセント（左ボーダー色等）は使用禁止**。アイコンとテキスト色のみで状態を表現

---

## カラーアクセント禁止ルール（全コンポーネント共通）

**全てのカードパネル・ボックスコンポーネントにおいて、枠線へのカラーアクセント（色付きボーダー、上部色バー、左ボーダー色等）の使用を禁止する。**

- スコアカード: `border-top` の色分け → 廃止。`border: 1px solid var(--border)` に統一
- 提案カード: `border-left` の色分け → 廃止。`border: 1px solid var(--border)` に統一
- メトリクスカード: ボーダー色変更 → 廃止
- ゲージカード: ボーダー色変更 → 廃止
- アラートボックス: `border-left` の色分け → 廃止
- 状態の区別はテキスト色（`.up` / `.down`）、バッジテキスト、アイコンで表現する

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

---

## 運用ワークフロー

### フォルダ構成（クライアントごと）

```
{client-id}/
├── profile.yaml        ← クライアント定義（KPI・重点テーマ・レポートスタイル）
├── inbox/              ← 素材置き場（PDF・メモ・スプシURL等、何でも放り込む）
│   ├── {YYYY-MM}_試算表.pdf
│   ├── {YYYY-MM}_面談メモ.md
│   └── {YYYY-MM}_スプシURL.txt
├── data/               ← 構造化データ蓄積（Claude Codeが自動生成）
│   └── {YYYY-MM}.yaml
├── db/                 ← 累積経営DB（Claude Codeが自動追記）
│   ├── monthly_pl.csv  ← PL月次推移
│   ├── monthly_kpi.csv ← 業種固有KPI月次推移
│   ├── monthly_bs.csv  ← BS月次推移（BS提出ありの場合）
│   └── monthly_store.csv ← 店舗別月次推移（多店舗の場合）
├── index.html          ← クライアントポータル
└── {report}.html       ← レポート本体
```

### レポート生成フロー

```
「○○社の{月}レポート作って」

  Step 1: profile.yaml 読み込み
          → KPI定義・重点テーマ・レポートスタイルを把握

  Step 2: inbox/ の該当月の素材を全て読み込み
          → PDF → 数値抽出
          → メモ → 論点抽出
          → URL → アクセスして内容取得

  Step 3: data/{YYYY-MM}.yaml に構造化データを保存
          → 過去データ（data/内の他YAML）と比較可能にする

  Step 4: 分析（下記の分析フレームワークに従う）
          → 第1層〜第4層を順に算出
          → profile.yamlのtarget/alert_thresholdと照合
          → focus_topicsの進捗判定

  Step 5: レポート生成（HTML）
          → 本CLAUDE.mdのデザインシステム・コンポーネントに準拠
          → REPORT_SPEC.mdのセクション仕様に準拠
          → profile.yamlのreport_styleに従う
          → excluded_sectionsは出力しない

  Step 6: {client-id}/ にレポートHTMLを保存
```

### 面談メモのフォーマット

inbox/ に以下の3ブロック構成で記載する。厳密なフォーマットは不要、箇条書きで可。

```markdown
# {会社名} {YYYY-MM} 面談メモ

## 数字（言ってたこと）
- 売上○○万くらい
- 原価率が○○%台

## トピック
- 新メニュー投入予定
- 採用状況

## 気になったこと
- 社長の様子や温度感
- 把握できていなさそうな問題
```

---

## 分析フレームワーク

### 第1層: 財務分析（全社必須）

全クライアント共通で以下の項目をYoY（前年同月比）・MoM（前月比）で算出する。

| 項目 | YoY | MoM | 備考 |
|------|:---:|:---:|------|
| 売上高 | o | o | 金額＋増減率 |
| 売上総利益（粗利益） | o | o | 金額＋粗利率も併記 |
| 固定費合計 | o | o | 金額＋増減率 |
| 重点コスト項目（2〜3項目） | o | o | profile.yamlのfocus_costsに定義 |
| 営業利益 | o | o | 金額＋営業利益率も併記 |

重点コスト項目は業種によって金額が大きくなる項目（人件費・外注費・原材料費・家賃等）をprofile.yamlで指定する。

### 第2層: 収益性・効率性指標

profile.yamlのefficiencyに定義された指標のみ算出・表示する。全社一律ではない。

| 指標 | 対象業種の例 |
|------|------------|
| 客数・客単価 | 飲食、フィットネス、学習塾 |
| ロス率（廃棄率） | 飲食、製造 |
| 労働分配率 | サービス業全般（不動産賃貸を除く） |
| ROI | マーケティング、不動産 |
| ROA | 全業種 |
| ROE | 全業種 |

業種固有KPI（profile.yamlのindustry_kpis）もこの層で出力する。

### 第3層: 財務健全性（BS項目）

profile.yamlの `balance_sheet.available: true` の場合のみ算出・表示する。

| 指標 |
|------|
| 流動比率 |
| 自己資本比率 |

BS未提出（`available: false`）の場合:
- 該当セクション自体を非表示
- レポート末尾に「BS提出によりさらに深い財務健全性分析が可能です」と添える

### 第4層: キャッシュフロー

profile.yamlの `cashflow.available: true` の場合のみ算出・表示する。

| 指標 | 算出方法 |
|------|---------|
| FCF（フリーキャッシュフロー） | 営業CF − 投資CF |

method: simplified の場合は簡易法（当期純利益＋減価償却費−運転資本増減）で推定する。

---

## 月次レポート構成順序

```
 1. ヘッダー（本CLAUDE.mdの統一仕様に準拠）
 2. Executive Summary（summary-box。3行以内で結論）
 3. Key Metrics（score-row / score-card）
 4. 財務分析
    ├── 売上高（YoY・MoM・推移チャート）
    ├── 売上総利益・粗利率（YoY・MoM）
    ├── 重点コスト項目（profile.yamlのfocus_costs、YoY・MoM）
    ├── 固定費合計（YoY・MoM）
    └── 営業利益・営業利益率（YoY・MoM）
 5. 収益性・効率性指標（該当項目のみ。metrics-grid）
 6. 業種固有KPI（該当項目のみ）
 7. 財務健全性（BS提出ありの場合のみ。gauge-row）
 8. キャッシュフロー（データありの場合のみ）
 9. 重点テーマの進捗（profile.yamlのfocus_topics）
10. 課題と提言（3項目以内。proposal-card）
11. Next Action（具体的なアクション、期限付き）
12. フッター（本CLAUDE.mdの統一仕様に準拠。CONFIDENTIAL必須）
```

---

## data/ 構造化データ仕様

Claude Codeがinbox/の素材を解釈し、以下の形式で data/{YYYY-MM}.yaml に蓄積する。

```yaml
period: "YYYY-MM"
source_files:
  - "{YYYY-MM}_試算表.pdf"
  - "{YYYY-MM}_面談メモ.md"

financial:
  revenue: 0              # 売上高（万円）
  cogs: 0                 # 売上原価
  gross_profit: 0         # 売上総利益
  gross_margin: 0.0       # 粗利率（%）
  fixed_costs: 0          # 固定費合計
  operating_profit: 0     # 営業利益
  operating_margin: 0.0   # 営業利益率（%）
  focus_costs:            # profile.yamlのfocus_costsに対応
    項目名: 0

efficiency:               # profile.yamlのefficiencyに対応
  項目名: null            # 算出不可の場合はnull

industry_kpis:            # profile.yamlのindustry_kpisに対応
  項目名: null

balance_sheet:            # available: trueの場合のみ
  current_ratio: null     # 流動比率（%）
  equity_ratio: null      # 自己資本比率（%）

cashflow:
  fcf: null               # FCF（万円）
  method: simplified

notes: |
  面談メモから抽出した定性情報
```

---

## 累積経営DB（db/）

### 目的
クライアントごとの経営指標を月次で蓄積し、四半期・半期・通期まとめ、前年比較、3期比較など深い分析の基盤とする。

### 運用ルール
- **レポート生成時に自動追記**: 月次レポートを生成するたびに、当月のデータをdb/の各CSVに1行追記する
- **既存行は上書きしない**: 同一periodの行が既に存在する場合のみ更新。それ以外は追記のみ
- **CSVはクライアントごとに独立**: 業種ごとにKPI項目が異なるため、全社統合はしない
- **db/フォルダは .gitignore で除外**: クライアント機密データをGitHubに上げない

### ファイル構成

| ファイル | 内容 | 対象 |
|--------|------|------|
| `monthly_pl.csv` | 損益計算書の月次推移（売上・粗利・営業利益・重点コスト等） | 全社 |
| `monthly_kpi.csv` | 業種固有KPIの月次推移（会員数・セッション数・案件数等） | 全社 |
| `monthly_bs.csv` | 貸借対照表の月次推移（流動比率・自己資本比率等） | BS提出ありの場合 |
| `monthly_store.csv` | 店舗別の月次推移（売上・営業利益・YoY等） | 多店舗ビジネスの場合 |

### monthly_pl.csv 共通列（全社）

```csv
period,revenue,cogs,gross_profit,gross_margin_pct,sg_and_a,labor_cost,labor_share_pct,operating_profit,operating_margin_pct,ordinary_profit,net_income,fcf,focus_cost_1_name,focus_cost_1,focus_cost_2_name,focus_cost_2,focus_cost_3_name,focus_cost_3
```

- `period`: YYYY-MM形式
- `focus_cost_1〜3`: profile.yamlのfocus_costsに対応する重点コスト項目
- 業種によって追加列あり（executive_comp, store_labor等）

### monthly_kpi.csv の列はクライアントごとに定義

profile.yamlの `industry_kpis` に対応する列を設定する。例:

**パーソナルジム（B.U.G）:**
```csv
period,members,new_members,total_sessions,avg_sessions,trainers,session_unit_price,labor_share_all_pct,toc_revenue,tob_revenue
```

**ウェブマーケ（ふ々屋）:**
```csv
period,online_salon,career_design,consulting,course_revenue,kodomoya,total_clients,backend_orders
```

### 活用方法

レポート生成時にdb/のCSVを読み込み、以下の分析に活用する:
- **前月比（MoM）**: 直近2行の比較
- **前年同月比（YoY）**: 12ヶ月前の行との比較
- **四半期まとめ**: 3ヶ月分の集計・平均
- **半期・通期まとめ**: 6ヶ月 or 12ヶ月分の集計
- **3期比較**: 過去3年分のデータを横並び比較
- **トレンド分析**: 推移チャートの描画

---

## デプロイ

- Gitの操作（commit / push）は本人のみが行う。福原・園子はGitを操作しない
- レポートHTML生成後、Google Drive経由で本人のPCに自動同期される
- 本人がレビュー後に git add → commit → push でGitHub Pagesに公開
- inbox/、data/、db/ は .gitignore で除外済み（クライアント機密データをGitHubに上げない）
