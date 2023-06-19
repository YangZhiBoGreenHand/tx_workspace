#!/bin/bash


Y='\033[1;33m' # yellow color
N='\033[0m' # No Color

echo -e "${Y}Runnning autopep8...${N}"

# 搜索当前目录下除了 env 目录以外的所有 .py 文件，并使用 autopep8 工具进行格式化
find . -path ./venv -prune -o -type f -name "*.py" -exec autopep8 --in-place --aggressive --aggressive {} \;

echo -e "${Y}Runnning isort...${N}"
isort -w 120 -m 2 ./app/**/*.py ./scripts/*.py