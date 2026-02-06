# procnii_todcm

Converts processed NIfTI files (`.nii` / `.nii.gz`) to DICOM using `nibabel` and `nii2dcm`.

>[!NOTE]
>Current functionality is limited to merging a segmentation mask to an underlay image and saving the result as dicom

## Installation

>[!NOTE]
>Due to a bug in nii2dcm, we use here a patched version that is installed as a first step
>Please follow all steps to make sure correct dependencies are installed and used

```bash
# create environment
mamba create -n procnii python=3.11     
mamba activate procnii

# install nii2dcm
git clone https://github.com/gurayerus/nii2dcm
cd nii2dcm
pip install -r requirements.txt
pip install . --no-build-isolation

# install procnii_todcm
cd ..
git clone https://github.com/gurayerus/procnii_todcm
cd procnii_todcm
pip install .
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
    --out ./test/output/subj1/subj1_merged.nii.gz
```

>[!NOTE]
>Optionally: Add a reference dicom to cmd:
>    --refdcm ./test/input/subj1/subj1_slice1.dcm


>[!WARNING]
>nii2dcm may print multiple "warning" messages. Check for "nii2dcm: DICOM files written to: ..." at the end of the output message
