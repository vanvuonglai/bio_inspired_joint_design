runALL.py:-> main file where we can change input parameters such as geometry, material and ossification constant.
OIM_algorithm.py-> ossification_inspired method including:
	- mesh generattion by gmsh using mesh_with_gmsh.py
	- contact model and update material properties using code_aster file: contact_oi_model.comm
Visualisation of results at each iteration (e.g.: using paraview)
	- mesh is stored in "contact_plate_plate_stressplane/results_all/plane_plane_contact/UNV" 
	- stress and Young's modulus distribution are stored in "contact_plate_plate_stressplane/results_all/plane_plane_contact/VTK" 
