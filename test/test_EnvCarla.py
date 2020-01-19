import sys
sys.path.append("C:\\temp Daten\\Lernbereich\\Git\\myhamidi\\Py")

import EnvCarla
import Agnt

def test_LoadWorld():
    Env = EnvCarla.clsCarlaEnv(nWorld = 1, smode=False, rmode=True)
    time.sleep(1) # Carla needs some time after map was loaded, the python script hat to stay alive during that time

def test_SpawnActor():
    Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=True)
    Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
    Env.wp_dis =5
    Env.SpawnActor(2,20,spectator=True)

def test_FollowWaypoints():
    Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=True)
    Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
    Env.wp_dis =5
    Env.SpawnActor(2,10,spectator=True)
    Env.ShowTargetWaypoint = True
    Env.SetStartTime()
    while Env.DeltaTime < 5:
            Env.Next()

def test_FollowWaypoints2Actors():
    Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=True)
    Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
    Env.wp_dis =5
    try:
        Env.SpawnActor(20,10,spectator=False)
        Env.SpawnActor(29,10,spectator=False)
        print(len(Env.actor_list))
        Env.ShowTargetWaypoint = True
        Env.SetStartTime()
        while Env.DeltaTime < 10:
            if Env.actor_speed[0] < 40 and Env.DeltaTime < 5:
                Env.Next([0],"gas",0.5)
            if Env.actor_speed[0] >= 0 and Env.DeltaTime > 6:
                Env.Next([0], "brake",0.5)
            print(Env.RetStateFeatures())
            print(Env.DeltaTime)
    finally:
        Env.RemoveActors()

def test_RewardState():
    Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=True)
    Agt = Agnt.clsAgent(Env.ReturnActionList(),Env.ReturnFeatureList())
    Agt.PerceiveEnv([0,0],0)
    Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
    Env.wp_dis =5
    try:
        Env.SpawnActor(20,15,spectator=False)
        Env.SpawnActor(29,25,spectator=False)
        print(len(Env.actor_list))
        Env.ShowTargetWaypoint = True
        Env.SetStartTime()
        Agt.SetParameter(["epsilon"],[[1, 0.60, 0.2, 0.2]])
        while Env.Time() - Env.StartTime < 30:
            Env.Next()
            if Env.Time() - Env.LastActionTime > 1:
                print(Env.RetStateFeatures())
                print(Env.RetReward())
                Agt.PerceiveEnv(Env.RetStateFeatures(),Env.RetReward())
                Env.NextAction([0], Agt.NextAction())
        Agt.Sequence.Export("csv/test/exports/AgtSeqFromCarla.csv")
    finally:
        Env.RemoveActors()

def test_showwaypoint():
    Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=True)
    Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True)
    Env.wp_dis = 5
    Env.SetStartTime()
    Env.SpawnActor(20,15,spectator=False)
    for i in range(len(Env.wp_list)):
        Env.DrawString(Env.wp_list[i].transform.location, str(i), EnvCarla.carla.Color(0,0,0), lt=600)
    while Env.Time() - Env.StartTime < 10:
        Env.Next()

def test_CreateScene():
    try:
        Env = EnvCarla.clsCarlaEnv(nWorld = 4, smode=False, rmode=True)
        Env.ImportWPS("csv/Carla-WPs-5.csv", IsRoute=True, ImpodrtIdx=True)
        Env.wp_dis = 5
        Env.ShowTargetWaypoint = True
        scene = "[road has lanes 3, \
lane 1 has vehicle at 0 with speed 20 has vehicle at 45 with speed 30, \
lane 2 has egovehicle with speed 28 has vehicle at 50 with speed 30, \
lane 3 has vehicle at -20 with speed 20 has vehicle at 10 with speed 20]"
        Env.SpawnActor(556,25,spectator=False)
        # Env.SpawnActor(554,25,spectator=False)
        # Env.SpawnScene(scene, 115)
        Env.SetStartTime()
        while Env.Time() - Env.StartTime < 20:
            Env.Next()
    finally:
        Env.RemoveActors()


# test_LoadWorld()
# test_SpawnActor()
# test_FollowWaypoints()
# test_FollowWaypoints2Actors()
# test_RewardState()
# test_showwaypoint()
test_CreateScene()