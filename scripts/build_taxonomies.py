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
