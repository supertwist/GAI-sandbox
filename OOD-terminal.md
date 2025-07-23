# Terminal commands for ComfyUI on OOD
Getting ComfyUI running on an OOD machine can be done with terminal commands; that may sound scary, but it's actually pretty easy, and you don't need to memorize the commands. Just open this page in browser once OOD is launched, and then copy/paste `lines that look like this` one at a time into the terminal, each followed by the "ENTER" key. This sequence of commands was put together by the **AWESOME Dhwanil Mori!** This is the cheat codes!

## When setting up ComfyUI for the *first time..*
First, load Anaconda (an interface for running Python code) and GIT (a tool for using shared code repositories, AKA 'repos'.)

```
ml anaconda git
```

Next, we'll activate Anaconda:

```
source /modules/apps/anaconda3/etc/profile.d/conda.sh
```

Next, we'll activate an 'environment' specifically for ComfyUI:

```
conda activate comfyui
```

Now the good stuff, installing ComfyUI:

```
git clone https://github.com/comfyanonymous/ComfyUI.git
```

And we'll go to the directory it now lives in:

```
cd ComfyUI
```

Next we'll install a really useful 'custom node' called **ComfyUI Manager.** The manager in turn will allow us to easily find and install other custom nodes (represented as graphical blocks in ComfyUI) and models (AIs tailored to do differet tasks, such as generate written language, images, sound, and 3D models) to create our own custom workflows, or enable workflows created by other people. To do this, we first need to point to the custom nodes directory:

```
cd custom_nodes
```

Next, we'll use GIT to install the Manager code to that directory:

```
git clone https://github.com/ltdrdata/ComfyUI-Manager comfyui-manager
```

Next, we'll download all the other software that ComfyUI depends on to run properly. Navigate back to the ComfyUI directory:

```
cd ../
```

Then:

```
pip install -r requirements.txt
```

And **finally,** we'll launch ComfyUI:

```
python main.py --gpu --listen 0.0.0.0 --port 8888
```

...And you are off to the races.

## *After* you've set up ComfyUI...
You've just installed all of the tools you'll need to get started. You won't need to regularly re-install ComfyUI, but each time you launch a new session in Cerberus Desktop, you'll need to reactivate the environment:

Reactivate these modules:

```
ml anaconda git
```

And:

```
source /modules/apps/anaconda3/etc/profile.d/conda.sh
```

Then activate the ComfyUI environment:

```
conda activate comfyui
```

**NOTE, sometimes there's a gotcha...**
Depending on where you left things the last time you logged into OOD, you might need to point the terminal to the ComfyUI directory. Here's an example:

<img width="866" alt="Screenshot 2025-07-03 at 11 02 03 AM" src="https://github.com/user-attachments/assets/2e9bbcff-7e5a-4283-91a0-d4ed0a921bf8" />

Let's dissect the bottom line (highlighted):
+ (comfyui) < is indicating that we are in the ComfyUI environment
+ [sprtwst@gpu005] < is indicating that I (my user account is sprtwst) am logged into the computer gpu005
+ $ < the dollar sign indicates the system is ready to accept a command

Great, but to run the next command (launching ComfyUI in a browser) we actually need to be in the ComfyUI directory. If we enter this command:

```
cd ComfyUI
```

and hit enter, now we see "ComfyUI" before the $, indicating we are in that subdirectory:

<img width="881" alt="Screenshot 2025-07-03 at 11 06 30 AM" src="https://github.com/user-attachments/assets/a4929436-731f-4c2e-bfb8-9891d0969ae5" />


OK, finally, launch the ComfyUI server:

```
python main.py --gpu --listen 0.0.0.0 --port 8888
```

## Running ComfyUI on Pegasus in the superchip queue:
*assumes you've installed ComfyUI*

First, activate the environment:

```
conda activate comfyui
```

Next, navigate to the ComfyUI folder:

```
cd ComfyUI
```

and finally, launch the server:

```
python main.py --gpu --listen 0.0.0.0 --port 8888
```

## Installing **ffmpeg** for voicecloning workflows:
*Assumes you've already installed ComfyUI. Start a fresh session in OOD, and activate the CompfyUI environment...*

Run this command:

```
conda install -c conda-forge ffmpeg
```

Dhwanil's **more complete notes** can be found [here.](https://gwu.box.com/s/20l98lcy3rp8boks12hmg73i0onblb3y)
