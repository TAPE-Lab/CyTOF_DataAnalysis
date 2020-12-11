
import os
import sys

import numpy as np
import pandas as pd
import umap

# import warnings
# warnings.filterwarnings('ignore')

# UMAP function
# umap embedding calculation; result saved in a pandas dataframe
# the names of the umap info columns are also defined here

def perform_umap(umap_params, all_together_vs_marks, no_arc):
    info_run = umap_params["info"]
    run_name = "UMAP_"+info_run
    #Calculate UMAP on arc tranf data (all_together...)
    umap_emb = pd.DataFrame(umap.UMAP(n_neighbors=umap_params["n"], 
                                min_dist=umap_params["m"],
                                metric=umap_params["d"],
                                n_components=umap_params["comp"],
                                repulsion_strength=umap_params["rs"],
                                negative_sample_rate=umap_params["nsr"]
                            ).fit_transform(all_together_vs_marks), 
                            columns=[f"{run_name}_D1",f"{run_name}_D2"])
    # append umap info columns into untransformed data
    # no_arc[run_name+"_D1"] = umap_emb[run_name+"_D1"]
    # no_arc[run_name+"_D2"] = umap_emb[run_name+"_D2"]
    umap_emb = umap_emb.reset_index(drop=True)
    no_arc = no_arc.reset_index(drop=True)
    no_arc = no_arc.join(umap_emb)

    return no_arc
        


            