"""Test code"""

import unittest
import sys
from app import app
from ProductionCode import data_procesor

dummyData = [
    ["NSHLPM", "ARSTDRG"],
    ["3", "1"],
    ["20", "6"],
    ["4", "15"],
    ["0", "9"],
    [" ", " "],
]


class TestMainPage(unittest.TestCase):
    """Tests the apps home page"""

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.app = app.test_client()

    def test_route(self):
        """Tests that the home page has the correct welcome text"""
        self.app = app.test_client()
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(
            b"Hello, this is the homepage. " +
            b"To find the frequency of meeting attended please do /meeting/frequency. " +
            b"To find the average number of meeting attended please do /meeting/count. " +
            b"To find the number of people with drug arrst counts within " +
            b"a range low-high please do /arrests/low/high eg. /arrests/1/3",
            response.data,
        )


class TestGetMeetingFrequency(unittest.TestCase):
    """Tests the path based method calls and pages"""

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.app = app.test_client()

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_route(self):
        """Tests a correct path that should display the methods result"""
        self.app = app.test_client()
        response = self.app.get("/meeting/frequency", follow_redirects=True)
        self.assertEqual(
            b"The average percentage of meetings attended is 33.75%", response.data
        )

    def test_bad_route(self):
        """Test a bad path that should display a correct usage hint"""
        self.app = app.test_client()
        response = self.app.get("/0", follow_redirects=True)
        self.assertEqual(
            b"404 Not Found: The requested URL was not found on the server. " +
            b"If you entered the URL manually please check your spelling and try again. " +
            b"Sorry, wrong format, do this instead /meeting/frequency or " +
            b"/meeting/count or arrests/low/high",
            response.data,
        )


class TestGetMeetingCount(unittest.TestCase):
    """Tests the path based method calls and pages"""

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.app = app.test_client()

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_route(self):
        """Tests a correct path that should display the methods result"""
        self.app = app.test_client()
        response = self.app.get("/meeting/count", follow_redirects=True)
        self.assertEqual(
            b"The average number of meetings attended is 6.75", response.data
        )

    def test_bad_route(self):
        """Test a bad path that should display a correct usage hint"""
        self.app = app.test_client()
        response = self.app.get("/0", follow_redirects=True)
        self.assertEqual(
            b"404 Not Found: The requested URL was not found on the server. " +
            b"If you entered the URL manually please check your spelling and try again. " +
            b"Sorry, wrong format, do this instead /meeting/frequency or " +
            b"/meeting/count or arrests/low/high",
            response.data,
        )

class TestGetDrugSaleArrests(unittest.TestCase):
    """Tests the drug sale arrests route"""

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.app = app.test_client()

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_drug_sale(self):
        """Test for route for drug sale arrests"""
        response = self.app.get('/arrests/1/10', follow_redirects=True)
        self.assertEqual(b"3 people", response.data)

    def test_bad_route(self):
        """Test a bad path that should display a correct usage hint"""
        self.app = app.test_client()
        response = self.app.get("/0", follow_redirects=True)
        self.assertEqual(
            b"404 Not Found: The requested URL was not found on the server. " +
            b"If you entered the URL manually please check your spelling and try again. " +
            b"Sorry, wrong format, do this instead /meeting/frequency or " +
            b"/meeting/count or arrests/low/high",
            response.data,
        )

class TestMeetingFrequency(unittest.TestCase):
    """Testing the get_row_titles method"""

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_meeting_frequency(self):
        """Checks that the meeting frequency is returned"""
        self.assertEqual(data_procesor.meeting_frequency(), 33.75, "Should be 33.75")


class TestMeetingCount(unittest.TestCase):
    """Testing the get_row_by_titles method"""

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_meeting_count(self):
        """Checks that the meeting frequency is returned"""
        self.assertEqual(data_procesor.meeting_count(), 6.75, "Should be 6.75")


class TestDrugSaleArrests(unittest.TestCase):
    """Testing the get_silly method"""

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_normal_range(self):
        """Checks that the meeting frequency is returned"""
        self.assertEqual(data_procesor.drug_sale_arrests(1, 10), 3, "Should be 3")

    def test_small_range(self):
        """Checks that the meeting frequency is returned"""
        self.assertEqual(data_procesor.drug_sale_arrests(2, 4), 0, "Should be 0")

    def test_big_range(self):
        """Checks that the meeting frequency is returned"""
        self.assertEqual(data_procesor.drug_sale_arrests(0, 30), 4, "Should be 4")


class TestGetColNumWithTitle(unittest.TestCase):
    """Testing the get_col_num_with_title method"""

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_correct_name(self):
        """Testing that for a correct name input it returns the correct column"""
        self.assertEqual(
            data_procesor.get_col_num_with_title("NSHLPM"), 0, "should be 0"
        )

    def test_incorrect_name(self):
        """Testing that for a incorrect name input it returns -1"""
        self.assertEqual(
            data_procesor.get_col_num_with_title("AAAA"), -1, "should be -1"
        )


class TestGetSum(unittest.TestCase):
    """Testing the get_sum method"""

    def test_correct_values(self):
        """Testing that for a correct values the sum is output"""
        self.assertEqual(data_procesor.get_sum_array(["1", "2", "3"]), 6, "should be 6")

    def test_incorrect_value(self):
        """Testing that for incorrect values the sum is unchanhged"""
        self.assertEqual(
            data_procesor.get_sum_array(["1", "2", "3", "value"]),
            6,
            "should be 6",
        )

    def test_blank_value(self):
        """Testing that for incorrect values the sum is unchanhged"""
        self.assertEqual(
            data_procesor.get_sum_array(["1", "2", "3", ""]), 6, "should be 6"
        )


class TestGetMax(unittest.TestCase):
    """Testing the get_max method"""

    def test_correct_values(self):
        """Testing that for a correct values the max is output"""
        self.assertEqual(data_procesor.get_max_num(["1", "2", "3"]), 3, "should be 3")

    def test_incorrect_value(self):
        """Testing that for incorrect values the max is unchanhged"""
        self.assertEqual(
            data_procesor.get_max_num(["1", "2", "3", "value"]),
            3,
            "should be 3",
        )

    def test_blank_value(self):
        """Testing that for incorrect values the max is unchanhged"""
        self.assertEqual(
            data_procesor.get_max_num(["1", "2", "3", ""]), 3, "should be 3"
        )


class TestGetTotalValid(unittest.TestCase):
    """Testing the get_total_valid_method"""

    def test_correct_values(self):
        """Testing that for a correct values the valid cell count is output"""
        self.assertEqual(
            data_procesor.get_total_valid(["1", "2", "3"]), 3, "should be 3"
        )

    def test_incorrect_value(self):
        """Testing that for incorrect values the valid cell count is unchanhged"""
        self.assertEqual(
            data_procesor.get_total_valid(["1", "2", "3", "value"]),
            3,
            "should be 3",
        )

    def test_blank_value(self):
        """Testing that for incorrect values the valid cell count is unchanhged"""
        self.assertEqual(
            data_procesor.get_total_valid(["1", "2", "3", ""]), 3, "should be 3"
        )


class TestGetTotalCountInRange(unittest.TestCase):
    """Testing the get_count_in_range_method"""

    def test_correct_values(self):
        """Testing that for a correct values the sum is output"""
        self.assertEqual(
            data_procesor.get_total_count_in_range(["1", "2", "3"], 1, 2),
            2,
            "should be 2",
        )

    def test_correct_values_large_range(self):
        """Testing that for a correct values the sum is output"""
        self.assertEqual(
            data_procesor.get_total_count_in_range(["1", "2", "3"], -1, 20),
            3,
            "should be 3",
        )

    def test_incorrect_value(self):
        """Testing that for incorrect values the sum is unchanhged"""
        self.assertEqual(
            data_procesor.get_total_count_in_range(["1", "2", "3", "value"], 1, 2),
            2,
            "should be 2",
        )

    def test_blank_value(self):
        """Testing that for incorrect values the sum is unchanhged"""
        self.assertEqual(
            data_procesor.get_total_count_in_range(["1", "2", "3", ""], 1, 2),
            2,
            "should be 2",
        )


class TestGetCol(unittest.TestCase):
    """Testing the get_col method"""

    def setUp(self):
        """Sets up the dummy data"""
        data_procesor.initalize_dummy_data(dummyData)

    def test_correct_name(self):
        """Testing that for a correct name input it returns the correct column"""
        self.assertEqual(
            data_procesor.get_col(1),
            ["1", "6", "15", "9", " "],
            'should be ["1", "6", "15", "9", " "]',
        )

    def test_incorrect_column_index(self):
        """Testing that for a incorrect name input it returns -1"""
        self.assertRaises(IndexError, data_procesor.get_col, sys.maxsize)


if __name__ == "__main__":
    unittest.main()
