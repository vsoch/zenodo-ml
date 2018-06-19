#!/bin/bash

for ext in $(ls $PWD) 
    do
       if [ "${ext}" != "ARCHIVE" ]; then
          count=$(find "${ext}" -type f -name *.png | wc -l)
          echo "Extension ${ext} has ${count} png image files" 
       fi
done

# Extension c has 174777 png image files
# Extension cc has 58104 png image files
# Extension cpp has 177850 png image files
# Extension cs has 30310 png image files
# Extension css has 79386 png image files
# Extension csv has 231612 png image files
# Extension cxx has 34280 png image files
# Extension data has 389398 png image files
# Extension f90 has 91652 png image files
# Extension go has 52204 png image files
# Extension html has 208349 png image files
# Extension java has 249181 png image files
# Extension js has 398383 png image files
# Extension json has 298246 png image files
# Extension m has 80262 png image files
# Extension map has 171895 png image files
# Extension md has 49654 png image files
# Extension txt has 450363 png image files
# Extension xml has 190485 png image files

total=$(find "." -type f -name *.png | wc -l)
echo "Total of ${total} png images."

# Total of 3416391 png images
