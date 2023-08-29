
import os
import pathlib
from subprocess import Popen
import mesh_with_gmsh as mesh_A1A2A3A4A5 # Module to creat mesh
from templates import export_template
import json

from matplotlib import pyplot as plt
import numpy as np
import copy

def OIM(L,ho,h1,lcontour,lc,Encc,Nuncc,Eecc,Nuecc,Fy,kappa,koii,case_name,aster_root_folder):

#%% geometry parameters used for GMSH    
    jsonData=dict()
    jsonData['l2']=L
    
    jsonData['l1']=L
    jsonData['h3']=ho
    jsonData['h2']=ho
    jsonData['h1']=h1
    jsonData['h4']=h1
    jsonData['h0']=L-ho-h1
    jsonData['h5']=L-ho-h1
    jsonData['lcontour']=lcontour
    jsonData['lc']=lc
    
    with open(str(pathlib.Path(__file__).parent.resolve()) +'/'+case_name+'/parameters.json', "w") as outfile:
        json.dump(jsonData,outfile)  
    

#%% ALL PATHS where RESULTS are stored
    
    foldersave='results_all' # folder to store all files
    if os.path.exists(str(pathlib.Path(__file__).parent.resolve())+'/'+case_name+'/'+foldersave)==False:
        path = os.path.join(str(pathlib.Path(__file__).parent.resolve())+'/'+case_name , foldersave)
        os.mkdir(path)    
        
    
    nameficheroi='plane_plane1_'+str(kappa)+'koi'+str(koii) 
    
    paths_dic = dict()
    
    paths_dic['main_root'] = str(pathlib.Path(__file__).parent.resolve())+'/'+case_name+'/'+foldersave
    paths_dic['aster_root'] = aster_root_folder
    
    main_root = paths_dic['main_root']
    aster_root = paths_dic['aster_root']
    
    paths_dic['analysis_comm'] = main_root + '/analysis.comm'
    paths_dic['analyses_directory'] = main_root +'/'+ nameficheroi
    paths_dic['json_input_data'] = paths_dic['analyses_directory'] + '/input_params.json'
    
    # Find and Delete the existing ANALYSIS directory
    if os.path.exists(main_root+'/'+nameficheroi)==False:
        path = os.path.join(main_root, nameficheroi)
        os.mkdir(path)
    
    # Path                 
    required_dirs = ['UNV','RMED','MESS','EXPORT','COMM','VTK','JSON']
    
    for item in required_dirs:
        temp_path = paths_dic['analyses_directory'] + '/' + item
        paths_dic[item] = temp_path
        pathlib.Path(temp_path).mkdir(parents=True, exist_ok=True)
       
    
    namereper = {'name':'/'+case_name+'/'+foldersave+'/'+nameficheroi}      
    
    namereper_object = json.dumps(namereper, indent = 4)
        
        # Writing to sample.json
    with open('namereper.json', "w") as outfile:
            outfile.write(namereper_object)
            
    #%% COMPUTATION BEGINS
    varcp=np.array([]) # Quality indicator
    maxcp=np.array([]) # maximum contact pressure
    enercp=np.array([])# total deformation energy
    smises=np.array([]) # Maximun Von Mises stress
    
    plt.close('all')
    
    maxnum=101
    reso=1
    iteration_all=0
    for num in range(0,maxnum):
        
        print(num)
        Fyi=Fy/1
        iteration = copy.copy(num) #+ 1
        path_Eevo = main_root + '/E_evolution.txt'
        path_elems_criteria = main_root + '/elems_criteria.txt'
    
        path_export = paths_dic['EXPORT'] + f'/analysis_{iteration}.export'
        path_mess = paths_dic['MESS'] + f'/analysis_{iteration}.mess'
        path_comm = paths_dic['COMM'] + f'/analysis_{iteration}.comm'
        path_A1 = paths_dic['UNV'] + f'/analysis_{iteration}_A1.unv'
        path_A2 = paths_dic['UNV'] + f'/analysis_{iteration}_A2.unv'
        path_A3 = paths_dic['UNV'] + f'/analysis_{iteration}_A3.unv'
        path_A4 = paths_dic['UNV'] + f'/analysis_{iteration}_A4.unv'
        path_A5 = paths_dic['UNV'] + f'/analysis_{iteration}_A5.unv'
        path_rmed = paths_dic['RMED'] + f'/analysis_{iteration}.rmed'
        path_vtk = paths_dic['VTK'] + f'/analysis_{iteration}.vtk'
        elems_props_current = paths_dic['JSON'] + f'/dct_pgA2_{iteration}.json'
        elems_props_new = paths_dic['JSON'] + f'/dct_pgA2_{iteration + 1}.json'
        
        path_cp_values = paths_dic['RMED'] + f'/cp_values_{iteration}.json'
        
    
        # Data to be written
        temp_dic = {
            'iteration': iteration,
            'main_root': main_root,
            'path_A1': path_A1,
            'path_A2': path_A2,
            'path_A3': path_A3,
            'path_A4': path_A4,
            'path_A5': path_A5,
            'path_elems_criteria': path_elems_criteria,
            'path_rmed': path_rmed,
            'path_vtk': path_vtk,
            'elems_props_new': elems_props_new,
            'elems_props_current': elems_props_current,
            'path_cp_values': path_cp_values,
            'path_Eevo': path_Eevo,
            'Encc': Encc,
            'Eecc': Eecc,
            'Eecc0': Eecc,
            'Ecc': Eecc,
            'Nuncc': Nuncc,
            'Nuecc': Nuecc,
            'Emin': Encc,
            'Emax': Eecc,
            'Fy': Fyi,
            'h1': h1,
            'l2': L,
            'lcontour':lcontour,
            'kappa':kappa,
            'koi':koii,
            'repertoire':main_root + '/'+ nameficheroi,
            'fichier_folder':case_name+'/'+foldersave,
    
        }
    
        # Serializing json 
        json_object = json.dumps(temp_dic, indent = 4)
        
        # Writing to sample.json
        with open(paths_dic['json_input_data'], "w") as outfile:
            outfile.write(json_object)
        
    
        # Create export files with parameters for code_aster
        with open(path_export, 'w') as file:
            text = export_template(aster_root, path_comm, path_mess)
            file.write(text)
    
        # creat file .comm
        with open('contact_oi_model.comm', 'r') as file : 
            filedata = file.read()     
       
        with open(path_comm, 'w') as file:
            file.write(filedata)
    
        # creat mesh using GMSH
        if iteration_all==0: # as geomtry does not change, we can use an unique geometry during the whole process
            path_A1o=copy.copy(path_A1)
            path_A3o=copy.copy(path_A3)
            path_A5o=copy.copy(path_A5)
        
        mesh_A1A2A3A4A5.A1(path_A1,path_A1o,iteration_all,str(pathlib.Path(__file__).parent.resolve()) +'/'+case_name+'/parameters.json', disp_mesh = 0, mtype = 5, res = 7, localRefine = 1)
        mesh_A1A2A3A4A5.A3(path_A3,path_A3o,iteration_all,str(pathlib.Path(__file__).parent.resolve()) +'/'+case_name+'/parameters.json', disp_mesh = 0, mtype = 5, res = 15, localRefine = 1)
        mesh_A1A2A3A4A5.A5(path_A5,path_A5o,iteration_all,str(pathlib.Path(__file__).parent.resolve()) +'/'+case_name+'/parameters.json', disp_mesh = 0, mtype = 5, res = 15, localRefine = 1)
        
    
        # run the simulation
        run_file = path_export
        aster_run = Popen(aster_root+ " " + run_file, shell='True', executable="/bin/sh")
        aster_run.wait()
        
        # Get results
        x = list()# x-cooordinate of contact points
        cp = list()# Contact pressure
        with open(path_cp_values,"r") as jsonfile:
            file = json.load(jsonfile)
    
        for key in file:
            if key!="energy_defor" and key!='s_mises_max'and key!='oi_seuil'and key!='necartilage':
                x.append(float(key))
                cp.append(file[key])
       
        # Expected uniform pressure
        punif=0*np.array(cp) 
        for jjj in range(0,len(punif)):
            punif[jjj]=-Fy/L                             
        #store data
        max_cp = max(cp)
        cp=np.array(cp)
        maxcp=np.append(maxcp,np.max(cp))
        enercp=np.append(enercp,file["energy_defor"])
        smises=np.append(smises,file["s_mises_max"])
      
        if num==0: # contact pressure while all elements are ossified
            cpoo=copy.copy((np.array(cp)).tolist())                
        if num==1:# contact pressure while all elements are NOT ossified
            cpo1=copy.copy((np.array(cp)).tolist())           
        relaRe=((max(cpoo)-punif[0])-(max_cp-punif[0]))/(max(cpoo)-punif[0])*100 # compute quality indicator Q
        varcp=np.append(varcp,relaRe)                                
    
        # DRAW AND SAVE FIGURES
        plt.figure(1)
    
        if num==0:
           plt.plot(x,punif,'k--',label='Uniform pressure')
           plt.plot(x,cp,'r',label='Mat-design-all-ossified')  
        if num==1:
           plt.plot(x,cp,'k',label='Mat-design-all-non-ossified')  
    
        plt.xlabel(r'Radius (mm)')
        plt.ylabel(r'Contact stress (MPa)')
        plt.title(r'Contact pressure vs radius')
        if num==maxnum-1:
           plt.plot(x,cp,'b',linewidth=num/10+0.05,label= 'final iteration')
        elif num>=1:
           plt.plot(x,cp,'b-',linewidth=num/10+0.05)           
        plt.xlim(0,L+10)
        #ax.legend(prop=font)
        plt.legend()
        
        plt.savefig(case_name+'/'+foldersave +'/pressure_Fy'+str(int(-Fy))+'_koi'+str(koii)+'_Ecartilage'+str(int(Encc/1000))+'GPa.eps')
    
        
        plt.figure(3)
        plt.plot(maxcp,'-bo')
        plt.title('max contact pressure vs iteration')
        plt.ylabel('Maximal pressure (MPa)')
        plt.xlabel('iteration')
        plt.savefig(case_name+'/'+foldersave +'/maxpressure_Fy'+str(int(-Fy))+'_koi'+str(koii)+'_Ecartilage'+str(int(Encc/1000))+'GPa.eps')
    
    
        plt.figure(4)
        plt.plot(enercp,'-bo')
        plt.xlabel('iteration')
        plt.ylabel('Deformation energy(J)')
        plt.title('deformation energy vs iteration')
        plt.savefig(case_name+'/'+foldersave +'/deformationEner_Fy'+str(int(-Fy))+'_koi'+str(koii)+'_Ecartilage'+str(int(Encc/1000))+'GPa.eps')
        plt.figure(5)
        plt.plot(smises,'-bo')
        plt.xlabel('iteration')
        plt.ylabel('Max Von Mises Stress(MPa)')
        plt.title('Max Von Mises Stress vs iteration')
        plt.savefig(case_name+'/'+foldersave +'/vonmises_Fy'+str(int(-Fy))+'_koi'+str(koii)+'_Ecartilage'+str(int(Encc/1000))+'GPa.eps')
    
        plt.figure(6)
        plt.plot(varcp,'-bo')
        plt.title('Q vs iteration')
        plt.xlabel('iteration')
        plt.savefig(case_name+'/'+foldersave +'/qualityIndicatorQ_Fy'+str(int(-Fy))+'_koi'+str(koii)+'_Ecartilage'+str(int(Encc/1000))+'GPa.eps')
       
        iteration_all=iteration_all+1
        
        # condition to stop simulation
        res1= file['necartilage']# number of cartilage elements
    
        if np.abs(res1-reso)<=2 and iteration>=10: 
            break
        reso=copy.copy(res1) 
    return x,cpoo,cpo1,cp
