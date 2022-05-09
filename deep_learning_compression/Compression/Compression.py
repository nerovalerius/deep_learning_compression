# Dependencies:
# JPEG:  nconvert - download, build and install from https://www.xnview.com/en/xnconvert/#downloads
# JPEGXR: nconvert - download, build and install from https://www.xnview.com/en/xnconvert/#downloads
# JPEG2000: openjpeg - download, build and install from https://github.com/uclouvain/openjpeg/blob/master/INSTALL.md

import os
import subprocess
from abc import abstractmethod

from PIL import Image


class ConvCompressor:

    METHOD_NAME = ""

    @staticmethod
    @abstractmethod
    def compress(input_file, output_file, target_ratio):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def decompress(input_file, output_file):
        raise NotImplementedError()


class JpegCompressor:

    METHOD_NAME = "JPEG"

    @staticmethod
    def compress(self, input_file, output_file, target_ratio):
        """Compress input file with the jpeg codec to required compression ratio"""
        # search the right q (Quality factor for jpeg)
        # to achieve atleast the target_ratio by using bisection
        q_l = 1
        q_r = 100
        q_m = 50
        q_m_last = 0
        while q_m != q_m_last:
            ratio = _nconvert_comp(input_file, output_file, q_m, "jpeg")
            if ratio <= target_ratio:
                q_r = q_m
            else:
                q_l = q_m
            q_m_last = q_m
            q_m = q_l + (q_r - q_l) // 2
        return ratio

    @staticmethod
    def decompress(input_file, output_file):
        """Decompress the given input file with the jpeg codec"""
        ratio = _nconvert_decomp(input_file, output_file)
        return ratio


class JpegXrCommpressor:

    METHOD_NAME = "JPEGXR"

    @staticmethod
    def compress(input_file, output_file, target_ratio):
        """Compress input file with the jpegXR codec to required compression ratio"""
        # search the right q (Quality factor for jpegXR)
        # to achieve atleast the target_ratio by using bisection
        q_l = 1
        q_r = 100
        q_m = 50
        q_m_last = 0
        while q_m != q_m_last:
            ratio = _nconvert_comp(input_file, output_file, q_m, "jxr")
            if ratio <= target_ratio:
                q_r = q_m
            else:
                q_l = q_m
            q_m_last = q_m
            q_m = q_l + (q_r - q_l) // 2
        return ratio

    @staticmethod
    def decompress(input_file, output_file):
        """Decompress the given input file with the jpegXR codec"""
        ratio = _nconvert_decomp(input_file, output_file)
        return ratio


class Jpeg2kCommpressor:

    METHOD_NAME = "JPEG2K"

    @staticmethod
    def compress(input_file, output_file, target_ratio):

        """Compress input file with the jpeg2000 codec to required compression ratio"""
        args = "opj_compress -i -o -OutFor J2K -r".split(" ")
        args.append(str(target_ratio))
        args.insert(2, input_file)
        args.insert(4, output_file)
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("opj_compress Exception: " + result.stderr)
        size_in = os.path.getsize(input_file)
        size_out = os.path.getsize(output_file)
        ratio = size_in / size_out
        return ratio

    @staticmethod
    def decompress(input_file, output_file):
        """Decompress the given input file with the jpeg2000 codec"""
        im = Image.open(input_file)
        im.save(output_file, format="PPM")
        size_in = os.path.getsize(input_file)
        size_out = os.path.getsize(output_file)
        ratio = size_in / size_out
        return ratio


def _nconvert_comp(input_file, output_file, q, alg):
    args = "nconvert -o -overwrite -out -q".split(" ")
    args.append(input_file)
    args.insert(2, output_file)
    args.insert(-2, alg)
    args.insert(-1, str(q))
    print(args)
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("nconvert Exception: " + result.stderr)
    size_in = os.path.getsize(input_file)
    size_out = os.path.getsize(output_file)
    return size_in / size_out


def _nconvert_decomp(input_file, output_file):
    args = "nconvert -o -overwrite -out".split(" ")
    args.append(input_file)
    args.insert(2, output_file)
    args.insert(-1, "ppm")
    print(args)
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("nconvert Exception: " + result.stderr)
    size_in = os.path.getsize(input_file)
    size_out = os.path.getsize(output_file)
    return size_in / size_out


# if __name__ == "__main__":
#     JC = Jpeg2kCommpressor()
#     print(JC.compress("test.ppm", "test20.j2k", 22))
#     print(1 / JC.decompress("test20.j2k", "test_out.ppm"))
# #     # im = Image.open("test_out.ppm")
# #     # im.show()
