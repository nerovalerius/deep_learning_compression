import sys
from pathlib import Path

import tensorflow as tf
from PIL import Image
from tensorflow_compression_local.models.tfci import *


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


if __name__ == "__main__":

    model = "b2018-gdn-128-1"
    model2 = "b2018-gdn-128-2"

    inp = "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tmp/big_building.ppm"
    out = "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tmp/big_building_compressed.tfci"
    outc = "/home/pfeiffer/repos/Media-Data-Formats-PS/deep_learning_compression/tmp/big_building_compressed.png"

    c = DeepLearningCompressor(model)

    c.compress(inp, out)
    c.decompress(out, outc)
