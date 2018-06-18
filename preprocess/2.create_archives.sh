#!/bin/bash

mkdir -p $PWD/ARCHIVE
for ext in $(ls $PWD) 
    do
       if [ "${ext}" != "ARCHIVE" ]; then
           echo "Creating Archive for ${ext}..."
           tar -zcf $PWD/ARCHIVE/$ext.tar.gz ${ext}
       fi
done
