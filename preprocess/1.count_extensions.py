#!/bin/env python

from collections import OrderedDict
import matplotlib.pylab as plt
import pickle
import sys
import numpy

# I get frustrated sometimes seeing all these "one line to test, trained classifier
# and you're done! tutorials on the internet. Why? Mostly because I don't like
# black boxes. When I started learning methods for machine learning, my program
# had us implement them from scratch. It was hard, but it was satisfying because
# you really understood what was going on. Then years later packages were
# easy to use that would let you do this in one line. The problem? We have all
# these "learn data science!" courses that jump over the details and just give
# you the one liner. This is like choosing the destination over the journey.
# I can spend an entire day looking at just counts of things, whereas someone
# might skip over this all together. My response of course is to do data analysis,
# but do it my way :) Slow, stupid, and simple.

################################################################################

# Step 0: Count Extensions

# This script will test if we can use deep learning to classify images
# based on extension. I actually first started by attempting to split my data
# into test and training, but quickly realized that I would run out of memory
# to just try and load everything. Thus I would need to do some kind of 
# "feed and train" strategy, but now we face another problem! I don't know,
# a priorii, the number of extensions (or obviously what they are) and
# this would be essential to assemble my vector of train and test labels
# as I go. So I stepped back, and instead did this first step to
# just COUNT the extensions. For this first portion, I would want to:
#   1. create a dictionary lookup by extension, and count
#   2. plot/visualize the counts to understand the distributions
# I would expect there to be MANY file "extensions" that aren't even extensions,
# and a subset of files without extensions (e.g., README) that are also
# meaningful to classify.

from helpers.load import ( recursive_find, load_all, load_by_extension )

data_base = sys.argv[1]
# data_base = '/tmp/data'
# data_base = '/scratch/users/vsochat/WORK/zenodo-ml'

ext_counts = dict()
count = 0

for image_pkl in recursive_find(data_base, 'images_*.pkl'):

    # within extensions
    try:
        images = load_by_extension(image_pkl)
    except:
         print('Error loading %s!' %image_pkl)
         continue

    for ext, imageset in images.items():
    
        # If we don't have a label yet for ext
        if ext not in ext_counts:
            ext_counts[ext] = imageset.shape[0]
        else:
            ext_counts[ext]+= imageset.shape[0]
        
    count+=1
    print('Load %s, %s extensions' %(count, len(ext_counts)))

# Save extensions
pickle.dump(ext_counts, open('extension_counts.pkl','wb'))
# ext_counts = pickle.load(open('extension_counts.pkl','rb'))

# I had originally wanted to just "plot them all" but the total extensions was 
# almost 20K, and there was no way this would work or be meaningful. I needed
# to realize what was important wasn't the many extensions with a small
# number of files (at least to start) but rather the top ones. I decided to
# first try removing the extensions with count less than 100.

def filter_by_value(d, value=100, plot=True):
    filtered = {k:v for k,v in d.items() if v > value}
    print('Original extension counts filtered from %s down to %s' %(len(d),
                                                                    len(filtered)))
    return filtered


def filter_and_plot(d, value=100, title=None):
    if title is None:
        title = "Proportion of Code by Extension Type, > %s samples" %value
    filtered = filter_by_value(d, value=value)
    plt.hist(list(filtered.values()), bins=10)
    plt.title(title)
    plt.show()
    return filtered


filter_and_plot(ext_counts)
# Original extension counts filtered from 19926 down to 1077

filtered = filter_and_plot(ext_counts, value=10000)
# Original extension counts filtered from 19926 down to 57

# The second plot is more reasonable - it shows us that the maximum number of
# samples for an extension is over 400,000, and that most of the upper range
# of counts (~33 extensions) fall between having 0 and 100K samples. When
# we do this, we are left with 57 extensions! So how about we filter to
# 60 total to get a reasonable set from 0 to the max?

# The fact that there are SO many files with "niche extensions" tells me two 
# things. For the niche extensions as a result of "niche langauges," we 
# probably can say this is meaningful and reflects less popular langauges/
# extensions / data format files. For the niche extensions that people
# just make up, well this teaches us that people don't understand 
# the purpose of file extensions :) I suppose they are meaningful to them?

# Now that we've cut the data to a reasonable working size, let's look
# at the actual extensions! First we need a function to sort a dictionary,
# so the plot can be sorted.

def sort_dict(d, reverse=True):
    return [(k,v) for v,k in sorted([(v,k) for k,v in d.items()],reverse=reverse)]

sorted_counts = sort_dict(filtered)
x,y = zip(*sorted_counts)

# Plot the result
pos = numpy.arange(len(x))
plt.bar(pos,y,color='g')
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(x)

# Rotate
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

# Finishing up Counting - visualize counts and discuss!

plt.title("Top %s extensions, ordered by total samples across ~10K repositories." %len(x))
plt.show()


# Here is my early thinking about this result. First, these are definitely
# somewhat scientific code repositories, because we see csv and json in the top
# results. Sure, they could be csv/json for general data for some Windows
# user to load in excel, but I think it's more unlikely that a non-programmer
# is going out of his or her way to use version control. The second hint is that
# the fourth top language is python. We don't see R until waaay down in the list.
# I think this likely reflects the fact that, despite what the internet says,
# python is a lot more utilized for *other things* (web applications, etc.)
# whereas R is a very niche data science programming that just touches into
# webby things with Shiny. Is there a way we could possible untangle these two
# things, to look at Python for data science vs. Python for web applications?
# Likely yes, if we look at co-occurence of extensions within a repository 
# (I just added this to our TODO list).

# I am REALLY surprised that .gif are the number one file. I had thought about
# nixing true images (e.g., gif, png, bmp, etc.) from the analysis, but don't
# think this is fair to do. From this I would guess there are sites that host
# gif that are using Github to store their data. Just a guess, I would need
# to look at the repos :)

# OHMYGOD don't even get me started about the DS_STORE. I had labmates in the
# past who would not use Github reposibily. Aka, they did this:
# git add *
# And now their nasty Mac datastore files are cluttered in all these repos. 
# Seriously, gross! If you wanted to find repositories with files that shouldn't
# be there, just use the DS_STORE as a signature for "I added things 
# irresponsibly."

# I am happy to see that c and h files both appeared in the top, and in almost
# equal proportions. This also makes sense. Java is also another leader, although
# not as high up as Python :)

# I am also happy to see a high prevalence of markdown (.md) and LICENSE files,
# and maybe a bit disappointed that README didn't make the top. Is it the case
# that README is in there, but not properly counted because of differences in
# extension? Possibly, for example, we could have had README.md, README.txt, and
# README (without extension) and the first two would be reflected in ".txt" and
# ".md." Actually, I'd say a bit portion of the .txt are from README files.
# We should break this down later since it's the most populat extension (TODO)

################################################################################

## Step 2: Load the text files and determine what the files are called.

from helpers.load import load_by_regexp

txt_counts = dict()
count = 0

for image_pkl in recursive_find(data_base, 'images_*.pkl'):

    # find those with .txt
    try:
        images = load_by_regexp(image_pkl, regexp='[.]txt$')
    except:
         print('Error loading %s!' %image_pkl)
         continue

    for ext, imageset in images.items():
    
        print('Adding %s' %ext)
        # If we don't have a label yet for ext
        if ext not in txt_counts:
            txt_counts[ext] = imageset.shape[0]
        else:
            txt_counts[ext] += imageset.shape[0]
        
    count+=1
    print('Load %s, %s unique txt files' %(count, len(txt_counts)))


# Again, let's look at the distribution for the top .txt files.

title = "Breakdown of .txt file extension, sample count > 1000"
filtered = filter_and_plot(txt_counts, value=1000, title=title)

# The plot isn't super meaningful, but it narrows down our set to the top
# 34 files names so we can look at them! 

sorted_counts = sort_dict(filtered)
x,y = zip(*sorted_counts)

# Plot the result
pos = numpy.arange(len(x))
plt.bar(pos,y,color='g')
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(x)

# Rotate
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

# Finishing up Counting - visualize counts and discuss!

plt.title("Breakdown of top %s with .txt extension by total samples across ~10K repositories." %len(x))
plt.show()

# Make loglog plot and say it's zipfy
