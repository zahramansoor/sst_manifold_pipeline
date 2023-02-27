# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 15:45:37 2023

@author: Han
"""



import os, sys, shutil, suite2p
import argparse   
import pandas as pd, numpy as np
from utils.utils import makedir

def main(**args):
    
    #args should be the info you need to specify the params
    # for a given experiment, but only params should be used below
    params = fill_params(**args)    
    
    if args["stepid"] == 0:
        #######################################MAKE FOLDERS######################################################

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
        #######################################CHECK TO SEE IF FILES ARE TRANSFERRED AND MAKE TIFS###################################################
        
        #check to see if imaging files are transferred
        imagingfl=[xx for xx in os.listdir(os.path.join(params["datadir"],
                                        params["mouse_name"], params["day"])) if "000" in xx][0]
        imagingflnm=os.path.join(params["datadir"], params["mouse_name"], params["day"], imagingfl)
        sbxfl=[os.path.join(imagingfl,xx) for xx in os.listdir(imagingflnm) if "sbx" in xx]
        if len(imagingfl)==1:
            #convert sbx to tif
            import matlab.engine
            eng = matlab.engine.start_matlab()
            eng.loadVideoTiffNoSplit_EH2_new_sbx_uint16(imagingflnm,sbxfl,"bi new") #bi new=scan type
        
    elif args["stepid"] == 11:
        #######################################RUN SUITE2P###################################################
        
        #check to see if imaging files are transferred
        imagingfl=[xx for xx in os.listdir(os.path.join(params["datadir"],
                                        params["mouse_name"], params["day"])) if "000" in xx][0]
        if len(imagingfl)==1:           
            #do suite2p
            # set your options for running
            ops = suite2p.default_ops() # populates ops with the default options
            #edit ops if needed
            ops["reg_tif"]=True
            ops["nplanes"]=1
            ops["delete_bin"]=False
            ops["move_bin"]=False
            
            # provide an h5 path in 'h5py' or a tiff path in 'data_path'
            # db overwrites any ops (allows for experiment specific settings)
            db = {
                  'h5py': [], # a single h5 file path
                  'h5py_key': 'data',
                  'look_one_level_down': False, # whether to look in ALL subfolders when searching for tiffs
                  'data_path': [os.path.join(params["datadir"], params["mouse_name"], params["day"], imagingfl)], # a list of folders with tiffs 
                                                         # (or folder of folders with tiffs if look_one_level_down is True, or subfolders is not empty)
                                                       
                  'subfolders': [], # choose subfolders of 'data_path' to look in (optional)
                  # 'fast_disk': 'C:/BIN', # string which specifies where the binary file will be stored (should be an SSD)
                }

        # run one experiment
        opsEnd = suite2p.run_s2p(ops=ops, db=db)

    elif args["stepid"] == 21:
        ####################################POST CNN --> INITIALISING RECONSTRUCTED ARRAY FOR ARRAY JOB####################################
        
        sys.stdout.write("\ninitialising reconstructed array...\n"); sys.stdout.flush()
        np.lib.format.open_memmap(params["reconstr_arr"], mode="w+", shape = params["inputshape"], dtype = params["dtype"])
        sys.stdout.write("done :]\n"); sys.stdout.flush()

    elif args["stepid"] == 2:
        #####################################POST CNN --> RECONSTRUCTION AFTER RUNNING INFERENCE ON TIGER2#################################
        
        #reconstruct
        sys.stdout.write("\nstarting reconstruction...\n"); sys.stdout.flush()
        reconstruct_memmap_array_from_tif_dir(**params)
        if params["cleanup"]: shutil.rmtree(params["cnn_dir"])

    elif args["stepid"] == 3:
        ##############################################POST CNN --> FINDING CELL CENTERS#####################################################   
        
        save_params(params, params["data_dir"])
        
        #find cell centers, measure sphericity, perimeter, and z span of a cell
        csv_dst = calculate_cell_measures(**params)
        sys.stdout.write("\ncell coordinates and measures saved in {}\n".format(csv_dst)); sys.stdout.flush()
        
    elif args["stepid"] == 4:
        ##################################POST CNN --> CONSOLIDATE CELL CENTERS FROM ARRAY JOB##############################################
        
        #part 1 - check to make sure all jobs that needed to run have completed; part 2 - make pooled results
        consolidate_cell_measures(**params)


def fill_params(scratch_dir, expt_name, stepid, jobid):

    params = {}

    #slurm params
    params["stepid"]        = stepid
    params["jobid"]         = jobid 
    
    #experiment params
    params["expt_name"]     = os.path.basename(os.path.abspath(expt_name))
        
    params["scratch_dir"]   = scratch_dir
    params["data_dir"]      = os.path.join(params["scratch_dir"], params["expt_name"])
    
    #changed paths after cnn run
    params["cnn_data_dir"]  = os.path.join(params["scratch_dir"], params["expt_name"])
    params["cnn_dir"]       = os.path.join(params["cnn_data_dir"], "output_chnks") #set cnn patch directory
    params["reconstr_arr"]  = os.path.join(params["cnn_data_dir"], "reconstructed_array.npy")
    params["output_dir"]    = params["cnn_data_dir"]
    
    #pre-processing params
    params["dtype"]         = "float32"
    params["cores"]         = 8
    params["verbose"]       = True
    params["cleanup"]       = False
    
    params["window"]        = (20, 192, 192)
    
    #way to get around not having to access lightsheet processed directory in later steps
    try:
	#find cell channel tiff directory
        fsz                     = os.path.join(expt_name, "full_sizedatafld")
        vols                    = os.listdir(fsz); vols.sort()
        src                     = os.path.join(fsz, vols[len(vols)-1]) #hack - try to load param_dict instead?
        if not os.path.isdir(src): src = os.path.join(fsz, vols[len(vols)-2])     
        params["cellch_dir"]    = src
        params["inputshape"]    = get_dims_from_folder(src)
        params["patchsz"]       = (60, int((params["inputshape"][1]/2)+320), int((params["inputshape"][2]/2)+320)) #cnn window size for lightsheet = typically 20, 192, 192 for 4x, 20, 32, 32 for 1.3x
        params["stridesz"]      = (params["patchsz"][0]-params["window"][0], params["patchsz"][1]-params["window"][1],
                                   params["patchsz"][2]-params["window"][2])
        params["patchlist"]     = make_indices(params["inputshape"], params["stridesz"])
    except:
        dct = csv_to_dict(os.path.join(params["cnn_data_dir"], "cnn_param_dict.csv"))
        if "cellch_dir" in dct.keys():
            params["cellch_dir"]    = dct["cellch_dir"]
        
        params["inputshape"]    = dct["inputshape"]
        params["patchsz"]       = dct["patchsz"] 
        params["stridesz"]      = dct["stridesz"]
        params["patchlist"]     = dct["patchlist"]
        
    
    #model params - useful to save for referenece; need to alter per experimental cohort
    params["model_name"] = "20200316_peterb_zd_train"
    params["checkpoint"] = 12000
    #post-processing params
    params["threshold"]     = (0.80,1) #h129 = 0.6; prv = 0.85; this depends on model
    params["zsplt"]         = 30
    params["ovlp_plns"]     = 30
        
    return params

def save_params(params, dst):
    """ 
    save params in cnn specific parameter dictionary for reconstruction/postprocessing 
    can discard later if need be
    """
    (pd.DataFrame.from_dict(data=params, orient="index").to_csv(os.path.join(dst, "cnn_param_dict.csv"),
                            header = False))
    sys.stdout.write("\nparameters saved in: {}".format(os.path.join(dst, "cnn_param_dict.csv"))); sys.stdout.flush()
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument("stepid", type=int,
                        help="Step ID to run patching, reconstructing, or cell counting")
    parser.add_argument("jobid",
                        help="Job ID to run as an array job")
    parser.add_argument("expt_name",
                        help="Tracing output directory (aka registration output)")
    parser.add_argument("scratch_dir",
                        help="Scratch directory to store image chunks/memory mapped arrays")
    
    args = parser.parse_args()
    
    main(**vars(args))