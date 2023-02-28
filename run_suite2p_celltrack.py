# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:45:37 2023

@author: Han
"""

import os, sys, shutil, suite2p, tifffile
import argparse   
import pandas as pd, numpy as np
from utils.utils import makedir

def main(**args):
    
    #args should be the info you need to specify the params
    # for a given experiment, but only params should be used below
    params = fill_params(**args)    
    
    if args["stepid"] == 0:
        ###############################MAKE FOLDERS#############################

        #check to see if day directory exists
        if not os.path.exists(os.path.join(params["datadir"],params["mouse_name"], params["day"])): 
            print(f"Folder for day {params['day']} of mouse {params['mouse_name']} does not exist. \n\
                  Making folders...")
            makedir(os.path.join(params["datadir"],params["mouse_name"], params["day"]))
            #behavior folder
            makedir(os.path.join(params["datadir"],params["mouse_name"], params["day"], "behavior"))
            makedir(os.path.join(params["datadir"],params["mouse_name"], params["day"], "behavior", "vr"))
            makedir(os.path.join(params["datadir"],params["mouse_name"], params["day"], "behavior", "clampex"))
            #camera 
        
    	
    elif args["stepid"] == 1:
        ####CHECK TO SEE IF FILES ARE TRANSFERRED AND MAKE TIFS/RUN SUITE2P####
        #args should be the info you need to specify the params
        # for a given experiment, but only params should be used below
        params = fill_params(**args) 
        
        print(params)
        #check to see if imaging files are transferred
        imagingfl=[xx for xx in os.listdir(os.path.join(params["datadir"],
                                        params["mouse_name"], params["day"])) if "000" in xx][0]
        imagingflnm=os.path.join(params["datadir"], params["mouse_name"], params["day"], imagingfl)
        sbxfl=[os.path.join(imagingflnm,xx) for xx in os.listdir(imagingflnm) if "sbx" in xx][0]
        
        if len(imagingfl)!=0:           
            print(imagingfl)
            #https://github.com/jcouto/sbxreader; download dependency
            from sbxreader import sbx_memmap
            dat = sbx_memmap(sbxfl)
            #check if tifs exists

            #copied from ed's legacy version: loadVideoTiffNoSplit_EH2_new_sbx_uint16
            for nn,i in enumerate(range(0, dat.shape[0], 3000)): #splits into tiffs of 3000 planes each
                stack = np.array(dat[i:i+3000])
                #crop in x
                stack=np.squeeze(stack)[:,:,89:718] #hard coded crop from ed's og script
                tifffile.imwrite(sbxfl[:-4]+f'_{nn+1:03d}.tif', stack.astype('uint16'))

            #do suite2p
            # set your options for running
            ops = suite2p.default_ops() # populates ops with the default options
            #edit ops if needed, based on user input
            ops["reg_tif"]=params["reg_tif"] 
            ops["nplanes"]=params["nplanes"] 
            ops["delete_bin"]=params["delete_bin"] #False
            ops["move_bin"]=params["move_bin"]
            ops["save_mat"]=params["save_mat"]
            
            # provide an h5 path in 'h5py' or a tiff path in 'data_path'
            # db overwrites any ops (allows for experiment specific settings)
            db = {
                  'h5py': [], # a single h5 file path
                  'h5py_key': 'data',
                  'look_one_level_down': False, # whether to look in ALL subfolders when searching for tiffs
                  'data_path': [imagingflnm], # a list of folders with tiffs 
                                                         # (or folder of folders with tiffs if look_one_level_down is True, or subfolders is not empty)
                                                       
                  'subfolders': [], # choose subfolders of 'data_path' to look in (optional)
                  # 'fast_disk': 'C:/BIN', # string which specifies where the binary file will be stored (should be an SSD)
                }

            # run one experiment
            opsEnd = suite2p.run_s2p(ops=ops, db=db)

def fill_params(mouse_name, day, datadir, reg_tif, nplanes, delete_bin,
                move_bin, stepid, save_mat):

    params = {}

    #slurm params
    params["stepid"]        = stepid
    
    #experiment params
    params["mouse_name"]    = mouse_name        
    params["day"]           = day
    params["datadir"]       = datadir
    #suite2p params
    params["reg_tif"]       = reg_tif
    params["nplanes"]       = nplanes
    params["delete_bin"]    = delete_bin
    params["move_bin"]      = move_bin
    params["save_mat"]      = save_mat
        
    return params

def save_params(params, dst):
    """ 
    save params in parameter dictionary for reconstruction/postprocessing 
    """
    (pd.DataFrame.from_dict(data=params, orient="index").to_csv(os.path.join(dst, "param_dict.csv"),
                            header = False))
    sys.stdout.write("\nparameters saved in: {}".format(os.path.join(dst, "param_dict.csv"))); sys.stdout.flush()
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument("stepid", type=int,
                        help="Step ID to run folder name, suite2p processing, cell tracking")
    parser.add_argument("mouse_name",
                        help="e.g. E200")
    parser.add_argument("day", type=str,
                        help="day of imaging")
    parser.add_argument("datadir", type=str,
                        help="Main directory with mouse names and days")
    parser.add_argument("--reg_tif", default=True,
                        help="Whether or not to save move corrected imagings")
    parser.add_argument("--nplanes", default=1,
                        help="Number of planes imaged")
    parser.add_argument("--delete_bin", default=False,
                        help="Delete data.bin to run suite2p")
    parser.add_argument("--move_bin", default=False,
                        help="Move data.bin from fast disk")
    parser.add_argument("--save_mat", default=True,
                        help="Save Fall.mat (needed for cell tracking)")    
    
    args = parser.parse_args()
    
    main(**vars(args))