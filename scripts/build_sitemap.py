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
