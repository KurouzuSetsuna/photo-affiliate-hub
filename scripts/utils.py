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
