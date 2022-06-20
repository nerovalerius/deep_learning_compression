import sys
from pathlib import Path

from PIL import Image

# TODO
# This is just a workaround, because python in my WSL
# adds the folder of the script to sys.path instead
# of the workspace folder of vscode, which is cwd, when
# you run or debug a script in vscode.
# We should resolve this by using a venv.
root = Path("./")
sys.path.insert(0, str(root.resolve()))

from deep_learning_compression.Storage.Storage import Storage

if __name__ == "__main__":

    reduction_factor = 3

    s = Storage()

    dataSetName = "ImageCompressionBenchmark8BitRGB"

    files = s.GetAllFileInformationOfASingleDataSet(setName=dataSetName)

    for f_obj in files:
        im = Image.open(f_obj.Filepath.as_posix())

        red_size = tuple([s // reduction_factor for s in im.size])

        im = im.crop(
            box=(
                0,
                0,
                int(np.ceil(im.width/reduction_factor/32)*32),
                int(np.ceil(im.height/reduction_factor/32)*32)
            )
        )  # im.resize(red_size, Image.BILINEAR)

        im.save(f_obj.Filepath.as_posix())
