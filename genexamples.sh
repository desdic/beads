#!/bin/bash

./beads.py -i images/donald.jpg -o images/donald_all.jpg
./beads.py -i images/donald.jpg -x 8 -y 8 -o images/donald_all8x8.jpg
./beads.py -i images/donald.jpg -m beads -o images/donald_allbeads.jpg
./beads.py -i images/donald.jpg -b beads/hama.txt -o images/donald_hama.jpg
./beads.py -i images/donald.jpg -b beads/hama.txt -f -o images/donald_hamafast.jpg
./beads.py -i images/donald.jpg -b beads/multiplebeads.txt -f -o images/donald_multifast.jpg
