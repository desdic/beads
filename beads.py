#!/usr/bin/env python

import sys, time, getopt, math
from PIL import Image, ImageFilter, ImageDraw
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from datetime import timedelta
from multiprocessing import Pool
import multiprocessing
#, Process

__version__ = 2.0

class grid():
    def __init__(self, region, box, xgrid=16,ygrid=16,fastcolor=True, beadlist={}):
        self.region = region
        self.box = box
        self.fastcolor=fastcolor
        self.beadlist=beadlist
        self.xgrid = xgrid
        self.ygrid = ygrid
        self.color = (0,0,0)

""" help """
def help():
    print "Beads version %s" % __version__
    print "Option:"
    print "-h\t this help"
    print "-q\t be quiet and do not display progress"
    print "-f\t Use a fast way to find the best suited bead. Only used when using a list of beadcolors"
    print "-i\t Specify a input file"
    print "-x\t Set xgrid facter. Default set to 16"
    print "-y\t Set ygrid facter. Default set to 16"
    print "-b\t Specify a input file for beadcolors"
    print "-o\t Output file for final product"
    print "-m\t Mode. Default drawing is a box but if you add beads it will draw with beads"
    print "-c\t background color. Default is 0,0,0 (Black)"
    print "-n\t Number of CPUs to use. Default is all of them"
    print "\nExample: ./beads.py -i donald.jpg -b hama.txt -f -o donald_hama.jpg"
    sys.exit(0)

""" Fast but inaccurate way to find the distance between 2 colors """
def colordistance(color1, color2):
    return abs( color1[0] - color2[0] ) + abs( color1[1] - color2[1] ) + abs ( color1[2] - color2[2] )

def worker(gridwork):
    ret = []

    predefinedcolors = False
    if len(gridwork.beadlist):
        predefinedcolors = True

    ravg, gavg, bavg = 0, 0, 0
    blockpixels = gridwork.xgrid*gridwork.ygrid
    offset=0
    for y in range(0,gridwork.ygrid):
        for x in range(0,gridwork.xgrid):
            travg, tgavg, tbavg = gridwork.region[offset]
            ravg+=travg
            gavg+=tgavg
            bavg+=tbavg
            offset+=1

    nr, ng, nb = (ravg/blockpixels), (gavg/blockpixels), (bavg/blockpixels)
    if predefinedcolors:
        index = gridwork.beadlist.keys()[0]
        if gridwork.fastcolor:
            closest = colordistance((nr, ng, nb), (gridwork.beadlist[index][0], gridwork.beadlist[index][1], gridwork.beadlist[index][2]))
        else:
            rgblab = convert_color(sRGBColor( nr, ng, nb), LabColor)
            closest = delta_e_cie2000(rgblab, convert_color(sRGBColor( gridwork.beadlist[index][0], gridwork.beadlist[index][1], gridwork.beadlist[index][2] ), LabColor))

        for key in gridwork.beadlist:
            hr = gridwork.beadlist[key][0]
            hg = gridwork.beadlist[key][1]
            hb = gridwork.beadlist[key][2]

            if fastcolor:
                delta = colordistance((nr, ng, nb), (hr, hg, hb))
            else:
                beadlab = convert_color(sRGBColor( hr, hg, hb ), LabColor)
                delta = delta_e_cie2000(rgblab, beadlab)

            if delta < closest:
                index = key
                closest = delta

        nr, ng, nb = gridwork.beadlist[index][0], gridwork.beadlist[index][1], gridwork.beadlist[index][2]

    gridwork.color = (nr, ng, nb)
    ret.append((gridwork.color,gridwork.box))
    return ret
    

def main(image,bgcolor,xgrid,ygrid,fastcolor,beadlist,numworkers=4,mode='box',output=''):
    
    origimage = Image.open(image)
    if origimage.mode!='RGB':
        print "Mode: %s not supported" % (origimage.mode)
        sys.exit(1)

    """ Convert to 256 colors and back to 24bit to get the RGB values """
    convertedimage = origimage.convert('P', palette=Image.ADAPTIVE).convert('RGB')

    """ Image but be divideable with xgrid/ygrid """
    optimalx = int(origimage.width/xgrid)*xgrid
    optimaly = int(origimage.height/ygrid)*ygrid
    pegboard = Image.new(origimage.mode, (optimalx,optimaly), bgcolor)

    jobqueue = []

    ystart = 0
    blocks = 0
    for y in xrange(0,optimaly,ygrid):
        xstart = 0
        for x in xrange(0,optimalx,xgrid):
            box = (x, y, x+xgrid, y+ygrid)
            region = convertedimage.crop(box)

            job = grid(list(region.getdata()), box, xgrid, ygrid, fastcolor, beadlist)

            jobqueue.append(job)

    pool = Pool(processes=numworkers)
    result = pool.map(worker, jobqueue)

    for x in result:
        color = x[0][0]
        box = x[0][1]
        regionout = Image.new(convertedimage.mode, (xgrid,ygrid), bgcolor)

        if mode=='beads':
            d = ImageDraw.Draw(regionout)
            r=0
            d.ellipse((0-r, 0-r, xgrid+r, ygrid+r), fill=color)
            r=-1*(math.sqrt(xgrid*2))
            d.ellipse((0-r, 0-r, xgrid+r, ygrid+r), fill=bgcolor)
        else:
            for yr in xrange(0,ygrid):
                for xr in xrange(0,xgrid):
                    regionout.putpixel((xr,yr),color)

        pegboard.paste(regionout, box)


    if mode!='beads':
        d = ImageDraw.Draw(pegboard)
        for y in xrange(0,pegboard.height,ygrid):
            for x in xrange(0,pegboard.width,xgrid):
                d.line((x,y,pegboard.height,y),fill=bgcolor)
                d.line((x,0,x,pegboard.height),fill=bgcolor)
        d.line((pegboard.width-1,0,pegboard.width-1,pegboard.height),fill=bgcolor)

    if output=='':
        pegboard.show()
    else:
        if output!=image:
            pegboard.save(output)

if __name__ == "__main__":

    xgrid, ygrid = 16, 16
    image = ''
    output = ''
    bgcolor = (0,0,0)
    bgcolortmp = ''
    progress = True
    fastcolor = False
    beadsfile = ''
    mode = 'box'
    numworkers = multiprocessing.cpu_count()
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv,"hqfi:x:y:b:o:m:c:n:",[])
    for opt, arg in opts:
        if opt =='-h':
            help()
        if opt in ('-q'):
            progress = False
        if opt in ('-x'):
            xgrid = int(arg)
        if opt in ('-y'):
            ygrid = int(arg)
        if opt in ('-f'):
            fastcolor = True
        if opt in ('-b'):
            beadsfile = arg
        if opt in ('-i'):
            image = arg
        if opt in ('-m'):
            mode = arg
        if opt in ('-n'):
            numworkers = int(arg)
        if opt in ('-c'):
            bgcolortmp = arg
            tmp = bgcolortmp.split(',')
            bgcolor = (int(tmp[0]), int(tmp[1]), int(tmp[2]))
        if opt in ('-o'):
            output = arg

    if beadsfile=='':
        beadslist = {}
    else:
        beadslist = eval(open(beadsfile).read())

    if image=='':
        print "No input image specified\n"
        help()

    main(image,bgcolor,xgrid,ygrid,fastcolor,beadslist,numworkers,mode,output)

