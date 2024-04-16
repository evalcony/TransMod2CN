#!/bin/bash

# 提示用户输入namespace
echo "输入namespace。若无则直接按回车(enter)"

# 读取用户输入
read NAMESPACE

# resource 目录
if [ ! -d resource ]; then
    mkdir resource
fi

cd resource

# 判断用户输入参数
if [ -n "$NAMESPACE" ]; then
  # 用户输入不为空，则存入NAMESPACE变量中
  echo "创建namespace目录：$NAMESPACE"
  mkdir "$NAMESPACE"

  # 进入namespace目录
  cd "$NAMESPACE"
fi

echo '创建 tra/'
mkdir tra

echo '创建 output/'
mkdir output

echo '创建 temp_dir/'
mkdir temp_dir

echo '删除并创建 readlog.txt'
rm -rf readlog.txt
touch readlog.txt

if [ -n "$NAMESPACE" ]; then
  cd ..
fi

cd ..

# 指定要追加的内容
APPEND=$NAMESPACE
echo 'APPEND='$NAMESPACE

# 指定要修改的文件
FILE=appconf_demo.ini

# 使用 sed 命令更新目标行内容
sed -e 's/namespace=/namespace='$APPEND'/g' $FILE > appconf.ini

echo '生成appconf.ini'

echo '脚本执行结束'