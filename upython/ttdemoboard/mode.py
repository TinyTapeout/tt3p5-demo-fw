'''
Created on Jan 23, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''


class RPMode:
    SAFE = 0
    ASICONBOARD = 1
    ASIC_MANUAL_INPUTS = 2
    STANDALONE = 3
    
    @classmethod
    def fromString(cls, s:str):
        modeMap = {  
            'SAFE': cls.SAFE,
            'ASICONBOARD': cls.ASICONBOARD,
            'ASIC_MANUAL_INPUTS': cls.ASIC_MANUAL_INPUTS,
            'STANDALONE': cls.STANDALONE
        }
        
        if s is None or not hasattr(s, upper):
            return None
        sup = s.upper()
        if sup not in modeMap:
            # should we raise here?
            return None 
        
        return modeMap[sup]
    
    @classmethod
    def toString(cls, mode:int):
        nameMap = { 
            cls.SAFE: 'SAFE',
            cls.ASICONBOARD: 'ASICONBOARD',
            cls.ASIC_MANUAL_INPUTS: 'ASIC_MANUAL_INPUTS',
            cls.STANDALONE: 'STANDALONE'
        }
        if mode in nameMap:
            return nameMap[mode]
        
        return 'UNKNOWN'