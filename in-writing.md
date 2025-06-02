# IN WRITING (for Jake Messick)

Preamble:
The overal goal is to create a safe sandbox for non-techincal artists (students and faculty at the Corcoran School of Arts and Design) to explore generative AI tools that expose more parameters than simply a text pronpt, and tools beyond those currently offered by the university (primarily Copilot and Adobe Creative Cloud.) Typical users would range from completely non-technical (imagine a first-year painting student) to slightly more advanced (imagine an interaction design grad student). Additionally, these tools are computationally intensive and would benefit from the power of the HPC. We think ComfyUI is a good starting point: it has a grahical interface for creating custom workflows; in addition to txt2img it has txt2audio, txt2video, and txt2model in various stages of development. These capabilities are all of interest to creators. By staging these tools internally we aim to eliminate some security issues (unlike using an API, there is no data going out to a third party for processing.)

Big picture:
In an ideal world we would have dedicated hardware to provide these tools as a service. In that world, this system should look like:

+ SSO for authentication (user doesn't need to create/remember new user/pass, no need for SSH.)
+ Web interface that points to an array of tools for users to experiment with (ComfyUI, Gradio-surfaced tools). Should not require use of terminal (user should not have to know unix or python.)
+ Documentation for users.
+ Everything local to GW, no sharing of data with third parties.
+ Integration with GW BOX such that user's data, custom workflows, models, and other user-specific data is easily accessible.
+ Documentation for maintainers.

Near-term
To get to that ideal world we need to learn more about how these tools work, and what the true cost is. In the near-term we hope to:
+ test install ComfyUI and dependencies to OOD desktop (Cerberus).
+ document in GitHub:
+ install process (for future maintainers)
+ potential affordances that might simplify the process to make it more user-friendly


for Jake and Joe
kevin.weiss1@gwu.edu



for beginning users:
use stable existing workflows

for intermediate users:
create and save/load custom workflows
add modules at user level


some things we discussed
+ Open OnDemand (OOD)
+ web interface with SSO > on login go to screen with a couple of buttons that launch SLURM scripts
+ scripts include
    + launch slurm session for 4 hours
    + user info to set save path to users BOX
        + copy from SCRATCH to BOX/user

What is the sandbox?
Low- to intermnediate level of difficulty
Generative AI tools for artists that expose more parameters, allowing for greater creative experimentation and better understanding of the strengths and weaknesses of GenAI.
