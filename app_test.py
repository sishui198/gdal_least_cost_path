""" Tests ffor app """
import unittest
from app import *
import cookbook

class AppTests(unittest.TestCase):

    def test_import_dataset_given_filepath_should_return_something(self):
        filepath = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"
        dataset = get_dataset_from_filepath(filepath)
        expected = None
        self.assertIsNot(dataset, expected)

    def test_import_dataset_given_filepath_should_return_valid_dataset(self):
        filepath = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"
        dataset = get_dataset_from_filepath(filepath)

        expected_pixel_value = 68
        actual_pixel_value = get_array_from_dataset(dataset)[0, 0]
        self.assertEqual(expected_pixel_value, actual_pixel_value)

    def test_import_dataset_given_10by10_should_return_10by10_dataset(self):
        filepath = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"
        dataset = get_dataset_from_filepath(filepath)

        array = get_array_from_dataset(dataset)
        self.assertEqual(len(array), 10)
        self.assertEqual(len(array[0]), 10)


    def test_get_path_given_raster_and_points_should_return_non_empty_dataset(self):
        filepath = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"
        cost_dataset = get_dataset_from_filepath(filepath)
        start_point = Point(1, 1)
        dest_point = Point(9, 9)
        expected = get_path_from_cost_surface(
            cost_dataset,
            start_point,
            dest_point
        )
        actual = None
        self.assertIsNot(expected, actual)

    def test_get_path_given_raster_and_points_should_return_path(self):
        filepath = "C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif"
        cost_dataset = get_dataset_from_filepath(filepath)
        start_point = Point(1, 1)
        dest_point = Point(9, 9)
        expected = get_path_from_cost_surface(
            cost_dataset,
            start_point,
            dest_point
        )

        expected_pixel_value = 0
        actual_pixel_value = expected[0, 0]
        self.assertEqual(expected_pixel_value, actual_pixel_value)

        expected_pixel_value = 1
        actual_pixel_value = expected[1, 1]
        self.assertEqual(expected_pixel_value, actual_pixel_value)

        expected_pixel_value = 1
        actual_pixel_value = expected[5, 5]
        self.assertEqual(expected_pixel_value, actual_pixel_value)

        expected_pixel_value = 1
        actual_pixel_value = expected[9, 9]
        self.assertEqual(expected_pixel_value, actual_pixel_value)

    def test_create_raster_given_array_and_path(self):
        expected = None
        dataset = get_dataset_from_filepath("C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif")
        dataset_array = get_path_from_cost_surface(dataset, Point(0, 0), Point(9, 9))
        output_path = "C:\\Users\\Diego\\Desktop\\python_workspace\\raster_bsp.tif"
        raster = convert_array_to_Tiff_raster(dataset_array, output_path)
        self.assertIsNot(raster, expected)

    def test_create_array_given_path_should_return_array(self):
        expected = None
        data_array = convert_Tiff_raster_to_array("C:\\Users\\Diego\\Desktop\\python_workspace\\10x10_bsp.tif")
        self.assertIsNot(data_array, expected)


if __name__ == '__main__':
    unittest.main()
