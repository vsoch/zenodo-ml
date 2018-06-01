# Zenodo ML

This is a part of the [Dinosaur Dataset](https://vsoch.github.io/datasets) series. I'll parse a dataset for you to use, show you
how to use it, and you can do awesome research with it. Instructions for use are below, and
see the section on Questions if you are looking for ideas of what to do with it.

 - [Generation](#generation): is how I produced the dataset. You can skip it if you just want to use it.
 - [Usage](#usage): is likely what you are interseted in, how to use the dataset.


## Assumptions

 1. We use an "image size" of 80 by 80, under the assumption that the typical editor / programming language prefers lines of max length 80 (see Python's Pep8 specification) and most machine learning algorithms prefer square images.
 2. We filter the files down to those less than or equal to 100,000 bytes (100KB --> 0.1 MB). This still leads to having on the order of a few thousand images (each 80x80) for one small script.
 3. We filter down the Zenodo repos to the first 10K within the set of the bucket called "software."
 4. I filtered out repos that (were strangely common) related to something to do with "gcube."
 5. We take a greedy approach in parsing files - in the case that a single file produces some special error, we pass it in favor of continued processing of the rest.


## Generation

To generate the dataset, the entire code is provided in a Docker container. If you don't
want to use the version on Docker Hub, you can build it locally.

```bash
docker build -t vanessa/zenodo-ml .
singularity pull --name zenodo-ml docker://vanessa/zenodo-ml
```

### Sherlock at Stanford

```bash
module load singularity
singularity pull --name zenodo-ml docker://vanessa/zenodo-ml
mkdir -p $SCRATCH/zenodo-ml && cd $SCRATCH/zenodo-ml
mv /scratch/users/vsochat/.singularity/zenodo-ml $SCRATCH/zenodo-ml/
```

Now you have a container binary called `zenodo-ml` in your `$SCRATCH/zenodo-ml` folder.


### Download from Zenodo

**optional**

The first step is to produce a file called "records.pkl" that should contain about 10K
different records from the Zenodo API. You should [create an API key](https://zenodo.org/account/settings/applications/tokens/new/), save the key to a file called `.secrets` in the directory you are going to run
the container, and then run the container and map your present working directory to it. 
That looks like this:

```bash
docker run -v $PWD:/code -it vanessa/zenodo-ml exec python /code/0.download_records.py
```

You don't actually need to do this, because the `records.pkl` is already provided in the container.

### Parse Records

**optional**

Once you have the `records.pkl` you can load them in for parsing! This will generate a data
folder in your present working directory with subfolders, each corresponding to a Zenodo identifier.

```bash
docker run -v $PWD:/data -it vanessa/zenodo-ml python /code/1.parse_records.py
singularity exec zenodo-ml python /code/1.parse_records.py
```

### Loading Data
Let's take a look at the contents of one of the subfolders under folder:

```bash
tree data/1065022/
    metadata_1065022.pkl    
    images_1065022.pkl    
```

The filenames speak for themselves! Each is a python pickle, which means that you can
load them with `pickle` in Python. The file `images_*.pkl` contains a dictionary data structure
with keys as files in the repository, and each index into the array is a list of file segments.
A file segment is an 80x80 section of the file (the key) that has had it's characters converted
to ordinal. You do this in Python as follows:

```python
#  Character to Ordinal (number)
char = 'a'
number = ord(char)
print(number)
97

# Ordinal back to character
chr(number)
'a'
```

#### Images
Here is how you would load and look at an image.

```python
import pickle

image_pkl = os.path.abspath('data/1065022/images_1065022.pkl')
images = pickle.load(open(image_pkl, 'rb'))
```

Remember, this entire pickle is for just one repository that is found in a record from Zenodo! If you
look at the images "keys" you will see that each one corresponds to a file in the repository.

```python
images.keys()
```

It follows, then, that if we index images for a particular key, we are going to find images! Specifically,
we will find a giant list of 80x80 images, where each image is a 2D numpy array with characters converted
to ordinal (as we showed above).

**more coming soon!**

## Analysis Ideas

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

