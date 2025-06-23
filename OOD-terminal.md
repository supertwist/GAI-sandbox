# Terminal commands for ComfyUI on OOD

## When setting up ComfyUI for the *first time..*

First, load Anaconda (an interface for running Python code) and GIT (a tool for using shared code repositories, AKA 'repos'.)

`ml anaconda git`

Next, we'll activate Anaconda:

`source /modules/apps/anaconda3/etc/profile.d/conda.sh`

Next, we'll activate an 'environment' specifically for ComfyUI:

`conda activate comfyui`

Next we'll install a really useful 'custom node' called **ComfyUI Manager.** The manager in turn will allow us to easily find and install other custom nodes (represented as graphical blocks in ComfyUI) and models (AIs tailored to do differet tasks, such as generate written language, images, sound, and 3D models) to create our own custom workflows, or enable workflows created by other people. To do this, we first need to point to the custom nodes directory:

`cd custom nodes`

Next, we'll use GIT to install the Manager code to that directory:

`git clone https://github.com/ltdrdata/ComfyUI Manager comfyui manager

Next, we'll download all the other software that ComfyUI depends on to run properly. Navigate back to the ComfyUI directory:

`cd ..`

Then:

`pip install -r requirements.txt`

And **finally,** we'll launch ComfyUI:

`python main.py --gpu --listen 0.0.0.0 --port 8888`

...And you are off to the races.

## *After* you've set up ComfyUI...

*Coming soon...*
