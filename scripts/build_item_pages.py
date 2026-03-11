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
