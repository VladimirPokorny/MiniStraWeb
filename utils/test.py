import unittest
from iban_calculator import IBANCalculator  # replace with the actual module name

class TestIBANCalculator(unittest.TestCase):
    def test_make_iban(self):
        test_cases = [
            {
                'country_code': 'CZ',
                'prefix_number': 0,
                'account_number': 158475698,
                'bank_code': '0800',
                'expected_result': 'CZ3908000000000158475698'
            },
            {
                'country_code': 'CZ',
                'prefix_number': 115,
                'account_number': 158475698,
                'bank_code': '0800',
                'expected_result': 'CZ8708000001150158475698'
            },
            {
                'country_code': 'CZ',
                'prefix_number': 9996,
                'account_number': 9999999999,
                'bank_code': '0100',
                'expected_result': 'CZ4701000099969999999999'
            }
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                calculator = IBANCalculator(
                    country_code=test_case['country_code'],
                    account_number=test_case['account_number'],
                    bank_code=test_case['bank_code'],
                    prefix_number=test_case['prefix_number']
                )
                result = calculator.make_iban()
                self.assertEqual(result, test_case['expected_result'])

if __name__ == '__main__':
    unittest.main()