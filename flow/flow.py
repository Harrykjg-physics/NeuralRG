
import numpy as np
import torch
from torch import nn

class Flow(nn.Module):

    def __init__(self, prior = None,name = "Flow"):
        super(Flow, self).__init__()
        self.name = name
        self.prior = prior

    def __call__(self,*args,**kargs):
        return self.sample(*args,**kargs)

    def sample(self,batchSize, prior = None):
        if prior is None:
            prior = self.prior
        assert prior is not None
        z = prior.sample(batchSize)
        logp = prior.logProbability(z)
        x,logp_ = self.generate(z)
        return x,logp+logp_

    def inference(self,x):
        raise NotImplementedError(str(type(self)))

    def generate(self,z):
        raise NotImplementedError(str(type(self)))

    def logProbability(self,x):
        z,logp = self.inference(x)
        if self.prior is not None:
            return self.prior.logProbability(z)+logp
        return logp

    def save(self,saveDict):
        saveDict[self.name] = self.state_dict()
        return saveDict

    def load(self,saveDict):
        self.load_state_dict(saveDict)
        return saveDict