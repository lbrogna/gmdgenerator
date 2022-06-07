ReadMe file for Luke Brogna's Multiple Calibration Analysis .gmd File Creator

For comments, questions, or to report bugs, contact lbrogna@clarku.edu

In analyzing multiple calibration lengths and their effects on simulation output, it is necessary to execute 
many model runs, for each duration. When done manually, the process of calculating and inputting the 
correct pixel quantities is tedious and prone to error. This program's main goal is to automate that 
process for Terrset's GeoMod land change modeler by creating batches of .gmd files, which store 
GeoMod run parameter information. This text file will serve as a step-by-step guide on how to use this 
program as a research aid or education tool. It is in the user's best interest to read the below 
instructions before attempting to use the program. There is example data contained in a folder named 
exampleData included with this program. If one wishes to use the example data to perform GeoMod 
runs, they should copy the data into their Terrset working folder, which is where all data used as 
inputs in this program should live.

Initial Session Parameters
Two decisions must be made before beginning to input data, allocation mode and stratification mode. 
These options are found at the top of the left-hand side of the interface. The data is parsed differently 
depending upon which options are chosen in this section, so these buttons are the first ones a user 
should click upon opening the creation tool.
ALLOCATION MODE: Shortened to 'a-mode' in the interface, this option affects how GeoMod will 
allocate change during each run. If the user selects 'static,' then state 1 will include both loss and 
persistence of the losing category during the calibration period. With the 'static' method, the allocation 
rule (or suitability image) which GeoMod uses to allocate changing pixels, will be the same across all 
model runs. If the user selects 'dynamic,' state 1 will include only the loss of the losing category during 
the calibration period. With the 'dynamic' method, a new suitability image is calculated for every model 
run based on the loss in the calibration image.
STRATIFICATION MODE: Shortened to 's-mode' in the interface, this option affects how the user wishes 
the model run to be stratified, as GeoMod has the capability to simulate land change within individual 
strata. If the user selects 'unstratified,' the resulting parameter files will not be stratified. If the user 
selects 'stratified,' the resulting parameter files will be stratified by a user provided strata image.

i. Dates
The next section deals with the simulation dates. In the left-most input box in this section, the user 
should type the start year of the validation period (which is also the end year for the calibration period). 
In the right-most input box in this section, the user should type the last year for which they have data, 
such that the validation and calibration periods are equal in duration. This year will be the latest year 
that the program will produce a simulation run for.

ii. Simulation Output Naming Convention
These input boxes dictate what the output images produced by GeoMod will be named. The user can 
input a prefix, a suffix or neither. The output names are concatenated as follows 
'prefix'_cal_len_?'suffix', where the ? is replaced by the length of the calibration interval for that 
particular run.

iii. Loss Data
This section deals with the loss data that will serve as the basis for the simulated quantities in the 
resulting .gmd files. These inputs require some manipulation in Terrset of a loss image such as the one 
contained in the exampleData file called 'Loss0020a.'

a. Loss Areas
This file open tool takes different text files as inputs depending on the user's 's-mode' choice. If the user 
chose to do an unstratified analysis, the user must input a text file containing the tabular pixel areas of 
the loss image obtained by using Terrset's Area module on the loss image (see LossAreas file in 
exampleData for guidance). If the user elected to perform a stratified analysis, the file input should be 
the tabular pixel areas result of Terrset's CrossTab module, with the strata image as the rows and the 
loss image as the columns (see LossByState in the exampleData folder).

b. Legend Info
For the program to read the loss data provided in part a. of this section, the user must provide legend 
information about the loss image. In this way, the program attempts to give some leeway in the creation 
of the loss images, however there is one requirement: the actual loss categories in the image must all 
fall within a certain range of legend codes, which are input into the top two boxes of this section. The 
bottom two boxes contain the legend codes for the non-loss aggregate land cover categories. When 
using the example data, the correct inputs for this section are (from left to right starting with the two 
upper boxes): 2, 21, 22, 1.

iv. Driver Variables or Suitability Image
It is important to note that if the user selected 'dynamic' as the 'a-mode' option, then a set of driver 
variables, not a suitability image, must be used for effective analysis. Driver variables must be input into 
the program as a .rgf file. The suitability image must be input in the form of a .rst file. If the user chose 
'static' as the 'a-mode' option, it is recommended that they first use driver variables, use one of the 
resulting files to complete a GeoMod run, then use the resulting suitability image to input back into this 
section, in order to create a new batch of files. This is because in 'static' mode, the suitability image will 
be the same in all runs, so it is a waste of time and computing resources to continually ask GeoMod to 
calculate that suitability image.

v. Additional Information
This section contains two file opener buttons. The first will only be activated if the user is performing a 
stratified analysis, in which case they should input the strata image .rst file. The other file open button is 
for the initial landcover image(s). If in 'dynamic' a-mode, the user should input a .rgf file containing the 
initial landcover images ordered by shortest calibration interval at the top to longest at the bottom. If in 
'static' a-mode, the file input should be the .rst file of the single landuse image at the start of the 
validation period and the end of the calibration period.

Editing and Saving
With the necessary data input into the interface, the user can now press the 'preview and edit' button. If 
all goes well, an example template of the .gmd file text should appear in the right pane of the UI. From 
here, users with experience in the formatting of .gmd files can freely edit the text. Users should steer 
clear of any instances of  'xxx' they see in the editor, as these are areas which will be changing when the 
batch of files is created.
When the .gmd file has been edited to the user's satisfaction, they may press the 'save file batch' 
button. A prompt will appear querying the user for a destination folder and a text input. This text input 
will be used as a prefix for the created .gmd files.



