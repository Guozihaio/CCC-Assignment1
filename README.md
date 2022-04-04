# COMP90024 -Cluster and Cloud Computing Assignment 1 – Multicultural City 
Code created by   
Zihao Guo 931278   
Yan Yan 1320588

# Project descprition
Assignment is to search the large Twitter data set (bigTwitter.json) and using the language used
when tweeting, the number of tweets in those languages and the tweet location (lat/long) count the total number of
tweets in a given cell that are made in different languages. The final result will be a score for each cell with the following
format, where the numbers are obviously representative.
Application should allow a given number of nodes and cores to be utilized. Specifically, your application should
be run once to search the bigTwitter.json file on each of the following resources:

<b> • 1 node and 1 core; </b>

<b> • 1 node and 8 cores; </b>

<b> • 2 nodes and 8 cores (with 4 cores per node). </b>

# File Include

• multi.py -- Constructor for classes

• newmain.py -- main file for loading Json file and data processing

• 1Node1Cores.slurm&nbsp;&nbsp;    1nodes8cores.slurm&nbsp;&nbsp;      2Node8Cores.slurm &nbsp;&nbsp;  

• 1Node1Cores.out&nbsp;&nbsp;    1nodes8cores.out&nbsp;&nbsp;      2Node8Cores.out &nbsp;&nbsp; 

• Assignment 1 report.pdf

# How to use

To run the program on Spartan, Three slurm files configured with three different resources, which are 1node1core, 1node8cores, and 2nodes8cores. 
Run the command: 
<pre> 
sbatch 1Node1Cores.slurm 

sbatch 1Node8Cores.slurm 

sbatch 2Node8Cores.slurm 
</pre>
              
will submit a new job to the Slurm queue on Spartan. A job ID will be given after that. To track the progress of the job, run squeue -u username to check the status of the work. When the status shows finished, a file named slurm-jobID.out will be in the directory. Run more slurm-jobID.out to check the performance of each job.

Or

<b>Run </b> 
<pre>mpiexec -n &nbsp#num of cores&nbsp; python3&nbsp; newmain.py;&nbsp sydGrid.json&nbsp; #anyTwitter.json;&nbsp #batch_size;&nbsp;</pre> on your local computer
