# Beads

It started out when my daughter and I was playing with Hama beads (http://www.hama.dk). I wanted to create some better and more funny pegboards. So I created this little program to convert a 24bit image to a pegboard. I have seen a few on the internet but all of them assume that you have all the beads in every color. So I have created a version where you can specify a list of the beads that you and your kid have.

I have add 2 color list of beads that I have found online. Unfortunately I haven't been able to get a list of RGB values from Hama.

# Requirements

In order for this to work you have to install Pillow (Fork of PIL) and Colormath

```
pip install pillow
pip install colormath
```

# Examples

## Original image:
![alt text][orig]

## Created using: ./beads.py -i images/donald.jpg -o images/donald_all.jpg
![alt text][all]

## Created using: ./beads.py -i images/donald.jpg -o images/donald_all8x8.jpg
![alt text][all8]

## Created using: ./beads.py -i images/donald.jpg -b beads/hama.txt -o images/donald_hama.jpg
![alt text][hama]

## Created using: ./beads.py -i images/donald.jpg -b beads/hama.txt -f -o images/donald_hamafast.jpg
![alt text][hamafast]

## Created using: ./beads.py -i images/donald.jpg -b beads/multiplebeads.txt -f -o images/donald_multifast.jpg
![alt text][multi]


[orig]: images/donald.jpg "Original image"
[all]: images/donald_all.jpg "Converted image using all colors"
[all8]: images/donald_all.jpg "Converted image using all colors but with a 8x8 grid"
[hama]: images/donald_hama.jpg "Converted image using hama colors"
[hamafast]: images/donald_hamafast.jpg "Converted image using hama colors with fast color match"
[multi]: images/donald_multifast.jpg "Converted image using multiple colors with fast color match"
