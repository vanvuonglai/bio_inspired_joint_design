

import os
import pathlib
# unity: force: N, length:mm, pressure: MPa

aster_root_folder=os.getenv('HOME')+'/salome_meca/appli_V2019.0.3_universal/salome shell -- as_run' # folder of code_aster
from OIM_algorithm import OIM # import  ossification-inspired method (OIM) algorithm



# work folder
case_name='contact_plate_plate_stressplane' 


if os.path.exists(str(pathlib.Path(__file__).parent.resolve())+'/'+case_name)==False: # if the folder does not exist, creat it!
    path = os.path.join(str(pathlib.Path(__file__).parent.resolve()), case_name)
    os.mkdir(path) 

#%% GEOMETRY
L=50 # width ànd height of the two bodies
ho=5 # thickness of the articular regions
h1=40# thickness of the design domains
lcontour=10# width of hte zone where the  uniform force is applied
lc=2# mesh size

#%% MATERIAL PROPERTIES
    
Eecc=200000 # Young modulus of bone
Nuecc = 0.3;# Poisson's ratio of bone
Encc=80000 # Young modulus of cartilage
Nuncc = 0.3;# Poisson's ratio of cartialge


#%% Applied force:
Fy=-2500

#%% PARAMETERS USED IN THE BIO-INSPIRED METHOD
kappa=100   # ossification constant 
koii=0.2    # percentage of elements ossified in the design domains

#%% computation using ossification-inspired algorithm

x,cpoo,cpo1,cp=OIM(L,ho,h1,lcontour,lc,Encc,Nuncc,Eecc,Nuecc,Fy,kappa,koii,case_name,aster_root_folder)   
# x: contact coodinates in x-direction
# cpoo: contact pressure if design domains are all ossified
# cpo1: contact pressure if design domains are not ossified    
# cp: contact pressure obtained with ossification-inspired algorithm
  
    
    

