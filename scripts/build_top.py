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
