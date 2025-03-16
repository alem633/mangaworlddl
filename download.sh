#!/bin/bash
counter=1

if [ $# -eq 0 ]; then
    echo "no arguments"
    echo "usage: $0 [manga link] [optional pdf name]"
    exit 1
fi

make

./mangaworlddl $1
rm -rf download
mkdir download

while IFS= read -r url; do
    wget -O "download/$counter.png" "$url"
    ((counter++))
done < output.txt

make clean

if [ -n "$2" ]; then
    cd download
    sorted_files=$(ls -v *.png)  
    magick $sorted_files "$2"   
    rm *.png
    cd ..
fi

