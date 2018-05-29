#!/usr/bin/env python
#
# Copyright (C) 2018 Vanessa Sochat.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import os

here = os.getcwd()
jobfile = '%s/run_jobs.sh' %here
output_folder = '%s/WORK/zenodo-ml' %os.environ['SCRATCH']
job_limit = 1000

# The container must exist
if not os.path.exists(jobfile):
    print('Where is the jobfile, %s? Bad researcher!' %jobfile)
    sys.exit(1)

with open(jobfile, 'r') as fh:
    jobs = fh.readlines()

def count_queue():
    user = os.environ['USER']
    return int(os.popen('squeue -u %s | wc -l' %user).read().strip('\n'))

idx = 0
count = count_queue()
while count < job_limit and len(jobs) > 0:
    job = jobs.pop(0).strip('\n')
    jobnum =  os.path.basename(job).replace('.sh','').split('_')[-1]
    outfolder = os.path.join(output_folder, jobnum) 
    if not job.startswith('#') and not os.path.exists(outfolder): 
        print('Running index %s, zenodo id %s' %(idx, jobnum))
        os.system(job)
    idx+=1
    count = count_queue()
