import sys
from pathlib import Path

import tensorflow as tf
from PIL import Image
from tensorflow_compression_local.models.tfci import *
import subprocess


# Attention: This is very dirty! I am writing a 'wrapper' around the cmd tool, that
# enables us to run already trained models. The tensforflow impolementation can not
# decode ppm strings, so this was added.
# 'read_image' function is overwriting the original modules 'read_png' function.
def read_image(filename):
    """Loads a PNG image file."""
    im = np.array(Image.open(filename))
    image = tf.convert_to_tensor(im)
    return tf.expand_dims(image, 0)


module = sys.modules["tensorflow_compression_local.models.tfci"]
module.read_png = read_image
sys.modules["tensorflow_compression_local.models.tfci"] = module




class DeepLearningCompressor:
    def __init__(self, model_name):
        self.modelName = model_name

    def compress(self, input_file_path, output_file_path):
        """Compress the image to a *.tfci file"""
        
        raise NotImplementedError()

    def decompress(self, input_file_path, output_file_path):
        """Decompress a *.tfci file with the model used for compressing.

        The model that was used is inferred from the file.
        """

        raise NotImplementedError()


class DeepLearningCompressorTF(DeepLearningCompressor):
    "Deep Learning Compressor Implementation for tensorflow/compression"
    def __init__(self, model_name):
        self.modelName = model_name

    def compress(self, input_file_path, output_file_path):
        """Compress the image to a *.tfci file"""

        if isinstance(input_file_path, Path):
            input_file_path = input_file_path.as_posix()

        if isinstance(output_file_path, Path):
            output_file_path = output_file_path.as_posix()

        args = parse_args(
            ["", "compress", self.modelName, input_file_path, output_file_path]
        )

        compress(
            args.model,
            args.input_file,
            args.output_file,
            args.rd_parameter,
            args.rd_parameter_tolerance,
            args.target_bpp,
            args.bpp_strict,
        )

    def decompress(self, input_file_path, output_file_path):
        """Decompress a *.tfci file with the model used for compressing.

        The model that was used is inferred from the file.
        """

        if isinstance(input_file_path, Path):
            input_file_path = input_file_path.as_posix()

        if isinstance(output_file_path, Path):
            output_file_path = output_file_path.as_posix()

        args = parse_args([" ", "decompress", input_file_path, output_file_path])
        decompress(args.input_file, args.output_file)



class DeepLearningCompressorRecurrentNN(DeepLearningCompressor):
    def __init__(self, model_name, quality):
        self.modelName = model_name

        if quality < 0 or quality > 15:
            raise Exception("Quality values must be between 0 and 15!")
        self.quality = quality

    def compress(self, input_file_path, output_file_path):
        """Compress the image to a *.tfci file"""

        if isinstance(input_file_path, Path):
            input_file_path = input_file_path.as_posix()

        if isinstance(output_file_path, Path):
            output_file_path = output_file_path.as_posix()


        process = subprocess.Popen(["python",
        "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tf-models/research/compression/image_encoder_v2/encoder.py",
        f"--input_image={input_file_path}",
        f"--output_codes={output_file_path}", "--model=compression_residual_gru/residual_gru.pb", f"--iteration={self.quality}"]
                    ,stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, universal_newlines=True)

        stdout, stderr = process.communicate()
        print(f"compressed rnn {input_file_path}")
        pass

    def decompress(self, input_file_path, output_file_path):
        """Decompress a *.tfci file with the model used for compressing.

        The model that was used is inferred from the file.
        """

        if isinstance(input_file_path, Path):
            input_file_path = input_file_path.as_posix()

        if isinstance(output_file_path, Path):
            output_file_path = output_file_path.as_posix()

        process = subprocess.Popen(["python",
        "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tf-models/research/compression/image_encoder_v2/decoder.py",
        f"--input_codes={input_file_path}",
        f"--output_directory={output_file_path}", "--model=compression_residual_gru/residual_gru.pb"]
                    ,stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, universal_newlines=True)

        stdout, stderr = process.communicate()
        pass





if __name__ == "__main__":

    model = "b2018-gdn-128-1"
    model2 = "b2018-gdn-128-2"

    inp = "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tmp/big_building_small.ppm"
    out = "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tmp/big_building_compressed.tfci"
    outc = "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tmp/big_building_compressed.png"

    c = DeepLearningCompressorRecurrentNN(model,2)

    c.compress(inp, out)
    c.decompress(out, outc)
