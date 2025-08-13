#!/bin/bash
WATCH_DIR="/www/wwwroot/qinag.fun" # 替换为你的Nginx根目录
SCRIPT_PATH="/www/wwwroot/qinag.fun/update_index.py" # 替换为你的脚本路径

inotifywait -m -r -e create,delete,modify,move "$WATCH_DIR" | while read -r directory events filename; do
# 只处理HTML文件和目录变化
if [[ "$filename" == *.html || -d "$directory$filename" ]]; then
echo "检测到变化，更新索引..."
python "$SCRIPT_PATH"
fi
done
