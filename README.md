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

## Running tests

Tests run inside Maya via `mayapy` (not from system Python). Ensure `ml_tools` is on `MAYA_MODULE_PATH` so `scripts/` resolves the same way as in Maya.

Install dev dependencies into Maya's Python (once per Maya install):

```text
"C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" -m pip install -r requirements-dev.txt
```

Run the full suite:

```text
"C:\Program Files\Autodesk\Maya2024\bin\mayapy.exe" -m pytest tests/ -v
```

Exclude UI entry-point smoke tests:

```text
mayapy -m pytest tests/ -v -m "not ui"
```

Note: `mayapy` runs in batch mode, so Maya UI commands are unavailable. Entry-point smoke for `ui()` tools is skipped automatically; logic tests call underlying functions directly. Run UI smoke interactively from Maya's Script Editor if needed.

## ml_dynamics

**ml_dynamics** (secondary motion / XPBD simulation) has moved to the standalone **anim_dynamics** repository. Install both repos on `MAYA_MODULE_PATH` if you use dynamics alongside other ml_tools scripts. See `G:\My Drive\packages\anim_dynamics\README.md` for install and test instructions.
