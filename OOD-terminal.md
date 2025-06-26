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
cd custom nodes
```

Next, we'll use GIT to install the Manager code to that directory:

```
git clone https://github.com/ltdrdata/ComfyUI-Manager comfyui-manager
```

Next, we'll download all the other software that ComfyUI depends on to run properly. Navigate back to the ComfyUI directory:

```
cd ..
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

And finally, launch the ComfyUI server:

```
python main.py --gpu --listen 0.0.0.0 --port 8888
```
