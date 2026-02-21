#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日 A 股交易报告生成器 - ESA Pages 版本
生成 JSON 数据 + Astro 静态页面
"""

import os
import glob
import json
from datetime import datetime, timedelta

WORKSPACE = "/home/rende/.openclaw/workspace"
TRADING_DIR = os.path.join(WORKSPACE, "trading")
REPO_DIR = "/home/rende/a-stock-daily"
PUBLIC_DATA_DIR = os.path.join(REPO_DIR, "public", "data")
DIST_DATA_DIR = os.path.join(REPO_DIR, "dist", "data")
OUTPUT_JSON_PUBLIC = os.path.join(PUBLIC_DATA_DIR, "stocks.json")
OUTPUT_JSON_DIST = os.path.join(DIST_DATA_DIR, "stocks.json")


def get_latest_file(pattern):
    """获取匹配模式的最新文件"""
    files = glob.glob(os.path.join(TRADING_DIR, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)


def parse_csv_stocks(filepath):
    """解析候选股票 CSV"""
    stocks = []
    if not filepath or not os.path.exists(filepath):
        return stocks
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) < 2:
            return stocks
        
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) >= 6:
                stocks.append({
                    'code': parts[0],
                    'name': parts[1],
                    'price': parts[2],
                    'change': parts[3],
                    'volume': parts[4],
                    'reason': parts[5] if len(parts) > 5 else ""
                })
    return stocks


def main():
    """主函数"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    date_file = today.strftime("%Y%m%d")
    
    # 获取最新文件
    stocks_file = get_latest_file(f"candidate_stocks_{date_file}.csv")
    if not stocks_file:
        yesterday = today - timedelta(days=1)
        date_file = yesterday.strftime("%Y%m%d")
        stocks_file = get_latest_file(f"candidate_stocks_{date_file}.csv")
        date_str = yesterday.strftime("%Y-%m-%d")
    
    # 解析数据
    stocks = parse_csv_stocks(stocks_file)
    
    # 创建数据目录
    os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)
    os.makedirs(DIST_DATA_DIR, exist_ok=True)
    
    # 生成 JSON
    data = {
        'date': date_str,
        'count': len(stocks),
        'stocks': stocks
    }
    
    # 同时写入 public/data 和 dist/data
    with open(OUTPUT_JSON_PUBLIC, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(OUTPUT_JSON_DIST, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已生成：{OUTPUT_JSON_PUBLIC}")
    print(f"✅ 数据已生成：{OUTPUT_JSON_DIST}")
    print(f"📅 数据日期：{date_str}")
    print(f"📊 候选股票：{len(stocks)}只")
    
    return 0


if __name__ == "__main__":
    exit(main())
