import gmsh
import json
import sys
import shutil
import numpy as np

n = 1

def A1(path,patho,iterationall,jsonfile, disp_mesh = 0, mtype = 5, res = 10, localRefine = 1):
    
    if iterationall==0:
        with open(jsonfile) as f:
            jsonData = json.load(f)
        lc = jsonData['lc']
        l1 = jsonData['l1']
        l2 = jsonData['l2']
        h1 = jsonData['h1']
        h2 = jsonData['h2']
        h3 = jsonData['h3']
        h4 = jsonData['h4']
        h5 = jsonData['h5']
        h0 = jsonData['h0']
        
   
        gmsh.initialize()
        gmsh.model.add('mesh')
    
        factory = gmsh.model.geo
    # Create the first zone
        p1 = factory.addPoint(0, 0, 0, lc/n, 10)
        p2 = factory.addPoint(l1, 0, 0, lc/n, 20)
        p3 = factory.addPoint(l1, h1, 0, lc/n, 30)
        p4 = factory.addPoint(0, h1, 0, lc/n, 50)
    
        L1 = factory.addLine(p1, p2, 60)
        L2 = factory.addLine(p2, p3, 70)
        L3 = factory.addLine(p3, p4, 80)
        L4 = factory.addLine(p4, p1, 90)
    #    factory.mesh.setTransfiniteCurve(L1, int(l1/lc*2))
        factory.mesh.setTransfiniteCurve(L4, int(h1/lc*2))    
        factory.mesh.setTransfiniteCurve(L1, int(l1/lc*2))
        factory.mesh.setTransfiniteCurve(L3, int(l1/lc*2))
        factory.mesh.setTransfiniteCurve(L2, int(h1/lc*2))
        clA1 = factory.addCurveLoop([L1,L2,L3,L4], 110)
        psA1 = factory.addPlaneSurface([clA1], 120)
    
     # Create the second zone
        p7 = factory.addPoint(l1, h1 + h2, 0, lc/n, 230)
        p8 = factory.addPoint(0, h1 + h2, 0, lc/n, 240)
        
      
        L6 = factory.addLine(p4, p8, 280)
        L7 = factory.addLine(p8, p7, 290)
    #    L7=factory.addCircleArc(p7, pcenter,p8, 290)
        L8 = factory.addLine(p7, p3, 300)
    
        factory.mesh.setTransfiniteCurve(L8, int(h2/lc*2))   
        factory.mesh.setTransfiniteCurve(L6, int(h2/lc*2))  
        factory.mesh.setTransfiniteCurve(L7, int(l1/lc*2))       
        
        clA2 = factory.addCurveLoop([L3,L6,L7,L8], 340)
        psA2 = factory.addPlaneSurface([clA2], 360) 
        
     
        p32 = factory.addPoint(l1, -h0, 0, lc/n, 31)
        p42 = factory.addPoint(0, -h0, 0, lc/n, 51)    
        L22 = factory.addLine(p2, p32, 71)
        L32 = factory.addLine(p32, p42, 81)
        L42 = factory.addLine(p42, p1, 91)    
    
        factory.mesh.setTransfiniteCurve(L22, int(h0/lc))   
        factory.mesh.setTransfiniteCurve(L32, int(l1/lc))  
        factory.mesh.setTransfiniteCurve(L42, int(h0/lc))   
    
        clA0 = factory.addCurveLoop([L1,L22,L32,L42], 341)
        psA0 = factory.addPlaneSurface([clA0], 361)     
        
        gmsh.option.setNumber("Mesh.Algorithm", mtype)
    
        # gmsh.model.mesh.setRecombine(2, psA21)
        gmsh.option.setNumber("Mesh.RecombineAll", 1)    
        
        
    
        pgFixed = gmsh.model.addPhysicalGroup(1, [L32], 130)
        pgSymA1 = gmsh.model.addPhysicalGroup(1, [L4,L42], 150)
        pgSymA11 = gmsh.model.addPhysicalGroup(1, [L2,L22], 151)
        pgA1 = gmsh.model.addPhysicalGroup(2, [psA1], 160)
    
    
        pnFixed = gmsh.model.setPhysicalName(1, pgFixed, "pgFixed")
        pnSymA1 = gmsh.model.setPhysicalName(1, pgSymA1, "pgSymA1")
        pnSymA11 = gmsh.model.setPhysicalName(1, pgSymA11, "pgSymA11")
        pgA2 = gmsh.model.addPhysicalGroup(2, [psA2], 161)
        pgA0 = gmsh.model.addPhysicalGroup(2, [psA0], 162)
        pnA0= gmsh.model.setPhysicalName(2, pgA0, "pgA0")
        pnA1 = gmsh.model.setPhysicalName(2, pgA1, "pgA1")
        pnA2 = gmsh.model.setPhysicalName(2, pgA2, "pgA2")
    
        pgCtA2 = gmsh.model.addPhysicalGroup(1, [L7], 390)
    
        pgSymA2 = gmsh.model.addPhysicalGroup(1, [L6], 400)
        pgSymA22 = gmsh.model.addPhysicalGroup(1, [L8], 401)
    
    
        pnCtA2 = gmsh.model.setPhysicalName(1, pgCtA2, "pgCtA2")
        pnSymA2 = gmsh.model.setPhysicalName(1, pgSymA2, "pgSymA2")
        pnSymA22 = gmsh.model.setPhysicalName(1, pgSymA22, "pgSymA22")
    
        factory.synchronize()
        gmsh.model.mesh.generate(2)   
    
    
        mesh_name = 'mesh' + '.unv'
        WRITE_unv = gmsh.write(mesh_name)
    
        if disp_mesh:
            if '-nopopup' not in sys.argv:
                gmsh.fltk.run()
    
        gmsh.finalize()
        shutil.move(mesh_name,path)
    else:
        shutil.copy(patho,path) 




def A3(path,patho,iterationall,jsonfile, disp_mesh = 0, mtype = 5, res = 10, localRefine = 1):
    if iterationall==0:
    
        with open(jsonfile) as f:
            jsonData = json.load(f)
        lc = jsonData['lc']
        l1 = jsonData['l1']
        l2 = jsonData['l2']
        h1 = jsonData['h1']
        h2 = jsonData['h2']
        h3 = jsonData['h3']
        h4 = jsonData['h4']
        h5 = jsonData['h5']
        
    
        gmsh.initialize()
        gmsh.model.add('mesh')
    
        factory = gmsh.model.geo
        
        p10 = factory.addPoint(0, h1+h2, 0, lc/n, 2100)
        p11 = factory.addPoint(l2, h1+h2, 0, lc/n, 2200)
       
        
        p12 = factory.addPoint(l2, h1+h2+h3, 0, lc/n, 2300)
        p13 = factory.addPoint(0, h1+h2+h3, 0, lc/n, 2400)
    
    #    L10 = factory.addCircleArc(p10, pcenter,p11, 2700)
        L10 = factory.addLine(p10, p11, 2700)
        L11 = factory.addLine(p11, p12, 2800)
        L12 = factory.addLine(p12, p13, 2900)
    #    L12=factory.addCircleArc(p12, pcenter,p13, 2900)
        L13 = factory.addLine(p13, p10, 3000)
    
        factory.mesh.setTransfiniteCurve(L10, int(l2/lc*2))
        factory.mesh.setTransfiniteCurve(L12, int(l2/lc*2))   
        factory.mesh.setTransfiniteCurve(L11, int(h2/lc*2))
        factory.mesh.setTransfiniteCurve(L13, int(h2/lc*2))   
        clA3 = factory.addCurveLoop([L10, L11,L12,L13], 3400)
        psA3 = factory.addPlaneSurface([clA3], 3600)
    
    #%%
        p16 = factory.addPoint(l2, h1 + h2 + h3 + h4, 0, lc/n, 23000)
        p17 = factory.addPoint(0, h1 + h2 + h3 + h4, 0, lc/n, 24000)     
        L15 = factory.addLine(p13, p17, 28000)
        L16 = factory.addLine(p17, p16, 28001)
        L17 = factory.addLine(p16, p12, 30000)
    
        factory.mesh.setTransfiniteCurve(L16, int(l2/lc)*2)
        factory.mesh.setTransfiniteCurve(L15, int(h4/lc*2))         
        factory.mesh.setTransfiniteCurve(L17, int(h4/lc*2))       
        
        
        clA4 = factory.addCurveLoop([L12, L15,L16,L17], 34000)
        psA4 = factory.addPlaneSurface([clA4], 36000)
        
        factory.synchronize()
    
    
        gmsh.option.setNumber("Mesh.Algorithm", mtype)
    
       
        gmsh.option.setNumber("Mesh.RecombineAll", 1)
    
        MESH = gmsh.model.mesh.generate(2)
    
    
        pgCtA3 = gmsh.model.addPhysicalGroup(1, [L10], 3900)
        pgSymA3 = gmsh.model.addPhysicalGroup(1, [L13], 4000)
        pgSymA33 = gmsh.model.addPhysicalGroup(1, [L11], 4001)
        pgA3 = gmsh.model.addPhysicalGroup(2, [psA3], 4200)
    
    
        pnCtA3 = gmsh.model.setPhysicalName(1, pgCtA3, "pgCtA3")
        pnSymA3 = gmsh.model.setPhysicalName(1, pgSymA3, "pgSymA3")
        pnSymA33 = gmsh.model.setPhysicalName(1, pgSymA33, "pgSymA33")
        pnA3 = gmsh.model.setPhysicalName(2, pgA3, "pgA3")
    
    
        pgColA42 = gmsh.model.addPhysicalGroup(1, [L16], 39000)
        pgSymA4 = gmsh.model.addPhysicalGroup(1, [L15], 40000)
        pgSymA44 = gmsh.model.addPhysicalGroup(1, [L17], 40001)
        pgA4 = gmsh.model.addPhysicalGroup(2, [psA4], 42000)
    
    
        pnColA42 = gmsh.model.setPhysicalName(1, pgColA42, "pgColA42")
        pnSymA4 = gmsh.model.setPhysicalName(1, pgSymA4, "pgSymA4")
        pnSymA44 = gmsh.model.setPhysicalName(1, pgSymA44, "pgSymA44")
        pnA4 = gmsh.model.setPhysicalName(2, pgA4, "pgA4")
    
    
    
    ##
        mesh_name = 'mesh' + '.unv'
        WRITE_unv = gmsh.write(mesh_name)
    
        if disp_mesh:
            if '-nopopup' not in sys.argv:
                gmsh.fltk.run()
    
        gmsh.finalize()
        shutil.move(mesh_name,path)
    else:
        shutil.copy(patho,path)    


def A5(path,patho,iterationall,jsonfile, disp_mesh = 0, mtype = 5, res = 10, localRefine = 1):
    if iterationall==0:
        with open(jsonfile) as f:
            jsonData = json.load(f)
        lc = jsonData['lc']
        l1 = jsonData['l1']
        l2 = jsonData['l2']
        h1 = jsonData['h1']
        h2 = jsonData['h2']
        h3 = jsonData['h3']
        h4 = jsonData['h4']
        h5 = jsonData['h5']
        lcontour = jsonData['lcontour']
    
        gmsh.initialize()
        gmsh.model.add('mesh')
    
        factory = gmsh.model.geo
    
        p18 = factory.addPoint(0, h1 + h2 + h3 + h4, 0)
        p19 = factory.addPoint(l2, h1 + h2 + h3 + h4, 0)
        p20 = factory.addPoint(l2, h1 + h2 + h3 + h4 + h5, 0)
        p201 = factory.addPoint(lcontour, h1 + h2 + h3 + h4 + h5, 0)
        
        p21 = factory.addPoint(0, h1 + h2 + h3 + h4 + h5, 0)
    
        L18 = factory.addLine(p18, p19, 270000)
        L19 = factory.addLine(p19, p20, 280000)
        L20 = factory.addLine(p20, p201, 290000)
        L201 = factory.addLine(p201, p21, 290001)
        
        L21 = factory.addLine(p21, p18, 30000)
    
        clA5 = factory.addCurveLoop([L18, L19,L20,L201,L21], 340000)
        psA5 = factory.addPlaneSurface([clA5], 360000)
    
        factory.mesh.setTransfiniteCurve(L18, max(3,int(l2/lc)*2))
        factory.mesh.setTransfiniteCurve(L20, max(3,int((l2-lcontour)/lc)*2))
        factory.mesh.setTransfiniteCurve(L201, max(3,int((lcontour)/lc)*2))
        factory.mesh.setTransfiniteCurve(L19, max(3,int(h5/lc)*2))
        factory.mesh.setTransfiniteCurve(L21, max(3,int(h5/lc)*2))
        factory.synchronize()
    

        gmsh.option.setNumber("Mesh.Algorithm", mtype)
    
        # gmsh.model.mesh.setRecombine(2, psA21)
        gmsh.option.setNumber("Mesh.RecombineAll", 1)
    
    
    
        MESH = gmsh.model.mesh.generate(2)
    
        pgColA5 = gmsh.model.addPhysicalGroup(1, [L18], 380000)
        pgLoad = gmsh.model.addPhysicalGroup(1, [L201], 390000)
        pgSymA5 = gmsh.model.addPhysicalGroup(1, [L21], 40000)
        pgSymA55 = gmsh.model.addPhysicalGroup(1, [L19], 41000)
        pgA5 = gmsh.model.addPhysicalGroup(2, [psA5], 42000)
    
        pnColA5 = gmsh.model.setPhysicalName(1, pgColA5, "pgColA5")
        pnLoad = gmsh.model.setPhysicalName(1, pgLoad, "pgLoad")
        pnSymA5 = gmsh.model.setPhysicalName(1, pgSymA5, "pgSymA5")
        pnSymA55 = gmsh.model.setPhysicalName(1, pgSymA55, "pgSymA55")
        pnA5 = gmsh.model.setPhysicalName(2, pgA5, "pgA5")
    
        mesh_name = 'mesh' + '.unv'
        WRITE_unv = gmsh.write(mesh_name)
    
        if disp_mesh:
            if '-nopopup' not in sys.argv:
                gmsh.fltk.run()
    
        gmsh.finalize()
        shutil.move(mesh_name,path)    
    else:
        shutil.copy(patho,path)         
        
