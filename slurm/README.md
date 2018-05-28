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
containertree0.err    containertree3.out  run_101.sh  run_115.sh  run_129.sh  run_142.sh  run_156.sh  run_16.sh   run_183.sh  run_22.sh  run_36.sh  run_4.sh   run_63.sh  run_77.sh  run_90.sh
containertree0.out    containertree4.err  run_102.sh  run_116.sh  run_12.sh   run_143.sh  run_157.sh  run_170.sh  run_184.sh  run_23.sh  run_37.sh  run_50.sh  run_64.sh  run_78.sh  run_91.sh
containertree10.err   containertree4.out  run_103.sh  run_117.sh  run_130.sh  run_144.sh  run_158.sh  run_171.sh  run_185.sh  run_24.sh  run_38.sh  run_51.sh  run_65.sh  run_79.sh  run_92.sh
...
```

### Test the Job
You'll notice in the above listing I had already started testing, because I have output and error files. First, let's test one job. I opened up
the run_jobs.sh script to get one last line, and run it manually:

```bash
sbatch -p russpold /scratch/users/vsochat/WORK/container-tree/examples/summary_tree_slurm/jobs/run_192.sh
```

You can look at the output and error files to see how you screwed up. Trust me, you will.

```bash
cat jobs/containertree192.err
```

What errors did I have? I forgot to load a module first. Then I added the line and forget to end the `writelines`
command with a newline. Then I loaded the wrong version of python and it didn't find the module.
 I wouldn't have known these issues without looking at the error files. I also needed to check 
continuously on if the job was running, period, with:

```bash
squeue --user vsochat
```

Then check that your output is generated successfully. Is the correct data there?

```bash
ls result/
```

### Submit All Jobs
When you are content that you are done screwing up, submit all jobs:

```bash
bash run_all.sh
```

Then pray.


## Compile Result

Once the jobs have finished running, your output folder should be robust with pickles!

```bash
ls result/

```

And you can use combine.py to combine them. Note that it's going to generate
a data.json in the present working directory. If you did this more nicely, you would
have written a script to take this as an input argument.

```bash
python3 combine.py
```

I'm too ornery with cluster computing to do this nicely :)
