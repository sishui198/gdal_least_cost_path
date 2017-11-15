""" asd a"""
from osgeo import ogr, gdal
import os
import numpy
from skimage.graph import route_through_array
import cookbook

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def get_array_from_dataset(dataset):
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    #_display_array(array)
    return array


def get_dataset_from_filepath(filepath):
    """Imports dataset using gdal library."""
    dataset = gdal.Open(
        filepath,
        gdal.GA_ReadOnly
    )
    return dataset

def convert_Tiff_raster_to_array(user_input_path):
    raster = gdal.Open(user_input_path)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array


def get_path_from_cost_surface(cost_dataset, start_point, dest_point):
    CostSurfacefn = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"
    # coordinates to array index
    startCoordX = start_point.x
    startCoordY = start_point.y
    startIndexX, startIndexY = cookbook.coord2pixelOffset(
        CostSurfacefn,
        startCoordX,
        startCoordY
    )

    stopCoordX = dest_point.x
    stopCoordY = dest_point.y
    stopIndexX, stopIndexY = cookbook.coord2pixelOffset(
        CostSurfacefn,
        stopCoordX,
        stopCoordY
    )

    costSurfaceArray = convert_Tiff_raster_to_array(CostSurfacefn)
    _display_array(costSurfaceArray)
    print("##############")
    # create path
    indices, weight = route_through_array(
        costSurfaceArray,
        (startIndexY, startIndexX),
        (stopIndexY, stopIndexX),
        geometric=True,
        fully_connected=True
    )
    indices = numpy.array(indices).T
    path = numpy.zeros_like(costSurfaceArray)
    path[indices[0], indices[1]] = 1
    _display_array(path)
    return path




def convert_array_to_Tiff_raster(array, output_path):
    driver = gdal.GetDriverByName('GTiff')
    cols = array.shape[1]
    rows = array.shape[0]
    outRaster = driver.Create(output_path, cols, rows, 1, gdal.GDT_Byte)
    return outRaster


def _display_array(array):
    for row in array:
        for pixel in row:
            print(pixel, end="")
        print()

def main():

    user_input_path = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"

    data_raster = get_dataset_from_filepath("C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif")

    data_array = convert_Tiff_raster_to_array(user_input_path)

    path_dataset = get_path_from_cost_surface(data_array, Point(0, 0), Point(9, 9))

    output_path = "C:\\Users\\Diego\\Desktop\\python_workspace\\path_raster.tif"
    path_raster = convert_array_to_Tiff_raster(path_dataset, output_path)

if __name__ == '__main__':
    main()

