# procnii_todcm

Converts processed NIfTI files (`.nii` / `.nii.gz`) to DICOM using `nibabel` and `nii2dcm`.

>[!NOTE]
>Current functionality is limited to merging a segmentation mask to an underlay image and saving the result as dicom

## Installation 
```bash
mamba create -n procnii python=3.14
mamba activate procnii
git clone https://github.com/gurayerus/procnii_todcm
cd procnii_todcm
pip install -e .
```
>[!NOTE]
>Package will be installed in a mamba environment. Replace "mamba" to "conda" for using a conda environment.

### Verify
```bash
procnii_todcm -h
```

## Usage
Run the test case (from the root directory):

```bash
procnii_todcm \
    --img ./test/input/subj1/subj1_T1.nii.gz \
    --mask ./test/input/subj1/subj1_T1_seg.nii.gz \
    --mapping ./test/input/subj1/mapping.json \
    --refdcm ./test/input/subj1/subj1_slice1.dcm \
    --out ./test/output/subj1/subj1_merged.nii.gz
```

>[!WARNING]
>nii2dcm may print multiple "warning" messages. Check for "nii2dcm: DICOM files written to: ..." at the end of the output message
