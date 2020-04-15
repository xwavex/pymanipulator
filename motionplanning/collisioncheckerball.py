import numpy as np
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
import utils.collisiondetection as cd
from panda3d.core import *
import pandaplotutils.pandageom as pg
import gc

class CollisionCheckerBall(object):
    """
    check the collision of a robot, using ball fitting

    """

    def __init__(self, robotball):
        """
        set up the collision checker

        :param robotball is an object of robotsim/robot.robotball

        author: weiwei
        date: 20170615
        """

        self.__robotball = robotball


    def isSelfCollided(self, robot):
        """
        check the collision of a single arm

        :param armid: 'lft' or 'rgt'
        :return:

        author: weiwei
        date: 20170615
        """

        bcndict = self.__robotball.genbcndict(robot)

        if 'body' in bcndict and len(bcndict) > 1:
            bodynp = None
            bodyarmcnp = NodePath("collision nodepath")
            countdlw = 0
            for key, bcn in bcndict.items():
                countdlw = countdlw + 1
                print("DLW " + str(countdlw) + ", key = " + str(key) + " : " + str(bcn))
                # RACE CONDITION???????????
            for key, bcn in bcndict.items():
                if key is 'body':
                    bodynp = bodyarmcnp.attachNewNode(bcn)
                else:
                    bodyarmcnp.attachNewNode(bcn)
                ctrav = CollisionTraverser()
                chan = CollisionHandlerQueue()
                print("aaa k = " + str(key) + ", bcn = " + str(bcn) + " : " + str(bodynp))
                print("bbb " + str(chan))
                ctrav.addCollider(bodynp, chan)
                ctrav.traverse(bodyarmcnp)
                if chan.getNumEntries() > 0:
                    print("arm/hnd-body collision")
                    return True
            bcndict.pop('body')

        if 'rgthnd' in bcndict and len(bcndict) > 1:
            rgthandnp = None
            rgthndarmcnp = NodePath("collision nodepath")
            for key, bcn in bcndict.items():
                if key is 'rgthnd':
                    rgthandnp = rgthndarmcnp.attachNewNode(bcn)
                else:
                    rgthndarmcnp.attachNewNode(bcn)
                ctrav = CollisionTraverser()
                chan = CollisionHandlerQueue()
                ctrav.addCollider(rgthandnp, chan)
                ctrav.traverse(rgthndarmcnp)
                if chan.getNumEntries() > 0:
                    print("rgthnd-arm collision")
                    return True
            bcndict.pop('rgthnd')

        if 'lfthnd' in bcndict and len(bcndict) > 1:
            lfthandnp = None
            lfthndarmcnp = NodePath("collision nodepath")
            for key, bcn in bcndict.items():
                if key is 'lfthnd':
                    lfthandnp = lfthndarmcnp.attachNewNode(bcn)
                else:
                    lfthndarmcnp.attachNewNode(bcn)
                ctrav = CollisionTraverser()
                chan = CollisionHandlerQueue()
                ctrav.addCollider(lfthandnp, chan)
                ctrav.traverse(lfthndarmcnp)
                if chan.getNumEntries() > 0:
                    print("lfthnd-arm collision")
                    return True
            bcndict.pop('lfthnd')

        return False

    def isCollided(self, robot, obstaclelist = []):
        """
        check the collision of a single arm

        :param armid: 'lft' or 'rgt'
        :return:

        author: weiwei
        date: 20170615
        """

        bselfcollided = self.isSelfCollided(robot)
        if bselfcollided:
            return True
        else:
            # obj robot
            bcndict = self.__robotball.genbcndict(robot)
            robotcnp = NodePath("collision nodepath")
            for key, bcn in bcndict.items():
                robotcnp.attachNewNode(bcn)

            for obstacle in obstaclelist:
                bottomLeft, topRight = obstacle.getTightBounds()
                box = CollisionBox(bottomLeft, topRight)
                tmpcolnode = CollisionNode("auto gen")
                tmpcolnode.addSolid(box)
                obstaclenp = robotcnp.attachNewNode(tmpcolnode)
                ctrav = CollisionTraverser()
                chan = CollisionHandlerQueue()
                ctrav.addCollider(obstaclenp, chan)
                ctrav.traverse(robotcnp)
                if chan.getNumEntries() > 0:
                    print("obstacle-robot collision")
                    return True
                # obstaclenp.reparentTo(base.render)
                # obstaclenp.show()
                obstaclenp.removeNode()

            return False

if __name__=="__main__":

    # show in panda3d
    from direct.showbase.ShowBase import ShowBase
    from panda3d.core import *
    from panda3d.bullet import BulletSphereShape
    import pandaplotutils.pandageom as pandageom
    import pandaplotutils.pandactrl as pandactrl
    # from direct.filter.CommonFilters import CommonFilters
    # from robotsim.ur5dual import ur5dual
    # from robotsim.ur5dual import ur5dualplot
    from robotsim.ur3dual import ur3dual
    from robotsim.ur3dual import ur3dualmesh
    from robotsim.ur3dual import ur3dualball
    # from robotsim.nextage import nxt
    # from robotsim.nextage import nxtplot
    # from manipulation.grip.robotiq85 import rtq85nm
    # from manipulation.grip.hrp5three import hrp5threenm

    base = pandactrl.World(camp = [3000,0,3000], lookatp = [0,0,700])

    robotpose = [-135.0, 5.0, -180.0, -45.0, -90.0, 0]
    robot = ur3dual.Ur3DualRobot()
    robot.movearmfk(robotpose)
    robotmeshgen = ur3dualmesh.Ur3DualMesh()
    robotball = ur3dualball.Ur3DualBall()

    robotmnp = robotmeshgen.genmnp(robot)
    robotmnp.reparentTo(base.render)
    bcnlist = robotball.genbcndict(robot)
    robotball.showbcn(base, bcnlist)

    cdchecker = CollisionCheckerBall(robotball)
    print(cdchecker.isSelfCollided(robot))
    base.run()