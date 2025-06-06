# IN WRITING (for Jake Messick)

## Preamble:
The overal goal is to create a safe sandbox for non-techincal artists (students and faculty at the Corcoran School of Arts and Design) to explore generative AI tools that expose more parameters than simply a text pronpt, and tools beyond those currently offered by the university (primarily Copilot and Adobe Creative Cloud.) Typical users would range from completely non-technical (imagine a first-year painting student) to slightly more advanced (imagine an interaction design grad student). Additionally, these tools are computationally intensive and would benefit from the power of the HPC. We think running ComfyUI on OOD is a good place to start exploring: unlike the availble Apporto VMs, OOD has more powerful GPUs and allow users to experiment with various installs. ComfUI has a graphical interface for creating custom workflows; in addition to txt2img it has txt2audio, txt2video, and txt2model in various stages of development. These capabilities are all of interest to creators. By staging these tools internally we aim to eliminate some security issues (unlike using an API, there is no data going out to a third party for processing.)

## Big picture:
In an ideal world we would have dedicated hardware to provide these tools as a service. In that world, this system should look like:

+ SSO for authentication (user doesn't need to create/remember new user/pass, no need for SSH.)
+ Web interface that points to an array of tools for users to experiment with (ComfyUI, Gradio-surfaced tools). Should not require use of terminal (user should not have to know unix or python.)
+ Documentation for users.
+ Everything local to GW, no sharing of data with third parties.
+ Integration with GW BOX such that user's data, custom workflows, models, and other user-specific data is easily accessible.
+ Documentation for maintainers.

## Near-term
To get to that ideal world we need to learn more about how these tools work, and what the true cost is. In the near-term we hope to:
+ Test install ComfyUI and dependencies to OOD desktop (Cerberus).
+ Identify ways of streamlining the process for acivating modules and installing ComfyUI (and its dependencies and additional models)
+ Create a tutorial for a nontechnical users that includes onboarding to HPC, launching OOD, and activation ComfyUI
+ Create a set of annotated workflows in ComfyUI to get beginers started
+ Evaluate speed of ComfyUI (compare running in OOD vs on an M2 Mac)
+ Explore parallelizing acrose multiple nodes? (possible on OOD?)
+ Can we add comfyui as a interactive application in the HPC dashboard, where there are two options of cerberus and peagesus desktops?
  

## If time allows this summer...
We'd like to experiment/explore: 
+ Can we build a command line script that could launch a ComfyUI server directly?
+ Could said script be launced from a secure web page?
+ Can we integrate GW Box such that all outputs are backed up automagically for the user?
+ Can we create a Google sheet app that tracks parameters for each job and compares outputs of multiple jobs in one document?
