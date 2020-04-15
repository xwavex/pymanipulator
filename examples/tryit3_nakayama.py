import os
import database.dbaccess as db
from manipulation.grip.robotiq85 import rtq85nm
from manipulation.grip import freegrip
from pandaplotutils import pandactrl

base = pandactrl.World(camp=[700, 300, 700], lookatp=[0, 0, 100])
this_dir, this_filename = os.path.split(__file__)
print(this_dir)

# object_name = "planerearstay22"
# object_name = "bunny16000"
# object_name = "bunny17000"
# object_name = "bunnysim"
# object_name = "housingshaft"
# object_name = "housing"
# object_name = "planefrontstay"
# object_name = "planelowerbody"
# object_name = "planerearstay212"
# object_name = "planerearstay215"
# object_name = "planerearstay22"
# object_name = "planerearstay23"
# object_name = "planerearstay24"
# object_name = "planerearstay26"
# object_name = "planerearstay28"
# object_name = "planerearstay2"
# object_name = "planerearstay"
object_name = "plane"
# object_name = "planewheel"
# object_name = "sandpart2"
# object_name = "sandpart"
# object_name = "tool2"
# object_name = "tool"
# object_name = "ttube"

# object_name = "weidmueller_clamp_1"
# object_name = "weidmueller_clamp_2"
# object_name = "weidmueller_clamp_3"

objpath = os.path.join(this_dir, "../manipulation/grip/objects", object_name + ".stl")
objnp = base.pg.loadstlaspandanp_fn(objpath)
objnp.reparentTo(base.render)
# base.run()

global countdlw
countdlw = 0

handpkg = rtq85nm

# freegriptst = freegrip.Freegrip(objpath, handpkg, readser=False, torqueresist = 70, dotnormplan=.90, dotnoarmovlp=.95, dotnormpara = -.80)
# freegriptst.segShow(base, togglesamples=False, togglenormals=False,
#                     togglesamples_ref=False, togglenormals_ref=False,
#                     togglesamples_refcls=False, togglenormals_refcls=False)

# freegriptst.removeFgrpcc(base)
# freegriptst.removeHndcc(base, discretesize=16)

gdb = db.GraspDB()
# freegriptst.saveToDB(gdb)

data = gdb.loadFreeAirGrip(object_name, 'rtq85')
if data:
    global freegriprotmats
    freegripid, freegripcontacts, freegripnormals, freegriprotmats, freegripjawwidth = data
    print(len(freegripid))
    # for i, freegriprotmat in enumerate(freegriprotmats):
    #     countdlw = countdlw + 1
    #     if countdlw < 3:
    #         # if i>120 and i-120 < 30:
    #         rtqhnd = rtq85nm.Rtq85NM(hndcolor=[1, 1, 1, .2])
    #         rtqhnd.setMat(pandanpmat4=freegriprotmat)
    #         rtqhnd.setJawwidth(freegripjawwidth[i])
    #         rtqhnd.reparentTo(base.render)


# def updateshow(task):
#     freegriptst.removeFgrpccShow(base)
#     # freegriptst.removeFgrpccShowLeft(base)
#     # freegriptst.removeHndccShow(base)
#     return task.again
# taskMgr.doMethodLater(.1, updateshow, "tickTask")

def updateshow(task):
    global countdlw, freegriprotmats
    if countdlw < (len(freegriprotmats) - 1):
        countdlw = countdlw + 1
        freegriprotmat = freegriprotmats[countdlw]
        rtqhnd = rtq85nm.Rtq85NM(hndcolor=[1, 1, 1, .2])
        rtqhnd.setMat(pandanpmat4=freegriprotmat)
        rtqhnd.setJawwidth(freegripjawwidth[countdlw])
        rtqhnd.reparentTo(base.render)
    return task.again
taskMgr.doMethodLater(1.0, updateshow, "tickTask")

base.run()