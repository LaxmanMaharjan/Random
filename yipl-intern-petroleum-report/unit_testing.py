"""Module for Unit Testing.

Authur: Laxman Maharjan
Contact: lxmnmrzn@gmail.com
"""

import unittest
from unittest.mock import patch
from reportgenerator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """Do Unit Testing.

    This class is used for unit testing for our code
    """

    def test_ReportGenerator(self):
        """Do testing for requests from given url."""
        url = "https://raw.githubusercontent.com/younginnovations/"\
              "internship-challenges/master/programming/"\
              "petroleum-report/data.json"

        with patch('reportgenerator.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            obj = ReportGenerator(url)
            response = obj.get_dataset()
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
