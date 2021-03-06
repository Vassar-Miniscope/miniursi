# HOPPER INSTRUCTIONS

## SETUP

### 1: Connect to Vassar's VPN
VPN instructions can be found here: https://servicedesk.vassar.edu/solutions/571021-vassarone-setting-up-multi-factor-authentication-with-duo

### 2: Log-in to Hopper
a.	Open the Terminal and type the command:  
<code>$ ssh -p 22022 *username*@jr.cs.vassar.edu</code>  
where *username* is your Vassar username

b.	Enter your Hopper password and change your password if you would like (your password and instructions for changing it should have been provided in an e-mail from Matt Tarantino when you were granted access to Hopper)

### 3: Move to the shared Miniscope directory
Type the command:  
<code>$ cd /work/miniscopepipeline/miniursi</code>

To examine the contents of our directory, use the command  
<code>$ ls</code>

### 4: Install necessary packages
Type the following command to execute the bash script and download the necessary packages to run the pipeline. You should only have to do this once unless the bash script is updated or your user environment in Hopper has changed.  
<code>$ ./install.sh</code>

### 5. Add videos to Hopper from Google Drive
Add videos to the shared Google Drive “Miniscope Videos”. Make sure you keep videos in appropriate folders otherwise this process will be much harder. For each video, make sure that it is shared so anyone with the link can see the file.  
In Hopper, move to the drive folder in miniursi:  
<code>$ cd drive</code>  
Then run the drive_list.py script using:  
<code>$ python3 drive_list.py</code>  
This will create the functions necessary to pull files from Google Drive.  
Then, make the specific folders you want to download the videos into by continuing to use the cd command. If you want to make a new folder, use the following command:  
<code>$ mkdir *folder_name*</code>  
To prepare to transfer an entire folder of videos to Hopper, you need to set the folder ID in the upload.py file (this for now should be done in GitHub followed by a git pull command once you are in our directory in Hopper). There is only one line in the file that needs to be edited which looks like this:  
<code>upload('1tr_Laq--VNw5gyVPYQgASNY3iFp9aYyX')</code>  
The folder ID is the string in the upload function. You can find it by looking at the folder’s sharable link on Google Drive. For example, if I have the following link:
<code>https://drive.google.com/file/d/1-3_0s_102qDE6NeWmyP6byVD2XIdN5hd/view?usp=sharing</code>  
Then the folder ID to be put in the upload function is:  
<code>1-3_0s_102qDE6NeWmyP6byVD2XIdN5hd</code>  
All that’s left is to execute the upload function once you are in Hopper:  
<code>$ python3 upload.py</code>  
Alternatively, if you don't want to change things in Github, you can open an ipython session:  
<code>$ ipython</code>  
and then run the following lines:  
<code>>>> from drive_list import SCOPES, store, creds, DRIVE, search, upload</code>  
<code>>>> upload('*folder_id*')</code>  
**Note that right now the upload function only works in the drive folder. Calling it from any other folder leads to the API taking over your terminal trying to get you to sign in and eventually crashing (I think Hopper confuses it). After you upload the videos you will have to use Cyberduck or the Microsoft equivalent cloud storage browser to move them into the folder you made for them.**  
Note that *you will have to have shared permissions of the folder to anyone with the link for this process to work*. Otherwise you will get several permission denied errors. Lastly, Hopper can only handle so many videos at a time. It is suggested that if you have groups of videos that are larger than 15 that you split them evenly in subfolders for processing and run the cross-registration file on them after to unify the whole session.   
  
**Note the section below does not yet work - command tries to identify a new randomly named directory, waiting for dev response**  
If there are individual videos that were not transferred due to not being in the correct original folder or some other issue, you can enter the following command to add that single video to the google drive:  
<code>gdown https://drive.google.com/uc?id=file_id -O output_directory</code>  
The file_id will be different for each video and can be found by looking at the video’s sharable link on Google Drive the same way you get a folder ID. The output_directory is where you want the video to end up. Make sure to cohesively store it in the folder structure you want to work with and to put the correct file name and type at the end of the command. So, if I wanted to name a file ‘Test.avi’ and store it in my downloads on my computer, I would write this at the end of the gdown command:  
<code>-O ‘/Users/me/Downloads/Test.avi’</code>

## RUNNING THE SCRIPT

### 6: Examine the nodes
To check general information about the nodes type:  
<code>$ sinfo</code>  
b.	To check the active job queue type:  
<code>$ squeue</code>  
These commands will generally tell you what parts of Hopper are in use and what are available. This will inform when/where you run either interactive sessions or batch scripts.

### 7: Specify the correct directory and config file  
From the /work/miniscopepipeline/miniursi directory enter the following command:  
<code>$ vi ursi_pipeline.py</code>  
This will open the file within your terminal and make it available for editing. Next, scroll down to where it says '## import config'. You should see something like this:  
<code>## import config</code>  
<code>from minian.config_mouse16 import minian_path,...</code>  
We need to edit the file to call the config file you want to use. First, hit 'i' on the keyboard to allow editing of the file. Then, enter the config file you want in the format of <code>minian.*chosen_config_file*</code> at the beginning of the chunk of code. **BE VERY CAREFUL TO NOT EDIT ANYTHING ELSE IN THIS FILE, OTHERWISE THE PIPELINE WILL NOT WORK.** However, if the file does get bugged in this process, you can simply pull the original from git and try again. Once you are done editing, hit the <code>esc</code> key. Then type <code>ZZ</code> to save and exit.  
Then, change directory to the minian directory using  
<code>$ cd minian</code>  
From there, access the editor with the config file you plan to use:  
<code>$ vi *config_name*</code>  
Once in the editor, move down to the <code>dpath</code> variable and enter the path to the folder of videos you want to analyze in string format. **AGAIN, DO NOT EDIT ANYTHING ELSE.** Once you are done, exit in the same way and return to the miniursi directory using <code>$ cd ..</code>.  
Note that these are the same steps necessary to specify the path to the correct folder in the crossregistration file, the only difference is that you will enter <code>$ vi ursi_crossreg.py</code> to access that file.

### 8: Run an interactive session
To start an interactive session, type:  
<code>$ srun -N 1 --ntasks-per-node=16 --pty bash</code>  
where -N is the number of nodes you are requesting, and ntasks-per-node is how many tasks you want to run in parallel on each node. To start an interactive session on the GPU, type:  
<code>$ srun -p gpu –-pty bash</code>  
You should see that you have been moved to @lambda-server. After either of these commands is executed, the terminal will work the as a normal local terminal session (Unix) except on the node(s) you’ve connected to on Hopper.  
Note that the environment when you launch an interactive session, the environment is based on the environment when you launched the session, extra variables set automatically by Slurm, and settings in the bash file (which should install the necessary packages for the pipeline).   
To run the pipeline script in the interactive session, check that you are in the right directory and type:  
<code>$ python3 ursi_pipeline.py</code>  

### 9: Cross-Registration in an interactive session
To run the cross-registration script in the interactive session, make sure you have run the pipeline script on all the videos to be cross registered. Then change the parameter ‘dpath’ in the config_crossreg.py file within the minian folder to the directory containing the videos to be cross-registered and their corresponding pipeline_output folders (e.g. to cross register all sessions for Animal15, dpath should be set to ./videos/Animal15). The steps to do this are the same as for the normal pipeline in (7). Additionally, you will have to set the sess variable in the ursi_crossreg.py pipeline file (found in the normal miniursi directory). This must be set to the list of the names of the folders you are cross-registering. Note that each pair of videos + output should be in a unique folder. Once all that is set, run the following command from the miniursi directory.  
<code>$ python3 ursi_crossreg.py</code>

### 10: Configure DeepLabCut Environment
These steps only need to be done once to make sure the the DLC environment is configured with your user. First, start an interactive session as specified in (7). Then, enter this command to make sure conda is configured with your user:  
<code>/anaconda3/condabin/conda init bash</code>  
If there are changes made in this step, you may have to restart the terminal for them to take effect. Once that is set, run the following command to create the DLC-GPU environment:  
<code>conda env create -f /tmp/DLC-GPU.yaml</code>  
Once the environment has been created, you should be able to use the command  
<code>$ conda activate DLC-GPU</code>  
to activate the environment. Then, see below for the steps on how to run DLC.  

### 11: Use DeepLabCut  
To use DeepLabCut, first make sure you are in the docker directory:  
<code>$ cd $HOME/work/miniscopepipeline/miniursi/Docker4DeepLabCut2.0</code>  
Then start an interactive session on the gpu in Hopper as specified in (7). Once you are in the session, enter the following command:  
<code>$ conda activate DLC-GPU</code>  
Once the DLC-GPU environment is running, execute the following command to make a container necessary to run the docker (which essentially creates GPU compatibility with DLC):  
<code>$ GPU=1 bash ./dlc-docker run -d --name *container_name* vassar/dlcdocker</code>  
If you get an error saying that your container name (specified by whatever you enter as *container_name*) is already in use, you have a couple options. You can use that container by running the exec step (see below), or you can stop and remove the existing container with that name using the following commands:  
<code>$ docker stop *container_name*</code>  
<code>$ docker rm *container_name*</code>  
Once the container you want to use is running, run the following line to enter it:  
<code>$ docker exec --user $USER -it *container_name* /bin/bash</code>  
To make sure that you aren't calling the GUI (which is not usable in Hopper), run the following command before you start python:  
<code>$ export DLClight=True</code>  
Then open an iPython session...  
<code>$ ipython </code>  
...and import DLC:  
<code>import deeplabcut</code>  
Once this is done, all DeepLabCut commands will be available. Run each line as follows to extract positions.  
<code> config_path = *path_to_config_file* </code>  
**Make sure that the project_path and video_sets within the config file are set to Hopper paths** 
<code> deeplabcut.train_network(config_path, displayiters = *displayiters*, saveiters = *saveiters*, maxiters = *maxiters*) </code>   
If unchanged, the defaults are *displayiters* = 1000 (display loss per 1k iterations, highly recommend changing to a higher number), *saveiters* = 150000 (a checkpoint file will be saved every 150k iterations), *maxiters* = 1030000 (maximum training iterations).    
<code> deeplabcut.evaluate_network(config_path) </code>   
<code> deeplabcut.analyze_videos(config_path, *video_path*, save_as_csv=True) </code>   
*video_path* is a list of full paths to the videos you want to analyze ['/path/to/video1', '/path/to/video2', 'path/to/video3']. When entered as ['/path/to/folder'], all videos under that folder with extension '.avi' will be analyzed. Note that only one folder can be entered.
<code> deeplabcut.create_labeled_video(config_path, *video_path*, draw_skeleton = True) </code>   
(Optional) To produce plots of the trajectories of body parts throughout the videos, type:   
<code> deeplabcut.plot_trajectories(config_path, *video_path*) </code>    
To exit iPython and return to the container, type:    
<code>exit()</code>  
To exit the container, just enter:  
<code>exit</code>  
To exit the DeepLabCut environment, type:  
<code>$ conda deactivate</code>  

### 12.1: Downloading Results (Pipeline)
For now, this is easiest to do from a graphical user client (WinSCP for windows, CyberDuck for Macs) where you can interact with Hopper like a normal folder directory. The pipeline outputs three different .csv files for each folder it is run on. traces.csv holds the temporal information about the calcium traces detected by the pipeline for each identified neuron. spikes.csv holds the temporal information of the inferred spiking of each identified neuron. Lastly, spatial.csv holds the spatial information for each of the identified units (although at this point this file is not critical). Additionally, when cross-registration is run there will be a .csv called mappings.csv that tells you which units correspond with one another across sessions. These files are used in the R notebooks in this Github (which are currently in the works).  

### 12.2 Downloading Results (DLC)
NEED INFO. 

### X: Creating and running a batch script - FOR FUTURE/NOT YET CONFIGURED ON HOPPER
Batch scripts in Hopper need to be created and uploaded to our shared environment before they can be called. The script contains resource requests and other job options for the batch. An example of this kind of script is shown below:  
![batch1](/img/batch1.png "Batch1")  

The batch script is made up of a header (where you can see all the #SBATCH calls) and the commands to execute the job. The description for most of the header variables are below:  
![batch2](/img/batch2.png "Batch2")  

Following the header, the commands of the script are meant to reference the locations of the working directory for the batch and the program file that will be called (in our case the miniscope pipeline). Note that for our project we are going to be using the gpu so make sure to request the gpu partition in the script not general or emc.  
Once the script has been created locally, you can upload it to our shared directory in Hopper in two ways:  
1.	Use a graphical user client (WinSCP for windows, CyberDuck for Macs). Once one of these is downloaded, you can connect to the Vassar hostname (jr.cs.vassar.edu) and the port (22022 or just 22 if connected to the VPN) and view Hopper in a more interactive directory (such as Finder on Macs). Then you can just drag and drop your batch files into our directory in Hopper.  
2.  Use the terminal and the following command:  
<code>scp -P 22022 *username@local_machine:/path/to/myfile* *username@jr.cs.vassar.edu:/path/to/file-destination*</code>  

Lastly, to execute the batch request you enter the following command:  
<code>sbatch -*options* *batch-script-file*</code>  
*-options* are optional manual entry of the batch variables listed above which if entered will supersede whatever is written in the batch script. *batch-script-file* should just be the name of the batch script you wish to run.
