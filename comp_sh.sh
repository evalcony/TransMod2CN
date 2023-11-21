#!/bin/bash

FILENAME=$1

NAMESPACE=tsujatha

cp resource/$NAMESPACE/v10/$FILENAME resource/$NAMESPACE/comp/_$FILENAME
cp resource/$NAMESPACE/output/$FILENAME resource/$NAMESPACE/comp/$FILENAME

cd tools

python3 file_compare.py -f1 'comp/'$FILENAME -f2 'comp/_'$FILENAME > tsu_comp.txt

subl tsu_comp.txt

cd ..

subl resource/$NAMESPACE/output/$FILENAME

subl resource/$NAMESPACE/v10/$FILENAME

subl resource/$NAMESPACE/tra/$FILENAME