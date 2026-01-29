import os
import argparse
from procnii_todcm.utils_nifti import merge_img_and_mask as merge_img
from nii2dcm.run import run_nii2dcm

def main():
    parser = argparse.ArgumentParser(
        prog="procnii_todcm",
        description="Merge processed NIfTI images and save to DICOM"
    )

    parser.add_argument(
        "--img",
        required=True,
        help="Input NIfTI image, e.g. T1 scan (.nii or .nii.gz)"
    )

    parser.add_argument(
        "--mask",
        required=True,
        help="Input NIfTI mask, e.g. segmentation (.nii or .nii.gz)"
    )

    parser.add_argument(
        "--mapping",
        required=True,
        help="Input mapping file to map image and mask intensities to new integer values (.json)"
    )

    parser.add_argument(
        "--refdcm",
        required=True,
        help="Reference dicom file (.dcm)"
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output Nifti image name (.nii or .nii.gz)"
    )

    args = parser.parse_args()

    ## Create output folder
    outdir = os.path.dirname(args.out)
    dcmdir = os.path.join(outdir, 'dicoms')
    os.makedirs(dcmdir, exist_ok=True)

    ## Merge underlay image and overlay mask
    print('Merging img and mask ...')
    merge_img(args.img, args.mask, args.mapping, args.out)

    ## Save output as dicom
    print('Saving to dicom ...')
    run_nii2dcm(args.out, dcmdir, 'MR', args.refdcm)
