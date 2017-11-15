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
    return array


def get_dataset_from_filepath(filepath):
    """Imports dataset using gdal library."""
    dataset = gdal.Open(
        filepath,
        gdal.GA_ReadOnly
    )
    return dataset


def get_path_from_cost_surface(cost_dataset, start_point, dest_point):
    CostSurfacefn = "C:\\Users\\Diego\\Desktop\\python_workspace\\bsp.tif"
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

    costSurfaceArray = cookbook.raster2array(CostSurfacefn)

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
    return path


def conver_array_to_Tiff_raster(array,output_path):
    driver = gdal.GetDriverByName('GTiff')
    cols = array.shape[1]
    rows = array.shape[0]
    outRaster = driver.Create(output_path, cols, rows, 1, gdal.GDT_Byte)
    return outRaster

def main():

    dataset = get_dataset_from_filepath("C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif")
    path_dataset = get_path_from_cost_surface(dataset, Point(0, 0), Point(10, 10))
    print(path_dataset)
    print(path_dataset[10, 10])

    output_path = "C:\\Users\\Diego\\Desktop\\python_workspace\\path_raster.tif"
    path_raster = conver_array_to_Tiff_raster(path_dataset, output_path)
     
    # data_array = get_array_from_dataset(path_dataset) 
    
    # print(data_array[0, 0])

if __name__ == '__main__':
    main()

