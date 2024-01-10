'''
Created on Jan 9, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

import json
import time
from ttdemoboard.pins import Pins

class Design:
    def __init__(self, projectMux, projindex:int, info:dict):
        self.mux = projectMux
        self.project_index = projindex
        self.count = int(projindex)
        self.name = info['macro']
        self.repo = info['repo']
        self.commit = info['commit']
        self._all = info
        
    def enable(self):
        self.mux.enable(self)
        
    def __str__(self):
        return self.name 
    
    def __repr__(self):
        return f'<Design {self.project_index}: {self.name}>'
        
class DesignIndex:
    def __init__(self, projectMux, srcJSONFile:str='shuttle_index.json'):
        self._shuttle_index = dict()
        self._project_count = 0
        with open(srcJSONFile) as fh:
            index = json.load(fh)
            for project in index["mux"]:
                des = Design(projectMux, project, index["mux"][project])
                self._shuttle_index[des.name] = des
                setattr(self, des.name, des)
                self._project_count += 1
                
    @property 
    def count(self):
        return self._project_count
                
    @property 
    def names(self):
        return self._shuttle_index.keys()
    
    @property 
    def all(self):
        return self._shuttle_index.values()
                
        
class ProjectMux:
    def __init__(self, pins:Pins):
        self.p = pins 
        self._design_index = None
        self.enabled = None
    
    def reset(self): 
        self.p.cinc(0)
        self.p.ncrst(0)
        self.p.ctrl_ena(0)
        time.sleep_ms(10)
        self.p.ncrst(1)
        time.sleep_ms(10)
        self.enabled = None
        
    def enable(self, design:Design):
        self.reset()
        # send the number of pulses required
        for _c in range(design.count):
            self.p.cinc(1)
            time.sleep_ms(1)
            self.p.cinc(0)
            time.sleep_ms(1)
        
        self.p.ctrl_ena(1)
        self.enabled = design
    
    @property
    def projects(self):
        if self._design_index is None:
            self._design_index = DesignIndex(self)

        return self._design_index
    
    
    
    
    def __getattr__(self, name):
        if hasattr(self.projects, name):
            return getattr(self.projects, name)
        raise AttributeError
        