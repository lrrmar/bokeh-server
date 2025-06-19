#!/bin/bash

sed -i '1s/^"//g' $1 
sed -i '$s/"$//g' $1 
sed -i 's/\\n/\n/g' $1
sed -i 's/\\"/"/g' $1
