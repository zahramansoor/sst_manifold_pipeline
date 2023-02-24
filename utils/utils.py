# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 16:06:02 2023

@author: Han
"""

import os, sys

def makedir(dr):
    if not os.path.exists(dr): os.mkdir(dr)
    return 
