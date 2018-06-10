# Analyses for Zenodo-ML

 0. Do the words in the scripts follow a pareto principle, both across scripts and within languages, and within extensions.
 1. Can we classify the language or extension based on the images using deep learning.
 2. Can we identify software that are provided as packages on various managers (e.g., MANIFEST.in setup.py indicates python)
 3. Is there a signature of software that is associated with tags for the software?
 4. Is there a signature of software that can be used to predict any kind of metadata field?

Once we have signatures for software above...

 5. Can we identify software in containers?
 6. What software groups are commonly found together? (Why might that be?)
 7. What are the most / least used software (published in Zenodo)
 8. Can we use the classified software groups to classify the containers (and organize / index)

Questions  prompted by the above

 1. I noticed that Python is way ahead of R, and I'm wondering if we can use co-occurence to untangle "python for data science" vs. "python for webby thing"
 2. Where are all the gifs? Is it one / few really big repos or generally across? As a follow up, for the leading script counts, which ones are most evenly distributed vs. just overly represented by a few HUGE repos?
 3. Break down .txt files - is there common ones there?
