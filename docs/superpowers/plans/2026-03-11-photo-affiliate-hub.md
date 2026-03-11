# Photo Affiliate Hub Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Build a 3-category (camera bags, tripods, SD cards) affiliate static site generator using Python + Jinja2 + Markdown, deployed via GitHub Actions to GitHub Pages.

**Architecture:** `generate.py` orchestrates modular `build_*.py` scripts that read JSON product data and Markdown content, render Jinja2 templates, and output static HTML to `site/`. Config is read from `config.yml` with environment variable overrides.

**Tech Stack:** Python 3.x, Jinja2, python-markdown, PyYAML, GitHub Actions, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-03-11-photo-affiliate-hub-design.md`

---

## Chunk 1: Project Foundation

### Task 1: Create directory structure

- [ ] Create all directories:

```bash
mkdir -p photo-affiliate-hub/{data,content/{camera-bags,tripods,sd-cards,learn,usecases,pages},templates/partials,assets/{css,js,images},scripts,site,.github/workflows}
```

### Task 2: Create config and requirements files

- [ ] Create `photo-affiliate-hub/requirements.txt`:

```
Jinja2>=3.1.0
Markdown>=3.5.0
PyYAML>=6.0
```

- [ ] Create `photo-affiliate-hub/.gitignore`:

```
site/
__pycache__/
*.pyc
.DS_Store
```

- [ ] Create `photo-affiliate-hub/config.yml`:

```yaml
site:
  title: "フォト機材おすすめガイド"
  url: "https://KurouzuSetsuna.github.io/product-recommendation-site"
  base_path: "/product-recommendation-site"
  description: "カメラバッグ・三脚・SDカードのおすすめを比較するガイドサイト"
  locale: "ja"
  author: "フォト機材おすすめガイド編集部"

build:
  output_dir: "site"
  validate_required_fields: true

analytics:
  ga_measurement_id: ""
```

### Task 3: Create data files

- [ ] Create `photo-affiliate-hub/data/categories.json`:

```json
[
  {
    "slug": "camera-bags",
    "name": "カメラバッグ",
    "description": "用途別・サイズ別に比較できるカメラバッグ特集",
    "item_data_file": "camera_bags.json"
  },
  {
    "slug": "tripods",
    "name": "三脚",
    "description": "軽量・動画向け・コスパ重視で比較する三脚特集",
    "item_data_file": "tripods.json"
  },
  {
    "slug": "sd-cards",
    "name": "SDカード",
    "description": "V60 / V90 を中心に動画向けSDカードを比較",
    "item_data_file": "sd_cards.json"
  }
]
```

- [ ] Create `photo-affiliate-hub/data/camera_bags.json`:

```json
[
  {
    "slug": "lowepro-flipside-trek-450",
    "name": "Lowepro Flipside Trek BP 450 AW",
    "brand": "Lowepro",
    "category": "camera-bags",
    "asin": "B01MYUPUUE",
    "price_range": "30000〜40000円",
    "capacity": "30L",
    "weight": 1800,
    "waterproof": true,
    "image": "/assets/images/items/lowepro-flipside-trek-450.webp",
    "tags": ["登山", "大容量", "一眼レフ", "防水"],
    "description": "登山・トレッキング向けの大容量バックパック。背面アクセスで安全性が高い。",
    "features": ["背面アクセス", "30L大容量", "防水仕様", "三脚取り付け可能"],
    "suitable_for": ["登山", "旅行", "本格撮影"]
  },
  {
    "slug": "peak-design-everyday-20l",
    "name": "Peak Design Everyday Backpack 20L",
    "brand": "Peak Design",
    "category": "camera-bags",
    "asin": "B07H9JFZ2V",
    "price_range": "45000〜55000円",
    "capacity": "20L",
    "weight": 1530,
    "waterproof": true,
    "image": "/assets/images/items/peak-design-everyday-20l.webp",
    "tags": ["街歩き", "スタイリッシュ", "普段使い", "防水"],
    "description": "都市型撮影に最適なスタイリッシュなバックパック。MagLatchシステムで素早いアクセス。",
    "features": ["MagLatchシステム", "カスタマイズ仕切り", "ラップトップ収納", "防水ジッパー"],
    "suitable_for": ["街歩き", "旅行", "普段使い"]
  },
  {
    "slug": "manfrotto-advanced-travel-bp",
    "name": "Manfrotto Advanced Travel Backpack",
    "brand": "Manfrotto",
    "category": "camera-bags",
    "asin": "B086VV1ZRL",
    "price_range": "25000〜35000円",
    "capacity": "26L",
    "weight": 1600,
    "waterproof": false,
    "image": "/assets/images/items/manfrotto-advanced-travel-bp.webp",
    "tags": ["旅行", "機内持ち込み", "一眼レフ", "バックパック"],
    "description": "旅行に特化した機能性バックパック。機内持ち込みサイズに収まる。",
    "features": ["機内持ち込みサイズ", "三脚ストラップ", "USB充電ポート", "サイドアクセス"],
    "suitable_for": ["旅行", "出張", "風景撮影"]
  },
  {
    "slug": "tenba-axis-v2-20l",
    "name": "Tenba Axis V2 20L",
    "brand": "Tenba",
    "category": "camera-bags",
    "asin": "B092XW3QY3",
    "price_range": "20000〜28000円",
    "capacity": "20L",
    "weight": 1300,
    "waterproof": true,
    "image": "/assets/images/items/tenba-axis-v2-20l.webp",
    "tags": ["コスパ", "街歩き", "ミラーレス", "防水"],
    "description": "コストパフォーマンスに優れたミラーレス向けバックパック。軽量で使いやすい。",
    "features": ["軽量1.3kg", "ラップトップ収納15インチ", "レインカバー付属", "撥水加工"],
    "suitable_for": ["街歩き", "スナップ", "日常使い"]
  },
  {
    "slug": "hakuba-luftdesign-slim-shoulder",
    "name": "HAKUBA ルフトデザイン スリムショルダー06",
    "brand": "HAKUBA",
    "category": "camera-bags",
    "asin": "B07B5NV2RD",
    "price_range": "8000〜12000円",
    "capacity": "6L",
    "weight": 390,
    "waterproof": false,
    "image": "/assets/images/items/hakuba-luftdesign-slim-shoulder.webp",
    "tags": ["コスパ", "ショルダー", "ミラーレス", "軽量"],
    "description": "手頃な価格で使いやすい国内ブランドのショルダーバッグ。ミラーレスにちょうど良いサイズ。",
    "features": ["軽量390g", "クッション仕切り", "前面ポケット", "雨蓋付き"],
    "suitable_for": ["スナップ", "日常使い", "初心者"]
  }
]
```

- [ ] Create `photo-affiliate-hub/data/tripods.json`:

```json
[
  {
    "slug": "manfrotto-mt190xpro4",
    "name": "Manfrotto MT190XPRO4",
    "brand": "Manfrotto",
    "category": "tripods",
    "asin": "B00I3Y4KIA",
    "price_range": "30000〜40000円",
    "max_height": 165,
    "min_height": 10,
    "weight": 2200,
    "max_load": 7000,
    "material": "アルミ",
    "image": "/assets/images/items/manfrotto-mt190xpro4.webp",
    "tags": ["定番", "スタジオ", "風景", "アルミ"],
    "description": "プロも使う定番アルミ三脚。90度横倒しポールで多彩なアングルに対応。",
    "features": ["90°横倒しポール", "4段", "センターポールロック", "スパイク脚先"],
    "suitable_for": ["スタジオ", "風景", "ポートレート"]
  },
  {
    "slug": "joby-gorillapod-5k",
    "name": "Joby GorillaPod 5K",
    "brand": "Joby",
    "category": "tripods",
    "asin": "B00FZGI7JO",
    "price_range": "15000〜20000円",
    "max_height": 38,
    "min_height": 8,
    "weight": 540,
    "max_load": 5000,
    "material": "樹脂",
    "image": "/assets/images/items/joby-gorillapod-5k.webp",
    "tags": ["柔軟", "ミラーレス", "旅行", "軽量"],
    "description": "どこにでも巻きつけられる柔軟な三脚。軽量で旅行に最適。",
    "features": ["自由に曲がる脚", "540g軽量", "自由雲台付き", "最大5kg対応"],
    "suitable_for": ["旅行", "Vlog", "スナップ"]
  },
  {
    "slug": "velbon-ultra-luxi-l",
    "name": "Velbon Ultra LUXi L",
    "brand": "Velbon",
    "category": "tripods",
    "asin": "B0057KWDVU",
    "price_range": "12000〜18000円",
    "max_height": 155,
    "min_height": 59,
    "weight": 1280,
    "max_load": 4000,
    "material": "アルミ",
    "image": "/assets/images/items/velbon-ultra-luxi-l.webp",
    "tags": ["コスパ", "軽量", "旅行", "アルミ"],
    "description": "軽量コンパクトで持ち運びやすい国内ブランドの三脚。コスパ抜群。",
    "features": ["1.28kg軽量", "4段", "ウルトラロック", "自由雲台付き"],
    "suitable_for": ["旅行", "日常", "初心者"]
  },
  {
    "slug": "leofoto-ls-284c",
    "name": "Leofoto LS-284C",
    "brand": "Leofoto",
    "category": "tripods",
    "asin": "B07FKXMKQP",
    "price_range": "40000〜55000円",
    "max_height": 145,
    "min_height": 13,
    "weight": 1100,
    "max_load": 8000,
    "material": "カーボン",
    "image": "/assets/images/items/leofoto-ls-284c.webp",
    "tags": ["カーボン", "軽量", "登山", "プロ"],
    "description": "高品質カーボンファイバー製の軽量三脚。登山・トレッキングに最適。",
    "features": ["カーボン1.1kg", "最大8kg耐荷重", "反転格納", "スパイク脚先"],
    "suitable_for": ["登山", "風景", "プロ"]
  },
  {
    "slug": "gitzo-gt1545t",
    "name": "Gitzo GT1545T Series 1 Traveler",
    "brand": "Gitzo",
    "category": "tripods",
    "asin": "B00G4BMMZE",
    "price_range": "70000〜90000円",
    "max_height": 148,
    "min_height": 15,
    "weight": 1100,
    "max_load": 10000,
    "material": "カーボン",
    "image": "/assets/images/items/gitzo-gt1545t.webp",
    "tags": ["プロ", "カーボン", "旅行", "最高峰"],
    "description": "プロフェッショナル向けカーボントラベラー三脚の最高峰。脚を逆向きに格納できコンパクト収納。",
    "features": ["逆折り畳み", "最大10kg耐荷重", "カーボン製", "防塵防水"],
    "suitable_for": ["プロ", "旅行", "風景"]
  }
]
```

- [ ] Create `photo-affiliate-hub/data/sd_cards.json`:

```json
[
  {
    "slug": "sony-tough-sf-g64t",
    "name": "Sony TOUGH SF-G64T (V90 64GB)",
    "brand": "Sony",
    "category": "sd-cards",
    "asin": "B076GKS8LK",
    "price_range": "15000〜20000円",
    "capacity": "64GB",
    "speed_class": "V90",
    "read_speed": 300,
    "write_speed": 299,
    "waterproof": true,
    "image": "/assets/images/items/sony-tough-sf-g64t.webp",
    "tags": ["V90", "8K", "動画向け", "高耐久"],
    "description": "ソニーの最高峰V90対応SDカード。防水・防塵・耐衝撃のTOUGH仕様。",
    "features": ["V90最速クラス", "防水・防塵・耐衝撃", "18kN曲げ強度", "X線防護"],
    "suitable_for": ["8K動画", "プロ", "シネマ"]
  },
  {
    "slug": "prograde-v90-64gb",
    "name": "ProGrade Digital V90 SDXC 64GB",
    "brand": "ProGrade Digital",
    "category": "sd-cards",
    "asin": "B083TXNMTG",
    "price_range": "12000〜16000円",
    "capacity": "64GB",
    "speed_class": "V90",
    "read_speed": 250,
    "write_speed": 200,
    "waterproof": false,
    "image": "/assets/images/items/prograde-v90-64gb.webp",
    "tags": ["V90", "プロ向け", "動画", "高速"],
    "description": "プロ向けブランドのV90対応カード。安定した高速書き込みが特長。",
    "features": ["250MB/s読み込み", "200MB/s書き込み", "プロ品質管理", "5年保証"],
    "suitable_for": ["4K/6K動画", "プロ", "シネマ"]
  },
  {
    "slug": "lexar-2000x-v90-64gb",
    "name": "Lexar Professional 2000x V90 64GB",
    "brand": "Lexar",
    "category": "sd-cards",
    "asin": "B078WZPQS7",
    "price_range": "10000〜14000円",
    "capacity": "64GB",
    "speed_class": "V90",
    "read_speed": 300,
    "write_speed": 260,
    "waterproof": false,
    "image": "/assets/images/items/lexar-2000x-v90-64gb.webp",
    "tags": ["V90", "高速", "動画", "コスパ"],
    "description": "2000倍速を誇るV90対応カード。高速・大容量で動画撮影の定番。",
    "features": ["300MB/s読み込み", "260MB/s書き込み", "2000x速度", "USB 3.0リーダー付属"],
    "suitable_for": ["4K/8K動画", "バースト撮影", "シネマ"]
  },
  {
    "slug": "sandisk-extreme-pro-v90-64gb",
    "name": "SanDisk Extreme PRO V90 64GB",
    "brand": "SanDisk",
    "category": "sd-cards",
    "asin": "B09X7FXHVJ",
    "price_range": "8000〜12000円",
    "capacity": "64GB",
    "speed_class": "V90",
    "read_speed": 300,
    "write_speed": 260,
    "waterproof": true,
    "image": "/assets/images/items/sandisk-extreme-pro-v90-64gb.webp",
    "tags": ["V90", "信頼性", "動画", "防水"],
    "description": "世界的に信頼されるSanDiskのV90フラッグシップ。防水・耐高温で過酷な環境でも安心。",
    "features": ["防水・耐X線・耐衝撃", "30年保証", "Rescue Pro DX付属", "防温-25〜85℃"],
    "suitable_for": ["4K/8K動画", "アウトドア", "プロ"]
  },
  {
    "slug": "angelbird-av-pro-sd-v90-64gb",
    "name": "Angelbird AV PRO SD V90 64GB",
    "brand": "Angelbird",
    "category": "sd-cards",
    "asin": "B07MJ44S6Q",
    "price_range": "14000〜18000円",
    "capacity": "64GB",
    "speed_class": "V90",
    "read_speed": 280,
    "write_speed": 260,
    "waterproof": false,
    "image": "/assets/images/items/angelbird-av-pro-sd-v90-64gb.webp",
    "tags": ["V90", "映像制作", "高信頼", "オーストリア製"],
    "description": "映像制作プロが選ぶオーストリア製V90カード。温度範囲と耐久性に優れる。",
    "features": ["動作温度-25〜85℃", "オーストリア製", "長期耐久設計", "全バッファ書き込み"],
    "suitable_for": ["シネマ", "映像制作", "プロ"]
  }
]
```

- [ ] Create `photo-affiliate-hub/data/rankings.json`:

```json
{
  "camera-bags": ["peak-design-everyday-20l", "lowepro-flipside-trek-450", "tenba-axis-v2-20l"],
  "tripods": ["leofoto-ls-284c", "manfrotto-mt190xpro4", "velbon-ultra-luxi-l"],
  "sd-cards": ["sony-tough-sf-g64t", "sandisk-extreme-pro-v90-64gb", "lexar-2000x-v90-64gb"]
}
```

- [ ] Create `photo-affiliate-hub/data/site_meta.json`:

```json
{}
```

---

## Chunk 2: Content Files

### Task 4: Camera bags content

- [ ] Create `photo-affiliate-hub/content/camera-bags/best-camera-bags-for-travel.md`:

```markdown
---
title: 旅行向けカメラバッグおすすめ7選【2026年最新】
slug: best-camera-bags-for-travel
category: camera-bags
description: 旅行に持っていけるカメラバッグを徹底比較。機内持ち込み対応・軽量・収納力で選ぶおすすめを紹介。
template: article
related_items:
  - lowepro-flipside-trek-450
  - manfrotto-advanced-travel-bp
  - peak-design-everyday-20l
tags:
  - カメラバッグ
  - 旅行
  - 機内持ち込み
publish: true
updated_at: 2026-03-11
---

## 旅行用カメラバッグの選び方

旅行にカメラを持っていくなら、バッグ選びが重要です。ここでは**機内持ち込みサイズ**・**防水性**・**アクセスしやすさ**の3点を中心に比較します。

### 機内持ち込みサイズを確認する

国際線の機内持ち込みは通常 **55×40×25cm** 以内が目安です。三辺合計が115cm以内のバッグを選びましょう。

### 防水性能をチェックする

急な雨でも機材を守れる防水仕様（撥水加工または防水ジッパー）のバッグを選ぶことをおすすめします。

### カメラへのアクセス方法

「背面アクセス型」は安全性が高く、「サイドアクセス型」は素早く取り出せます。撮影スタイルに合わせて選びましょう。

## おすすめランキング

旅行向けカメラバッグのおすすめを厳選して紹介します。

## まとめ

旅行用カメラバッグは「サイズ・防水・アクセス性」の3点で選ぶのが基本です。本格的な旅行には Lowepro や Manfrotto、スタイリッシュさを求めるなら Peak Design がおすすめです。
```

- [ ] Create `photo-affiliate-hub/content/camera-bags/best-camera-bags-for-beginners.md`:

```markdown
---
title: 初心者におすすめのカメラバッグ5選【ミラーレス対応】
slug: best-camera-bags-for-beginners
category: camera-bags
description: カメラを買ったばかりの初心者向けカメラバッグを厳選。使いやすさ・価格・デザインで比較。
template: article
related_items:
  - hakuba-luftdesign-slim-shoulder
  - tenba-axis-v2-20l
  - peak-design-everyday-20l
tags:
  - カメラバッグ
  - 初心者
  - ミラーレス
publish: true
updated_at: 2026-03-11
---

## 初心者がカメラバッグを選ぶポイント

初めてカメラバッグを選ぶ場合、**価格・使いやすさ・見た目**の3点を重視しましょう。

### 価格帯の目安

- ショルダーバッグ：5,000〜15,000円
- バックパック（エントリー）：10,000〜25,000円
- バックパック（プレミアム）：30,000円〜

### ミラーレスカメラに合ったサイズ

フルサイズミラーレス＋標準ズーム程度なら、20L前後のバックパックまたは小型ショルダーで十分です。

## おすすめランキング

初心者に特におすすめのカメラバッグを紹介します。

## まとめ

初心者には手頃な価格でシンプルに使えるバッグがおすすめです。まずは HAKUBA のショルダーバッグや Tenba のバックパックから始めてみましょう。
```

- [ ] Create `photo-affiliate-hub/content/camera-bags/lightweight-camera-bags.md`:

```markdown
---
title: 軽量カメラバッグおすすめ5選【1kg以下】
slug: lightweight-camera-bags
category: camera-bags
description: 軽くて持ち運びやすいカメラバッグを厳選。重さ1kg前後の軽量モデルを比較・紹介します。
template: article
related_items:
  - hakuba-luftdesign-slim-shoulder
  - tenba-axis-v2-20l
  - peak-design-everyday-20l
tags:
  - カメラバッグ
  - 軽量
  - コンパクト
publish: true
updated_at: 2026-03-11
---

## 軽量カメラバッグのメリット

長時間の撮影や歩き回る街撮りでは、バッグの重さが疲労に直結します。軽量バッグは体への負担を減らし、より楽しく撮影できます。

### 重さの目安

| タイプ | 軽量の目安 |
|--------|-----------|
| ショルダー | 500g以下 |
| バックパック | 1.3kg以下 |

## おすすめランキング

軽量カメラバッグのおすすめを紹介します。

## まとめ

軽量重視なら HAKUBA のショルダーバッグ、バックパックなら Tenba Axis V2 が1.3kgで軽量かつ機能的です。
```

### Task 5: Tripods content

- [ ] Create `photo-affiliate-hub/content/tripods/best-lightweight-tripods.md`:

```markdown
---
title: 軽量三脚おすすめ7選【カーボン・旅行向け】
slug: best-lightweight-tripods
category: tripods
description: 軽くて持ち運びやすい三脚を厳選。カーボン製から手頃なアルミ製まで比較します。
template: article
related_items:
  - leofoto-ls-284c
  - gitzo-gt1545t
  - velbon-ultra-luxi-l
tags:
  - 三脚
  - 軽量
  - カーボン
  - 旅行
publish: true
updated_at: 2026-03-11
---

## 軽量三脚の選び方

旅行・登山用の三脚は**重量・収納サイズ・耐荷重**で選びましょう。

### 素材別の特徴

| 素材 | 重量 | 価格 | 特徴 |
|------|------|------|------|
| カーボン | 軽い | 高め | 振動吸収・軽量 |
| アルミ | 普通 | 手頃 | 耐久性・コスパ |

### 重さの目安

- 旅行・登山：1.5kg以下
- 日常使い：2kg以下

## おすすめランキング

軽量三脚のおすすめを紹介します。

## まとめ

最高峰を求めるなら Gitzo か Leofoto のカーボン製、コスパ重視なら Velbon が安心です。
```

- [ ] Create `photo-affiliate-hub/content/tripods/best-tripods-for-video.md`:

```markdown
---
title: 動画撮影向け三脚おすすめ5選【YouTube・Vlog対応】
slug: best-tripods-for-video
category: tripods
description: 動画撮影に最適な三脚を厳選。パン・チルトがなめらかなビデオ三脚を比較。
template: article
related_items:
  - manfrotto-mt190xpro4
  - joby-gorillapod-5k
  - leofoto-ls-284c
tags:
  - 三脚
  - 動画
  - YouTube
  - ビデオ三脚
publish: true
updated_at: 2026-03-11
---

## 動画向け三脚の選び方

動画撮影では**水平維持・なめらかなパン・耐荷重**が重要です。

### ビデオ雲台 vs 自由雲台

動画撮影には**ビデオ雲台**（パン・チルトを別々に操作）が最適です。自由雲台は静止画向きですが、Vlog用途なら自由雲台でも十分です。

## おすすめランキング

動画撮影向けの三脚を紹介します。

## まとめ

本格的な動画制作には Manfrotto の4段三脚、手軽なVlogには Joby GorillaPod がおすすめです。
```

- [ ] Create `photo-affiliate-hub/content/tripods/best-budget-tripods.md`:

```markdown
---
title: コスパ最強の三脚おすすめ5選【1万円以下】
slug: best-budget-tripods
category: tripods
description: 1万円前後で買えるコスパの良い三脚を厳選。初心者にも使いやすいモデルを比較。
template: article
related_items:
  - velbon-ultra-luxi-l
  - joby-gorillapod-5k
  - manfrotto-mt190xpro4
tags:
  - 三脚
  - コスパ
  - 初心者
  - 安い
publish: true
updated_at: 2026-03-11
---

## 予算1万円の三脚で何が買える？

1万円前後でも、日常撮影で十分使える三脚が手に入ります。ただし、重量や耐荷重には妥協が必要な場合があります。

### チェックポイント

- 最大耐荷重：使用するカメラ＋レンズの重量の2倍以上
- 最大高さ：目線の高さ（150cm前後）に届くか
- 収納サイズ：持ち運びやすいか

## おすすめランキング

コスパ重視の三脚を紹介します。

## まとめ

コスパ重視なら Velbon Ultra LUXi L が国産ブランドで信頼性も高くおすすめです。
```

### Task 6: SD cards content

- [ ] Create `photo-affiliate-hub/content/sd-cards/best-v90-sd-cards.md`:

```markdown
---
title: V90対応SDカードおすすめ7選【4K/8K動画向け】
slug: best-v90-sd-cards
category: sd-cards
description: 4K/6K/8K動画撮影に必須のV90対応SDカードを徹底比較。速度・耐久性・価格で選ぶおすすめ。
template: article
related_items:
  - sony-tough-sf-g64t
  - prograde-v90-64gb
  - sandisk-extreme-pro-v90-64gb
  - lexar-2000x-v90-64gb
  - angelbird-av-pro-sd-v90-64gb
tags:
  - SDカード
  - V90
  - 動画
  - 4K
  - 8K
publish: true
updated_at: 2026-03-11
---

## V90とは？

V90はSDカードのビデオスピードクラスの最高規格で、**最低90MB/sの持続書き込み速度**が保証されます。4K・6K・8K動画の撮影に必須のスペックです。

### ビデオスピードクラスの比較

| クラス | 最低書き込み速度 | 用途 |
|--------|----------------|------|
| V30 | 30MB/s | 4K（低ビットレート） |
| V60 | 60MB/s | 4K（高ビットレート）、6K |
| V90 | 90MB/s | 4K/6K/8K、RAW動画 |

## おすすめランキング

V90対応SDカードのおすすめを紹介します。

## まとめ

最高の信頼性を求めるなら Sony TOUGH、コスパを求めるなら SanDisk Extreme PRO がおすすめです。
```

- [ ] Create `photo-affiliate-hub/content/sd-cards/best-v60-sd-cards.md`:

```markdown
---
title: V60対応SDカードおすすめ5選【4K動画向けコスパ最強】
slug: best-v60-sd-cards
category: sd-cards
description: V60対応SDカードをコスパ・速度・信頼性で比較。4K動画撮影に最適なカードを厳選紹介。
template: article
related_items:
  - sony-tough-sf-g64t
  - lexar-2000x-v90-64gb
  - sandisk-extreme-pro-v90-64gb
tags:
  - SDカード
  - V60
  - 動画
  - 4K
  - コスパ
publish: true
updated_at: 2026-03-11
---

## V60はどんな人に向くか

V60は**4K動画（高ビットレート）や連写撮影**に適したスペックです。V90より手頃な価格で、多くの撮影シーンをカバーします。

### V60が向く用途

- 4K/60p動画（200Mbps以下）
- RAW写真の連写
- 4K/30p動画（高ビットレート）

## おすすめランキング

V60対応SDカードのおすすめを紹介します。

## まとめ

普段の4K動画撮影ならV60で十分なケースが多いです。コスパ重視の方にはV60がおすすめです。
```

- [ ] Create `photo-affiliate-hub/content/sd-cards/best-sd-cards-for-4k-video.md`:

```markdown
---
title: 4K動画撮影におすすめのSDカード7選【2026年最新】
slug: best-sd-cards-for-4k-video
category: sd-cards
description: 4K動画撮影に使えるSDカードをV60・V90別に比較。コマ落ちしない書き込み速度の選び方も解説。
template: article
related_items:
  - sony-tough-sf-g64t
  - sandisk-extreme-pro-v90-64gb
  - prograde-v90-64gb
  - lexar-2000x-v90-64gb
tags:
  - SDカード
  - 4K動画
  - V60
  - V90
publish: true
updated_at: 2026-03-11
---

## 4K動画に必要な書き込み速度

4K動画のビットレートはカメラによって異なります。使用するカメラのスペックに合ったSDカードを選びましょう。

### ビットレート別の必要速度

| ビットレート | 必要な最低速度 | 推奨スピードクラス |
|------------|-------------|-----------------|
| 〜100Mbps | 13MB/s | V30 |
| 〜400Mbps | 50MB/s | V60 |
| 400Mbps〜 | 90MB/s | V90 |

## おすすめランキング

4K動画向けSDカードのおすすめを紹介します。

## まとめ

4K動画撮影のSDカードはカメラのビットレート仕様を確認してから選びましょう。高ビットレート機にはV90をおすすめします。
```

### Task 7: Learn, usecases, pages content

- [ ] Create `photo-affiliate-hub/content/learn/how-to-choose-camera-bag.md`:

```markdown
---
title: カメラバッグの選び方【種類・サイズ・素材を解説】
slug: how-to-choose-camera-bag
category: camera-bags
description: カメラバッグの選び方を初心者にもわかりやすく解説。バックパック・ショルダー・メッセンジャーの違いも紹介。
template: learn
tags:
  - カメラバッグ
  - 選び方
  - 初心者
publish: true
updated_at: 2026-03-11
---

## カメラバッグの種類

カメラバッグには大きく3種類あります。

### バックパック型

両肩で支えるため長時間の携行に向いています。大容量で機材をたくさん持ち歩けます。

### ショルダーバッグ型

横から素早くカメラを取り出せます。機動性重視のスナップ撮影に最適です。

### メッセンジャーバッグ型

スタイリッシュで街歩きに馴染みます。ただし片肩に重量がかかるため注意。

## サイズの選び方

| 機材量 | 推奨サイズ |
|--------|----------|
| ボディ＋単焦点1本 | 5〜10L |
| ボディ＋ズーム2本 | 15〜20L |
| ボディ複数＋レンズ多数 | 25L〜 |

## 素材・耐久性のチェックポイント

- 撥水加工：軽い雨なら問題なし
- 防水ジッパー：本格的な雨でも安心
- レインカバー付属：旅行・登山に便利

## まとめ

まずは自分の撮影スタイル（街撮り・旅行・登山など）と機材量を確認して、それに合ったバッグを選びましょう。
```

- [ ] Create `photo-affiliate-hub/content/learn/how-to-choose-tripod.md`:

```markdown
---
title: 三脚の選び方【用途別・素材別に徹底解説】
slug: how-to-choose-tripod
category: tripods
description: 三脚の選び方を初心者向けに解説。カーボンvsアルミ、耐荷重、雲台の選び方まで網羅。
template: learn
tags:
  - 三脚
  - 選び方
  - 初心者
publish: true
updated_at: 2026-03-11
---

## 三脚を選ぶ前に確認すること

三脚を選ぶ際は、**何を撮るか**と**どこで使うか**を先に決めましょう。

## 素材の選び方

### カーボン製

軽量で振動吸収に優れます。価格は高めですが、本格的な撮影には最適です。

### アルミ製

コストパフォーマンスが高く、初心者にも扱いやすいです。重めですが丈夫。

## 耐荷重の目安

三脚の耐荷重は**使用機材の重量の2倍以上**を選ぶのが安全です。

## 雲台の種類

| 雲台タイプ | 向く用途 |
|----------|---------|
| 自由雲台 | 静止画全般、スナップ |
| 3way雲台 | 風景、建築 |
| ビデオ雲台 | 動画、ライブ配信 |
| パノラマ雲台 | 360度パノラマ |

## まとめ

旅行・登山にはカーボン製の軽量三脚、スタジオや風景にはアルミ製の安定した三脚がおすすめです。
```

- [ ] Create `photo-affiliate-hub/content/learn/what-is-v60-v90.md`:

```markdown
---
title: V60・V90とは？SDカードのスピードクラスを完全解説
slug: what-is-v60-v90
description: SDカードのビデオスピードクラスV60・V90の違いを初心者にもわかりやすく解説。どちらを買えばいいかも紹介。
template: learn
tags:
  - SDカード
  - V60
  - V90
  - 動画
publish: true
updated_at: 2026-03-11
---

## ビデオスピードクラスとは

ビデオスピードクラス（Video Speed Class）は、SDカードの最低持続書き込み速度を保証する規格です。動画撮影時のコマ落ちを防ぐために重要な指標です。

## V60とV90の違い

| 規格 | 最低書き込み速度 | 向く用途 |
|------|----------------|---------|
| V30 | 30MB/s | 4K（低ビットレート） |
| V60 | 60MB/s | 4K（高ビットレート）・6K |
| V90 | 90MB/s | 4K/6K/8K・RAW動画 |

## どちらを選ぶべきか

### V60で十分なケース

- 4K/30p（200Mbps以下）
- 写真の連写撮影
- 動画をあまり撮らない方

### V90が必要なケース

- 4K/60p以上の高ビットレート動画
- 6K・8K動画撮影
- RAW動画記録

## まとめ

カメラのスペック表で「動画ビットレート」を確認し、400Mbpsを超えるならV90、それ以下ならV60で問題ないことが多いです。
```

- [ ] Create `photo-affiliate-hub/content/usecases/travel-camera-bag.md`:

```markdown
---
title: 旅行用カメラバッグの選び方と持ち物リスト
slug: travel-camera-bag
description: 旅行にカメラを持っていく際のバッグ選びと、おすすめの持ち物リストを紹介します。
template: usecase
tags:
  - カメラバッグ
  - 旅行
  - 持ち物
publish: true
updated_at: 2026-03-11
---

## 旅行撮影のシナリオ

海外旅行や国内旅行でカメラを持ち歩く場合、「荷物をコンパクトに」「機材を安全に」「素早く撮れる」の3点が重要です。

## 旅行用カメラバッグの条件

1. **機内持ち込みサイズ**：預け荷物リスクを避ける
2. **防水・撥水**：突然の雨に対応
3. **背面アクセス**：スリ対策
4. **ラップトップ収納**：旅行中の編集作業に対応

## 旅行の持ち物リスト

- ボディ（1台）
- レンズ（広角ズーム + 単焦点）
- 予備バッテリー × 2
- SDカード × 3枚以上
- 充電ケーブル・アダプター
- 小型三脚またはゴリラポッド

## おすすめバッグ

旅行には機内持ち込みサイズの Manfrotto Advanced Travel Backpack や Peak Design Everyday Backpack 20L がおすすめです。
```

- [ ] Create `photo-affiliate-hub/content/usecases/video-tripod-for-youtube.md`:

```markdown
---
title: YouTube動画撮影に使える三脚の選び方
slug: video-tripod-for-youtube
description: YouTubeやSNS向けの動画撮影に最適な三脚を紹介。一人での撮影やVlogにも使えるモデルを比較。
template: usecase
tags:
  - 三脚
  - YouTube
  - Vlog
  - 動画
publish: true
updated_at: 2026-03-11
---

## YouTube撮影に三脚が必要な理由

手持ち撮影では映像がブレやすく、視聴者が疲れます。三脚を使えば安定した映像が撮れ、チャンネルのクオリティが上がります。

## YouTube向け三脚の選び方

### 一人撮影の場合

自撮りやVlogには**自由雲台付きの軽量三脚**が使いやすいです。カメラの向きを素早く変えられます。

### 据え置き撮影の場合

トーク動画や商品紹介には**ビデオ雲台付きの安定した三脚**がおすすめです。

## おすすめの組み合わせ

- Vlog・外ロケ：Joby GorillaPod 5K（どこにでも固定できる）
- 室内トーク：Manfrotto MT190XPRO4（安定感抜群）
- 持ち運び重視：Velbon Ultra LUXi L（コスパ◎）
```

- [ ] Create `photo-affiliate-hub/content/usecases/sd-card-for-4k60p.md`:

```markdown
---
title: 4K60p動画撮影に必要なSDカードの選び方
slug: sd-card-for-4k60p
description: 4K60p動画撮影でコマ落ちしないSDカードの選び方と、おすすめのV90カードを紹介します。
template: usecase
tags:
  - SDカード
  - 4K60p
  - 動画
  - V90
publish: true
updated_at: 2026-03-11
---

## 4K60pに必要なSDカードのスペック

4K/60p動画は高ビットレート（多くの場合200〜400Mbps）を記録するため、**V90以上のSDカード**が必要です。

## カメラ別の推奨スペック

| カメラ | ビットレート | 必要クラス |
|--------|------------|----------|
| Sony α7 IV | 4K/60p 200Mbps | V60以上 |
| Sony α7S III | 4K/120p 600Mbps | V90必須 |
| Canon EOS R5 | 4K/60p RAW | V90必須 |
| Nikon Z8 | 4K/60p RAW | V90必須 |

## 4K60p向けおすすめSDカード

V90の中でも書き込み速度が安定しているものを選ぶことが重要です。

**おすすめ1位：Sony TOUGH SF-G (V90)**
書き込み299MB/sで余裕を持って録画できます。

**おすすめ2位：SanDisk Extreme PRO V90**
信頼性と価格のバランスが良く、多くのカメラマンに支持されています。

## まとめ

4K60p以上の撮影にはV90のSDカードを選び、カメラのスペックに余裕を持ったものを選びましょう。
```

- [ ] Create `photo-affiliate-hub/content/pages/about.md`:

```markdown
---
title: このサイトについて
slug: about
template: page
publish: true
updated_at: 2026-03-11
---

## フォト機材おすすめガイドについて

当サイトは、カメラバッグ・三脚・SDカードなどの写真・動画撮影機材を比較・紹介するアフィリエイトメディアです。

実際の使用感や公式スペックをもとに、撮影シーン別・用途別のおすすめ情報を発信しています。

## 掲載情報について

掲載している商品情報・価格は執筆時点のものです。最新の情報は各販売店のページをご確認ください。

## お問い合わせ

ご意見・ご要望はGitHubのIssueよりお寄せください。
```

- [ ] Create `photo-affiliate-hub/content/pages/disclosure.md`:

```markdown
---
title: 広告掲載・アフィリエイト開示
slug: disclosure
template: page
publish: true
updated_at: 2026-03-11
---

## アフィリエイトプログラムについて

当サイトはAmazonアソシエイトプログラムをはじめとするアフィリエイトプログラムに参加しています。

商品リンクをクリックして購入された場合、当サイトに紹介料が支払われることがあります。

## 掲載内容の中立性

アフィリエイト報酬の有無にかかわらず、掲載内容は客観的な情報に基づき作成しています。

## Amazonアソシエイト

当サイトはAmazon.co.jpを宣伝しリンクすることによってサイトが紹介料を獲得できる手段を提供することを目的に設定されたアフィリエイトプログラムである、Amazonアソシエイト・プログラムの参加者です。
```

- [ ] Create `photo-affiliate-hub/content/pages/privacy.md`:

```markdown
---
title: プライバシーポリシー
slug: privacy
template: page
publish: true
updated_at: 2026-03-11
---

## アクセス解析について

当サイトでは、Googleアナリティクスを使用してアクセス情報を収集することがあります。収集されるデータは匿名であり、個人を特定するものではありません。

## Cookieについて

アクセス解析のためにCookieを使用することがあります。ブラウザの設定でCookieを無効にすることができます。

## 免責事項

当サイトの情報は正確を期していますが、内容の正確性・完全性を保証するものではありません。掲載情報の利用により生じた損害について、当サイトは責任を負いかねます。
```

---

## Chunk 3: Python Scripts

### Task 8: Create utils.py

- [ ] Create `photo-affiliate-hub/scripts/utils.py`:

```python
#!/usr/bin/env python3
"""共通ユーティリティ"""

import json
import os
import re
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import markdown as md_module

PROJECT_ROOT = Path(__file__).parent.parent


def load_config():
    """config.yml を読み込み、環境変数で上書きする"""
    with open(PROJECT_ROOT / 'config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 環境変数で上書き
    ga_id = os.environ.get('GA_MEASUREMENT_ID', '')
    if ga_id:
        config['analytics']['ga_measurement_id'] = ga_id

    return config


def load_categories():
    """categories.json を読み込む"""
    with open(PROJECT_ROOT / 'data' / 'categories.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def load_items_for_category(category):
    """カテゴリの商品データを読み込む"""
    filename = category['item_data_file']
    filepath = PROJECT_ROOT / 'data' / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        items = json.load(f)

    required_fields = ['slug', 'name', 'category', 'asin']
    for item in items:
        missing = [f for f in required_fields if not item.get(f)]
        if missing:
            raise ValueError(f"商品データ '{item.get('slug', '?')}' に必須フィールドが欠損: {missing}")

    return items


def load_all_items(categories):
    """全カテゴリの商品データを読み込む"""
    all_items = []
    items_by_slug = {}
    for cat in categories:
        items = load_items_for_category(cat)
        all_items.extend(items)
        for item in items:
            items_by_slug[item['slug']] = item
    return all_items, items_by_slug


def load_rankings():
    """rankings.json を読み込む"""
    filepath = PROJECT_ROOT / 'data' / 'rankings.json'
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def parse_markdown_file(filepath):
    """Markdownファイルをパースしてfront matterと本文HTMLを返す"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # front matter を抽出
    fm = {}
    body = content
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            fm = {}
        body = content[fm_match.end():]

    # Markdown → HTML
    parser = md_module.Markdown(extensions=['tables', 'fenced_code'])
    html = parser.convert(body)

    return fm, html


def make_affiliate_url(asin, associate_id=None):
    """AmazonアフィリエイトURLを生成する"""
    if not asin:
        return '#'
    base = f"https://www.amazon.co.jp/dp/{asin}/"
    if associate_id:
        return f"{base}?tag={associate_id}"
    return base


def setup_jinja(config):
    """Jinja2環境を構築する"""
    templates_dir = PROJECT_ROOT / 'templates'
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    env.globals['config'] = config
    env.globals['site'] = config['site']
    env.globals['base_path'] = config['site']['base_path']
    return env


def ensure_dir(path):
    """ディレクトリを作成する"""
    Path(path).mkdir(parents=True, exist_ok=True)


def write_html(path, html):
    """HTMLファイルを書き出す"""
    ensure_dir(Path(path).parent)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[OK] {path}')


def copy_assets(site_dir):
    """assetsをsiteディレクトリにコピーする"""
    import shutil
    src = PROJECT_ROOT / 'assets'
    dst = site_dir / 'assets'
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print('[OK] assets コピー完了')
```

### Task 9: Create build_taxonomies.py

- [ ] Create `photo-affiliate-hub/scripts/build_taxonomies.py`:

```python
#!/usr/bin/env python3
"""関連記事・パンくずデータ生成（HTML出力なし）"""


def build_related_articles(articles, max_count=3):
    """
    各記事に対して、同カテゴリ・共通タグで関連記事リストを付与する。
    articles: list of dict (front_matter + extra keys: slug, url, content_html)
    """
    for article in articles:
        cat = article.get('category', '')
        tags = set(article.get('tags') or [])
        related = []
        for other in articles:
            if other['slug'] == article['slug']:
                continue
            score = 0
            if other.get('category') == cat:
                score += 2
            common_tags = tags & set(other.get('tags') or [])
            score += len(common_tags)
            if score > 0:
                related.append((score, other))
        related.sort(key=lambda x: -x[0])
        article['related_articles'] = [r for _, r in related[:max_count]]
    return articles


def build_breadcrumbs(page_type, base_path, category=None, title=None):
    """
    パンくずリストデータを生成する。
    Returns list of {'name': str, 'url': str}
    """
    crumbs = [{'name': 'ホーム', 'url': f'{base_path}/'}]

    if page_type == 'category':
        crumbs.append({'name': category['name'], 'url': None})

    elif page_type == 'article':
        crumbs.append({'name': category['name'], 'url': f"{base_path}/{category['slug']}/"})
        crumbs.append({'name': title, 'url': None})

    elif page_type == 'item':
        crumbs.append({'name': category['name'], 'url': f"{base_path}/{category['slug']}/"})
        crumbs.append({'name': title, 'url': None})

    elif page_type in ('learn', 'usecase'):
        section_name = '使い方・選び方' if page_type == 'learn' else '用途別ガイド'
        section_url = f"{base_path}/learn/" if page_type == 'learn' else f"{base_path}/usecases/"
        crumbs.append({'name': section_name, 'url': section_url})
        crumbs.append({'name': title, 'url': None})

    elif page_type == 'page':
        crumbs.append({'name': title, 'url': None})

    return crumbs
```

### Task 10: Create build_top.py and build_category_indexes.py

- [ ] Create `photo-affiliate-hub/scripts/build_top.py`:

```python
#!/usr/bin/env python3
"""トップページ生成"""

from pathlib import Path
from scripts.utils import write_html


def build_top(site_dir, jinja_env, categories, items_by_slug, rankings, recent_articles):
    """トップページ (index.html) を生成する"""
    template = jinja_env.get_template('top.html')

    # カテゴリ別おすすめ商品
    featured = {}
    for cat in categories:
        slugs = rankings.get(cat['slug'], [])
        featured[cat['slug']] = [items_by_slug[s] for s in slugs if s in items_by_slug]

    html = template.render(
        page_title=None,
        categories=categories,
        featured_items=featured,
        recent_articles=recent_articles[:6],
        current_page='home',
    )
    write_html(site_dir / 'index.html', html)
    print('[OK] トップページ生成完了')
```

- [ ] Create `photo-affiliate-hub/scripts/build_category_indexes.py`:

```python
#!/usr/bin/env python3
"""カテゴリトップページ生成"""

from pathlib import Path
from scripts.utils import write_html
from scripts.build_taxonomies import build_breadcrumbs


def build_category_indexes(site_dir, jinja_env, categories, items_by_category, articles_by_category, base_path):
    """各カテゴリのインデックスページを生成する"""
    template = jinja_env.get_template('category_index.html')

    for cat in categories:
        slug = cat['slug']
        items = items_by_category.get(slug, [])
        articles = articles_by_category.get(slug, [])
        breadcrumbs = build_breadcrumbs('category', base_path, category=cat)

        html = template.render(
            page_title=f"{cat['name']} おすすめ・比較ガイド",
            page_description=cat['description'],
            category=cat,
            items=items[:5],
            articles=articles,
            breadcrumbs=breadcrumbs,
            current_page='category',
        )
        out_dir = site_dir / slug
        write_html(out_dir / 'index.html', html)

    print(f'[OK] カテゴリインデックス {len(categories)} 件生成完了')
```

### Task 11: Create build_articles.py

- [ ] Create `photo-affiliate-hub/scripts/build_articles.py`:

```python
#!/usr/bin/env python3
"""記事ページ生成（比較記事・学習記事・用途別・固定ページ）"""

from pathlib import Path
from scripts.utils import parse_markdown_file, write_html
from scripts.build_taxonomies import build_breadcrumbs


TEMPLATE_MAP = {
    'article':  'article.html',
    'learn':    'learn.html',
    'usecase':  'usecase.html',
    'page':     'page.html',
}

CONTENT_DIRS = {
    'camera-bags': ('article', 'camera-bags'),
    'tripods':     ('article', 'tripods'),
    'sd-cards':    ('article', 'sd-cards'),
    'learn':       ('learn', 'learn'),
    'usecases':    ('usecase', 'usecases'),
    'pages':       ('page', None),
}


def build_articles(site_dir, jinja_env, content_dir, items_by_slug, categories_by_slug, base_path, associate_id=None):
    """全記事ページを生成する。articles リストを返す（トップページ等で使用）"""
    all_articles = []

    for dir_name, (template_type, url_prefix) in CONTENT_DIRS.items():
        src_dir = content_dir / dir_name
        if not src_dir.exists():
            continue

        for md_file in sorted(src_dir.glob('*.md')):
            fm, content_html = parse_markdown_file(md_file)

            if not fm.get('publish', True):
                print(f'[SKIP] {md_file.name} (publish: false)')
                continue

            slug = fm.get('slug', md_file.stem)
            title = fm.get('title', slug)
            template_name = TEMPLATE_MAP.get(fm.get('template', template_type), 'article.html')
            template = jinja_env.get_template(template_name)

            # 関連商品
            related_item_slugs = fm.get('related_items') or []
            related_items = [items_by_slug[s] for s in related_item_slugs if s in items_by_slug]

            # アフィリエイトURL付与
            for item in related_items:
                from scripts.utils import make_affiliate_url
                item['affiliate_url'] = item.get('affiliate_url') or make_affiliate_url(item.get('asin'), associate_id)

            # カテゴリ情報
            cat_slug = fm.get('category')
            category = categories_by_slug.get(cat_slug) if cat_slug else None

            # パンくず
            if template_type == 'article' and category:
                breadcrumbs = build_breadcrumbs('article', base_path, category=category, title=title)
            elif template_type in ('learn', 'usecase'):
                breadcrumbs = build_breadcrumbs(template_type, base_path, title=title)
            elif template_type == 'page':
                breadcrumbs = build_breadcrumbs('page', base_path, title=title)
            else:
                breadcrumbs = [{'name': 'ホーム', 'url': f'{base_path}/'}]

            html = template.render(
                page_title=title,
                page_description=fm.get('description', ''),
                fm=fm,
                content=content_html,
                related_items=related_items,
                breadcrumbs=breadcrumbs,
                updated_at=fm.get('updated_at', ''),
                tags=fm.get('tags') or [],
                category=category,
                current_page=template_type,
            )

            # 出力パス
            if template_type == 'page':
                out_path = site_dir / slug / 'index.html'
            elif url_prefix:
                out_path = site_dir / url_prefix / slug / 'index.html'
            else:
                out_path = site_dir / slug / 'index.html'

            write_html(out_path, html)

            # 記事メタ情報を蓄積
            article_meta = {
                'slug': slug,
                'title': title,
                'description': fm.get('description', ''),
                'category': cat_slug,
                'template': template_type,
                'tags': fm.get('tags') or [],
                'updated_at': str(fm.get('updated_at', '')),
                'url': str(out_path).replace(str(site_dir), '').replace('index.html', ''),
            }
            all_articles.append(article_meta)

    print(f'[OK] 記事 {len(all_articles)} 件生成完了')
    return all_articles
```

### Task 12: Create build_item_pages.py

- [ ] Create `photo-affiliate-hub/scripts/build_item_pages.py`:

```python
#!/usr/bin/env python3
"""商品個別ページ生成"""

from scripts.utils import write_html, make_affiliate_url
from scripts.build_taxonomies import build_breadcrumbs


def build_item_pages(site_dir, jinja_env, all_items, items_by_slug, categories_by_slug, base_path, associate_id=None):
    """全商品の個別ページを生成する"""
    template = jinja_env.get_template('item.html')
    count = 0

    for item in all_items:
        cat_slug = item.get('category')
        category = categories_by_slug.get(cat_slug)

        # 関連商品：同カテゴリの他商品
        related = [i for i in all_items if i['category'] == cat_slug and i['slug'] != item['slug']][:3]

        # アフィリエイトURL
        affiliate_url = item.get('affiliate_url') or make_affiliate_url(item.get('asin'), associate_id)

        # 関連商品にもアフィリエイトURL付与
        for r in related:
            r['affiliate_url'] = r.get('affiliate_url') or make_affiliate_url(r.get('asin'), associate_id)

        breadcrumbs = build_breadcrumbs('item', base_path, category=category, title=item['name'])

        html = template.render(
            page_title=f"{item['name']} レビュー・スペック",
            page_description=item.get('description', ''),
            item=item,
            affiliate_url=affiliate_url,
            related_items=related,
            breadcrumbs=breadcrumbs,
            category=category,
            current_page='item',
        )

        out_path = site_dir / 'items' / item['slug'] / 'index.html'
        write_html(out_path, html)
        count += 1

    print(f'[OK] 商品ページ {count} 件生成完了')
```

### Task 13: Create build_sitemap.py

- [ ] Create `photo-affiliate-hub/scripts/build_sitemap.py`:

```python
#!/usr/bin/env python3
"""sitemap.xml と robots.txt の生成"""

from datetime import datetime


def build_sitemap(site_dir, site_url, all_items, all_articles, categories):
    """sitemap.xml を生成する"""
    today = datetime.now().strftime('%Y-%m-%d')
    urls = []

    # トップ
    urls.append({'loc': f'{site_url}/', 'priority': '1.0'})

    # カテゴリトップ
    for cat in categories:
        urls.append({'loc': f"{site_url}/{cat['slug']}/", 'priority': '0.9'})

    # 記事
    for article in all_articles:
        url = article.get('url', '')
        if url:
            loc = f"{site_url}{url}" if url.startswith('/') else f"{site_url}/{url}"
            urls.append({'loc': loc.rstrip('/') + '/', 'priority': '0.8'})

    # 商品ページ
    for item in all_items:
        urls.append({'loc': f"{site_url}/items/{item['slug']}/", 'priority': '0.7'})

    # sitemap.xml 出力
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append('  <url>')
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append(f"    <priority>{u.get('priority', '0.5')}</priority>")
        lines.append('  </url>')
    lines.append('</urlset>')

    with open(site_dir / 'sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('[OK] sitemap.xml 生成完了')


def build_robots_txt(site_dir, site_url):
    """robots.txt を生成する"""
    content = f"""User-agent: *
Allow: /

Sitemap: {site_url}/sitemap.xml
"""
    with open(site_dir / 'robots.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] robots.txt 生成完了')
```

### Task 14: Create generate.py

- [ ] Create `photo-affiliate-hub/scripts/generate.py`:

```python
#!/usr/bin/env python3
"""サイト生成メインスクリプト"""

import os
import shutil
import sys
from pathlib import Path

# scripts/ をパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.utils import (
    load_config, load_categories, load_all_items, load_rankings,
    setup_jinja, copy_assets
)
from scripts.build_top import build_top
from scripts.build_category_indexes import build_category_indexes
from scripts.build_articles import build_articles
from scripts.build_item_pages import build_item_pages
from scripts.build_sitemap import build_sitemap, build_robots_txt

PROJECT_ROOT = Path(__file__).parent.parent


def main():
    print('\n=== Photo Affiliate Hub サイト生成開始 ===\n')

    # 設定読み込み
    config = load_config()
    associate_id = os.environ.get('AMAZON_ASSOCIATE_ID', '')
    if associate_id:
        print(f'[INFO] Amazon Associate ID: {associate_id}')
    else:
        print('[WARNING] AMAZON_ASSOCIATE_ID が未設定です')

    base_path = config['site']['base_path']
    site_url = config['site']['url']

    # データ読み込み
    categories = load_categories()
    all_items, items_by_slug = load_all_items(categories)
    rankings = load_rankings()
    categories_by_slug = {c['slug']: c for c in categories}

    print(f'[INFO] カテゴリ: {len(categories)} 件')
    print(f'[INFO] 商品: {len(all_items)} 件')

    # site/ ディレクトリを初期化
    site_dir = PROJECT_ROOT / config['build']['output_dir']
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir(parents=True)

    # assets コピー
    copy_assets(site_dir)

    # Jinja2 環境
    jinja_env = setup_jinja(config)

    # 記事を先にビルドして一覧を収集
    content_dir = PROJECT_ROOT / 'content'
    all_articles = build_articles(
        site_dir, jinja_env, content_dir,
        items_by_slug, categories_by_slug, base_path, associate_id
    )

    # カテゴリ別に集計
    items_by_category = {}
    articles_by_category = {}
    for cat in categories:
        items_by_category[cat['slug']] = [i for i in all_items if i['category'] == cat['slug']]
        articles_by_category[cat['slug']] = [a for a in all_articles if a.get('category') == cat['slug']]

    # トップページ
    recent_articles = sorted(all_articles, key=lambda a: a.get('updated_at', ''), reverse=True)
    build_top(site_dir, jinja_env, categories, items_by_slug, rankings, recent_articles)

    # カテゴリトップ
    build_category_indexes(site_dir, jinja_env, categories, items_by_category, articles_by_category, base_path)

    # 商品個別ページ
    build_item_pages(site_dir, jinja_env, all_items, items_by_slug, categories_by_slug, base_path, associate_id)

    # サイトマップ・robots
    build_sitemap(site_dir, site_url, all_items, all_articles, categories)
    build_robots_txt(site_dir, site_url)

    print(f'\n=== 生成完了 → {site_dir} ===\n')


if __name__ == '__main__':
    main()
```

---

## Chunk 4: Templates & Assets

### Task 15: Create base.html

- [ ] Create `photo-affiliate-hub/templates/base.html`:

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}{{ page_title ~ ' | ' if page_title else '' }}{{ site.title }}{% endblock %}</title>
  <meta name="description" content="{{ page_description or site.description }}">
  <link rel="canonical" href="{{ site.url }}{{ canonical_path | default('') }}">
  <!-- OGP -->
  <meta property="og:title" content="{{ page_title or site.title }}">
  <meta property="og:description" content="{{ page_description or site.description }}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{ site.url }}{{ canonical_path | default('') }}">
  <meta name="twitter:card" content="summary">
  <!-- CSS -->
  <link rel="stylesheet" href="{{ base_path }}/assets/css/style.css">
  <!-- Analytics -->
  {% if config.analytics.ga_measurement_id %}
  <script async src="https://www.googletagmanager.com/gtag/js?id={{ config.analytics.ga_measurement_id }}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '{{ config.analytics.ga_measurement_id }}');
  </script>
  {% endif %}
  {% block extra_head %}{% endblock %}
</head>
<body>
  {% include 'partials/header.html' %}

  <main class="site-main">
    <div class="container">
      {% if breadcrumbs %}{% include 'partials/breadcrumbs.html' %}{% endif %}
      {% block content %}{% endblock %}
    </div>
  </main>

  {% include 'partials/footer.html' %}

  <script src="{{ base_path }}/assets/js/main.js"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

### Task 16: Create partials

- [ ] Create `photo-affiliate-hub/templates/partials/header.html`:

```html
<header class="site-header">
  <div class="container">
    <div class="header-inner">
      <a href="{{ base_path }}/" class="site-logo">{{ site.title }}</a>
      <nav class="site-nav">
        <a href="{{ base_path }}/" {% if current_page == 'home' %}class="active"{% endif %}>ホーム</a>
        <a href="{{ base_path }}/camera-bags/" {% if category and category.slug == 'camera-bags' %}class="active"{% endif %}>カメラバッグ</a>
        <a href="{{ base_path }}/tripods/" {% if category and category.slug == 'tripods' %}class="active"{% endif %}>三脚</a>
        <a href="{{ base_path }}/sd-cards/" {% if category and category.slug == 'sd-cards' %}class="active"{% endif %}>SDカード</a>
        <a href="{{ base_path }}/learn/what-is-v60-v90/">学ぶ</a>
      </nav>
    </div>
  </div>
</header>
```

- [ ] Create `photo-affiliate-hub/templates/partials/footer.html`:

```html
<footer class="site-footer">
  <div class="container">
    <nav class="footer-nav">
      <a href="{{ base_path }}/">ホーム</a>
      <a href="{{ base_path }}/camera-bags/">カメラバッグ</a>
      <a href="{{ base_path }}/tripods/">三脚</a>
      <a href="{{ base_path }}/sd-cards/">SDカード</a>
      <a href="{{ base_path }}/about/">このサイトについて</a>
      <a href="{{ base_path }}/disclosure/">広告開示</a>
      <a href="{{ base_path }}/privacy/">プライバシーポリシー</a>
    </nav>
    <p class="affiliate-notice">当サイトはAmazonアソシエイトプログラム等のアフィリエイトプログラムに参加しています。<a href="{{ base_path }}/disclosure/">詳細はこちら</a></p>
    <p class="copyright">&copy; 2026 {{ site.title }}</p>
  </div>
</footer>
```

- [ ] Create `photo-affiliate-hub/templates/partials/breadcrumbs.html`:

```html
<nav class="breadcrumbs" aria-label="パンくずリスト">
  <ol>
    {% for crumb in breadcrumbs %}
    <li>
      {% if crumb.url %}<a href="{{ crumb.url }}">{{ crumb.name }}</a>{% else %}<span>{{ crumb.name }}</span>{% endif %}
      {% if not loop.last %}<span class="sep">›</span>{% endif %}
    </li>
    {% endfor %}
  </ol>
</nav>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {% for crumb in breadcrumbs %}
    {
      "@type": "ListItem",
      "position": {{ loop.index }},
      "name": "{{ crumb.name }}",
      "item": "{{ site.url }}{{ crumb.url or '' }}"
    }{% if not loop.last %},{% endif %}
    {% endfor %}
  ]
}
</script>
```

- [ ] Create `photo-affiliate-hub/templates/partials/related_items.html`:

```html
{% if related_items %}
<section class="related-items">
  <h2>おすすめ商品</h2>
  <div class="item-grid">
    {% for item in related_items %}
    <div class="item-card">
      <a href="{{ base_path }}/items/{{ item.slug }}/">
        <div class="item-card-img">
          {% if item.image %}<img src="{{ base_path }}{{ item.image }}" alt="{{ item.name }}" loading="lazy">
          {% else %}<div class="no-image">No Image</div>{% endif %}
        </div>
        <div class="item-card-body">
          <p class="item-brand">{{ item.brand }}</p>
          <h3 class="item-name">{{ item.name }}</h3>
          {% if item.price_range %}<p class="item-price">{{ item.price_range }}</p>{% endif %}
        </div>
      </a>
      {% if item.affiliate_url %}
      <a href="{{ item.affiliate_url }}" class="btn btn-amazon" target="_blank" rel="noopener nofollow">Amazonで見る</a>
      {% endif %}
    </div>
    {% endfor %}
  </div>
</section>
{% endif %}
```

- [ ] Create `photo-affiliate-hub/templates/partials/article_cards.html`:

```html
{% if articles %}
<div class="article-list">
  {% for article in articles %}
  <article class="article-card">
    <a href="{{ base_path }}{{ article.url }}">
      <h3>{{ article.title }}</h3>
      <p>{{ article.description }}</p>
      {% if article.updated_at %}<time>{{ article.updated_at }}</time>{% endif %}
    </a>
  </article>
  {% endfor %}
</div>
{% endif %}
```

### Task 17: Create page templates

- [ ] Create `photo-affiliate-hub/templates/top.html`:

```html
{% extends 'base.html' %}

{% block content %}
<section class="hero">
  <h1>{{ site.title }}</h1>
  <p>{{ site.description }}</p>
</section>

<section class="categories">
  <h2>カテゴリ一覧</h2>
  <div class="category-grid">
    {% for cat in categories %}
    <a href="{{ base_path }}/{{ cat.slug }}/" class="category-card">
      <h3>{{ cat.name }}</h3>
      <p>{{ cat.description }}</p>
    </a>
    {% endfor %}
  </div>
</section>

{% for cat in categories %}
{% if featured_items[cat.slug] %}
<section class="featured-items">
  <h2>{{ cat.name }} おすすめ</h2>
  <div class="item-grid">
    {% for item in featured_items[cat.slug] %}
    <div class="item-card">
      <a href="{{ base_path }}/items/{{ item.slug }}/">
        <div class="item-card-img">
          {% if item.image %}<img src="{{ base_path }}{{ item.image }}" alt="{{ item.name }}" loading="lazy">
          {% else %}<div class="no-image">No Image</div>{% endif %}
        </div>
        <div class="item-card-body">
          <p class="item-brand">{{ item.brand }}</p>
          <h3 class="item-name">{{ item.name }}</h3>
          {% if item.price_range %}<p class="item-price">{{ item.price_range }}</p>{% endif %}
        </div>
      </a>
    </div>
    {% endfor %}
  </div>
  <a href="{{ base_path }}/{{ cat.slug }}/" class="btn btn-more">{{ cat.name }}をもっと見る</a>
</section>
{% endif %}
{% endfor %}

{% if recent_articles %}
<section class="recent-articles">
  <h2>新着記事</h2>
  {% set articles = recent_articles %}
  {% include 'partials/article_cards.html' %}
</section>
{% endif %}
{% endblock %}
```

- [ ] Create `photo-affiliate-hub/templates/category_index.html`:

```html
{% extends 'base.html' %}

{% block content %}
<div class="page-header">
  <h1>{{ category.name }} おすすめ・比較ガイド</h1>
  <p>{{ category.description }}</p>
</div>

{% if articles %}
<section class="article-section">
  <h2>比較・おすすめ記事</h2>
  {% include 'partials/article_cards.html' %}
</section>
{% endif %}

{% if items %}
<section class="item-section">
  <h2>おすすめ商品</h2>
  {% set related_items = items %}
  {% include 'partials/related_items.html' %}
</section>
{% endif %}
{% endblock %}
```

- [ ] Create `photo-affiliate-hub/templates/article.html`:

```html
{% extends 'base.html' %}

{% block content %}
<article class="article-page">
  <header class="article-header">
    <h1>{{ page_title }}</h1>
    {% if updated_at %}<time class="updated-at">最終更新: {{ updated_at }}</time>{% endif %}
    <p class="affiliate-disclosure">※本記事にはアフィリエイトリンクが含まれています。<a href="{{ base_path }}/disclosure/">詳細</a></p>
  </header>

  {% if related_items %}
  {% include 'partials/related_items.html' %}
  {% endif %}

  <div class="article-body">{{ content }}</div>

  {% if related_items %}
  <section class="cta-section">
    <h2>この記事で紹介した商品</h2>
    {% include 'partials/related_items.html' %}
  </section>
  {% endif %}

  {% if fm.related_articles %}
  <section class="related-articles">
    <h2>関連記事</h2>
    {% set articles = fm.related_articles %}
    {% include 'partials/article_cards.html' %}
  </section>
  {% endif %}
</article>
{% endblock %}
```

- [ ] Create `photo-affiliate-hub/templates/item.html`:

```html
{% extends 'base.html' %}

{% block content %}
<article class="item-page">
  <header class="item-header">
    <p class="item-brand-label">{{ item.brand }}</p>
    <h1>{{ item.name }}</h1>
    {% if item.price_range %}<p class="item-price-range">参考価格: {{ item.price_range }}</p>{% endif %}
  </header>

  {% if affiliate_url %}
  <div class="cta-top">
    <a href="{{ affiliate_url }}" class="btn btn-amazon btn-large" target="_blank" rel="noopener nofollow">Amazonで価格を確認する</a>
    <p class="affiliate-disclosure">※アフィリエイトリンクです。<a href="{{ base_path }}/disclosure/">詳細</a></p>
  </div>
  {% endif %}

  {% if item.image %}
  <div class="item-main-image">
    <img src="{{ base_path }}{{ item.image }}" alt="{{ item.name }}">
  </div>
  {% endif %}

  <section class="item-description">
    <h2>商品概要</h2>
    <p>{{ item.description }}</p>
  </section>

  {% if item.features %}
  <section class="item-features">
    <h2>特長</h2>
    <ul>
      {% for f in item.features %}<li>{{ f }}</li>{% endfor %}
    </ul>
  </section>
  {% endif %}

  {% if item.suitable_for %}
  <section class="item-suitable">
    <h2>こんな方におすすめ</h2>
    <ul>
      {% for s in item.suitable_for %}<li>{{ s }}</li>{% endfor %}
    </ul>
  </section>
  {% endif %}

  <!-- スペック表 -->
  <section class="item-specs">
    <h2>スペック</h2>
    <table class="spec-table">
      <tbody>
        <tr><th>ブランド</th><td>{{ item.brand }}</td></tr>
        {% if item.capacity %}<tr><th>容量</th><td>{{ item.capacity }}</td></tr>{% endif %}
        {% if item.speed_class %}<tr><th>スピードクラス</th><td>{{ item.speed_class }}</td></tr>{% endif %}
        {% if item.read_speed %}<tr><th>読み込み速度</th><td>{{ item.read_speed }}MB/s</td></tr>{% endif %}
        {% if item.write_speed %}<tr><th>書き込み速度</th><td>{{ item.write_speed }}MB/s</td></tr>{% endif %}
        {% if item.weight %}<tr><th>重量</th><td>{{ item.weight }}g</td></tr>{% endif %}
        {% if item.max_load %}<tr><th>最大耐荷重</th><td>{{ item.max_load }}g</td></tr>{% endif %}
        {% if item.max_height %}<tr><th>最大高さ</th><td>{{ item.max_height }}cm</td></tr>{% endif %}
        {% if item.material %}<tr><th>素材</th><td>{{ item.material }}</td></tr>{% endif %}
        {% if item.waterproof is not none %}<tr><th>防水</th><td>{{ '対応' if item.waterproof else '非対応' }}</td></tr>{% endif %}
      </tbody>
    </table>
  </section>

  {% if affiliate_url %}
  <div class="cta-bottom">
    <a href="{{ affiliate_url }}" class="btn btn-amazon btn-large" target="_blank" rel="noopener nofollow">Amazonで購入する</a>
  </div>
  {% endif %}

  {% if related_items %}
  <section class="related-items-section">
    <h2>同じカテゴリの商品</h2>
    {% include 'partials/related_items.html' %}
  </section>
  {% endif %}
</article>
{% endblock %}
```

- [ ] Create `photo-affiliate-hub/templates/learn.html`:

```html
{% extends 'base.html' %}

{% block content %}
<article class="learn-page">
  <header class="learn-header">
    <h1>{{ page_title }}</h1>
    {% if updated_at %}<time class="updated-at">最終更新: {{ updated_at }}</time>{% endif %}
  </header>

  <div class="article-body">{{ content }}</div>

  {% if related_items %}
  <section class="related-items-section">
    <h2>関連商品</h2>
    {% include 'partials/related_items.html' %}
  </section>
  {% endif %}
</article>
{% endblock %}
```

- [ ] Create `photo-affiliate-hub/templates/usecase.html`:

```html
{% extends 'base.html' %}

{% block content %}
<article class="usecase-page">
  <header class="usecase-header">
    <h1>{{ page_title }}</h1>
    {% if updated_at %}<time class="updated-at">最終更新: {{ updated_at }}</time>{% endif %}
    <p class="affiliate-disclosure">※本記事にはアフィリエイトリンクが含まれています。<a href="{{ base_path }}/disclosure/">詳細</a></p>
  </header>

  <div class="article-body">{{ content }}</div>

  {% if related_items %}
  <section class="related-items-section">
    <h2>おすすめ商品</h2>
    {% include 'partials/related_items.html' %}
  </section>
  {% endif %}
</article>
{% endblock %}
```

- [ ] Create `photo-affiliate-hub/templates/page.html`:

```html
{% extends 'base.html' %}

{% block content %}
<article class="static-page">
  <header class="page-header">
    <h1>{{ page_title }}</h1>
    {% if updated_at %}<time class="updated-at">最終更新: {{ updated_at }}</time>{% endif %}
  </header>
  <div class="article-body">{{ content }}</div>
</article>
{% endblock %}
```

### Task 18: Create CSS and JS

- [ ] Create `photo-affiliate-hub/assets/css/style.css`:

```css
/* ===== CSS Variables ===== */
:root {
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-amazon: #ff9900;
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-border: #e5e7eb;
  --color-bg: #ffffff;
  --color-bg-subtle: #f9fafb;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif;
  --max-width: 1100px;
  --radius: 8px;
}

/* ===== Reset ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-sans); color: var(--color-text); background: var(--color-bg); line-height: 1.7; }
img { max-width: 100%; height: auto; }
a { color: var(--color-primary); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ===== Layout ===== */
.container { max-width: var(--max-width); margin: 0 auto; padding: 0 1rem; }

/* ===== Header ===== */
.site-header { background: var(--color-bg); border-bottom: 1px solid var(--color-border); padding: 0.75rem 0; position: sticky; top: 0; z-index: 100; }
.header-inner { display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
.site-logo { font-size: 1.1rem; font-weight: 700; color: var(--color-text); }
.site-nav { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.site-nav a { font-size: 0.9rem; color: var(--color-text-muted); }
.site-nav a.active, .site-nav a:hover { color: var(--color-primary); }

/* ===== Main ===== */
.site-main { padding: 2rem 0 4rem; min-height: 60vh; }

/* ===== Footer ===== */
.site-footer { background: var(--color-bg-subtle); border-top: 1px solid var(--color-border); padding: 2rem 0; margin-top: 4rem; font-size: 0.85rem; color: var(--color-text-muted); }
.footer-nav { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.affiliate-notice { margin-bottom: 0.5rem; }
.copyright { }

/* ===== Breadcrumbs ===== */
.breadcrumbs { margin-bottom: 1.5rem; }
.breadcrumbs ol { display: flex; flex-wrap: wrap; gap: 0.25rem; list-style: none; font-size: 0.85rem; color: var(--color-text-muted); }
.breadcrumbs .sep { color: var(--color-border); }

/* ===== Hero ===== */
.hero { text-align: center; padding: 3rem 1rem; background: var(--color-bg-subtle); border-radius: var(--radius); margin-bottom: 3rem; }
.hero h1 { font-size: 2rem; margin-bottom: 0.75rem; }
.hero p { color: var(--color-text-muted); font-size: 1.1rem; }

/* ===== Category Grid ===== */
.categories { margin-bottom: 3rem; }
.categories h2 { font-size: 1.4rem; margin-bottom: 1rem; }
.category-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
.category-card { display: block; padding: 1.5rem; border: 1px solid var(--color-border); border-radius: var(--radius); transition: border-color 0.2s; }
.category-card:hover { border-color: var(--color-primary); text-decoration: none; }
.category-card h3 { font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--color-text); }
.category-card p { font-size: 0.9rem; color: var(--color-text-muted); }

/* ===== Item Grid ===== */
.item-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem; }
.item-card { border: 1px solid var(--color-border); border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; }
.item-card a { color: inherit; }
.item-card-img { aspect-ratio: 1; background: var(--color-bg-subtle); display: flex; align-items: center; justify-content: center; }
.item-card-img img { width: 100%; height: 100%; object-fit: contain; }
.no-image { color: var(--color-text-muted); font-size: 0.8rem; }
.item-card-body { padding: 0.75rem; flex: 1; }
.item-brand { font-size: 0.75rem; color: var(--color-text-muted); margin-bottom: 0.25rem; }
.item-name { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.25rem; }
.item-price { font-size: 0.85rem; color: var(--color-text-muted); }

/* ===== Buttons ===== */
.btn { display: inline-block; padding: 0.6rem 1.2rem; border-radius: var(--radius); font-weight: 600; font-size: 0.9rem; text-align: center; transition: background 0.2s; }
.btn-amazon { background: var(--color-amazon); color: #fff; }
.btn-amazon:hover { background: #e88a00; text-decoration: none; color: #fff; }
.btn-more { background: var(--color-primary); color: #fff; margin-top: 1rem; }
.btn-more:hover { background: var(--color-primary-dark); text-decoration: none; color: #fff; }
.btn-large { padding: 0.875rem 2rem; font-size: 1rem; }

/* ===== Article ===== */
.article-header, .learn-header, .usecase-header, .page-header { margin-bottom: 2rem; }
.article-header h1, .learn-header h1, .usecase-header h1, .page-header h1 { font-size: 1.75rem; line-height: 1.4; margin-bottom: 0.5rem; }
.updated-at { font-size: 0.85rem; color: var(--color-text-muted); display: block; margin-bottom: 0.5rem; }
.affiliate-disclosure { font-size: 0.8rem; color: var(--color-text-muted); padding: 0.5rem; background: var(--color-bg-subtle); border-left: 3px solid var(--color-border); margin-bottom: 1rem; }

.article-body h2 { font-size: 1.3rem; margin: 2rem 0 0.75rem; padding-bottom: 0.5rem; border-bottom: 2px solid var(--color-border); }
.article-body h3 { font-size: 1.1rem; margin: 1.5rem 0 0.5rem; }
.article-body p { margin-bottom: 1rem; }
.article-body ul, .article-body ol { margin: 0.5rem 0 1rem 1.5rem; }
.article-body li { margin-bottom: 0.25rem; }
.article-body table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.article-body th, .article-body td { padding: 0.6rem 0.75rem; border: 1px solid var(--color-border); text-align: left; }
.article-body th { background: var(--color-bg-subtle); font-weight: 600; }

/* ===== Item Page ===== */
.item-page .item-header { margin-bottom: 1.5rem; }
.item-brand-label { font-size: 0.85rem; color: var(--color-text-muted); margin-bottom: 0.25rem; }
.item-price-range { font-size: 1rem; color: var(--color-primary); font-weight: 600; margin-top: 0.25rem; }
.cta-top, .cta-bottom { margin: 1.5rem 0; padding: 1.5rem; background: var(--color-bg-subtle); border-radius: var(--radius); text-align: center; }
.item-main-image { margin: 1.5rem 0; max-width: 400px; }
.spec-table { width: 100%; border-collapse: collapse; margin: 0.5rem 0; }
.spec-table th { background: var(--color-bg-subtle); padding: 0.5rem 0.75rem; border: 1px solid var(--color-border); text-align: left; width: 40%; }
.spec-table td { padding: 0.5rem 0.75rem; border: 1px solid var(--color-border); }
.item-features ul, .item-suitable ul { list-style: disc; margin-left: 1.5rem; }
.item-features li, .item-suitable li { margin-bottom: 0.25rem; }

/* ===== Article List ===== */
.article-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.article-card { border: 1px solid var(--color-border); border-radius: var(--radius); overflow: hidden; }
.article-card a { display: block; padding: 1rem; color: inherit; }
.article-card h3 { font-size: 1rem; margin-bottom: 0.4rem; }
.article-card p { font-size: 0.85rem; color: var(--color-text-muted); margin-bottom: 0.4rem; }
.article-card time { font-size: 0.75rem; color: var(--color-text-muted); }
.article-card:hover { border-color: var(--color-primary); }

/* ===== Sections ===== */
.featured-items, .recent-articles, .article-section, .item-section, .related-items, .cta-section, .related-articles, .related-items-section { margin-top: 3rem; }
.featured-items h2, .recent-articles h2, .article-section h2, .item-section h2, .related-items h2, .cta-section h2, .related-articles h2, .related-items-section h2 { font-size: 1.3rem; margin-bottom: 1rem; padding-bottom: 0.4rem; border-bottom: 2px solid var(--color-border); }

/* ===== Responsive ===== */
@media (max-width: 640px) {
  .hero h1 { font-size: 1.5rem; }
  .site-nav { gap: 0.75rem; }
  .item-grid { grid-template-columns: repeat(2, 1fr); }
  .article-list { grid-template-columns: 1fr; }
}
```

- [ ] Create `photo-affiliate-hub/assets/js/main.js`:

```javascript
// Photo Affiliate Hub - Main JS
// JSなしでも閲覧可能な設計のため、最小限の実装

document.addEventListener('DOMContentLoaded', function () {
  // 外部リンクに target="_blank" rel="noopener" を付与（アフィリエイト以外）
  document.querySelectorAll('a[href^="http"]').forEach(function (link) {
    if (!link.rel.includes('noopener')) {
      link.setAttribute('rel', 'noopener noreferrer');
      link.setAttribute('target', '_blank');
    }
  });
});
```

---

## Chunk 5: GitHub Actions & Verification

### Task 19: Create GitHub Actions workflow

- [ ] Create `photo-affiliate-hub/.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: '0 21 * * *'  # 毎日 JST 06:00 (UTC 21:00)

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Build site
        env:
          AMAZON_ASSOCIATE_ID: ${{ secrets.AMAZON_ASSOCIATE_ID }}
          GA_MEASUREMENT_ID: ${{ secrets.GA_MEASUREMENT_ID }}
        run: python scripts/generate.py

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site/

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Task 20: Create README

- [ ] Create `photo-affiliate-hub/README.md`:

```markdown
# フォト機材おすすめガイド

カメラバッグ・三脚・SDカードのアフィリエイト向け静的サイト生成システム。

## 構成

- **カテゴリ**: カメラバッグ / 三脚 / SDカード
- **ビルド**: Python + Jinja2 + Markdown
- **公開**: GitHub Pages (`/product-recommendation-site`)

## セットアップ

```bash
pip install -r requirements.txt
python scripts/generate.py
```

## 環境変数（GitHub Secrets）

| 変数名 | 説明 | 必須 |
|--------|------|------|
| `AMAZON_ASSOCIATE_ID` | Amazonアソシエイトタグ | 推奨 |
| `GA_MEASUREMENT_ID` | Google Analytics ID | 任意 |

## 商品追加

`data/camera_bags.json`, `data/tripods.json`, `data/sd_cards.json` にエントリを追加。
必須フィールド: `slug`, `name`, `category`, `asin`

## 記事追加

`content/<category>/` に Markdown ファイルを追加。front matter に `publish: true` を設定。
```

### Task 21: Verify build

- [ ] Install dependencies and run the build:

```bash
cd photo-affiliate-hub
pip install -r requirements.txt
python scripts/generate.py
```

Expected output:
```
=== Photo Affiliate Hub サイト生成開始 ===
[INFO] カテゴリ: 3 件
[INFO] 商品: 15 件
[OK] assets コピー完了
[OK] 記事 XX 件生成完了
[OK] トップページ生成完了
[OK] カテゴリインデックス 3 件生成完了
[OK] 商品ページ 15 件生成完了
[OK] sitemap.xml 生成完了
[OK] robots.txt 生成完了
=== 生成完了 → .../site ===
```

- [ ] Confirm these files exist in `site/`:
  - `site/index.html`
  - `site/camera-bags/index.html`
  - `site/tripods/index.html`
  - `site/sd-cards/index.html`
  - `site/items/sony-tough-sf-g64t/index.html`
  - `site/learn/what-is-v60-v90/index.html`
  - `site/sitemap.xml`
  - `site/robots.txt`
