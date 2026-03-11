# Photo Affiliate Hub — 設計書

Date: 2026-03-11

## 概要

カメラバッグ・三脚・SDカード の3カテゴリを1リポジトリで管理するアフィリエイト向け静的サイト生成システム。Python + Jinja2 + Markdown でビルドし、GitHub Actions で GitHub Pages に自動デプロイする。

## 確定仕様

| 項目 | 値 |
|------|----|
| プロジェクトディレクトリ | `photo-affiliate-hub/` |
| サイトURL | `https://KurouzuSetsuna.github.io/product-recommendation-site` |
| 言語 | 日本語 |
| アフィリエイト | Amazon ASIN + `AMAZON_ASSOCIATE_ID` 環境変数 |
| カテゴリ | camera-bags / tripods / sd-cards |
| ビルドツール | Python 3.x + Jinja2 + python-markdown |
| デプロイ | GitHub Actions → GitHub Pages |

## ディレクトリ構成

```
photo-affiliate-hub/
├── README.md
├── requirements.txt
├── config.yml
├── data/
│   ├── categories.json
│   ├── camera_bags.json
│   ├── tripods.json
│   ├── sd_cards.json
│   ├── rankings.json
│   └── site_meta.json
├── content/
│   ├── camera-bags/
│   │   ├── best-camera-bags-for-travel.md
│   │   ├── best-camera-bags-for-beginners.md
│   │   └── lightweight-camera-bags.md
│   ├── tripods/
│   │   ├── best-lightweight-tripods.md
│   │   ├── best-tripods-for-video.md
│   │   └── best-budget-tripods.md
│   ├── sd-cards/
│   │   ├── best-v60-sd-cards.md
│   │   ├── best-v90-sd-cards.md
│   │   └── best-sd-cards-for-4k-video.md
│   ├── learn/
│   │   ├── how-to-choose-camera-bag.md
│   │   ├── how-to-choose-tripod.md
│   │   └── what-is-v60-v90.md
│   ├── usecases/
│   │   ├── travel-camera-bag.md
│   │   ├── video-tripod-for-youtube.md
│   │   └── sd-card-for-4k60p.md
│   └── pages/
│       ├── about.md
│       ├── disclosure.md
│       └── privacy.md
├── templates/
│   ├── base.html
│   ├── top.html
│   ├── category_index.html
│   ├── article.html
│   ├── item.html
│   ├── learn.html
│   ├── usecase.html
│   ├── page.html               # about / disclosure / privacy 用
│   └── partials/
│       ├── header.html
│       ├── footer.html
│       ├── breadcrumbs.html
│       ├── related_items.html
│       └── article_cards.html
├── assets/
│   ├── css/style.css
│   └── js/main.js
├── scripts/
│   ├── generate.py          # オーケストレーター
│   ├── build_top.py
│   ├── build_category_indexes.py
│   ├── build_articles.py
│   ├── build_item_pages.py
│   ├── build_taxonomies.py
│   ├── build_sitemap.py
│   └── utils.py
├── site/                    # ビルド出力（Git管理外）
└── .github/
    └── workflows/
        └── deploy.yml
```

## config.yml スキーマ

```yaml
site:
  title: "フォト機材おすすめガイド"
  url: "https://KurouzuSetsuna.github.io/product-recommendation-site"
  base_path: "/product-recommendation-site"   # GitHub Pages サブパス
  description: "カメラバッグ・三脚・SDカードのおすすめを比較するガイドサイト"
  locale: "ja"

build:
  output_dir: "site"
  validate_required_fields: true  # 必須フィールド欠損時にビルドを中断する

analytics:
  ga_measurement_id: ""   # 環境変数 GA_MEASUREMENT_ID で上書き可
```

`base_path` はすべてのテンプレートで `{{ config.site.base_path }}` として使用し、相対パス (`../../`) は使わない。

## データ設計

### categories.json
```json
[
  { "slug": "camera-bags", "name": "カメラバッグ", "description": "用途別・サイズ別に比較できるカメラバッグ特集", "item_data_file": "camera_bags.json" },
  { "slug": "tripods",     "name": "三脚",         "description": "軽量・動画向け・コスパ重視で比較する三脚特集",  "item_data_file": "tripods.json" },
  { "slug": "sd-cards",   "name": "SDカード",      "description": "V60 / V90 を中心に動画向けSDカードを比較",    "item_data_file": "sd_cards.json" }
]
```

### 商品データ（例: sd_cards.json）
- 必須フィールド: `slug`, `name`, `category`, `asin`（欠損時はビルドを中断しエラーログを出力）
- アフィリエイトURL: `asin` から生成。`affiliate_url` フィールドがあればそちらを優先（Amazon以外のリンクに対応）
- オプション: `brand`, `capacity`, `speed_class`, `read_speed`, `write_speed`, `waterproof`, `image`, `tags`

### rankings.json
サイトトップページの「おすすめ商品」セクションで使用するカテゴリ別推薦スラッグリスト。
```json
{
  "camera-bags": ["slug-1", "slug-2", "slug-3"],
  "tripods": ["slug-1", "slug-2", "slug-3"],
  "sd-cards": ["slug-1", "slug-2", "slug-3"]
}
```

### site_meta.json
サイト共通メタ情報（config.yml で管理できない動的な値）。MVPでは空オブジェクト `{}` でよい。将来的に最終更新日などを持つ。

### Markdown front matter
```yaml
---
title: V90対応SDカードおすすめ7選
slug: best-v90-sd-cards
category: sd-cards
description: 4K/6K/8K動画撮影に向くV90対応SDカードを比較。
template: article
related_items: [sony-tough-v90-64gb, prograde-v90-128gb]
tags: [sdカード, v90, 動画撮影]
publish: true
updated_at: 2026-03-11
---
```

## URLポリシー

| ページ種別 | URL例 |
|-----------|-------|
| トップ | `/` |
| カテゴリトップ | `/camera-bags/` |
| 比較記事 | `/camera-bags/best-camera-bags-for-travel/` |
| 商品個別 | `/items/sony-tough-v90-64gb/` |
| 学習記事 | `/learn/what-is-v60-v90/` |
| 用途別 | `/usecases/travel-camera-bag/` |
| 固定ページ | `/about/`, `/disclosure/`, `/privacy/` |

## ビルド処理フロー

```
generate.py
  ├── utils.py: config.yml / categories.json / 全商品データ読み込み、共通ヘルパー
  ├── build_taxonomies.py: 関連記事・パンくずデータ生成（HTML出力なし、データ準備のみ）
  ├── build_top.py: トップページ生成 (/)
  ├── build_category_indexes.py: カテゴリトップ×3 (/camera-bags/ etc.)
  ├── build_articles.py: 比較記事 + 学習記事 + 用途別記事 + 固定ページ
  ├── build_item_pages.py: 商品個別ページ (/items/<slug>/)
  └── build_sitemap.py: sitemap.xml + robots.txt
```

`build_feeds.py` は MVP スコープ外。将来対応。

`publish: false` のMarkdown記事はビルド時にスキップし、`[SKIP]` ログを出力する。

## アフィリエイト

- `ASIN` を商品データに持つ
- `AMAZON_ASSOCIATE_ID` 環境変数から生成: `https://www.amazon.co.jp/dp/{ASIN}/?tag={ASSOCIATE_ID}`
- 未設定時はASINのみのURL（`https://www.amazon.co.jp/dp/{ASIN}/`）

## GitHub Actions

トリガー:
- `push` to `main`
- `workflow_dispatch`
- `schedule`: 毎日 21:00 UTC (JST 06:00)

環境変数（Secrets）:
- `AMAZON_ASSOCIATE_ID` — アフィリエイトタグ（未設定時はASINのみのURL）
- `GA_MEASUREMENT_ID`（省略可）— 未設定時はタグを出力しない

## SEO

全ページ必須:
- `<title>`, `<meta description>`, `canonical`
- OGP タグ
- パンくずリスト（JSON-LD BreadcrumbList）
- 関連記事・内部リンク
- 更新日表示
- 広告開示リンク（フッター）

## MVP スコープ

各カテゴリ:
- カテゴリトップ: 1ページ
- 比較記事: 3記事
- 学習記事: 1記事
- 用途別記事: 1記事
- 商品個別ページ: 5件以上

固定ページ: about / disclosure / privacy

## 受け入れ基準

1. `python scripts/generate.py` で `site/` に全HTMLが生成される
2. 3カテゴリすべてのページが出力される
3. GitHub Actionsで自動デプロイできる
4. 各ページにSEOメタ情報が付与される
5. アフィリエイトリンクが商品データから生成される
6. `sitemap.xml` と `robots.txt` が出力される
7. 解析タグを環境変数でON/OFFできる
