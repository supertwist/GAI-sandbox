# Example: Image to a printable 3D model

include
+ comfyUI workflow .json annotated
+ link to model card on huggingface
+ link to model repo

## Conversion from .GLB to .STL
[Meshlab](https://www.meshlab.net) is an open source Swiss Army knife for working with pointclouds and meshes. It can import and export a wide variety of formats, so it's a great conversion tool.

## Cleanup
A useful online tool for repairing .STL files is [FormWare Free Online stl repair](https://www.formware.co/onlinestlrepair). This tool ensures the mesh is watertight, surface normals are oriented correctly, surfaces are manifold, and so on... all the things that slicing software wants for a clean 3D print. Recommended for all models generated, if you intent them to be 3D-printable.
