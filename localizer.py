# Script for calculating localizers

import os
import numpy as np
from nilearn.glm.first_level import make_first_level_design_matrix
from nilearn.glm.first_level import FirstLevelModel

"""
Workflow:

1) load subject data
2) downsample to ico32 (10242 vertices)
3) create design matrix
4) fit model
5) calculate contrasts
5) extract t-maps, save outputs
"""

#helper functions
def get_subjects(data_dir):
    dirs = [x[0] for x in os.walk(data_dir)]
    return [d for d in dirs if 'subj' in d]

def get_data():
    #data loading function for a subject, probably nibabel or numpy

def downsample_data(array, mask_indices):

    ico32_mask = np.zeros((array.shape[0], 10242, array.shape[-1])) ## TODO: create full matrix of zeros, mask ico32 with ones

    ds = array[:,:10241,:] #slicing array to ico32
    mask = np.ma.array(array, mask=False)



def get_timing():
    #get stimuli timing for design matrix, probably separate csv file

def get_nuisance():
    #get nuiscance regressors for design matrix, probably in timing file

def create_basic_contrasts(design_matrix):
    #lifted from nilearn tutorial (https://shorturl.at/fAYGT), may need tweaking
    contrast_matrix = np.eye(design_matrix.shape[1])
    basic_contrasts = {
        column: contrast_matrix[i]
        for i, column in enumerate(design_matrix.columns)
        }

### Workflow, may need tweaking ###
subjects = get_subjects() ## TODO: figure out data directory

#testing on first subject
subject_data = get_data(subjects[0])
frame_times = subject_data.shape[0]
events = get_timing()
confounds = get_nuisance()
contrasts = create_basic_contrasts()

fmri_glm = FirstLevelModel()
design_matrices = make_first_level_design_matrix(
    frame_times=frame_times,
    events=events,
    confounds=confounds,
    )
fmri_glm = fmri_glm.fit(subject_data, design_matrices=design_matrices)
fmri_glm.compute_contrast(contrasts)

with open("subject_01_report", "w") as file:
    file.write(fmri.glm.generate_report())
