#!/usr/bin/env python3
"""記事ページ生成（比較記事・学習記事・用途別・固定ページ）"""

from pathlib import Path
from scripts.utils import parse_markdown_file, write_html, make_affiliate_url
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
