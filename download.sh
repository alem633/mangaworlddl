#!/bin/bash
counter=1

while IFS= read -r url; do
    aria2c -o "$counter.png" "$url"
    ((counter++))
done < output.txt

