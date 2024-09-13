#Pseudocode for calculating functional connectivity matrices

import neuroboros as nb
from scipy.spatial.distance import pdist, cdist, squareform

# Assumptions:
#   Functional data has already been transformed into surface data
#   Subject surface data is already divided by hemisphere

data = load_data(subj[0],'l') #fake function for loading  subject data

"""
taken from neuroboros/src/neuroboros/spaces.py > get_mapping()

df get_mapping(
    lr,
    source,
    target,
    mask=None,
    nn=False,
    keep_sum=False,
    source_mask=None,
    target_mask=None,
    **kwargs,
):
    Get mapping (transform) from one space to another.

    Parameters
    ----------
    lr : str
        Hemisphere, either 'l' or 'r'.
    source : str
        Source space, the space where the data is currently in.
    target : str
        Target space, the space where the data will be transformed into.
    mask : bool or boolean array or None
        Mask to apply to the mapping. If None or False, no mask is applied.
        If True, the group-based cortical mask is used.
        If a boolean array, it is used as the mask.
        ``source_mask`` and ``target_mask`` can be set separately, and they
        take precedence over ``mask``.
    nn : bool
        If True, use nearest neighbor interpolation.
        If False, use overlap-area-based interpolation.
    keep_sum : bool
        If True, keep the sum of the data. Useful for transforming area,
        volume, etc., where the total area/volume is preserved when
        ``keep_sum=True``.
    source_mask : bool or boolean array or None
        Mask to apply to the source space. Similar to ``mask``.
    target_mask : bool or boolean array or None
        Mask to apply to the target space. Similar to ``mask``.

    Returns
    -------
    M : sparse matrix
        Mapping matrix. Can be applied to data in the source space to
        transform it into the target space. For example, if ``X`` is a
        data matrix in the source space, then ``X @ M`` is the data matrix
        in the target space.


"""
xfm = nb.mapping('l', 'onavg-ico32', 'onavg-ico8', mask=True) #from tutorial
# onavg-ico32: 10,242 vertices per hemisphere; ~4mm vertex spacing
# onavg-ico8: 642 vertices per hemisphere; 10.7 mm vertex spacing

# mask=True > "group-based cortical mask is used"
# Where does this mask come from?
# Is this how the medial wall is removed?
# ***To-do: How to get group-level mask of medial wall? !!!

dm = data @ xfm #matrix multiplication, downsamples data to onavg-ico8

# Functional connectivity
fc = 1 - cdist(dm.T, data.T, 'correlation')
# Why 1-distance?
# Why distance correlation?
# Perhaps there are non-linear correlation between timeseries,
# but don't older papers use Pearson r?

# Should we calculate fc for every subject first?   !!!
hemis = ['l', 'r']
fc_mats = {}
for hemi in hemis:
    for subj in subj_list:
        subj_data = load_data(subj, hemi)
        subj_downsamp = data @ xfm
        key = f'{hemi}_{subj}'
        fc_mats[key] = 1 - cdist(subj_downsamp.T, subj_data.T, 'correlation)

# Searchlights
radius = 20 #what radius are we using?  !!!
sls, dists = nb.sls('l', radius, return_dists=True)

# Hyperalignment >> is this pyMVPA? !!!
from hyperalignment.procrustes import procrustes
from hyperalignment.searchlight import searchlight_procrustes

for hemi in hemis:
    for subj_a in subj_list:
        key_a = f'{hemi}_{subj_a}'
        conn1 = fc_mats[key_a]

        for subj_b in subj_list:
            if subj_a == subj_b:
                continue
            else:
                key_b = f'{hemi}_{subj_b}'
                conn2 = fc_mats[key_b]
                cha_procr = searchlight_procrustes(conn1, conn2, sls, dists, radius)

# If not pyMVPA implementation, what does searchlight_procrustes return?  !!!
# ***To-do: ask Jiahui if this workflow makes sense for CHA
# ***To-do: figure out searchlight_procrustes returns
# ***To-do: figure out how to split groups into train/test
#   CV-splits?
#   Probably should do a simple split first to see if this even works
