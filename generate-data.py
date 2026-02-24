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


def safe_float(value, default=0.0):
    """安全转换浮点数，处理空值"""
    if not value or value.strip() == '':
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def parse_csv_stocks(filepath, v2_filter=False):
    """解析候选股票 CSV - 新版格式（支持 V2.0 过滤）"""
    stocks = []
    if not filepath or not os.path.exists(filepath):
        return stocks
    
    print(f"📄 读取文件：{filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) < 2:
            print("⚠️  文件行数不足")
            return stocks
        
        # 新版 CSV 列：code,name,price,change_pct,volume_ratio,market_cap,roe,pe_ttm,pe_static,pb,pe_status,turnover_rate,ma20,ma60,ma20_prev,ma20_trend,macd,tech_status
        for i, line in enumerate(lines[1:], 2):
            parts = line.strip().split(',')
            if len(parts) >= 17:
                code = parts[0]
                name = parts[1]
                price = parts[2]
                change_pct = safe_float(parts[3])
                volume_ratio = parts[4]
                roe = parts[6]
                ma20_trend = parts[15]
                macd = parts[16]
                tech_status = parts[17] if len(parts) > 17 else ""
                
                # V2.0 过滤：排除涨幅>5%
                if v2_filter and change_pct > 5.0:
                    print(f"  ❌ 排除 {code} {name} (+{change_pct}%)")
                    continue
                
                # 安全转换数值
                roe_val = safe_float(roe)
                macd_val = safe_float(macd)
                volume_ratio_val = safe_float(volume_ratio)
                
                # 生成入选理由
                reasons = []
                if roe_val > 30:
                    reasons.append(f"ROE {roe}%")
                elif roe_val > 20:
                    reasons.append(f"ROE {roe}%")
                if ma20_trend == "向上":
                    reasons.append("均线多头")
                if macd_val > 0.5:
                    reasons.append("MACD 强势")
                elif macd_val > 0:
                    reasons.append("MACD 金叉")
                if volume_ratio_val > 3:
                    reasons.append(f"放量{volume_ratio}倍")
                
                reason = " | ".join(reasons) if reasons else tech_status
                
                stocks.append({
                    'code': code,
                    'name': name,
                    'price': price,
                    'change': str(change_pct),  # 转为字符串，避免前端类型错误
                    'volume': volume_ratio,
                    'reason': reason
                })
    return stocks


def main():
    """主函数"""
    import sys
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    date_file = today.strftime("%Y%m%d")
    
    # 检查是否使用 V2.0 过滤
    v2_filter = '--v2' in sys.argv
    
    # 获取最新文件（优先 V2.0 文件）
    if v2_filter:
        stocks_file = get_latest_file(f"candidate_stocks_{date_file}_v2.csv")
    else:
        stocks_file = get_latest_file(f"candidate_stocks_{date_file}.csv")
    
    if not stocks_file:
        yesterday = today - timedelta(days=1)
        date_file = yesterday.strftime("%Y%m%d")
        if v2_filter:
            stocks_file = get_latest_file(f"candidate_stocks_{date_file}_v2.csv")
        else:
            stocks_file = get_latest_file(f"candidate_stocks_{date_file}.csv")
        date_str = yesterday.strftime("%Y-%m-%d")
    
    # 解析数据（V2.0 过滤）
    stocks = parse_csv_stocks(stocks_file, v2_filter=v2_filter)
    
    # 创建数据目录
    os.makedirs(PUBLIC_DATA_DIR, exist_ok=True)
    os.makedirs(DIST_DATA_DIR, exist_ok=True)
    
    # 生成 JSON
    data = {
        'date': date_str,
        'count': len(stocks),
        'stocks': stocks,
        'version': 'V2.0' if v2_filter else 'V1.0'
    }
    
    # 同时写入 public/data 和 dist/data
    with open(OUTPUT_JSON_PUBLIC, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(OUTPUT_JSON_DIST, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    version_str = "V2.0" if v2_filter else "V1.0"
    print(f"✅ 数据已生成：{OUTPUT_JSON_PUBLIC}")
    print(f"✅ 数据已生成：{OUTPUT_JSON_DIST}")
    print(f"📅 数据日期：{date_str}")
    print(f"📊 候选股票：{len(stocks)}只 ({version_str})")
    
    return 0


if __name__ == "__main__":
    exit(main())
