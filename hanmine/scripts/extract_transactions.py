#!/usr/bin/env python3
"""
半嶺事務所 — 売上明細PDF → トランザクションCSV/顧客マスタCSV 抽出スクリプト

各月のPDFは形式が異なるため、月ごとにパーサを切り替える。
出力先:
  ../db/transactions.csv  : 取引明細（行=1取引）
  ../db/customers.csv      : 顧客マスタ（集計済）

使い方:
  python3 extract_transactions.py
"""

import os
import re
import csv
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import pdfplumber

INBOX = Path('/Users/yskzz121/Library/CloudStorage/GoogleDrive-y.uema@u-and-i.co.jp/共有ドライブ/U&I_Consulting/ui-consulting/hanmine/inbox')
DB    = Path(__file__).resolve().parent.parent / 'db'

# ============================================================
# 顧客名 正規化辞書 (表記ゆれ統一)
# ============================================================
NORMALIZE_MAP = {
    # ou2/オーツー/クレバリーホーム関連
    'ou2': 'ou2株式会社（クレバリーホーム）',
    'Ou2': 'ou2株式会社（クレバリーホーム）',
    'OU2': 'ou2株式会社（クレバリーホーム）',
    'クレバリーホーム': 'ou2株式会社（クレバリーホーム）',
    'Ou2(オーツ―)株式会社 クレバリーホーム': 'ou2株式会社（クレバリーホーム）',
    'Ou2(オーツ―)株式会社': 'ou2株式会社（クレバリーホーム）',
    'ou2株式会社': 'ou2株式会社（クレバリーホーム）',
    # パナソニックホームズ
    'パナソニックホームズ株式会社': 'パナソニックホームズ株式会社',
    'パナソニックホームズ': 'パナソニックホームズ株式会社',
    'パナソニックホームズ(': 'パナソニックホームズ株式会社',
    # エスケーホーム
    '株式会社エスケーホーム': '株式会社エスケーホーム',
    'エスケーホーム': '株式会社エスケーホーム',
    # ASAKA
    '株式会社ASAKA': '株式会社ASAKA',
    # 公嘱協会
    '公嘱': '公益社団法人 沖縄県公共嘱託登記土地家屋調査士協会',
    '公益社団法人 沖縄県公共嘱託登記土地家屋調査士協会': '公益社団法人 沖縄県公共嘱託登記土地家屋調査士協会',
    # 大鏡
    '大鏡建設(株)': '大鏡建設株式会社',
    '大鏡建設': '大鏡建設株式会社',
    '大鏡建設株式会社': '大鏡建設株式会社',
    # 大原
    '大原工業商事株式会社': '大原工業商事株式会社',
    # 沖電開発
    '沖電開発株式会社': '沖電開発株式会社',
    # 大和ハウス
    '大和ハウスパーキング': '大和ハウスパーキング',
    '大和ハウス工業株式会社': '大和ハウス工業株式会社',
    # 日商エステム
    '株式会社日商エステム': '株式会社日商エステム',
    '㈱日商エステム': '株式会社日商エステム',
    # 匡事務所
    '匡事務所': '土地家屋調査士法人匡事務所',
    '土地家屋調査士法人匡事務所': '土地家屋調査士法人匡事務所',
    # 新洋
    '株式会社新洋': '株式会社新洋',
    '(株)新洋': '株式会社新洋',
    # その他
    '株式会社琉信ハウジング': '株式会社琉信ハウジング',
    'STUDIO MONAKA': 'STUDIO MONAKA',
    '株式会社ライズ': '株式会社ライズ',
    '株式会社エレファントライフ': '株式会社エレファントライフ',
    'おきなわ法律事務所': 'おきなわ法律事務所',
    'レスター司法書士法人': 'レスター司法書士法人',
    '宮城匠司法書士事務所': '宮城匠司法書士事務所',
    'サファリエステート株式会社': 'サファリエステート株式会社',
    'エールクリエイト株式会社': 'エールクリエイト株式会社',
    '株式会社MOANA': '株式会社MOANA',
    '株式会社ADeR': '株式会社ADeR',
    '株式会社エー・アール・ジー': '株式会社エー・アール・ジー',
    'オール・デザイン': 'オール・デザイン',
    '株式会社福地組': '株式会社福地組',
    '株式会社建築意思': '株式会社建築意思',
    '株式会社福岡ビルメンテナンス': '株式会社福岡ビルメンテナンス',
    'リモビリエ株式会社': 'リモビリエ株式会社',
    'ハウスドゥジャパン': 'ハウスドゥジャパン',
    'Matthewsoffice株式会社': 'Matthewsoffice株式会社',
    '三和交通株式会社': '三和交通株式会社',
    '行政': '行政（公的機関）',
    '那覇市長': '行政（公的機関）',
    'N&A合同会社': 'N&A合同会社',
    '農業生産法人有限会社グラウンドパイオニア': '農業生産法人有限会社グラウンドパイオニア',
    'キーストーンエステート株式会社': 'キーストーンエステート株式会社',
    '株式会社ASAKA': '株式会社ASAKA',
}

# 顧客分類カテゴリ
CATEGORY_MAP = {
    'ou2株式会社（クレバリーホーム）': ('ハウスメーカー', '法人'),
    'パナソニックホームズ株式会社': ('ハウスメーカー', '法人'),
    '株式会社エスケーホーム': ('ハウスメーカー', '法人'),
    '大鏡建設株式会社': ('建設業', '法人'),
    '大原工業商事株式会社': ('建設業', '法人'),
    '沖電開発株式会社': ('不動産開発', '法人'),
    '大和ハウスパーキング': ('不動産開発', '法人'),
    '大和ハウス工業株式会社': ('ハウスメーカー', '法人'),
    '株式会社日商エステム': ('不動産開発', '法人'),
    '株式会社新洋': ('不動産開発', '法人'),
    '株式会社琉信ハウジング': ('不動産開発', '法人'),
    '株式会社ライズ': ('不動産開発', '法人'),
    '株式会社エレファントライフ': ('不動産開発', '法人'),
    '株式会社ADeR': ('不動産開発', '法人'),
    '株式会社エー・アール・ジー': ('不動産開発', '法人'),
    '株式会社ASAKA': ('不動産開発', '法人'),
    'サファリエステート株式会社': ('不動産開発', '法人'),
    'キーストーンエステート株式会社': ('不動産開発', '法人'),
    'ハウスドゥジャパン': ('ハウスメーカー', '法人'),
    '株式会社福地組': ('建設業', '法人'),
    '株式会社建築意思': ('建設業', '法人'),
    '株式会社福岡ビルメンテナンス': ('建設業', '法人'),
    'リモビリエ株式会社': ('不動産開発', '法人'),
    'Matthewsoffice株式会社': ('不動産開発', '法人'),
    '三和交通株式会社': ('その他法人', '法人'),
    '株式会社MOANA': ('不動産開発', '法人'),
    '土地家屋調査士法人匡事務所': ('士業連携', '法人'),
    'おきなわ法律事務所': ('士業連携', '法人'),
    'レスター司法書士法人': ('士業連携', '法人'),
    '宮城匠司法書士事務所': ('士業連携', '法人'),
    'エールクリエイト株式会社': ('その他法人', '法人'),
    'STUDIO MONAKA': ('設計事務所', '法人'),
    'オール・デザイン': ('設計事務所', '法人'),
    'N&A合同会社': ('不動産開発', '法人'),
    '農業生産法人有限会社グラウンドパイオニア': ('農業法人', '法人'),
    '公益社団法人 沖縄県公共嘱託登記土地家屋調査士協会': ('業界団体', '団体'),
    '行政（公的機関）': ('公的機関', '行政'),
}

def normalize_customer(raw):
    """生の取引先名を正規化"""
    if not raw:
        return ('不明', '不明')
    s = unicodedata.normalize('NFKC', str(raw)).strip()
    s = s.replace(' ', '').replace('\u3000', '')
    # 完全一致優先
    for k, v in NORMALIZE_MAP.items():
        if s == k.replace(' ','').replace('\u3000',''):
            return (v, 'matched')
    # 部分一致
    for k, v in NORMALIZE_MAP.items():
        kk = k.replace(' ','').replace('\u3000','')
        if kk and (kk in s or s in kk):
            return (v, 'partial')
    # 新規顧客 / 紹介 / 一般 系列の特殊扱い
    if '新規顧客' in s or '新規' in s:
        return ('新規顧客', 'special')
    if '紹介' in s or '設計事務所の紹介' in s:
        return ('紹介経由', 'special')
    if '一般' == s or s.startswith('一般'):
        return ('一般（個人スポット）', 'special')
    if '継続顧客' in s:
        return ('継続顧客', 'special')
    return (s, 'other')

def parse_amount(s):
    if s is None:
        return 0
    s = str(s).replace(',', '').replace('¥', '').replace('￥', '').strip()
    s = re.sub(r'[^\d-]', '', s)
    try:
        return int(s) if s else 0
    except ValueError:
        return 0

def parse_date_jp(s, ym_default):
    """日付文字列をYYYY-MM-DDに正規化。失敗時はym_default-01"""
    if not s:
        return f'{ym_default}-01'
    s = str(s).strip()
    # YYYY-MM-DD
    m = re.match(r'(\d{4})-(\d{1,2})-(\d{1,2})', s)
    if m:
        return f'{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
    # YYYY/M/D
    m = re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})', s)
    if m:
        return f'{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
    # MM/DD only
    m = re.match(r'(\d{1,2})/(\d{1,2})', s)
    if m:
        y, mo = ym_default.split('-')
        return f'{y}-{int(m.group(1)):02d}-{int(m.group(2)):02d}'
    # R8.M.D (令和)
    m = re.match(r'R(\d+)\.(\d{1,2})\.(\d{1,2})', s)
    if m:
        year = 2018 + int(m.group(1))
        return f'{year:04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
    return f'{ym_default}-01'


# ============================================================
# 各月パーサ
# ============================================================
def extract_text_lines(pdf_path):
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                lines.extend([l for l in txt.split('\n') if l.strip()])
    return lines

def parse_2025_07(pdf_path, ym='2025-07'):
    """7月: 簡易フォーマット (土地/建物セクション)"""
    lines = extract_text_lines(pdf_path)
    rows = []
    section = None
    for line in lines:
        if '土地' in line and 'ランク' in line:
            section = '土地'
            continue
        if line.startswith('建物') or '種別' in line and '相⼿先' in line:
            section = '建物'
            continue
        if line.startswith('7⽉計') or line.startswith('合計'):
            continue
        # 行例: "07/09 C 匡事務所 修理代 87,400"
        m = re.match(r'^(\d{1,2}/\d{1,2})\s+([ABCＡＢＣ売掛金]+)?\s*(.+?)\s+(\d{2,3}(?:,\d{3})*)\s*$', line)
        if m:
            date_s = m.group(1)
            rank = m.group(2) or ''
            rest = m.group(3).strip()
            amount = parse_amount(m.group(4))
            # rest = "相手先 + 業務内容" の混在
            rows.append({
                'year_month': ym,
                'date': parse_date_jp(date_s, ym),
                'customer_raw': rest.split()[0] if rest else '',
                'service': ' '.join(rest.split()[1:]) if len(rest.split()) > 1 else rest,
                'category': section or '',
                'rank': rank.strip(),
                'ref_no': '',
                'end_client': '',
                'amount': amount,
                'staff': '',
                'attribute': '',
                'source_file': pdf_path.name,
            })
    return rows

def parse_general_ledger(pdf_path, ym, amount_pos_from_end=1):
    """8月,9月,11月: 総勘定元帳形式 (売上高 から始まる)
    amount_pos_from_end: 末尾から何番目の数値を金額とするか
      8月=1（貸方金額のみ）, 9月=2（貸方+累計）, 11月=1
    """
    lines = extract_text_lines(pdf_path)
    rows = []
    has_attr = any('属性' in l and '部門' in l for l in lines[:5])
    for line in lines:
        if not line.startswith('売上高'):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        date = parts[1]
        rest = parts[2:]
        # 全数値トークンを抽出（ref_no = 2025_xxx は除外）
        nums = []
        for i, tok in enumerate(rest):
            if re.match(r'^\d{4}_\d+$', tok):
                continue
            try:
                v = int(tok.replace(',',''))
                if 1000 <= v <= 5000000:  # 妥当な取引額レンジ
                    nums.append((i, v))
            except ValueError:
                pass
        if not nums:
            continue
        # 末尾からN番目を取得
        idx = len(nums) - amount_pos_from_end
        if idx < 0:
            idx = 0
        amount = nums[idx][1]
        rest_pre = rest[:nums[idx][0]]
        cat = ''
        rank = ''
        for j, tok in enumerate(rest_pre):
            if tok in ('建物', '土地'):
                cat = tok
                if j+1 < len(rest_pre) and rest_pre[j+1] in ('A','B','C','Ａ','Ｂ','Ｃ'):
                    rank = rest_pre[j+1]
                break
        customer = rest_pre[0] if rest_pre else ''
        attr = ''
        if has_attr:
            for tok in rest_pre:
                if tok in ('リピートA','リピートB','リピートC','リピート','紹介','新規'):
                    attr = tok
                    break
        # ref_no
        ref_no = ''
        for tok in rest:
            if re.match(r'^\d{4}_\d+', tok):
                ref_no = tok[:8]
                break
        rows.append({
            'year_month': ym,
            'date': parse_date_jp(date, ym),
            'customer_raw': customer,
            'service': ' '.join(rest_pre[1:]) if len(rest_pre) > 1 else '',
            'category': cat,
            'rank': rank,
            'ref_no': ref_no,
            'end_client': '',
            'amount': amount,
            'staff': '',
            'attribute': attr,
            'source_file': pdf_path.name,
        })
    return rows

def parse_2025_12(pdf_path, ym='2025-12'):
    """12月: 中間形式"""
    lines = extract_text_lines(pdf_path)
    rows = []
    for line in lines:
        if not line.startswith('売上高'):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        date = parts[1]
        rest = parts[2:]
        # 末尾2つは金額の可能性 (貸方金額, 発生額累計) -> 1つ目を使う
        amounts = []
        i = len(rest)-1
        while i >= 0:
            try:
                a = int(rest[i].replace(',',''))
                amounts.insert(0, a)
                i -= 1
            except ValueError:
                break
        rest_pre = rest[:i+1]
        if not amounts:
            continue
        amount = amounts[0] if amounts else 0  # 貸方金額
        if amount > 10000000:
            continue
        cat = ''
        for tok in rest_pre:
            if tok in ('建物','土地'):
                cat = tok
                break
        customer = rest_pre[0] if rest_pre else ''
        rows.append({
            'year_month': ym,
            'date': parse_date_jp(date, ym),
            'customer_raw': customer,
            'service': ' '.join(rest_pre[1:]) if len(rest_pre) > 1 else '',
            'category': cat,
            'rank': '',
            'ref_no': '',
            'end_client': '',
            'amount': amount,
            'staff': '',
            'attribute': '',
            'source_file': pdf_path.name,
        })
    return rows

def parse_2026_01(pdf_path, ym='2026-01'):
    """1月: 土地/建物セクション独立, R8.M.D形式"""
    lines = extract_text_lines(pdf_path)
    rows = []
    section = None
    for line in lines:
        if line.strip() == '土地':
            section = '土地'
            continue
        if line.strip() == '建物':
            section = '建物'
            continue
        if line.startswith('取引日'):
            continue
        if '売上合計' in line or '件 ' in line:
            continue
        # R8.1.19 株式会社ライズ 土地 2025_2... 402,728 A
        m = re.match(r'^(R\d+\.\d{1,2}\.\d{1,2})\s+(.+?)\s+(土地|建物)\s+(.+?)\s+([\d,]+)(?:\s+([ABCＡＢＣ\d\.]+))?\s*$', line)
        if m:
            date = m.group(1)
            customer = m.group(2).strip()
            cat = m.group(3)
            mid = m.group(4)
            amount = parse_amount(m.group(5))
            rank = (m.group(6) or '').strip()
            # mid から ref_no 抽出
            ref_match = re.match(r'(\d{4}_\d+)', mid)
            ref_no = ref_match.group(1) if ref_match else ''
            rows.append({
                'year_month': ym,
                'date': parse_date_jp(date, ym),
                'customer_raw': customer,
                'service': mid,
                'category': cat,
                'rank': rank,
                'ref_no': ref_no,
                'end_client': '',
                'amount': amount,
                'staff': '',
                'attribute': '',
                'source_file': pdf_path.name,
            })
    return rows

def parse_2026_03(pdf_path, ym='2026-03'):
    """3月: テーブル形式 (土地/建物/その他セクション)"""
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            section = None
            for t in tables:
                for row in t:
                    if not row:
                        continue
                    first = (row[0] or '').strip() if row[0] else ''
                    if '土地関連' in first:
                        section = '土地'
                        continue
                    if '建物関連' in first:
                        section = '建物'
                        continue
                    if 'その他' in first and 'その他 小計' not in first:
                        section = 'その他'
                        continue
                    if '小計' in first or '合 計' in first or '合計' in first or '取引日' in first:
                        continue
                    # データ行
                    if not re.match(r'^\d{4}-\d{2}-\d{2}', first):
                        continue
                    date = first
                    customer = (row[1] or '').strip() if len(row) > 1 else ''
                    service = (row[2] or '').strip() if len(row) > 2 else ''
                    ref_no = (row[3] or '').strip() if len(row) > 3 else ''
                    end_client = (row[4] or '').strip() if len(row) > 4 else ''
                    amount = parse_amount(row[5]) if len(row) > 5 else 0
                    staff = (row[6] or '').strip() if len(row) > 6 else ''
                    rows.append({
                        'year_month': ym,
                        'date': date,
                        'customer_raw': customer,
                        'service': service,
                        'category': section or '',
                        'rank': '',
                        'ref_no': ref_no,
                        'end_client': end_client,
                        'amount': amount,
                        'staff': staff,
                        'attribute': '',
                        'source_file': pdf_path.name,
                    })
    return rows


# ============================================================
# メイン処理
# ============================================================
def main():
    sources = [
        ('2025-07', INBOX/'2025年７月'/'7月売上内訳.pdf', parse_2025_07),
        ('2025-08', INBOX/'2025年8月'/'2025年8月_内訳.pdf', lambda p: parse_general_ledger(p, '2025-08', amount_pos_from_end=1)),
        ('2025-09', INBOX/'2025年９月'/'2025年9月_売上内訳.pdf', lambda p: parse_general_ledger(p, '2025-09', amount_pos_from_end=2)),
        ('2025-11', INBOX/'2025年11月'/'売上内訳11月.pdf', lambda p: parse_general_ledger(p, '2025-11', amount_pos_from_end=1)),
        ('2025-12', INBOX/'2025年12月'/'売上内訳12月.pdf', parse_2025_12),
        ('2026-01', INBOX/'2026年1月'/'1月内訳.pdf', parse_2026_01),
        ('2026-03', INBOX/'2026年３月'/'3月売上一覧_土地建物別.pdf', parse_2026_03),
    ]
    all_rows = []
    for ym, path, parser in sources:
        if not path.exists():
            print(f'[skip] {ym}: file not found {path}', file=sys.stderr)
            continue
        try:
            rows = parser(path)
            print(f'[ok] {ym}: {len(rows)} transactions, sum=¥{sum(r["amount"] for r in rows):,}')
            all_rows.extend(rows)
        except Exception as e:
            print(f'[err] {ym}: {e}', file=sys.stderr)

    # 顧客名正規化
    for r in all_rows:
        norm, _ = normalize_customer(r['customer_raw'])
        r['customer'] = norm
        cat_info = CATEGORY_MAP.get(norm, ('その他', '不明'))
        r['customer_segment'] = cat_info[0]
        r['customer_type'] = cat_info[1]

    # transactions.csv 出力
    DB.mkdir(exist_ok=True)
    tx_path = DB / 'transactions.csv'
    fieldnames = ['year_month','date','customer','customer_raw','customer_segment','customer_type',
                  'category','rank','service','ref_no','end_client','amount','staff','attribute','source_file']
    with open(tx_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in all_rows:
            w.writerow({k: r.get(k, '') for k in fieldnames})
    print(f'\n[OUT] {tx_path}: {len(all_rows)} rows')

    # customers.csv 集計
    by_cust = defaultdict(lambda: {
        'transactions': 0, 'total_revenue': 0, 'months': set(),
        'first_seen': '9999-99', 'last_seen': '0000-00',
        'land_revenue': 0, 'building_revenue': 0, 'other_revenue': 0,
        'segment': '', 'type': '',
    })
    for r in all_rows:
        c = r['customer']
        if not c:
            continue
        b = by_cust[c]
        b['transactions'] += 1
        b['total_revenue'] += r['amount']
        b['months'].add(r['year_month'])
        if r['year_month'] < b['first_seen']:
            b['first_seen'] = r['year_month']
        if r['year_month'] > b['last_seen']:
            b['last_seen'] = r['year_month']
        if r['category'] == '土地':
            b['land_revenue'] += r['amount']
        elif r['category'] == '建物':
            b['building_revenue'] += r['amount']
        else:
            b['other_revenue'] += r['amount']
        b['segment'] = r['customer_segment']
        b['type'] = r['customer_type']

    cust_path = DB / 'customers.csv'
    fields_c = ['customer','customer_segment','customer_type','first_seen','last_seen',
                'months_active','transactions','total_revenue','avg_amount',
                'land_revenue','building_revenue','other_revenue','status']
    with open(cust_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields_c)
        w.writeheader()
        # 売上降順
        sorted_custs = sorted(by_cust.items(), key=lambda x: -x[1]['total_revenue'])
        latest_ym = max(r['year_month'] for r in all_rows)
        for cust, b in sorted_custs:
            ma = len(b['months'])
            avg = b['total_revenue'] // b['transactions'] if b['transactions'] else 0
            # active = 直近2ヶ月以内に取引あり
            status = 'active' if b['last_seen'] >= '2026-02' else ('dormant' if b['last_seen'] < '2025-12' else 'recent')
            w.writerow({
                'customer': cust,
                'customer_segment': b['segment'],
                'customer_type': b['type'],
                'first_seen': b['first_seen'],
                'last_seen': b['last_seen'],
                'months_active': ma,
                'transactions': b['transactions'],
                'total_revenue': b['total_revenue'],
                'avg_amount': avg,
                'land_revenue': b['land_revenue'],
                'building_revenue': b['building_revenue'],
                'other_revenue': b['other_revenue'],
                'status': status,
            })
    print(f'[OUT] {cust_path}: {len(by_cust)} customers')

    # 月次サマリー
    monthly_path = DB / 'monthly_customer_summary.csv'
    by_month = defaultdict(lambda: {'unique_customers': set(), 'transactions': 0, 'revenue': 0,
                                     'new_customers': 0, 'repeat_customers': 0,
                                     'new_revenue': 0, 'repeat_revenue': 0})
    seen_customers = set()
    sorted_months = sorted(set(r['year_month'] for r in all_rows))
    for ym in sorted_months:
        month_customers_seen_this_month = set()
        for r in all_rows:
            if r['year_month'] != ym:
                continue
            c = r['customer']
            by_month[ym]['transactions'] += 1
            by_month[ym]['revenue'] += r['amount']
            month_customers_seen_this_month.add(c)
            # 「特殊」系（新規顧客/紹介/一般）はセグメント別に判定
            if c in ('新規顧客', '紹介経由', '一般（個人スポット）'):
                by_month[ym]['new_revenue'] += r['amount']
            elif c not in seen_customers:
                # 当月初出 (履歴的初出)
                by_month[ym]['new_revenue'] += r['amount']
            else:
                by_month[ym]['repeat_revenue'] += r['amount']
        new_this = sum(1 for c in month_customers_seen_this_month if c not in seen_customers and c not in ('新規顧客','紹介経由','一般（個人スポット）'))
        repeat_this = sum(1 for c in month_customers_seen_this_month if c in seen_customers)
        # 新規/紹介/一般 の特殊カテゴリは新規枠
        special_count = sum(1 for c in month_customers_seen_this_month if c in ('新規顧客','紹介経由','一般（個人スポット）'))
        by_month[ym]['new_customers'] = new_this + special_count
        by_month[ym]['repeat_customers'] = repeat_this
        by_month[ym]['unique_customers'] = len(month_customers_seen_this_month)
        seen_customers.update(month_customers_seen_this_month)

    with open(monthly_path, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['year_month','unique_customers','transactions','revenue',
                    'new_customers','repeat_customers','new_revenue','repeat_revenue',
                    'new_rate_pct','repeat_rate_pct'])
        for ym in sorted_months:
            d = by_month[ym]
            tot = d['new_customers'] + d['repeat_customers']
            new_pct = round(d['new_customers'] / tot * 100, 1) if tot else 0
            rep_pct = round(d['repeat_customers'] / tot * 100, 1) if tot else 0
            w.writerow([ym, d['unique_customers'], d['transactions'], d['revenue'],
                        d['new_customers'], d['repeat_customers'],
                        d['new_revenue'], d['repeat_revenue'],
                        new_pct, rep_pct])
    print(f'[OUT] {monthly_path}: {len(sorted_months)} months')

if __name__ == '__main__':
    main()
