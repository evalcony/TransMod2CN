#!/bin/bash

FILENAME=$1

# ------------------- 获取 namespace
# 读取配置文件
conf_file="appconf.ini"

# 获取行号
line_num=$(grep -n "namespace =" "$conf_file" | cut -d ":" -f 1)

# 读取指定行
line=$(sed -n "$line_num"p "$conf_file")

# 获取`=`后面的内容
namespace=$(echo "$line" | cut -d "=" -f 2)

# 输出结果
echo "namespace: $namespace"

NAMESPACE=$namespace

# ---------------- 处理相关文件

cp resource/$NAMESPACE/v10/$FILENAME resource/$NAMESPACE/comp/_$FILENAME
cp resource/$NAMESPACE/output/$FILENAME resource/$NAMESPACE/comp/$FILENAME

cd tools

python3 file_compare.py -f1 'comp/'$FILENAME -f2 'comp/_'$FILENAME > tsu_comp.txt

subl tsu_comp.txt

cd ..

subl resource/$NAMESPACE/output/$FILENAME

subl resource/$NAMESPACE/v10/$FILENAME

subl resource/$NAMESPACE/tra/$FILENAME