# procnii_todcm

Convert processed NIfTI files (`.nii` / `.nii.gz`) to DICOM using
`nibabel` and `nii2dcm`.

## Installation 

In a mamba environment (or replace "mamba" to "conda" for conda env):

```bash
mamba create -n procnii python=3.14
mamba activate procnii
pip install -e .

# Verify
procnii_todcm -h

## Usage
Run the test case (from the root directory):

```bash
procnii_todcm \
    --img ./test/input/subj1/subj1_T1.nii.gz \
    --mask ./test/input/subj1/subj1_T1_seg.nii.gz \
    --mapping ./test/input/subj1/mapping.json \
    --refdcm ./test/input/subj1/subj1_slice1.dcm \
    --out ./test/output/subj1/subj1_merged.nii.gz

