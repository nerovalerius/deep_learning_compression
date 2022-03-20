# Dependencies:
# JPEG:  nconvert - download, build and install from https://www.xnview.com/en/xnconvert/#downloads
# JPEGXR: nconvert - download, build and install from https://www.xnview.com/en/xnconvert/#downloads
# JPEG2000: openjpeg - download an build and install from https://github.com/uclouvain/openjpeg/blob/master/INSTALL.md

import os
import subprocess


def jpeg(input_file, output_file, target_ratio):
    """Compress input file with the jpeg codec to required compression ratio"""
    # search the right q (Quality factor for jpeg)
    # for the target_ratio by using bisection
    q_l = 1
    q_r = 100
    q_m = 50
    q_m_last = 0
    while q_m != q_m_last:
        ratio = _nconvert_run(input_file, output_file, q_m, "jpeg")
        if ratio <= target_ratio:
            q_r = q_m
        else:
            q_l = q_m
        q_m_last = q_m
        q_m = q_l + (q_r - q_l) // 2
    # If the q_m + 1 yields a ratio which is nearer to the
    # target_ratio than the found q_m, use that one instead.
    # The bisect just finds a q_m, which yields a ratio >= target_ratio.
    # So q_m + 1 must be checked.
    if q_m > 1:
        ratio_1 = _nconvert_run(input_file, output_file, q_m + 1, "jpeg")
        if abs(target_ratio - ratio) < abs(target_ratio - ratio_1):
            ratio = _nconvert_run(input_file, output_file, q_m, "jpeg")
        else:
            ratio = ratio_1
    return ratio


def jpegXR(input_file, output_file, target_ratio):
    """Compress input file with the jpegXR codec to required compression ratio"""
    # search the right q (Quality factor for jpegXR)
    # for the target_ratio by using bisection
    q_l = 1
    q_r = 100
    q_m = 50
    q_m_last = 0
    while q_m != q_m_last:
        ratio = _nconvert_run(input_file, output_file, q_m, "jxr")
        if ratio <= target_ratio:
            q_r = q_m
        else:
            q_l = q_m
        q_m_last = q_m
        q_m = q_l + (q_r - q_l) // 2
    # If the q_m + 1 yields a ratio which is nearer to the
    # target_ratio than the found q_m, use that one instead.
    # The bisect just finds a q_m, which yields a ratio >= target_ratio.
    # So q_m + 1 must be checked.
    if q_m > 1:
        ratio_1 = _nconvert_run(input_file, output_file, q_m + 1, "jxr")
        if abs(target_ratio - ratio) < abs(target_ratio - ratio_1):
            ratio = _nconvert_run(input_file, output_file, q_m, "jxr")
        else:
            ratio = ratio_1
    return ratio


def jpeg2K(input_file, output_file, target_ratio):
    """Compress input file with the jpeg2000 codec to required compression ratio"""
    args = "opj_compress -i -o -OutFor J2K -r".split(" ")
    args.append(str(target_ratio))
    args.insert(2, input_file)
    args.insert(4, output_file)
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("nconvert Exception: " + result.stderr)
    size_in = os.path.getsize(input_file)
    size_out = os.path.getsize(output_file)
    ratio = size_in / size_out
    return ratio


def _nconvert_run(input_file, output_file, q, alg):
    args = "nconvert -o -overwrite -out -q".split(" ")
    args.append(input_file)
    args.insert(2, output_file)
    args.insert(-2, alg)
    args.insert(-1, str(q))
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("nconvert Exception: " + result.stderr)
    size_in = os.path.getsize(input_file)
    size_out = os.path.getsize(output_file)
    return size_in / size_out


# if __name__ == "__main__":
#     print(jpeg2K("flower.ppm", "flower20.j2k", 22))
#     print(jpegXR("flower.ppm", "flower20.jxr", 22))
#     print(jpeg("flower.ppm", "flower20.jpg", 22))
