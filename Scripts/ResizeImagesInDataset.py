from PIL import Image
from deep_learning_compression.Storage.Storage import Storage

if __name__ == "__main__":


    reduction_factor = 3


    s = Storage()

    dataSetName = "ImageCompressionBenchmark8BitRGB"

    files = s.GetAllFileInformationOfASingleDataSet(setName=dataSetName)


    for f_obj in files:
        im = Image.open(f_obj.Filepath.as_posix())

        red_size = tuple([s//reduction_factor for s in im.size])

        im = im.resize(red_size,Image.BILINEAR)

        im.save(f_obj.Filepath.as_posix())



    