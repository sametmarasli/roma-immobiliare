#!/bin/bash

for filename in $(ls blocks)
do  
 if echo $filename | grep -q block
 then
    echo $filename
    python blocks/$filename
fi
done

