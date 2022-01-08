# CRB_Weather_app
Supporting python  and Javascript code to parse NAM grib data for use in the Crop Residue Burning website of Manitoba Agriculture. This README will teach you how to install the program in your computer for development purposes. Before completing the steps below, install the latest PyCharm Community Edition and create/activate the py27 
environment. Please refer to the Daily-Data-Upload Job Aid.

## Cloning the Repository

### 1. Install required Python Packages

1. Search and open Anaconda Prompt (py27).

2. Navigate using cd commands until you're inside the Project_Directory folder. 

* For example: 
```
cd C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project_Directory
```
3. Finally, type ```pip install -r REQUIREMENTS.txt``` and press Enter

### 2. Install Git Gui and Git Bash

1. Navigate to ```https://git-scm.com/download/win```

2. Double click the Git .exe file to start the installation.

3. If prompted, choose Nano as the default Git editor.

4. If prompted, choose 'Use Git from the Windows Command Prompt'

5. If prompted, choose 'Use Windows default console window'

6. If prompted, leave the 'Configuring extra options' menu in its default state and click 'Install'.

### 3. Clone Repository using Git
There are two ways to do this: through github.com and through Git Bash. The Git Bash method is recommended as it is less
of a hassle when you want upload your changes to GitHub.

#### Git Bash method (Recommended)

1. Create a folder to contain the contents of CRB_Weather_app.

2. Using windows search, find and open Git Bash.

3. At the Git Bash terminal, use cd commands to navigate to the folder you created in step 1.

* For example:
```
cd C:\Users\CAmao\Documents\NEW_FOLDER
```

4. Type ```git clone https://github.com/charleamaoAGR/CRB_Weather_app.git``` and press Enter. Note: make sure you are outside of the
managed environment when completing this step.

#### GitHub.com method

1. Navigate to https://github.com/charleamaoAGR/CRB_Weather_app.

2. Click the green 'Clone or download' dropdown button and press Download Zip.

3. Extract the Zip file to your desired directory.

## Maintaining the Repository
All tasks outlined below will utilize Git Gui.

### Pushing changes to GitHub

1. Find Git Gui using windows search and run the program.

2. If prompted, navigate to the directory you created to house the program files.

3. Press the 'Stage Changed' button to prepare any changes you made to the code for commiting purposes.

4. Write a meaningful commit message on the textbox that explains the changes.

5. Click the 'Commit' button.

6. Click the 'Push' button.

7. If prompted to select a location to push the changes to:

* If repository was cloned using Git Bash, simply leave the push location as the 'origin' branch and press the 'Push' button.
* If repository was cloned using GitHub.com, type https://github.com/charleamaoAGR/CRB_Weather_app into the 'Arbritrary Location' textbox and press the 'Push' button.

### Pulling changes from GitHub

1. Open Git Gui.

2. If prompted, navigate to the directory you created to house the program files. 

3. Under the 'Remote' drop-down menu, select 'Fetch From' and click on 'Origin'.

4. Under the 'Merge' drop-down menu, click on 'Local Merge'. Leave as 'origin/Head' and press the 'merge' button. Note: make sure you have committed all of your changes before merging any changes from GitHub.

