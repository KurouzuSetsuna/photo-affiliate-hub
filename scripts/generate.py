#!/usr/bin/env python3
"""サイト生成メインスクリプト"""

import os
import shutil
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils import (
    load_config, load_categories, load_all_items, load_rankings,
    setup_jinja, copy_assets
)
from scripts.build_top import build_top
from scripts.build_category_indexes import build_category_indexes
from scripts.build_articles import build_articles
from scripts.build_item_pages import build_item_pages
from scripts.build_sitemap import build_sitemap, build_robots_txt


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
