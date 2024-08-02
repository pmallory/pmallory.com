import argparse
import glob
import os
import subprocess


# the string to be output
output = """title:
date: YYYY-MM-DD 00:00:00
Category:

"""

#each image will have these tags addes to output
img_template = """<a href="{}"><img src="{}" alt="" class="center" loading="lazy" /></a>
<p></p>

"""

#get directory of images from arg, cd to it
parser = argparse.ArgumentParser(
        prog="galerypost",
        description="Run this program with a directory full of images as its input and it'll give you markdown output for a gallery page with minified thumbnails")
parser.add_argument('dirname')
args = parser.parse_args()
os.chdir(args.dirname)

# for every jpg, add the img_template string to the output
for filename in sorted(glob.glob("*.jpg")):
    if not filename.startswith("small-"):
        output += img_template.format(args.dirname+filename, args.dirname+"small-"+filename)

#make thumbnail sized images with imagemagick
subprocess.Popen("bash -O extglob -c 'for f in !(small-*).jpg;  do   convert $f -resize '640x640' \"small-$f\";  done'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()

# this doesn't wotk b/c extglob isn't enabled, the uglier thing above works
#subprocess.run("for f in !(small-*).jpg;  do   convert $f -resize '640x640' \"small-$f\";  done", shell=True, executable="/bin/bash")

print(output)
