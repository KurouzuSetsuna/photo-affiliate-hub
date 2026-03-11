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
