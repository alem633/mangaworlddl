#!/bin/bash
counter=1

if [ $# -eq 0 ]; then
 echo "no arguments"
 exit 1
fi

make

./mangaworlddl $1
rm -rf download
mkdir download

while IFS= read -r url; do
    aria2c -o "download/$counter.png" "$url"
    ((counter++))
done < output.txt

make clean