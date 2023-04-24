# ml_tools

This is an updated git repository of all the tools found on [my website](http://morganloomis.com). It's provided as an alternative to downloading tools individually, if you want to stay up to date with everything.

Feel free to fork or contribute. 

## Installation

Download the most current release or clone the repository to a directory of your choice.

Setting the environment variable `MAYA_MODULE_PATH` is the easiest way to integrate the tools into Maya.  You can put the path to ml_tools either in the Maya.env file or set a system environment path prior to launching Maya via shell.

In the further examples, we will use `/path/to/ml_tools` as a path example. You have to replace it by the path you use.

### Via shell

#### Windows:
```
set "MAYA_MODULE_PATH=%MAYA_MODULE_PATH%;/path/to/ml_tools"
```
#### Linux / macOS:
```
export MAYA_MODULE_PATH=$MAYA_MODULE_PATH:/path/to/ml_tools
```

### Via Maya.env
You will need to edit the `Maya.env` located in your /maya/version folder. Where is it and how to open it [on the Autodesk manual](https://knowledge.autodesk.com/support/maya/learn-explore/caas/CloudHelp/cloudhelp/2020/ENU/Maya-EnvVar/files/GUID-8EFB1AC1-ED7D-4099-9EEE-624097872C04-htm.html).

Once Maya.env opened, add the following at the end of the file:  
```
MAYA_MODULE_PATH = /path/to/ml_tools
```

### Load the shelf:
In the shelf, click the gear icon on the left side, then Load Shelf:

![demo_maya_load_shelf](https://user-images.githubusercontent.com/16049822/80697264-05ea5100-8ad9-11ea-9eb4-dd22c4acf365.gif)
