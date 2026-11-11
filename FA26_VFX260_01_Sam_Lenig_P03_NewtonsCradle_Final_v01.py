##########################################################################################
# FA26_VFX260_01_Sam_Lenig_P03_NewtonsCradle_Final_v01
# Creating an animated Newton's Cradle scene
# by Sam Lenig
# Date Started: 2026-10-28
# Latest Modification: 2026-11-5
##########################################################################################

##########################################################################################
# SAFETY CHECK: Allows the script to run safely inside Maya or use a mock setup outside
##########################################################################################
                                                                                         #
try:                                                                                     #
    import maya.cmds as cmds                                                             #
    IN_MAYA = True                                                                       #
except ImportError:                                                                      #
    IN_MAYA = False                                                                      #
                                                                                         #
                                                                                         #
    class MockCmds:                                                                      #
        def __getattr__(self, name):                                                     #
            def mock(*args, **kwargs):                                                   #
                print(f"[MOCK] cmds.{name}({args}, {kwargs})")                           #
                return ["mock_result"]                                                   #
            return mock                                                                  #
                                                                                         #
    cmds = MockCmds()                                                                    #
                                                                                         #
                                                                                         #
##########################################################################################
##########################################################################################
##########################################################################################

import mtoa as ai 
from mtoa.core import createOptions

# global project prefix added to all generated assets
PFX = "SSL_"

# set up timeline playback options
cmds.playbackOptions(minTime=1, maxTime=210)
cmds.playbackOptions(animationStartTime=1, animationEndTime=210)

# rendering information
startFrame = 0
endFrame = 201
fullWidth = 1920
fullHeight = 1080
renderScale = 0.5
width = int(fullWidth * renderScale)
height = int(fullHeight * renderScale)
aspectRatio = width / height


def cleanupscene():
    # deletes any old objects in the scene that start with my prefix
    if cmds.objExists(PFX + "*"):
        cmds.delete(PFX + "*")


def sphere_mato():
    # builds the entire tomato: body sphere, leaf, and stem, then groups them

    # creates shape the main tomato body sphere
    Mato = cmds.polySphere(n=f"{PFX}sphere_mato01", radius=60, subdivisionsX=15, subdivisionsY=15)[0]
    cmds.select(Mato)
    cmds.scale(1, 0.836694, 1, relative=True)
    cmds.move(0, 52.503099, 0, relative=True)
    pivot_1 = (0.623489, 85.360506, 1.90735e-06) # sets the transform pivot which is important for the expressions to looks right
    
    # push and pull specific faces to give the tomato a stylized shape
    cmds.select(f"{Mato}.f[105:194]", f"{Mato}.f[210:224]") 
    cmds.scale(1, 0.676012, 1, relative=True, pivot=pivot_1)
    cmds.scale(1.032354, 1.032354, 1.032354, relative=True, pivot=pivot_1)
    cmds.move(0, -3.459121, 0, relative=True)
    
    pivot_2 = (16.281059, 88.660112, 0.79125)
    cmds.select([f"{Mato}.f[165:166]", f"{Mato}.f[175:181]", f"{Mato}.f[190:194]", f"{Mato}.f[210:211]", f"{Mato}.f[220:224]"], replace=True)
    cmds.scale(1, 0.603688, 1, relative=True, pivot=pivot_2)
    cmds.select(f"{Mato}.f[105:119]")
    cmds.scale(.99, .99, .99, relative=True, pivot=(0.966897, 0.966897, 0.966897))
    cmds.select(clear=True)
    
    # building the leafy top section
    Leaf = cmds.polyCylinder(n=f"{PFX}mato_leaf", radius=50, height=7, sc=1, sa=14)[0]
    cmds.select(
        f"{Leaf}.vtx[6]", f"{Leaf}.vtx[20]", f"{Leaf}.vtx[4]", f"{Leaf}.vtx[18]",
        f"{Leaf}.vtx[2]", f"{Leaf}.vtx[16]", f"{Leaf}.vtx[0]", f"{Leaf}.vtx[14]",
        f"{Leaf}.vtx[12]", f"{Leaf}.vtx[26]", f"{Leaf}.vtx[10]", f"{Leaf}.vtx[24]",
        f"{Leaf}.vtx[8]", f"{Leaf}.vtx[22]"
    )

    cmds.scale(3, 1, 3, relative=True)
    cmds.select(Leaf)
    cmds.scale(0.312484, 0.312484, 0.312484)
        
    cmds.select(f"{Leaf}.vtx[28:29]")
    cmds.scale(0, 0, 0, pivot=(1, 2.615879, 1))
    cmds.select(Leaf)
    cmds.move(0, 92, 0)
    cmds.select(clear=True)
  
    # builds the stem piece on top of the tomato
    Stem = cmds.polyCylinder(n=f"{PFX}mato_stem", radius=8, height=42, sc=1, sa=11, sh=2)[0]
    cmds.select(f"{Stem}.e[0:10]")
    cmds.scale(0.5, 1, 0.5, relative=True, pivot=(0, 50, 0))
    cmds.select(f"{Stem}.f[22:32]")
    cmds.move(5.13015, 0, 5.372986, relative=True)
    cmds.select(Stem)
    cmds.move(0, 110, 0, relative=True)
    cmds.select(Stem)
    cmds.move(-3.121665, 0, -5.488758, relative=True)
    cmds.select(f"{Stem}.f[33:43]")
    cmds.scale(1.5, 1, 1.5, relative=True, pivot=(0, 50, 0))
    cmds.select(Stem)
    cmds.scale(.7, .7, .7, relative=True)
    
    # groups everything together and freeze its transforms
    round_mato = cmds.group(Mato, Leaf, Stem, n=f"{PFX}round_mato")
    cmds.select(f"{round_mato}")
    cmds.makeIdentity(f"{round_mato}", apply=True, t=True, r=True, s=True)
    cmds.makeIdentity(apply=True, t=True, r=True, s=True)


def newtons_mato():
    # builds the swinging pendulumn pieces of the newtons cradle by duplicating the mato's!!!!
    
    # creates the first string and puts it in place
    string_01 = cmds.polyCylinder(n=f"{PFX}string_01", radius=2, height=250, sc=0, sa=6)[0]
    cmds.select(string_01)
    cmds.rotate(35, 0, 0, relative=True, objectSpace=True)
    cmds.move(0, 180, 56, relative=True)

    # creates the second string
    string_02 = cmds.polyCylinder(n=f"{PFX}string_02", radius=2, height=250, sc=0, sa=6)[0]
    cmds.select(string_02)
    cmds.rotate(-35, 0, 0, relative=True, objectSpace=True)
    cmds.move(0, 180, -68, relative=True)

    #groups the string
    strings = cmds.group(string_01, string_02, n=f"{PFX}strings")
    
    # groups the first swinging unit and set its pivot point
    swinging_group = cmds.group(f"{PFX}round_mato", strings, n=f"{PFX}swing_mato_01")
    all_swings = [swinging_group]
    cmds.xform(swinging_group, piv=(0, 290, 0), ws=True) # resetting pivot point for expression usage
    
    # defines offsets so the tomatoes are evenly spaced when duplicated
    offsets = [118, 234, 350, -120]

    # duplication loop
    for i, offset in enumerate(offsets, start=2): #loops through my offsets list 
        dup_name = f"{PFX}swing_mato_0{i}" # creates a set name for each duplication, based off which enumerate the loop is on the number after 0 will change
        new_mato = cmds.duplicate(swinging_group, n=dup_name)[0] # duplicates the swinging group from earlier, ensuring that only the transform information is used
        cmds.select(new_mato, replace=True)
        cmds.move(offset, 0, 0, relative=True) # moves based off the offset
        all_swings.append(new_mato) # stores the new information so the function can keep track and put everything into one big final group 
        
    # group all cradles into a master group
    cmds.group(all_swings, n=f"{PFX}mato_cradle_group") 
    cmds.select(clear=True) 
    

def pot():
    # creates the flower pot, hollows it out, and extracts the top faces for soil

    pot = cmds.polyCylinder(n=f"{PFX}pot_01", radius=32, height=45, sc=2, sa=18)[0]
    cmds.select(pot)
    cmds.move(0, 45, 0, relative=True)
    cmds.select(f"{pot}.f[0:17]", f"{pot}.f[54:71]")
    cmds.scale(.7, .7, .7, pivot=(0.824556, 0.824556, 0.824556))
    cmds.select(f"{pot}.f[0:17]", f"{pot}.f[54:71]")
    cmds.move(0, 6.883818, 0, relative=True)

    # shapes the rim of the pot
    cmds.select(f"{pot}.f[72:89]", f"{pot}.f[36:53]")
    cmds.polyExtrudeFacet()
    cmds.scale(1.2, 1.2, 1.2, pivot=(1.203874, 1.203874, 1.203874))
    cmds.select(f"{pot}.f[72:89]", f"{pot}.f[36:53]")
    cmds.move(0, -12.916502, 0, relative=True)
    cmds.select(f"{pot}.f[72:89]", f"{pot}.f[36:53]")
    cmds.polyExtrudeFacet()
    cmds.move(0, 13.783687, 0, relative=True)
    cmds.select(f"{pot}.f[72:89]", f"{pot}.f[36:53]")
    cmds.polyExtrudeFacet()
    cmds.scale(.8, .8, .8, pivot=(0.900314, 0.900314, 0.900314))
    cmds.select(f"{pot}.f[72:89]", f"{pot}.f[36:53]")
    cmds.move(0, 15.834149, 0, relative=True)
    cmds.polyExtrudeFacet()
    cmds.move(0, -5.460221, 0, relative=True)
    
    top_faces_expression = [f"{pot}.f[72:89]", f"{pot}.f[36:53]"]


############# transparency , google gemini helped me with this work around because extracting faces would not work

    soil = cmds.duplicate(pot, n=f"{PFX}pot_soil")[0] # duplicates the original pot and renames the duplication
    all_soil_faces = cmds.ls(f"{soil}.f[*]", flatten=True) # makes maya list each face on the pot and put them in an individual list of every single face name separately for easy selection, makes identification easier 
    top_faces_soil = [f.replace(pot, soil) for f in cmds.ls(top_faces_expression, flatten=True)] #look at the top rim face selection from the original pot, takes those original face names and swaps out the pot's name for the soil's name, creating a matching list of face components that correspond
    faces_to_delete_on_soil = [f for f in all_soil_faces if f not in top_faces_soil] #  Filters through all_soil_faces and creates a list of everything except the top faces top_faces_soil
    cmds.delete(faces_to_delete_on_soil) # deletes the isolated faces which is the side walls and bottom
    
    
    cmds.delete(top_faces_expression) # delete top faces on the original pot so it's hollow
    cmds.select(clear=True)


def vine():
    # builds twisting vines and side twigs extending out of the pot
    # briding did not work for this, maya I hate you
    vine = cmds.polyCylinder(n=f"{PFX}vine_01", radius=7, height=10, sc=0, sa=10)[0]
    
    cmds.select(f"{PFX}vine_01.e[0:9]")
    cmds.move(0, -13, 0, relative=True)
    
    # extrude and shape the main vine path upwards
    cmds.select(f"{vine}.f[10]")
    cmds.delete()
    cmds.select(f"{vine}.f[10]")
    cmds.delete()
    cmds.select(f"{vine}.e[10:19]")
    cmds.move(-4.046148, 3.909573, 0, relative=True)
    cmds.select(f"{vine}.e[10:19]")
    cmds.polyExtrudeEdge()
    cmds.move(0, 14.791642, 0, relative=True)
    cmds.select(f"{vine}.e[32]", f"{vine}.e[34]", f"{vine}.e[36]", f"{vine}.e[38]", f"{vine}.e[40]", f"{vine}.e[42]", f"{vine}.e[44]", f"{vine}.e[46]", f"{vine}.e[48:49]")
    cmds.polyExtrudeEdge()
    cmds.move(0, 37.97603, -1.419562, relative=True)

    # duplicated the beginning section of the vine and moves them aside for later so they can become twigs
    cmds.select(vine)
    twig01 = cmds.duplicate(vine, n=f"{PFX}twig_01")[0]
    cmds.select(twig01)
    cmds.move(43.654404, 0, 84.322288, relative=True)
    
    cmds.select(vine)
    twig02 = cmds.duplicate(vine, n=f"{PFX}twig_02")[0]
    cmds.select(twig02)
    cmds.move(1, 0, 80, relative=True)
    
    # continues extruding the main vine with rotations and scaling
    cmds.select(f"{vine}.e[52]", f"{vine}.e[54]", f"{vine}.e[56]", f"{vine}.e[58]", f"{vine}.e[60]", f"{vine}.e[62]", f"{vine}.e[64]", f"{vine}.e[66]", f"{vine}.e[68:69]")
    cmds.polyExtrudeEdge()
    cmds.move(0, 34.745235, 8.835614, relative=True)
    
    cmds.select(f"{vine}.e[72]", f"{vine}.e[74]", f"{vine}.e[76]", f"{vine}.e[78]", f"{vine}.e[80]", f"{vine}.e[82]", f"{vine}.e[84]", f"{vine}.e[86]", f"{vine}.e[88:89]")
    cmds.polyExtrudeEdge()
    cmds.move(2.904638, 62.506939, 9.811961, relative=True)
    
    cmds.select(f"{vine}.e[92]", f"{vine}.e[94]", f"{vine}.e[96]", f"{vine}.e[98]", f"{vine}.e[100]", f"{vine}.e[102]", f"{vine}.e[104]", f"{vine}.e[106]", f"{vine}.e[108:109]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(0, 25, 10, relative=True)
    cmds.scale(0.902896, 0.902896, 0.902896, relative=True, pivot=(-1.14151, 203.008301, 16.070943))
    # more vine work
    cmds.select(f"{vine}.e[112]", f"{vine}.e[114]", f"{vine}.e[116]", f"{vine}.e[118]", f"{vine}.e[120]", f"{vine}.e[122]", f"{vine}.e[124]", f"{vine}.e[126]", f"{vine}.e[128:129]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(0, 6, 0, relative=True)
    cmds.scale(0.902896, 0.902896, 0.902896, relative=True, pivot=(-1.14151, 203.008301, 16.070943))
 
    cmds.select(f"{vine}.e[132]", f"{vine}.e[134]", f"{vine}.e[136]", f"{vine}.e[138]", f"{vine}.e[140]", f"{vine}.e[142]", f"{vine}.e[144]", f"{vine}.e[146]", f"{vine}.e[148:149]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(0, 6, -1, relative=True)
    cmds.rotate(-31.099742, 0, 0, relative=True, pivot=(-1.14151, 195.999512, 25.757348), objectSpace=True, forceOrderXYZ=True)    
    cmds.scale(0.902896, 0.902896, 0.902896, relative=True, pivot=(-1.14151, 203.008301, 16.070943))

    cmds.select(f"{vine}.e[152]", f"{vine}.e[154]", f"{vine}.e[156]", f"{vine}.e[158]", f"{vine}.e[160]", f"{vine}.e[162]", f"{vine}.e[164]", f"{vine}.e[166]", f"{vine}.e[168:169]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(2, 6, -1, relative=True)
    cmds.rotate(-31.099742, 0, 0, relative=True, pivot=(-1.14151, 195.999512, 25.757348), objectSpace=True, forceOrderXYZ=True)    
    
    cmds.select(f"{vine}.e[172]", f"{vine}.e[174]", f"{vine}.e[176]", f"{vine}.e[178]", f"{vine}.e[180]", f"{vine}.e[182]", f"{vine}.e[184]", f"{vine}.e[186]", f"{vine}.e[188:189]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(4, 6, -1, relative=True)
    cmds.rotate(-31.099742, 0, 0, relative=True, pivot=(-1.14151, 195.999512, 25.757348), objectSpace=True, forceOrderXYZ=True)    
    # you guessed it, more vine work
    cmds.select(f"{vine}.e[192]", f"{vine}.e[194]", f"{vine}.e[196]", f"{vine}.e[198]", f"{vine}.e[200]", f"{vine}.e[202]", f"{vine}.e[204]", f"{vine}.e[206]", f"{vine}.e[208:209]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.rotate(-31.099742, 0, 0, relative=True, pivot=(-1.14151, 195.999512, 25.757348), objectSpace=True, forceOrderXYZ=True)    
    cmds.rotate(0, -26.869234, 0, relative=True, pivot=(8.45849, 198.651245, 9.727483), objectSpace=True, forceOrderXYZ=True)
    cmds.scale(0.7, 0.7, 0.7, relative=True, pivot=(-1.14151, 203.008301, 16.070943))
    cmds.move(9, 2, -5, relative=True)

    cmds.select(f"{vine}.e[212]", f"{vine}.e[214]", f"{vine}.e[216]", f"{vine}.e[218]", f"{vine}.e[220]", f"{vine}.e[222]", f"{vine}.e[224]", f"{vine}.e[226]", f"{vine}.e[228:229]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(7, 6, -4, relative=True)
    cmds.rotate(-31.099742, 0, 0, relative=True, pivot=(-1.14151, 195.999512, 25.757348), objectSpace=True, forceOrderXYZ=True)    
    cmds.scale(0.8, 0.8, 0.8, relative=True, pivot=(-1.14151, 203.008301, 16.070943))
    
    cmds.select(f"{vine}.e[232]", f"{vine}.e[234]", f"{vine}.e[236]", f"{vine}.e[238]", f"{vine}.e[240]", f"{vine}.e[242]", f"{vine}.e[244]", f"{vine}.e[246]", f"{vine}.e[248:249]", replace=True)
    cmds.polyExtrudeEdge()
    cmds.move(7, 6, -2, relative=True)
    cmds.rotate(-31.099742, 0, 0, relative=True, pivot=(-1.14151, 195.999512, 25.757348), objectSpace=True, forceOrderXYZ=True)    
    cmds.scale(0.750832, 0.750832, 0.750832, relative=True, pivot=(14.636409, 194.679001, 6.976342))
    
    cmds.select(f"{vine}.e[252]", f"{vine}.e[254]", f"{vine}.e[256]", f"{vine}.e[258]", f"{vine}.e[260]", f"{vine}.e[262]", f"{vine}.e[264]", f"{vine}.e[266]", f"{vine}.e[268:269]", replace=True)
    cmds.move(0, -3, 3, relative=True) 
    cmds.scale(0.305265, 0.305265, 0.305265, relative=True, pivot=(19.892233, 186.025551, 8.062039))
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
    cmds.select(clear=True)

    # position and style twig 01
    cmds.select(f"{PFX}twig_01.e[52]", f"{PFX}twig_01.e[54]", f"{PFX}twig_01.e[56]", f"{PFX}twig_01.e[58]", f"{PFX}twig_01.e[60]", f"{PFX}twig_01.e[62]", f"{PFX}twig_01.e[64]", f"{PFX}twig_01.e[66]", f"{PFX}twig_01.e[68:69]", add=True)
    cmds.scale(0.3, 0.3, 0.3, relative=True, pivot=(0.175241, 0.175241, 0.175241))
    cmds.select(f"{PFX}twig_01.e[52]", f"{PFX}twig_01.e[54]", f"{PFX}twig_01.e[56]", f"{PFX}twig_01.e[58]", f"{PFX}twig_01.e[60]", f"{PFX}twig_01.e[62]", f"{PFX}twig_01.e[64]", f"{PFX}twig_01.e[66]", f"{PFX}twig_01.e[68:69]", add=True)
    cmds.move(11, 33, 66, relative=True)
    cmds.select(clear=True)
    
    cmds.select(f"{PFX}twig_01.e[32]", f"{PFX}twig_01.e[34]", f"{PFX}twig_01.e[36]", f"{PFX}twig_01.e[38]", f"{PFX}twig_01.e[40]", f"{PFX}twig_01.e[42]", f"{PFX}twig_01.e[44]", f"{PFX}twig_01.e[46]", f"{PFX}twig_01.e[48:49]", add=True)
    cmds.scale(.8, .8, .8, relative=True, pivot=(0.730779, 0.730779, 0.730779))
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
    
    cmds.select(clear=True)
    cmds.select(f"{PFX}twig_01", replace=True)
    cmds.rotate(-90, 0, -60, relative=True, objectSpace=True, fo=True)
    cmds.move(-48, 140, -85, relative=True)
    cmds.scale(0.782653, 0.782653, 0.782653, relative=True)
    cmds.select(clear=True)
   
    # position and style twig 02
    cmds.select(f"{PFX}twig_02.e[52]", f"{PFX}twig_02.e[54]", f"{PFX}twig_02.e[56]", f"{PFX}twig_02.e[58]", f"{PFX}twig_02.e[60]", f"{PFX}twig_02.e[62]", f"{PFX}twig_02.e[64]", f"{PFX}twig_02.e[66]", f"{PFX}twig_02.e[68:69]", add=True)
    cmds.scale(0.3, 0.3, 0.3, relative=True, pivot=(0.175241, 0.175241, 0.175241))
    cmds.select(f"{PFX}twig_02.e[52]", f"{PFX}twig_02.e[54]", f"{PFX}twig_02.e[56]", f"{PFX}twig_02.e[58]", f"{PFX}twig_02.e[60]", f"{PFX}twig_02.e[62]", f"{PFX}twig_02.e[64]", f"{PFX}twig_02.e[66]", f"{PFX}twig_02.e[68:69]", add=True)
    cmds.move(8, 30, 60, relative=True)
    cmds.select(clear=True)
    cmds.select(f"{PFX}twig_02.e[32]", f"{PFX}twig_02.e[34]", f"{PFX}twig_02.e[36]", f"{PFX}twig_02.e[38]", f"{PFX}twig_02.e[40]", f"{PFX}twig_02.e[42]", f"{PFX}twig_02.e[44]", f"{PFX}twig_02.e[46]", f"{PFX}twig_02.e[48:49]", add=True)
    cmds.scale(0.8, 0.8, 0.8, relative=True, pivot=(0.730779, 0.730779, 0.730779))
    cmds.displaySmoothness(divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
  
    cmds.select(clear=True)
    cmds.select(f"{PFX}twig_02", replace=True)
    cmds.rotate(-80, -80, 3, relative=True, objectSpace=True, fo=True)
    cmds.scale(0.8, 0.8, 0.8, relative=True)
    cmds.move(-2, 65, -68, relative=True)
    cmds.rotate(0, 0, -87, relative=True, objectSpace=True, fo=True)
    cmds.select(clear=True)

    # groups vines and twigs into the final potted plant hierarchy
    vine_group = cmds.group(vine, f"{PFX}twig_01", f"{PFX}twig_02", n=f"{PFX}full_vine_01")
    cmds.select(clear=True)
    cmds.select(vine_group)
    cmds.move(0, 92, 0)
    potted_vine_group = cmds.group(f"{PFX}pot_01", f"{PFX}pot_soil", f"{PFX}full_vine_01", n=f"{PFX}Potted_Vine_01")


def skewer():
    # builds and shapes the skewer extruding and uniting meshes
    pole = cmds.polyCylinder(n=f"{PFX}skewer_01", radius=8, height=80, sc=1, sa=10)[0]
    
    # extrudes and modifies a cylinder 
    cmds.select(f"{PFX}skewer_01.f[20:29]")
    cmds.polyExtrudeFacet()
    cmds.scale(.8, .8, .8, pivot=(0.776659, 0.776659, 0.776659))
    cmds.move(0, 9.46864, 0, relative=True)
    cmds.polyExtrudeFacet()
    cmds.move(0, 350, 0, relative=True)
    cmds.polyExtrudeFacet()
    cmds.move(0, 19.003537, -10.781696, relative=True)
    cmds.polyExtrudeFacet()
    cmds.scale(.5, .5, .5, relative=True)
    cmds.move(0, 250, -5, relative=True)
    cmds.select(f"{PFX}skewer_01.vtx[53]")
    cmds.move(0, 15, .3, relative=True)
    
    target_faces = [f"{PFX}skewer_01.f[20:29]", f"{PFX}skewer_01.f[50:59]", f"{PFX}skewer_01.f[60:69]"] # identifies the faces i need duplicated
    
    # Same dupliation process as earlier with the pot, builds 2 pieces of geo and deletes the unneeded faces and used whats left over
    skewer_piece = cmds.duplicate(f"{PFX}skewer_01", n=f"{PFX}skewer_piece")[0]
    all_piece_faces = cmds.ls(f"{skewer_piece}.f[*]", flatten=True)
    keep_faces = [f.replace(f"{PFX}skewer_01", skewer_piece) for f in cmds.ls(target_faces, flatten=True)]
    faces_to_delete = [f for f in all_piece_faces if f not in keep_faces]
    cmds.delete(faces_to_delete)
    cmds.select(clear=True)
    
    cmds.select(skewer_piece)
    cmds.rotate(0, 180, 0)

    # combines the 2 meshes and renames
    combined_skew = cmds.polyUnite(pole, skewer_piece, ch=False)[0]
    combined_skew = cmds.rename(combined_skew, f"{PFX}big_skewer_01")

    
def knife():
    # creates knife and blade to knife
    blade = cmds.polyCube(n=f"{PFX}blade_01", width=45, height=200, depth=5, sh=5)
    
    # shapes the blade by tweaking edges and faces
    cmds.select(f"{PFX}blade_01.e[22]")
    cmds.move(3.648317, 3, 0, relative=True)
    cmds.select(f"{PFX}blade_01.e[23]")
    cmds.move(-32.065842, -7.058928, 0, relative=True)
    cmds.select(f"{PFX}blade_01.e[39]")
    cmds.move(-14, 0, 0, relative=True)
    cmds.select(f"{PFX}blade_01.e[37]")
    cmds.move(3.5, 0, 0, relative=True)
    cmds.select(f"{PFX}blade_01.e[35]")
    cmds.move(-9, 0, 0, relative=True)
    cmds.select(f"{PFX}blade_01.e[34]")
    cmds.move(2, 0, 0, relative=True)
    cmds.select(f"{PFX}blade_01.f[1]", f"{PFX}blade_01.f[9]", f"{PFX}blade_01.f[13]", f"{PFX}blade_01.f[18]")
    cmds.select(f"{PFX}blade_01.f[0]", f"{PFX}blade_01.f[10]", f"{PFX}blade_01.f[12]", f"{PFX}blade_01.f[17]", add=True)
    cmds.scale(1, 1, 1.4, pivot=(1.042727, 1.042727, 1.042727))
    cmds.select(blade)
    cmds.rotate(0, 0, 2.39546, relative=True, objectSpace=True, forceOrderXYZ=True)
    cmds.move(-4.117654, 0, 0, relative=True)
    
    # creates and position the handle cylinder
    handle = cmds.polyCylinder(n=f"{PFX}handle_01", radius=25, height=150, sc=0, sa=12)[0]
    cmds.select(handle)
    cmds.move(0, -171.353553, 0, relative=True)
    cmds.scale(1, 1, .5)

    # groups blade and handle together
    whole_knife = cmds.group(blade, handle, n=f"{PFX}knife_01")
    cmds.select(whole_knife)
    cmds.rotate(0, 0, 13.5, relative=True, objectSpace=True, forceOrderXYZ=True)


def cutting_board():
    # builds a wooden cutting board with a handle cutout and beveled edges
    board = cmds.polyPlane(n=f"{PFX}cutting_board", width=1, height=1, sw=5, sh=5)
    cmds.select(board)
    cmds.scale(570, 175.869101, 270)
    
    # shape the handle cutout area
    cmds.select(f"{PFX}cutting_board.f[3]", f"{PFX}cutting_board.f[8]", f"{PFX}cutting_board.f[13]", f"{PFX}cutting_board.f[18]", f"{PFX}cutting_board.f[23]")
    cmds.scale(.5, 1, 1, pivot=(0.564256, 1, 1))
    cmds.move(129.860739, 0, 0, relative=True)
    cmds.select(f"{PFX}cutting_board.f[8]", f"{PFX}cutting_board.f[13]", f"{PFX}cutting_board.f[18]")
    cmds.polyCircularize(constructionHistory=True, alignment=0, radialOffset=0, normalOffset=0, normalOrientation=0, smoothingAngle=30, evenlyDistribute=True, divisions=0, supportingEdges=0, twist=0, relaxInterior=True)
    cmds.scale(0.432867, 1, 1, relative=True, p=(187.142886, 0, 0))
    cmds.scale(1, 1, 1.200764, relative=True, p=(187.142886, 0, 0))
    cmds.move(47.654279, 0, 0, relative=True)
    cmds.delete(f"{PFX}cutting_board.f[8]", f"{PFX}cutting_board.f[13]", f"{PFX}cutting_board.f[18]")
    
    # extrudes thickness and bevel the edges
    cmds.select(f"{PFX}cutting_board.f[0:21]")
    cmds.polyExtrudeFacet()
    cmds.move(0, 24, 0, relative=True)
    cmds.select([
        "SSL_cutting_board.e[0]", "SSL_cutting_board.e[1]", "SSL_cutting_board.e[2]", "SSL_cutting_board.e[4]", "SSL_cutting_board.e[6]", "SSL_cutting_board.e[8]", "SSL_cutting_board.e[10]", "SSL_cutting_board.e[12]", "SSL_cutting_board.e[17:18]", "SSL_cutting_board.e[20]", "SSL_cutting_board.e[21]", "SSL_cutting_board.e[23]", "SSL_cutting_board.e[28]", "SSL_cutting_board.e[30]", "SSL_cutting_board.e[31]", "SSL_cutting_board.e[33]", "SSL_cutting_board.e[38]", "SSL_cutting_board.e[40]", "SSL_cutting_board.e[41]", "SSL_cutting_board.e[48]", "SSL_cutting_board.e[43]", "SSL_cutting_board.e[52]", "SSL_cutting_board.e[53]", "SSL_cutting_board.e[54]", "SSL_cutting_board.e[55]", "SSL_cutting_board.e[56]", "SSL_cutting_board.e[57]", "SSL_cutting_board.e[60]", "SSL_cutting_board.e[64]", "SSL_cutting_board.e[66]", "SSL_cutting_board.e[70]", "SSL_cutting_board.e[75]", "SSL_cutting_board.e[78]", "SSL_cutting_board.e[80]", "SSL_cutting_board.e[82]", "SSL_cutting_board.e[87]", "SSL_cutting_board.e[91]", "SSL_cutting_board.e[94]", "SSL_cutting_board.e[97]", "SSL_cutting_board.e[101]", "SSL_cutting_board.e[105]", "SSL_cutting_board.e[108]", "SSL_cutting_board.e[111]", "SSL_cutting_board.e[115]", "SSL_cutting_board.e[119]", "SSL_cutting_board.e[122]", "SSL_cutting_board.e[125]", "SSL_cutting_board.e[129]", "SSL_cutting_board.e[130]", "SSL_cutting_board.e[133]", "SSL_cutting_board.e[136:137]", "SSL_cutting_board.e[140]", "SSL_cutting_board.e[142]", "SSL_cutting_board.e[143]"
    ], r=True)
    cmds.polyBevel(fraction=1, segments=2, offsetAsFraction=True)


def dirt():
    # builds the uneven ground floor and an expanded background soil layer
    
    # creates the floor plane and move vertices around for a bumpy look
    dirt = cmds.polyPlane(n=f"{PFX}Floor", sw=20, sh=20)
    cmds.scale(1500, 1500, 1500, dirt)
    cmds.select(f"{PFX}Floor.vtx[100:101]", f"{PFX}Floor.vtx[17:19]", f"{PFX}Floor.vtx[349:350]", f"{PFX}Floor.vtx[116:117]", f"{PFX}Floor.vtx[248:249]", f"{PFX}Floor.vtx[361:362]", f"{PFX}Floor.vtx[7:9]", f"{PFX}Floor.vtx[1:2]", f"{PFX}Floor.vtx[21:22]", f"{PFX}Floor.vtx[42:43]", f"{PFX}Floor.vtx[37]", f"{PFX}Floor.vtx[370]", f"{PFX}Floor.vtx[289]", f"{PFX}Floor.vtx[92]", f"{PFX}Floor.vtx[95]", f"{PFX}Floor.vtx[52]", f"{PFX}Floor.vtx[87]", f"{PFX}Floor.vtx[129]", f"{PFX}Floor.vtx[193]", f"{PFX}Floor.vtx[253]", f"{PFX}Floor.vtx[107]", f"{PFX}Floor.vtx[388:389]", f"{PFX}Floor.vtx[324]", f"{PFX}Floor.vtx[277]", f"{PFX}Floor.vtx[206]", f"{PFX}Floor.vtx[333]", f"{PFX}Floor.vtx[146]")
    cmds.move(0, 15, 0, relative=True)
    
    cmds.select(f"{PFX}Floor.vtx[116:117]", f"{PFX}Floor.vtx[129]", f"{PFX}Floor.vtx[193]", f"{PFX}Floor.vtx[388:389]", f"{PFX}Floor.vtx[324]", f"{PFX}Floor.vtx[17:19]", f"{PFX}Floor.vtx[349:350]", f"{PFX}Floor.vtx[277]", f"{PFX}Floor.vtx[206]", f"{PFX}Floor.vtx[379]", f"{PFX}Floor.vtx[336]", f"{PFX}Floor.vtx[357]", f"{PFX}Floor.vtx[378]", f"{PFX}Floor.vtx[399]", f"{PFX}Floor.vtx[395:396]", f"{PFX}Floor.vtx[415:416]", f"{PFX}Floor.vtx[286]", f"{PFX}Floor.vtx[282]", f"{PFX}Floor.vtx[164]")
    cmds.move(0, 5, 0, relative=True)

    # duplicates the floor to make a massive background layer, looks cool with the lighting
    dirt_expand = cmds.duplicate(dirt[0], n=f"{PFX}floor_expand")[0]
    cmds.select(dirt_expand)
    cmds.move(0, -20, 0, relative=True)
    cmds.scale(3000, 3000, 3000)
    cmds.select(clear=True)

    # groups both floor pieces together
    cmds.group(dirt, dirt_expand, n=f"{PFX}dirt_floor")

    
def lock_in():
    # places all props into their correct positions and organizes them into groups
    
    if cmds.objExists(f"{PFX}cutting_board"):
        cmds.xform(f"{PFX}cutting_board", t=(7, 0, 0), ws=True)

    if cmds.objExists(f"{PFX}Potted_Vine_01"):
        cmds.xform(f"{PFX}Potted_Vine_01", t=(-225, 0, 100), ws=True)
        cmds.xform(f"{PFX}Potted_Vine_01", ro=(0, 45, 0), ws=True)
    
    if cmds.objExists(f"{PFX}big_skewer_01"):
        cmds.xform(f"{PFX}big_skewer_01", ro=(0, 22, -90), ws=True)
        cmds.xform(f"{PFX}big_skewer_01", t=(-200, 280, 100), ws=True)
        
    if cmds.objExists(f"{PFX}mato_cradle_group"):
        cmds.xform(f"{PFX}mato_cradle_group", s=(.8, .8, .8), ws=True)
        cmds.xform(f"{PFX}mato_cradle_group", t=(-109, 24, 0), ws=True)
    
    if cmds.objExists(f"{PFX}knife_01"):
        cmds.xform(f"{PFX}knife_01", t=(250, 270, 99), ws=True)
        cmds.xform(f"{PFX}knife_01", ro=(0, 0, 8), ws=True)

    
    all_elements = cmds.ls(f"{PFX}*", assemblies=True) # identifies every top-level root object that starts with my PFX
    exclude_list = [f"{PFX}mato_cradle_group", f"{PFX}Base_Side_01", f"{PFX}cutting_board"] # excludes geo that i dont want in the big group
    scene_elements = [obj for obj in all_elements if obj not in exclude_list] # filters through my list taking into account the exclusions
    
    if scene_elements:
        cmds.group(scene_elements, n=f"{PFX}Base_Side_01") # makes sure list isnt empty before grouping

    # group props into a side assembly and duplicate it to mirror the other side
    cmds.select(f"{PFX}Base_Side_01")
    other_side = cmds.duplicate(f"{PFX}Base_Side_01", f"{PFX}Base_Side_02")[0]
    cmds.select(other_side)
    cmds.rotate(0, 180, 0, relative=True, objectSpace=True, forceOrderXYZ=True)
    cmds.move(0, 0, -197, relative=True)
    
    # Put everything under a master base group
    cmds.group(f"{PFX}Base_Side_01", f"{PFX}Base_Side_02", f"{PFX}cutting_board", n=f"{PFX}entire_base")

# shaders were the hardest part for me
def create_wood_shader():
    name = f"{PFX}wood_shader" # sets the name to my desired name

    shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=name) # creates a new Arnold standard surface shader
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + "_SG") # creates a shading group for the material
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True) # connects the shader color to the shading group

    cmds.setAttr(shader + ".base", 1.0) # sets the base weight attribute to full
    cmds.setAttr(shader + ".specular", 0.2) # sets the specular reflection
    cmds.setAttr(shader + ".specularRoughness", 0.7) # sets the specular roughness 

    noise = cmds.shadingNode("noise", asTexture=True, name=name + "_Grain") # creates a procedural noise texture node for wood grain
    cmds.setAttr(noise + ".frequency", 4.0) # adjusts the frequency scale of the noise grain

    ramp = cmds.shadingNode("ramp", asTexture=True, name=name + "_Color_Ramp") # creates a ramp texture node to map wood colors
    cmds.setAttr(ramp + ".interpolation", 0) # sets ramp interpolation 

    colors = [ # begins a list of positions and RGB color values the wood palette
        (0.00, (0.055, 0.018, 0.006)), #dark brown 
        (0.25, (0.14, 0.045, 0.012)), #deep brown 
        (0.45, (0.32, 0.12, 0.035)), #mid brown 
        (0.65, (0.16, 0.05, 0.012)), #dark brown
        (0.85, (0.42, 0.20, 0.07)),  #lighter brown grain 
        (1.00, (0.25, 0.09, 0.025))  #defines final brown color 
    ] 

    for i, (pos, color) in enumerate(colors): # loops through each color entry with its index and values
        cmds.setAttr(ramp + f".colorEntryList[{i}].position", pos) # sets the position attribute on the ramp color entries
        cmds.setAttr(ramp + f".colorEntryList[{i}].color", *color, type="double3") # sets the RGB color attributes on the ramp

    cmds.connectAttr(noise + ".outAlpha", ramp + ".vCoord", force=True) # connects noise output to the ramp's vertical coordinate
    cmds.connectAttr(ramp + ".outColor", shader + ".baseColor", force=True) # connects the ramp color output to the shader's base color 

    for obj in cmds.ls(type="transform", long=True) or []: # loops safely through every transform object in the scene
        if obj.split("|")[-1] == f"{PFX}cutting_board": # checks if the object's short name matches the cutting board
            cmds.sets(obj, edit=True, forceElement=sg) # force assigns the wood material shading group to the cutting board mesh

    return shader # returns the created shader node name back to the caller


def dirt_shader(name="dirt_floor"):
    # builds a fine static-grain cell noise shader for the soil floors
    # pretty much same as the wood shader
    shader_name = name if name.startswith(PFX) else PFX + name

    shader = cmds.shadingNode("aiStandardSurface", asShader=True, name=shader_name)
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name + "_SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)

    cmds.setAttr(shader + ".base", 1.0)
    cmds.setAttr(shader + ".specular", 0.05)
    cmds.setAttr(shader + ".specularRoughness", 0.9)

    # use cell noise for tiny soil specks
    noise_node = cmds.shadingNode("aiCellNoise", asTexture=True, name=shader_name + "_CellNoise")
    
    if cmds.attributeQuery("scale", node=noise_node, exists=True):
        attr_type = cmds.getAttr(noise_node + ".scale", type=True)
        if attr_type == "float3":
            cmds.setAttr(noise_node + ".scale", 800.0, 800.0, 800.0, type="float3")
        else:
            cmds.setAttr(noise_node + ".scale", 800.0, 800.0, 800.0, type="double3")

    # map the noise through an earthy brown color ramp
    ramp_node = cmds.shadingNode("ramp", asTexture=True, name=shader_name + "_ColorRamp")
    cmds.setAttr(ramp_node + ".interpolation", 0)

    soil_colors = [
        (0.00, (0.12, 0.08, 0.05)),
        (0.45, (0.15, 0.08, 0.04)),
        (0.80, (0.29, 0.21, 0.16)),
        (1.00, (0.35, 0.24, 0.15))
    ]

    for i, (pos, color) in enumerate(soil_colors): # Loops through each soil color entry with its index, position, and RGB values
        cmds.setAttr(ramp_node + f".colorEntryList[{i}].position", pos) # Sets the position the ramp color
        cmds.setAttr(ramp_node + f".colorEntryList[{i}].color", *color, type="double3") # Sets the RGB color values for the ramp

    if cmds.attributeQuery("outColorR", node=noise_node, exists=True): # Checks if the noise node has a red color output channel as a saftey check
        cmds.connectAttr(noise_node + ".outColorR", ramp_node + ".vCoord", force=True) # connects red color output to the ramp's vertical coordinate input
    else: # fallback if the red color attribute doesn't exist
        cmds.connectAttr(noise_node + ".outAlpha", ramp_node + ".vCoord", force=True) # Connects the noise alpha output to the ramp's vertical coordinate input instead

    cmds.connectAttr(ramp_node + ".outColor", shader + ".baseColor", force=True) # connects the final ramp color output into the shader's base color attribute

    # Assign shader to both floor meshes
    for target in [f"{PFX}Floor", f"{PFX}floor_expand"]: # creates a loop to go through both the main floor and expanded background soil names
        for obj in cmds.ls(type="transform", long=True) or []: # loops through every transform object in the scene
            if obj.split("|")[-1] == target: # checks if the object's name matches the current target 
                shapes = cmds.listRelatives(obj, shapes=True, noIntermediate=True, fullPath=True) or [] # grabs all valid shape nodes under the object
                meshes = [shape for shape in shapes if cmds.nodeType(shape) == "mesh"] # filters shapes to keep only the mesh nodes
                if meshes: # checks if any valid mesh shapes were found
                    cmds.sets(meshes, edit=True, forceElement=sg) # force assigns the soil shading group to the floor meshes

    return shader

################ Transparency, Google Gemini helped me set up the arnold contours to work with my toon shader since i couldnt figure out how to do it all at once
def enable_arnold_contours():
    
    # Turns on Arnold's contour filter to give everything toon outlines
    if not cmds.pluginInfo("mtoa", query=True, loaded=True): # Checks if the Arnold plugin is already turned on
        cmds.loadPlugin("mtoa") # Loads Arnold into Maya if it's missing
    createOptions()
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
    filter_node = "defaultArnoldFilter" # Saves the default filter name into a handy variable

    if not cmds.objExists(filter_node): # Double-checks that the filter node actually exists
        raise RuntimeError("Arnold default filter was not created.") # Stops and throws an error if the filter node is missing
    cmds.setAttr(filter_node + ".aiTranslator", "contour", type="string") # Switches the filter type to 'contour' to draw the outlines

    if cmds.attributeQuery("width", node=filter_node, exists=True): # Checks if the width attribute is actually there
        cmds.setAttr(filter_node + ".width", 3.0) # Sets how thick the outline strokes will be


def create_toon(object_name=None, name="Toon", base_color=(0.8, 0.35, 0.2)): # Defines the function to build a custom Arnold toon shader
    
    name = name if name.startswith(PFX) else PFX + name # Makes sure the shader name uses prefix

    toon = cmds.shadingNode("aiToon", asShader=True, name=name) # Creates the main Arnold toon shader node
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=name + "_SG") # Creates a shading group engine for the toon material
    cmds.connectAttr(toon + ".outColor", sg + ".surfaceShader", force=True) # Connects the shader color output to the shading group

    cmds.setAttr(toon + ".base", 1.0) # Turns the base material weight all the way up
    cmds.setAttr(toon + ".baseColor", *base_color, type="double3") # Sets the base color of the object

    def make_ramp(ramp_name, entries): # sub-function to build and configure color ramps
        ramp = cmds.shadingNode("ramp", asTexture=True, name=ramp_name) # Creates a new ramp texture node
        cmds.setAttr(ramp + ".interpolation", 0) # Sets ramp interpolation to sharp steps for the cel-shaded look
        for i, (position, color) in enumerate(entries): # Loops through each color stop entry
            cmds.setAttr(ramp + ".colorEntryList[" + str(i) + "].position", position) # Sets the position along the ramp
            cmds.setAttr(ramp + ".colorEntryList[" + str(i) + "].color", *color, type="double3") # Sets the RGB color for that stop
        return ramp # Sends the finished ramp node back out

    # Cel-shading
    base_ramp = make_ramp(name + "_CelShading_Ramp", [ # Builds the shadow and highlight bands
        (0.00, (0.22, 0.22, 0.22)), # Dark shadow tone at the bottom
        (0.38, (0.22, 0.22, 0.22)), 
        (0.40, (0.62, 0.62, 0.62)), 
        (0.72, (0.62, 0.62, 0.62)), # Holds the mid-tone steady
        (0.74, (1.00, 1.00, 1.00)), 
        (1.00, (1.00, 1.00, 1.00))  # Holds the bright highlight at the top
    ]) 
    cmds.connectAttr(base_ramp + ".outColor", toon + ".baseTonemap", force=True) # plugs the base ramp into the toon shader's tonemap input

    # Specular highlight ramp
    specular_ramp = make_ramp(name + "_Highlight_Ramp", [ # Builds a separate ramp to control shiny reflections
        (0.00, base_color), # Blends with the base color early on
        (0.15, base_color), # Holds base color
        (0.18, (1.0, 1.0, 1.0)), 
        (1.00, (1.0, 1.0, 1.0))  # Holds the highlight
    ]) 
    cmds.connectAttr(specular_ramp + ".outColor", toon + ".specularTonemap", force=True) # into the toon shader it goes

    cmds.setAttr(toon + ".specular", 1.0) # Turns specular reflection weight on
    cmds.setAttr(toon + ".specularColor", 1.0, 1.0, 1.0, type="double3") # Sets highlight color to pure white
    cmds.setAttr(toon + ".specularRoughness", 0.25) # Controls how spread out the shine is

    # Outline ink settings, needed alongside the arnold contours to create the textures themselves, the arnold countours just turns on the setting
    cmds.setAttr(toon + ".edgeColor", 0.0, 0.0, 0.0, type="double3") # Sets the comic-book outline ink color to pure black
    cmds.setAttr(toon + ".edgeOpacity", 1.0) # Makes sure the outlines are fully opaque
    cmds.setAttr(toon + ".edgeWidthScale", .8) # Scales down the outline thickness slightly so it looks clean

    if object_name is not None: # Checks if a specific mesh was passed in to receive this material
        if not cmds.objExists(object_name): # Double-checks that the target object actually exists in the scene
            raise RuntimeError("Object does not exist: " + object_name) # Throws an error if the object is missing
        cmds.sets(object_name, edit=True, forceElement=sg) # Force-assigns the material shading group to that object

    return toon # Returns the finished toon shader back to the caller


def create_toon_for_objects():
    # Loops through scene objects and applies the appropriate toon shaders based on RGB values
    toon_colors = {
        f"{PFX}sphere_mato01": (.782, 0.173, 0.08),
        f"{PFX}mato_leaf": (.191, 0.52, 0.128), f"{PFX}mato_stem": (.191, 0.52, 0.128),
        f"{PFX}string_01": (0.27, 0.22, 0.151), f"{PFX}string_02": (0.27, 0.22, 0.151),
        f"{PFX}pot_01": (1.12, 0.484, 0.031), f"{PFX}pot_soil": (0.146, 0.08, 0.04),
        f"{PFX}vine_01": (.191, 0.52, 0.128), f"{PFX}twig_01": (.191, 0.52, 0.128), f"{PFX}twig_02": (.191, 0.52, 0.128),
        f"{PFX}big_skewer_01": (0.737, 0.737, 0.737),
        f"{PFX}blade_01": (0.737, 0.737, 0.737), f"{PFX}handle_01": (0.146, 0.08, 0.04),
    }

    default_color = (0.8, 0.35, 0.2) # Sets a fallback color just in case an object isn't listed above
    objects = cmds.ls(f"{PFX}*", type="transform", long=True) or [] # Grabs every transform object in the scene that uses the prefix
    created_materials = {} # Initializes an empty dictionary to keep track of shaders that were already generated

    for obj in objects: # Loops through every single prefixed transform object
        shapes = cmds.listRelatives(obj, shapes=True, noIntermediate=True, fullPath=True) or [] # Grabs all shape nodes underneath the current transform
        if not any(cmds.nodeType(shape) == "mesh" for shape in shapes): # Checks if the object actually contains a polygon mesh shape
            continue # Skips non-mesh objects like group nodes or cameras

        short_name = obj.split("|")[-1] # Extracts just the clean short name of the object from its long path
        if short_name == f"{PFX}Floor": # Checks if the object is the ground floor mesh
            continue # Skips the floor so it keeps its unique dirt shader instead of getting a toon shader

        color = toon_colors.get(short_name, default_color) 
        material_name = "Toon_" + short_name # Generates a unique shader name based on the object's name

        if material_name not in created_materials.values(): # Checks if the material has been built yet
            toon = create_toon(object_name=None, name=material_name, base_color=color) # Builds a new toon shader using toon function
            created_materials[material_name] = toon # Saves the newly created material into the dictionary 

        toon = created_materials[material_name] # Pulls the active material reference
        sg = cmds.listConnections(toon, type="shadingEngine") or [] 
        cmds.sets(obj, edit=True, forceElement=sg[0]) 

    return created_materials 


def animato():
    # adds math expressions to make the cradle units swing automatically
    cmds.expression(object=f"{PFX}swing_mato_04", s=f"{PFX}swing_mato_04.rotateZ = clamp(0,40,sin(time*3)*40)")
    cmds.expression(object=f"{PFX}swing_mato_05", s=f"{PFX}swing_mato_05.rotateZ = clamp(-40,0,sin(time*3)*40)")


def area_light():
    # Creates, scales, and positions the main Arnold area light
    light_transform = cmds.shadingNode("aiAreaLight", asLight=True, name=f"{PFX}areaLightShape")
    
    # Turn normalize off so the light's massive scale directly increases its power
    light_shapes = cmds.listRelatives(light_transform, shapes=True) or []
    if light_shapes:
        light_shape = light_shapes[0]
        cmds.setAttr(light_shape + ".normalize", 0)
        cmds.setAttr(light_shape + ".intensity", 1.0)
        cmds.setAttr(light_shape + ".exposure", 4.0)

    cmds.select(light_transform)
    cmds.move(613.547, 839.064, 138.778, light_transform, worldSpace=True)
    cmds.rotate(-26.891, 75.183, 0, light_transform, worldSpace=True)
    cmds.scale(273.517, 273.517, 273.517, light_transform)
    
    cmds.select(clear=True)
    return light_transform

def setCamera():
    # Sets up the custom render camera 
    camera = cmds.camera(name=PFX + 'myRenderCam')[0]
    cmds.select(camera)
    cmds.move(722.992, 433.77, -934.131, camera, worldSpace=True)
    cmds.rotate(-14.138, 1583, 0, camera, worldSpace=True)
    cmds.setAttr(f"{camera}.focalLength", 35)

    # Disable renderability for all other cameras
    all_cameras = cmds.ls(type='camera')
    for cam in all_cameras:
        cmds.setAttr(f'{cam}.renderable', 0)
    
    # ensures this is the only camera that can be rendered
    cmds.setAttr(f'{camera}.renderable', 1)
    cmds.optionVar(intValue=('renderSequenceAllCameras', 1))

    return camera


def setRenderSettings():
    # Configures Arnold renderer settings, resolutions, frame ranges, and EXR outputs
    ai.core.createOptions()

    cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
    cmds.setAttr("defaultRenderGlobals.imageFormat", 51)
    cmds.setAttr("defaultArnoldDriver.aiTranslator", "exr", type="string")

    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("defaultRenderGlobals.startFrame", startFrame)
    cmds.setAttr("defaultRenderGlobals.endFrame", endFrame)
    cmds.setAttr("defaultRenderGlobals.byFrameStep", 1)

    cmds.setAttr("defaultResolution.width", width)
    cmds.setAttr("defaultResolution.height", height)
    cmds.setAttr("defaultResolution.deviceAspectRatio", float(width) / height)

    cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)
    cmds.setAttr("defaultRenderGlobals.imageFilePrefix", "myTestRender", type="string")
    cmds.setAttr("defaultRenderGlobals.useFrameExt", 1)
    cmds.setAttr("defaultRenderGlobals.periodInExt", 1)
    cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)

    cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 2)
    cmds.setAttr("defaultArnoldRenderOptions.GISpecularDepth", 2)
    cmds.setAttr("defaultArnoldDriver.mergeAOVs", 1)


def renderScene():
    # Triggers the final Arnold batch render sequence
    cmds.RenderSequence()


def main():
    # Main execution pipeline: cleans up, builds geometry, applies shaders, lights, and renders
    cleanupscene()

    # Build all scene objects and props
    cutting_board()
    pot()
    vine()
    knife()
    skewer()
    sphere_mato()
    newtons_mato()
    lock_in()
    dirt()

    cmds.playbackOptions(min=startFrame, max=endFrame, ast=startFrame, aet=endFrame, loop='continuous')
    animato()
    # Apply materials, lighting, and outlines
    enable_arnold_contours()
    create_toon_for_objects()
    create_wood_shader()
    dirt_shader()
    area_light()
    
    # Set up camera, render settings, and start rendering
    camera = setCamera()
    setRenderSettings()
    renderScene()


# Kick off the script execution
main()