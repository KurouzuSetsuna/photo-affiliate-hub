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
