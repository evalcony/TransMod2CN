#!/bin/bash

echo '创建 tra/'
mkdir tra

echo '创建 output/'
mkdir output

echo '拷贝 appconf_demo.int 到 appconf.ini'
cp appconf_demo.ini appconf.ini

echo '删除并创建 readlogs.txxt'
del readlogs.txt
touch readlogs.txt

echo '脚本执行结束'