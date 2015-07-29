# Beads

It started out when my daughter and I was playing with Hama beads (http://www.hama.dk). I wanted to create some better and more funny pegboards. So I created this little program to convert a 24bit image to a pegboard. I have seen a few on the internet but all of them assume that you have all the beads in every color. So I have created a version where you can specify a list of the beads that you and your kid have.

I have added 2 color list of beads that I have found online. Unfortunately Hama does not have en RGB color codes needed to create a complete list.

# Requirements

The software is written using Python 2.7.x so of course Python is a requirement (Get it from python.org). The following libraries are also required: Pillow (Fork of PIL) and Colormath

```
pip install pillow
pip install colormath
```

# Examples

## Original image:
![alt text][orig]

## Created using: ./beads.py -i images/donald.jpg -o images/donald_all.jpg
![alt text][all]

## Created using: ./beads.py -i images/donald.jpg -x 8 -y 8 -o images/donald_all8x8.jpg
![alt text][all8]

## Created using: ./beads.py -i images/donald.jpg -m beads -o images/donald_allbeads.jpg
![alt text][allbeads]

## Created using: ./beads.py -i images/donald.jpg -b beads/hama.txt -o images/donald_hama.jpg
![alt text][hama]

## Created using: ./beads.py -i images/donald.jpg -b beads/hama.txt -f -o images/donald_hamafast.jpg
![alt text][hamafast]

## Created using: ./beads.py -i images/donald.jpg -b beads/multiplebeads.txt -f -o images/donald_multifast.jpg
![alt text][multi]


[orig]: images/donald.jpg "Original image"
[all]: images/donald_all.jpg "Converted image using all colors"
[all8]: images/donald_all8x8.jpg "Converted image using all colors but with a 8x8 grid"
[allbeads]: images/donald_allbeads.jpg "Converted image using all colors but showing the beads"
[hama]: images/donald_hama.jpg "Converted image using hama colors"
[hamafast]: images/donald_hamafast.jpg "Converted image using hama colors with fast color match"
[multi]: images/donald_multifast.jpg "Converted image using multiple colors with fast color match"

# TODO

Diplay the number beads for every color needed to create the pegboard

Add multiprocesser usage for faster processing
