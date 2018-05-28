# Zenodo ML

## Get an Interactive Node

```python
srun --mem 32000 --pty bash
```

Finally we continue! Let's load python.

## Load Dependencies

### Singularity
Load Singularity

```bash
module load singularity
```

Make sure it's loaded

```bash
which singularity
/share/software/user/open/singularity/2.4.6/bin/singularity
```

### Repository

The scripts are provided in the container, but since it's harder to rebuild and reupload the container (and easy
to pull the updated scripts we are working on) I'm going to clone the repository for this example.

```bash
git clone https://www.github.com/vsoch/zenodo-ml
```

### Container

This is a general pull example

```bash
singularity pull --name zenodo-ml docker://vanessa/zenodo-ml
```

This is for Sherlock at Stanford, used in these examples

```bash
singularity pull --name zenodo-ml docker://vanessa/zenodo-ml
mkdir -p $SCRATCH/zenodo-ml && cd $SCRATCH/zenodo-ml
mv /scratch/users/vsochat/.singularity/zenodo-ml $SCRATCH/zenodo-ml/
```

Now you have a container binary called `zenodo-ml` in your `$SCRATCH/zenodo-ml` folder.


## Download from Zenodo

**optional**

The first step is to produce a file called "records.pkl" that should contain about 10K
different records from the Zenodo API. You should [create an API key](https://zenodo.org/account/settings/applications/tokens/new/), save the key to a file called `.secrets` in the root zenodo-ml directory you are going to run
the container, and then run the container and map your present working directory to it. 
That looks like this:

```bash
CODE=$SCRATCH/zenodo-ml
PYTHONPATH= singularity exec --bind $CODE:/code zenodo-ml /opt/conda/bin/python /code/0.download_records.py
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=2&size=1000
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=3&size=1000
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=4&size=1000
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=5&size=1000
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=6&size=1000
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=7&size=1000
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=8&size=1000
...
Maximum number of results have been reached.
https://zenodo.org/api/records/?sort=mostrecent&type=software&page=10&size=1000
Maximum number of results have been reached.
Total of 9000 results.
```

We set the `PYTHONPATH` to be empty so that the python is isolated to the container. I can't predict what
you have on your local PYTHONPATH :)

## Slurm

Once we have our hits data, we want to work wit slurm, so let's go into the slurm folder.

```bash
cd $SCRATCH/zenodo-ml/slurm
```

## Submit Jobs
We could run a script in serial, but we are too impatient for this.

The basic idea is that the script [run.py](run.py) will be used to download and extract
images and metadata for one entry in records.pkl, each of which is an record from the Zenodo API
for a particular published code repository. In this case, "published" means that it has been
given a digital object identifier (DOI) and an archive of the code provided. Thus,
[run_all.py](run_all.py) will generate a `run_jobs.sh` script to submit instances of it
to sbatch. 

### Generate Job Submission Script
To generate `run_jobs.sh` we need to load the database, and create a jobs and result
folder in our present working directory, and write an sbatch job file for each job (container) 
we want to run.

```bash
python run_all.py
```

This generated the jobs:

```bash
ls jobs/
run_1000400.sh  run_1039952.sh  run_1122955.sh  run_1175323.sh  run_1214698.sh  run_1248981.sh  run_582349.sh  run_837334.sh
run_1000406.sh  run_1039961.sh  run_1122957.sh  run_1175348.sh  run_1214827.sh  run_1248992.sh  run_582351.sh  run_837336.sh
run_1000413.sh  run_1039986.sh  run_1122959.sh  run_1175415.sh  run_1214854.sh  run_1248996.sh  run_582354.sh  run_837338.sh
...
```

### Test the Job
You'll notice in the above listing I had already started testing, because I have output and error files. First, let's test one job. I opened up
the run_jobs.sh script to get one last line, and run it manually:

```bash
sbatch -p russpold /scratch/users/vsochat/zenodo-ml/slurm/jobs/run_1212458.sh
```

You can look at the output and error files to see how you screwed up. Trust me, you will.

```bash
cat jobs/zenodo-ml-1212458.err
```

You can check if a job is running with:

```bash
squeue --user vsochat
```

Then check that your output is generated successfully. Is the correct data there?

```bash
ls $SCRATCH/WORK/zenodo-ml/1212458
images_1212458.pkl  metadata_1212458.pkl
```

It doesn't hurt to load it and look at it too.

```
python3

import pickle
images = pickle.load(open('/scratch/users/vsochat/WORK/zenodo-ml/1212458/images_1212458.pkl','rb'))
meta = pickle.load(open('/scratch/users/vsochat/WORK/zenodo-ml/1212458/metadata_1212458.pkl','rb'))
```

Ta da! Let's run en masse.


### Submit All Jobs
When you are content that you are done screwing up, you can submit all jobs at once:

```bash
bash run_all.sh
```

Then pray.

OR if you have an upper limit and need to monitor the queue, you can (I have this limitation because Sherlock has a job limit) I've written a silly [submit.py](submit.py) script to do it for us.

```bash
python3 submit.py
```
