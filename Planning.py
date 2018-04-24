#! /usr/bin/env python
import adapy
import prpy
import rospy
import prpy
from makingEnvironment import makingEnvironment
import IPython
import numpy as np
import openravepy
import sys
import pdb
import time

# importing planning in clutter modulues
from taskPlanning import makeGrid as mG
from taskPlanning import planInClutter as pIC

class Planning(object):
        def __init__(self, robot = None, env = None, tag = None):
                self.robot = robot
                self.env = env
                self.tag = tag
                self.tableMap, self.targetObject, self.bodyOfConcern = self.clutterMap()
                self.planInClutter = pIC.planInClutter
                # pdb.set_trace()
                self.plan = self.planInClutter(self.tableMap, self.targetObject)
                ch = raw_input("Planning Complete, continue?");
                #self.executePlan()

        def clutterMap(self):
                kinbodies = self.env.GetBodies()
                bodyOfConcern = []
                for kinbody in kinbodies:
                        if "tomato_soup" in kinbody.GetName()\
                                or "fuze" in kinbody.GetName()\
                                or "potted" in kinbody.GetName():
                                bodyOfConcern.append(kinbody)
                tableObjects = []
                targetObject = None
                for obj in bodyOfConcern:
                        T = obj.GetTransform()
                        tag = int(obj.GetName()[-2:])
                        tabObj = mG.objectOnTable(-T[1][3] * 100, T[0][3] * 100, shape = 'circle', tag = tag)
                        tableObjects.append(tabObj)
                        if self.tag == tag:
                                targetObject = tabObj
                return mG.costMap(tableObjects), targetObject, bodyOfConcern

        def executePlan(self):
                if self.plan is not None:
                        for planStep in self.plan:
                                tag, newX, newY = planStep
                                # pdb.set_trace()
                                print tag
                                for reachObject in self.bodyOfConcern:
                                        if int(reachObject.GetName()[-2:]) == tag:
                                                ro = self.reachForObject(reachObject)
                                                if not ro:
                                                    return False
						go = self.graspObject(reachObject)
                                                self.goHome()
                                                if not go:
                                                    return False
                                                po = self.placeObject(reachObject, newX, newY)
                                                if not po:
                                                    return False

                        print "Now going for target"
                for targetObject in self.bodyOfConcern:
                        if self.targetObject.tag == int(targetObject.GetName()[-2:]):
                                ro = self.reachForObject(targetObject)
				if not ro:
				    return False
                                go = self.graspObject(targetObject)
				if not go:
				    return False
                                self.goHome()
                                self.robot.arm.hand.CloseHand(0)
                makingEnvironment.renew_env(self.env)
                return True

        def reachForObject(self, targetObject):
                #IPython.embed()
                timeStart = time.time()
                kinbodyTrans = targetObject.GetTransform()
                T0_w = kinbodyTrans
                Bw = np.zeros((6,2))
                if('tomato_soup_can' in targetObject.GetName() or \
			'fuze_bottle' in targetObject.GetName()):
                    print "I got tomato_soup_can"
                    Tw_e =  np.array([[ 0., 0., 1., -0.025], # away from can, radially
                                   [1., 0., 0., 0],
                                   [0., 1., 0., 0.05], # height from can
                                   [0., 0., 0., 1.]])
                    Bw[2,:] = [0.0, 0.020]
                    Bw[4,:] = [-np.pi, np.pi]
                elif 'potted_meat_can' in targetObject.GetName():
                    Tw_e =  np.array([[ 0., 0., 1., 0],
                                  [1., 0., 0., 0.],
                                  [0., 1., 0., 0.04],
                                  [0., 0., 0., 1.]])
                    rot90 = np.array([[1.,0.,0.,0.],[0.,0.,-1.,0.],[0.,1.,0.,0.],[0.,0.,0.,1.]])
                    Tw_e = np.dot(Tw_e, rot90)
                    Bw[2,:] = [0.0, 0.015]
                    Bw[5,:] = [-np.pi, np.pi]
                manip_idx = self.robot.GetActiveManipulatorIndex()
                grasp_tsr = prpy.tsr.TSR(T0_w,
                             Tw_e,
                             Bw,
                             manip_idx)
                self.robot.SetActiveDOFs([0, 1, 2, 3, 4, 5])
                chomp = prpy.planning.chomp
                planner = chomp.CHOMPPlanner()
                prpy.viz.RenderTSRList([grasp_tsr], self.robot.GetEnv(), render=True)
                self.robot.SetActiveManipulator('Mico')
                planner.setupEnv(self.env.CloneSelf(0))
                tsr_chain = prpy.tsr.TSRChain(sample_goal=True,
                                         sample_start=False,
                                         constrain=False,
                                         TSR=grasp_tsr)

                plan = None
                while plan is None:
                    ee_sample = grasp_tsr.sample()
                    try:
                        #plan = self.robot.arm.PlanToEndEffectorPose(ee_sample)
                        plan = self.robot.arm.PlanToTSR([tsr_chain])
                    except:
                        None
                    try:
                        planner.setupEnv(self.env.CloneSelf(0))
                        plan = planner.OptimizeTrajectory(self.robot, plan)
                    except:
                        None
                    if time.time() - timeStart > 30.0:
                       print "Reach for object failed: exitting"
                       return False
                print "Time to Plan to Reach: ", time.time() - timeStart

                ch = raw_input("Planning Complete. Execute path? (y/n)")
                if(ch == 'y' or ch == 'Y'):
                    self.robot.ExecutePath(plan)
                else:
                    return False
                return True

        def graspObject(self, targetObject):
                finger_link_inds = []
                grab_link = None
                for ind,link in enumerate(self.robot.GetLinks()):
                        if 'inger' in link.GetName():
                            finger_link_inds.append(ind)
                        if 'end_effector' in link.GetName():
                            grab_link = link
                self.robot.arm.hand.CloseHand(1.2)
                rospy.sleep(3)
                self.robot.Grab(targetObject, grablink = grab_link, linkstoignore = finger_link_inds)
                return True
                #self.env.RemoveKinBody(targetObject)
                #self.robot.arm.hand.CloseHand(0)

        def placeObject(self, targetObject, targetX = 0, targetY = 0):
                #IPython.embed()
                timeStart = time.time()
                T0_w = np.array([[1, 0, 0, targetX + 0.11],
                                 [0, 1, 0, targetY],
                                 [0, 0, 1, 0.73],
                                 [0, 0, 0, 1]])
                Tw_e =  np.array([[ 0., 0., 1., -0.025], # away from can, radially
                           [1., 0., 0., 0],
                           [0., 1., 0., 0.04], # height from can
                           [0., 0., 0., 1.]])
                Bw = np.zeros((6,2))
                Bw[2,:] = [0.0, 0.03]
                Bw[5,:] = [-np.pi, np.pi]
                manip_idx = self.robot.GetActiveManipulatorIndex()
                grasp_tsr = prpy.tsr.TSR(T0_w,
                             Tw_e,
                             Bw,
                             manip_idx)
                self.robot.SetActiveDOFs([0, 1, 2, 3, 4, 5])
                chomp = prpy.planning.chomp
                planner = chomp.CHOMPPlanner()
                prpy.viz.RenderTSRList([grasp_tsr], self.robot.GetEnv(), render=True)
                self.robot.SetActiveManipulator('Mico')
                planner.setupEnv(self.env.CloneSelf(0))
                tsr_chain = prpy.tsr.TSRChain(sample_goal=True,
                                         sample_start=False,
                                         constrain=False,
                                         TSR=grasp_tsr)

                plan = None
                while plan is None:
                    ee_sample = grasp_tsr.sample()
                    try:
                        #plan = self.robot.arm.PlanToEndEffectorPose(ee_sample)
                        plan = self.robot.arm.PlanToTSR([tsr_chain])
                    except:
                        None
                    try:
                        planner.setupEnv(self.env.CloneSelf(0))
                        plan = planner.OptimizeTrajectory(self.robot, plan)
                    except:
                        None
                    if time.time() - timeStart > 30.0:
                       print "Place for object failed: exitting"
                       return False
                print "Time to Plan to Reach: ", time.time() - timeStart
                ch = raw_input("Planning Complete. Execute path? (y/n)")
                if(ch == 'y' or ch == 'Y'):
                    self.robot.ExecutePath(plan)
                else:
                    return False
                self.robot.ReleaseAllGrabbed()
                self.robot.arm.hand.CloseHand(0.25)
                rospy.sleep(3)
                self.goHome()
                self.robot.arm.hand.CloseHand(0.15)
                rospy.sleep(3)
                return True

        def goHome(self):
                self.robot.arm.PlanToNamedConfiguration('home', execute = True)
        def goToUser(self):
                user_config = self.manip_config['user_home']

def planning_env(env, robot):
        manip_config = rospy.get_param("manipulator_config")
        Objects = manip_config['tags']
        ObjectTypes = manip_config['testObjectTypes']
        tags = manip_config['tags']

        robot.arm.hand.CloseHand(0)
        robot.arm.PlanToNamedConfiguration('home', execute = True)
        robot.arm.hand.CloseHand(0)
        makingEnvironment.addObjects(env, Objects, ObjectTypes, tags)
        makingEnvironment.addTable(env, robot)
        makingEnvironment.addConstraintBoxes(env, robot)

"""
if __name__ == "__main__":
        rospy.init_node('planning', anonymous = True)
        env, robot = adapy.initialize(
                sim = False,
                attach_viewer = 'rviz'
        )
        planning_env()
        planner = Planning(env = env, robot = robot, tag = 17)
        while not rospy.is_shutdown():
            rospy.loginfo("I'm planning")
"""
