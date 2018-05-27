# Zenodo ML

Software, whether compiled or not, is a collection of scripts. A script is a stack of lines,
and you might be tempted to relate it to a document or page in book. Actually, I think
we can conceptualize scripts more like images. A script is like an image in that it is a grid
of pixels, each of which has some pixel value. In medical imaging we may think of these
values in some range of grayscale, and with any kind of photograph we might imagine having
different color channels. A script is no different - the empty spaces are akin to values of zero,
and the various characters akin to different pixel values. While it might be tempting to use
methods like Word2Vec to assess code in terms of lines, I believe that the larger context of the
previous and next lines are important too. Thus, my specific aims are the following:

## Input Data
First I will

> identify a corpus of scripts and metadata

Zenodo, specifically the "software" bucket, is ideal for this case. From this database
I can extract about 10,000 software records, most of which are linked to a Github repository
and carry various amounts of metadata (from keywords to entire manuscript publications).

## Preprocessing
Then I will preprocess this data, meaning download of the repository, reading of the script files,
and representation of each file as an image. We will need to have equivalent dimensions regardless
of the language, and so I am not sure yet if I will want to "crop" the scripts in some manner,
or segment them into smaller pieces first.

## Relationship Extraction
The relationship (how two files are related to one another) in terms of location in the repository
might be meaningful, and so I will want to extract features related to this.

## Deep Learning
I want to give a go at using convolutional neural networks to generate features of the scripts.
I'm not experienced in doing this so I don't know what kinds of questions / analyses I'd like to try
until I dig in a bit.

# Goals

## Software Development
Here are some early goals that I think this work could help:

 - **comparison of software**: it follows logically that if we can make an association between features of software and some meaningful metadata tag, we can take unlabeled code and better organize it.
 - **comparison of containers**: in that our "unit of understanding" is not an entire container, if we are able to identify features of software, and then identify groups of software in containers, we can again better label the purpose / domain of the contianer.
 - **optimized / automated script generation**: If we have features of software, the next step is to make an association between features and what constitutes "good" software. For example, if I can measure the resource usage or system calls of a particular piece of software and I also can extract (humanly interpretable) features about it, I can use this information to make predictions about other software without using it.

## Personal
I'm getting a little bored with containers, and even more bored with the current obsession around AI and scaled nonsense. I want to do something different and fun that could be impactful, and at least keep myself busy :)
