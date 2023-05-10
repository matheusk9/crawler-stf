from unittest.mock import patch
import requests
import unittest


class TestExtracao(unittest.TestCase):
    """Doc"""

    def test_fake_request(self):
        response_mock = {'message': 'Hello, world!'}

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = response_mock

            response = requests.get('python.org')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), response_mock)


if __name__ == '__main__':
    unittest.main()
