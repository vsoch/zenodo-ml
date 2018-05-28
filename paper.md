# Zenodo ML: Dataset for Derivation of Software Similarity Metrics

Here we introduce Zenodo ML, a large dataset of XXX prepared code images from XXX code repositories referenced
on Github and available through the Zenodo application program interface (API). With this dataset, researchers can 
use machine learning to derive how features of software are associated with organizational and domain-specific metadata. It promises to allow for the development of models to automatically classify a piece of software based on the code alone, and use groupings of these classifications in the context of linux containers to address the problem of container curation, a currently unsolved problem. Each entry in the database is associated with a unique identifier in the Zenodo Database, and includes sets of 80x80 images organized by file name, metadata, and a Trie tree data structure that can be used for analyses that require understanding relationships between the various files. We provide the data in three formats that are ideal for loading into various machline learning packages, complete code for reproducing and updating the datasets, and detailed documentation for these components. Finally, BUILD A MODEL to show that... {ML WORK HERE}. We believe that this dataset and its provision will provide meaningful use for future researchers interested in assessment of software comparison for use cases from developing AI-driven operating systems to organization and comparison of software packages. To encourage this work, we have made all code and datasets publicly available at https://github.com/vsoch/zenodo-ml


# 1. Introduction
Machine learning, and specifically unsupervised deep learning, is an overwhelmingly popular modeling technique to gain insights from large datasets. Unfortunately, derivation and organization of these input data is often the most challenging and time intensive step before doing any kind of analysis. Further, this challenge is complicated by the lack of incentive structure to share data. While sharing of data is improving, there is largely little incentive to allocate time and resources toward just developing a high quality dataset for others to use. While individual researchers can conduct anlayses with personal datasets (http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0188511) to answer questions about software, a much better strategy is to release datasets for many more individuals to work on to scale discovery.s At the Stanford Research Computing Center (SRCC) we have recognized this challenge and are responding by allocating some of our development resources toward the development of datasets. Our goal is to provide preprocessed and organized data that is ready to go to answer some of the questions on the forefront of scientific computing for our users are the larger open source community.

# 2. Data
The dataset is primarily interested in published software, so Zenodo and it's application programming interface (API) were used as an entry point to discovery. Zenodo (https://www.zenodo.org) is an open source digital library that provides metadata and content about published code repositories in Github (https://www.github.com) under an open source CC0 license. With the Zenodo API, it's trivial to create a query to the API to get records with metadata and Github addresses to code repositories that have been granted a digital object identifier, a kind of "published" version, via the Zenodo service. To generate the dataset, we took the following approach:

 1. We queried the Zenodo API to filter down to the "software" bucket, returning records sorted by recency for submissions with software repositories. This resulted in just under 10,000 hits (N=9...X)
 2. For each hit, we downloaded the repository and versioned control via the Github url or compressed archive provided by Zenodo, if the Github link was not working.
 3. For each cloned respository, we derive an organizational tree, sets of 80x80 image matrices for machine learning, and metadata to provide to the researcher  

### 2.1 Code Images
We use an "image size" of 80 by 80, under the assumption that the typical editor / programming language prefers lines of max length 80 (see Python's Pep8 specification) and most machine learning algorithms prefer square images. We filter the files down to those less than or equal to 100,000 bytes (100KB --> 0.1 MB). This still leads to having on the order of a few thousand images (each 80x80) for one small script.  We take a greedy approach in parsing files - in the case that a single file produces some special error, we pass it in favor of continued processing of the rest. Complete code and instructions for preprocessing and reproducing this work is provided in the repository.

### 2.2 Container Tree
The organizational tree was derived with the ContainerTree {CITE @containertree} package. The data structure derives a set of nodes that stem from a common root (the repository base) each containing.

### 2.3 Metadata
A summary of metadata is included in Table 1.


### Table 1: Zenodo Metadata

| Key | Description |
|-----|-------------|

## 2.2 Preprocessing


## Assumptions

 4. I filtered out repos that (were strangely common) related to something to do with "gcube."
**DON'T DO THAT - Sherlock Can handle this (hopefully)**

## 2.3 Formats

# 3. Model

# 4. Discussion

# 5. Acknowledgements

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
