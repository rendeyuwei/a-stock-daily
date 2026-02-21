#!/bin/bash
# 每日报告更新脚本
# 由小豆自动执行

set -e

WORKSPACE="/home/rende/.openclaw/workspace"
REPO_DIR="/home/rende/a-stock-daily"
DATE=$(date +%Y-%m-%d)

echo "📅 生成每日报告：$DATE"

cd "$REPO_DIR"

# 1. 生成数据 JSON
python3 generate-data.py

# 2. 重新构建 Astro 项目
echo "🔨 构建静态站点..."
npm run build

# 3. 提交并推送
git add -A
git commit -m "daily: $DATE" || echo "No changes to commit"
git push

echo "✅ 报告已更新并推送"
