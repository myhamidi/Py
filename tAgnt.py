import Agnt

class clsAgent(Agnt.clsAgent):
    pass

    def TrainQ(self, maxIterations):
        flag = False
        for k in range(maxIterations):
            if self.buffer == self.batch:
                CopyQ = [[state.Q[j] for j in range(4)] for state in self.States]
                for i in range(len(self.Sequence)):
                    state0 = self.Sequence[i].state0; s0Idx = [state.features for state in self.States].index(state0)
                    state1 = self.Sequence[i].state1; s1Idx = [state.features for state in self.States].index(state1)
                    r = self.Sequence[i].reward
                    a = self.Sequence[i].actionInt
                    self.States[s0Idx].Q[a] = CopyQ[s0Idx][a] + self.alpha*(r +self.gamma*max(CopyQ[s1Idx]) - CopyQ[s0Idx][a])
                    if self.Sequence[i].state1[-1]==1:
                        state1 = self.Sequence[i].state1; s1Idx = [state.features for state in self.States].index(state1)
                        self.States[s1Idx].Q = [self.Sequence[i].totalreward]*4
                CopyQ2 = [[state.Q[j] for j in range(4)] for state in self.States]
                if CopyQ == CopyQ2:
                    print("No further progress in Q Training. Stopped at iteration: " + str(k))
                    break