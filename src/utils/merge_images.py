import json
import re
import numpy as np
import nibabel as nib


def quantize_from_percentile_mapping(image, percentile_map, mask=None):
    """
    Quantize image intensities using percentile->integer mapping.
    Example: { "perc5": 1, "perc95": 5 }
    """
    # Parse percentiles
    perc_values = {}
    for key, value in percentile_map.items():
        match = re.match(r"perc(\d+)", key)
        if not match:
            raise ValueError(f"Invalid percentile key: {key}")
        perc = float(match.group(1))
        perc_values[perc] = int(value)

    if len(perc_values) != 2:
        raise ValueError("Currently expects exactly two percentiles")

    # Sort by percentile
    (p_low, out_low), (p_high, out_high) = sorted(perc_values.items())

    if p_high <= p_low:
        raise ValueError("Percentiles must be increasing")

    # Select values for percentile computation
    values = image[mask > 0] if mask is not None else image

    low_val = np.percentile(values, p_low)
    high_val = np.percentile(values, p_high)

    if high_val <= low_val:
        raise ValueError("Degenerate percentile range")

    # Clip to percentile range
    clipped = np.clip(image, low_val, high_val)

    # Normalize and scale to integer range
    scaled = (clipped - low_val) / (high_val - low_val)
    quantized = np.round(
        scaled * (out_high - out_low)
    ).astype(np.int16) + out_low

    # Final clamp
    quantized = np.clip(quantized, out_low, out_high)

    return quantized


def main(t1_nifti, seg_nifti, mapping_file, output_nifti):
    # Load images
    t1_img = nib.load(t1_nifti)
    seg_img = nib.load(seg_nifti)

    t1_data = t1_img.get_fdata()
    seg_data = seg_img.get_fdata()

    if t1_data.shape != seg_data.shape:
        raise ValueError("T1 and segmentation images must match in shape")

    # Load mapping JSON
    with open(mapping_file, "r") as f:
        mapping = json.load(f)

    t1_mapping = mapping["t1_mapping"]
    seg_mapping = mapping["segmentation_mapping"]

    # Quantize T1 using percentile mapping
    quantified = quantize_from_percentile_mapping(
        t1_data,
        percentile_map=t1_mapping
    )

    # Overlay segmentation labels
    output = quantified.copy()
    for seg_label, new_value in seg_mapping.items():
        output[seg_data == int(seg_label)] = int(new_value)

    # Save integer NIfTI
    new_img = nib.Nifti1Image(
        output.astype(np.int16),
        affine=t1_img.affine,
        header=t1_img.header
    )
    new_img.set_data_dtype(np.int16)

    nib.save(new_img, output_nifti)
    print(f"Saved output to {output_nifti}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--t1", required=True)
    parser.add_argument("--seg", required=True)
    parser.add_argument("--mapping", required=True)
    parser.add_argument("--out", required=True)

    args = parser.parse_args()
    main(args.t1, args.seg, args.mapping, args.out)
