import glob
import os
import sys
import random
import time
import math
import pandas as pd

try:
    sys.path.append(glob.glob('../../CARLA_0.9.5/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

class clsCarlaEnv:
    def __init__(self,nWorld = 4, timestep = 0, smode = True, rmode = False):
        #Client, World, Map
        self.client = carla.Client('localhost', 2000)
        self.client.set_timeout(10.0)
        self.LoadMap(nWorld)
        self.map = self.world.get_map()

        #World Settings
        settings = self.world.get_settings()
        settings.synchronous_mode = smode
        settings.no_rendering_mode = not rmode
        self.world.apply_settings(settings)

        #Actors and Waypoints
        self.actor_list = []            # carla.Actor
        self.actor_listRoute = []       # route (str) the actor's location
        self.wp_list = []               # carla.Waypoint
        self.wp_listRoute = []          # route (str) the waypoint belongs to
        self.sensor = ""                # carla.Sensor (carla.Actor)
        self.actor_wpLog = []           # [leaving waypoint, heading waypoint]
        
        self.TargetRoute = ""

        #Parameter
        self.timestep = timestep
        self.wp_dis = 0
        self.actors_speed = 0

        # Environment Representation
        self.actions = ["gas","brake"]
        self.features = ["Ego v", "Forward d", "Forward v"]
        self.terminal = 0
        self.terminalPerceived = False

    def LoadMap(self, nWorld):
        if self.client.get_world().get_map().name == 'Town0'+ str(nWorld):
            self.world = self.client.get_world()
        else:
            self.world = self.client.load_world('Town0'+ str(nWorld))

# ==============================================================================
# -- Standard Environment Interface --------------------------------------------
# ==============================================================================      
    def SetStartPosition(self, Idx, speed = 10, spectator=False):
        trans = self.RetTransformOffset(self.wp_list[Idx].transform, z = 0.1)
        self.SetActor(trans, spectator=spectator)
        self.SetSensorToActor(0)
        self.SetActorVelocity(0,speed)

    def SetVehiclesAhead(self, nVehicles = 1, nSteps = 4):
        assert len(self.actor_list) == 1, "Error! More than 1 actor defined"
        waypoint = self.RetWayPoint(self.actor_list[0].get_location())
        for i in range(nVehicles):
            waypoint = self.RetWPAhead(waypoint,4)
            trans = self.RetTransformOffset(waypoint.transform, z = 0.1)
            self.SetActor(trans)

    def Next(self, action, timestep = 0.05):
        if action == self.actions[0]:
            self.ApplyGas(0,1)
        if action == self.actions[1]:
            self.ApplyBrake(0,1)
        self.TickAfterTimeStep(timestep)
        self.UpdateActorTransformToWaypointDrive(ShowHeadingPoint = True)
        self.RefreshAutopilotSpeed()
    
    def ReturnActionList(self):
        return self.actions
    
    def ReturnFeatureList(self):
        return self.features    

    def RetStateFeatures(self, actorN = 0):
        t = self.terminal
        if t == 1:
            self.terminalPerceived = True
        return [self.RetActorSpeed(actorN), self.RetActorFront(actorN,[0,50])[0], \
            self.RetActorFront(actorN,[0,50])[1], t]

    def RetReward(self,actorN = 0, timestep = 0.05):
        v = (self.RetLenVec(self.actor_list[actorN].get_velocity())-2)*timestep
        ret = v
        ret += math.fabs(1/(3.5-self.RetActorFront(actorN,[0,50])[0]))*(1/(3.5-self.RetActorFront(actorN,[0,50])[0]))*10
        return ret*10

# ==============================================================================
# -- Actor functions ----------------------------------------------------------
# ==============================================================================

    def SetActor(self, Transform, ActorType = 'grandtourer', spectator=False):
        bp = self.world.get_blueprint_library().filter(ActorType)[0]
        vehicle = self.world.try_spawn_actor(bp, Transform)
        self.Tick()
        if vehicle == None: 
            print("Vehicle Spawn failed")
            return
        else:
            self.actor_list.append(vehicle)
            self.actor_wpLog.append(0)  # append random stuff
            self.actor_wpLog[-1] = [-1,-1]
            print("Vehicle spawned at position: (" + str(Transform.location.x)+","+str(Transform.location.y)+")")  

        if spectator:
            self.world.get_spectator().set_transform(self.RetTransformOffset(Transform,x=-10,y=0,z=20))
        return

    def SetAutopilot(self, nActor, APmode = True):
        self.actor_list[nActor].set_autopilot(True)

    def SetActorsToAutopilot(self, APmode = True,speed = 10):
        self.actors_speed = speed
        for i in range(len(self.actor_list)-1):
            self.actor_list[i+1].set_autopilot(True)
            self.SetActorVelocity(i+1,speed)
            print(self.actor_list[i+1].id)

    def RefreshAutopilotSpeed(self):
        assert len(self.actor_list)>1, "Error! No other actors except ego actor found"
        for i in range(len(self.actor_list)-1):
            self.SetActorVelocity(i+1,self.actors_speed)

    def SetActorTransform(self, actorN, transform, HeadingTransform, ShowHeadingPoint = False):
        def RetTransformOffsetYaw(transform, yaw):
            YawTransform1 = self.RetTransformOffset(transform,yaw = yaw)
            YawTransform2 = self.RetTransformOffset(transform,yaw = -yaw)
            Scal1 = self.RetScalProd(YawTransform1.get_forward_vector(), VecToTarget)
            Scal2 = self.RetScalProd(YawTransform2.get_forward_vector(), VecToTarget)
            if Scal1>Scal2: 
                return YawTransform1
            return YawTransform2

        if ShowHeadingPoint: self.DrawPoint(HeadingTransform.location,carla.Color(255,255,255), lt=30)

        EgoVector = transform.get_forward_vector()
        VecToTarget = self.RetVecLocations(transform.location, HeadingTransform.location)
        cosalpha = self.RetScalProd(EgoVector, VecToTarget)/ (self.RetLenVec(VecToTarget)*self.RetLenVec(EgoVector))
        yaw = math.acos(cosalpha)*180/3.14
        self.actor_list[actorN].set_transform(RetTransformOffsetYaw(transform, yaw))

    def SetActorVelocity(self,actorN,v = 0):
        vecForward = self.actor_list[actorN].get_transform().get_forward_vector()
        self.actor_list[actorN].set_velocity(carla.Vector3D(x=vecForward.x*v,y=vecForward.y*v,z=0))

    def RetActorSpeed (self,actorN, includeZ = False):
        return self.RetLenVec(self.actor_list[actorN].get_velocity(), includeZ=includeZ)

    def RetActorFront(self,actorN, distance):
        ego = self.actor_list[actorN]
        route = self.RetRoute(ego.get_location())
        ret = []
        for i in range(len(self.actor_list)):
            if not i == actorN and self.RetRoute(self.actor_list[i].get_location()) == route:
                act = self.actor_list[i]
                d = self.RetDisLocations(ego.get_location(), act.get_location())
                if d < distance[1] and self.RetHeadingPrecision(ego.get_transform(),act.get_transform())>0: 
                    dat = [d,self.RetLenVec(act.get_velocity())]
                    ret.append(dat)
        if ret == []:
            return [0,0]
        return sorted(ret, key=lambda idx: idx[0])[0]

    def SetSensorToActor(self, actorN, sensor = 'sensor.other.collision'):
        bp = self.world.get_blueprint_library().find(sensor)
        tf = carla.Transform(carla.Location(x=0.8, z=1.7))
        self.sensor = self.world.spawn_actor(bp, tf, attach_to=self.actor_list[actorN])
        if self.sensor == None: 
            print("Sensor Spawn failed")
            return
        else:
            print("Sensor Spawned")
            self.sensor.listen(lambda data: self.CollisionHandler(data))
    
    def CollisionHandler(self,data):
        if self.terminal == 0:
            self.terminal = 1
            self.terminalPerceived = False

    def RemoveActors(self):
        print('destroying actors')
        for actor in self.actor_list:
            actor.destroy()
        self.sensor.destroy() 
        self.actor_list = [] 
        self.terminal = 0
        print('done.')

# ==============================================================================
# -- Waypoint Handling ---------------------------------------------------------
# ==============================================================================
   
    def CreateWaypoints(self, distance = 2):
        self.wp_dis = distance
        self.wp_list =  self.map.generate_waypoints(distance)
        self.wp_listRoute = ["-" for wp in self.wp_list]

    def RetNextWPidx(self, startWP, minD = 0.1, maxD = 2.5, maxDeltaScal = 0.1, route = ""):
        assert len(self.wp_list) > 0, "Error! Waypoint list is empty"
        assert self.wp_dis > 0, "Error! Waypoints distance not defined"
        tmpWPd = [];tmpIdx = []
        for i in range(len(self.wp_list)):
            if route == "" or route == self.wp_listRoute[i]:
                wp = self.wp_list[i]
                d = self.RetDisWaypoints(startWP,wp,True)
                if self.wp_dis*minD < d and d < self.wp_dis*maxD:
                    scprStart = self.RetScalProd(self.RetVecWaypoints(startWP,wp),startWP.transform.get_forward_vector())
                    scprNext = self.RetScalProd(self.RetVecWaypoints(startWP,wp),wp.transform.get_forward_vector())
                    if  maxDeltaScal*d > math.fabs(scprStart-d) and maxDeltaScal*d > math.fabs(scprNext-d):
                        tmpIdx.append(i)
                        tmpWPd.append(d)

        if len(tmpIdx) > 0:
            idx = tmpWPd.index(min(tmpWPd))
            return tmpIdx[idx]
        return -1

    def RetWayPoint(self, location, project_to_road=True, lane_type=carla.LaneType.Driving):
        return self.map.get_waypoint(location, project_to_road=project_to_road, lane_type=lane_type)

    def RetWaypointIndex(self,waypoint):
        for i in range(len(self.wp_list)):
            if self.wp_list[i].id == waypoint.id:
                return i 
            return -1

    def RetWPAhead(self, startWP, stepsAhead = 1):
        waypoint = self.wp_list[self.RetNextWPidx(startWP)]
        if stepsAhead > 1:
            for i in range(stepsAhead-1):
                waypoint = self.wp_list[self.RetNextWPidx(waypoint)]
        return waypoint

# ==============================================================================
# -- Driving  ------------------------------------------------------------------
# ==============================================================================

    def UpdateActorTransformToWaypointDrive(self,actorN = 0, ShowHeadingPoint = False, maxD = 10):
        assert len(self.actor_list)>0, "Error! No Actor in List"
        if maxD < self.RetDisLocations(self.actor_list[0].get_location(),self.wp_list[self.actor_wpLog[actorN][1]].transform.location) \
        or 0 > self.RetHeadingPrecision(self.actor_list[0].get_transform(), self.wp_list[self.actor_wpLog[actorN][1]].transform):
            idx = self.RetNextWPidx(self.RetWayPoint(self.actor_list[0].get_location()), route=self.TargetRoute)
            assert not idx == self.actor_wpLog[actorN][1], "Error! Next Wp Index failure"
            self.actor_wpLog[actorN][0] = self.actor_wpLog[actorN][1]
            self.actor_wpLog[actorN][1] = self.RetNextWPidx(self.RetWayPoint(self.actor_list[0].get_location()), route=self.TargetRoute)
            ActorTransform = self.actor_list[actorN].get_transform()
            self.SetActorTransform(0,ActorTransform, self.wp_list[self.actor_wpLog[actorN][1]].transform, ShowHeadingPoint=ShowHeadingPoint)
            
    def ApplyGas(self,actorN, deltaV):
        self.SetActorVelocity(actorN,v = self.RetActorSpeed(actorN)+deltaV)

    def ApplyBrake(self,actorN, deltaV):
        self.SetActorVelocity(actorN,v = self.RetActorSpeed(actorN)-deltaV)

# ==============================================================================
# -- Debug functions ----------------------------------------------------------
# ==============================================================================

    def DrawPoint(self, location, color,lt = 180):
        self.world.debug.draw_point(location,life_time = lt,color=color)

    def DrawPointsFromIdx(self, locationsIdx, color,lt = 180):
        for i in locationsIdx:
            self.world.debug.draw_point(self.wp_list[i].transform.location,life_time = lt,color=color)

    def DrawString(self, location, text, color = carla.Color(0,0,0),lt = 180):
        self.world.debug.draw_string(location,text,life_time = lt,color=color)

    def DrawArrow(self, location, vector, color = carla.Color(0,0,200),lt = 180):
        locationB = carla.Location(x=location.x+vector.x,y=location.y+vector.y,z=location.z+vector.z)
        self.world.debug.draw_arrow(location,locationB,life_time = lt,color=color)

# ==============================================================================
# -- Basis geometry functions ----------------------------------------------------------
# ==============================================================================

    def RetDisLocations(self, locationA, locationB, includeZ = False):
        d2 = (locationA.x-locationB.x)*(locationA.x-locationB.x) + (locationA.y-locationB.y)*(locationA.y-locationB.y)
        if includeZ:
            d2 += (locationA.z-locationB.z)*(locationA.z-locationB.z)
        return math.sqrt(d2)

    def RetDisWaypoints(self, waypointA, waypointB, includeZ = False):
        return self.RetDisLocations(waypointA.transform.location,waypointB.transform.location,includeZ)

    def RetVecLocations(self, locationA, locationB):
        return carla.Vector3D(x= locationB.x-locationA.x, y= locationB.y-locationA.y, z= locationB.z-locationA.z)  

    def RetVecWaypoints(self, waypointA, waypointB):
        return self.RetVecLocations(waypointA.transform.location, waypointB.transform.location)

    def RetLenVec(self,vector, includeZ = False):
        d2 = vector.x*vector.x+vector.y*vector.y
        if includeZ:
            d2 += vector.z*vector.z
        return math.sqrt(d2)

    def RetScalProd(self, vectorA, vectorB, includeZ = False):
        s = vectorA.x*vectorB.x + vectorA.y*vectorB.y
        if includeZ:
            s += vectorA.z*vectorB.z
        return s

# ==============================================================================
# -- Basis functions ----------------------------------------------------------
# ==============================================================================
    
    def RetTransform(self,x,y,z,yaw):
        return carla.Transform(carla.Location(x=x, y=y, z=z), carla.Rotation(yaw=yaw))

    def RetTransformOffset(self,transform, x=0,y=0,z=0,yaw=0, pitch=0, roll=0):
        return carla.Transform(carla.Location(x=transform.location.x+x, y=transform.location.y+y, z=transform.location.z+z), \
            carla.Rotation(yaw=transform.rotation.yaw+yaw, pitch=transform.rotation.pitch+pitch, roll = transform.rotation.roll+roll))

    def ReturnPosition(self,transform):
        return [transform.location.x, transform.location.y, transform.location.z]
    
    def RetLocationAslist(self,location, includeZ = False, rund = 2):
        if includeZ:
            return [round(location.x,rund), round(location.y,rund), round(location.z,rund)]
        return [round(location.x,rund), round(location.y,rund)]

    def RetHeadingPrecision(self,EgoTransform, TargetTransform):
        return self.RetScalProd(EgoTransform.get_forward_vector(), self.RetVecLocations(EgoTransform.location,TargetTransform.location))

    def RetRoute(self, location):
        idx = self.RetNextWPidx(self.RetWayPoint(location))
        return self.wp_listRoute[idx]

    def TickAfterTimeStep(self, timestep):
        self.world.tick()
        t1 = self.world.wait_for_tick().elapsed_seconds
        tstamp = t1
        while tstamp-t1 < timestep:
            self.world.tick()
            tstamp = self.world.wait_for_tick().elapsed_seconds
        return

    def Tick(self):
        self.world.tick()
        self.world.wait_for_tick()
        return

# ==============================================================================
# -- Export Import ----------------------------------------------------------
# ==============================================================================

    def ExportWPStoCSV(self, path, SplitCols = False, roundTo = 4):
        # Create full size data frame
        WPpd = pd.DataFrame()
        WPpd["location.x"] = [round(wp.transform.location.x,roundTo) for wp in self.wp_list]
        WPpd["location.y"] = [round(wp.transform.location.y,roundTo) for wp in self.wp_list]
        WPpd["location.z"] = [round(wp.transform.location.z,roundTo) for wp in self.wp_list]
        WPpd["vector.x"] = [round(wp.transform.get_forward_vector().x,roundTo) for wp in self.wp_list]
        WPpd["vector.y"] = [round(wp.transform.get_forward_vector().y,roundTo) for wp in self.wp_list]
        WPpd["vector.z"] = [round(wp.transform.get_forward_vector().z,roundTo) for wp in self.wp_list]
        WPpd["Route"] = [Route for Route in self.wp_listRoute]
        WPpd.to_csv(path, sep='|', encoding='utf-8', index = False)

    def ImportWPS(self,dataset_path, route = "", IsRoute = True):
        def WPAppend(self, df, col):
            x = WPImport.at[col,"location.x"]
            y = WPImport.at[col,"location.y"]
            z = WPImport.at[col,"location.z"]
            self.wp_list.append(self.RetWayPoint(carla.Location(x,y,z)))
            self.wp_listRoute.append(WPImport.at[col,"Route"])
        
        self.wp_list = []
        WPImport = pd.read_csv(dataset_path, skiprows = 0, na_values = "?", \
        comment='\t', sep="|", skipinitialspace=True, error_bad_lines=False)
        
        for col, _ in WPImport.iterrows():
            if IsRoute == False:
                WPAppend(self, WPImport, col)
            if IsRoute == True and route == "" and WPImport.at[col,"Route"].find("route")>-1:
                WPAppend(self, WPImport, col)
            if not route == "" and WPImport.at[col,"Route"] == route:
                WPAppend(self, WPImport, col)

    def ExportDrivenWPSIdxtoCSV(self, path, SplitCols = False, roundTo = 4):
        # Create full size data frame
        WPpd = pd.DataFrame()
        WPpd["Start, End"] = [wpIdx for wpIdx in self.actor_wpLog[0]]
        WPpd.to_csv(path, sep='|', encoding='utf-8', index = False)

# ==============================================================================
# -- Appendix: Route Creation --------------------------------------------------
# ==============================================================================    
    
    def RetListWPIdx(self,startWP, maxN = 5000):
        EgoWPsIdx = []
        firstWPidx = self.RetNextWPidx(startWP)
        EgoWPsIdx.append(firstWPidx)
        for i in range(1,maxN):
            nxtIdx = self.RetNextWPidx(self.wp_list[EgoWPsIdx[i-1]])
            if nxtIdx == -1:
                print("Error! Next Waypoint not found")
                return EgoWPsIdx
            if nxtIdx == firstWPidx and maxN == 5000:
                print("Waypoint Route closed")
                return EgoWPsIdx
            EgoWPsIdx.append(nxtIdx)
            print("Next Waypoint: " + str(self.RetLocationAslist(self.wp_list[nxtIdx].transform.location)),end ='\r')
        print("Error! Waypoint Route not closed")
        return EgoWPsIdx

    def SetWPRouteList(self, WPIdxList, text):
        for idx in WPIdxList:
            self.wp_listRoute[idx] = text 

# ==============================================================================
# -- frequently used API -------------------------------------------------------
# ==============================================================================   


# carla.Waypoint (class)
# -----------------------------------
# id (int)
# transform (carla.Transform)
# is_intersection (bool)
# is_junction (bool)
# lane_width (float)
# road_id (int)
# section_id (int)
# lane_id (int)
# s (float)
# lane_change (carla.LaneChange)
# lane_type (carla.LaneType)
# right_lane_marking (carla.LaneMarking)
# left_lane_marking (carla.LaneMarking)
# next(self, distance)
# get_right_lane(self)
# get_left_lane(self)

# carla.Transform (class)
# -----------------------------------
# location (carla.Location)
# rotation (carla.Rotation)
# transform(self, in_point)
# get_forward_vector(self)

# carla.Location(carla.Vector3D)
# -----------------------------------
# x (float)
# y (float)
# z (float)
# __init__(self, x=0.0, y=0.0, z=0.0)
# distance(self, location)

# carla.Rotation class
# -----------------------------------
# pitch (float)
# yaw (float)
# roll (float)
# __init__(self, pitch=0.0, yaw=0.0, roll=0.0)
# get_forward_vector(self)