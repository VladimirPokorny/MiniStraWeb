import re


class IBANCalculator:
    '''
    An IBANCalculator class calculates the International Bank Account Number (IBAN).

    Attributes
    ----------
    country_code : str
        A two-letter country code
    bank_code : str
        A four-letter bank code
    account_number : int
        An account number, at least 2 and up to 10 characters long
    prefix_number : int
        A prefix number, up to 6 characters long
    ''' 
    def __init__(self, country_code: str, account_number: int, bank_code: str, prefix_number: int=None):
        self.country_code = country_code
        self.bank_code = bank_code
        self.account_number = account_number
        self.prefix_number = prefix_number

        self.check_inputs()

    def make_account_identifier(self) -> str:
        '''
        Returns a string of 16 characters long, which is a concatenation of the prefix number and the account number.
        '''
        account_identifier = f'{str(self.prefix_number)}{str(self.account_number)}'
        return account_identifier.zfill(16)
    
    def make_iban_without_checksum(self) -> str:
        '''
        Returns a string of 24 characters long, which is a concatenation of the country code, the check digits, the bank code, and the account identifier.
        '''
        account_identifier = self.make_account_identifier()
        self.iban = f'{self.country_code}00{self.bank_code}{account_identifier}'
        return self.iban

    def check_inputs(self) -> None:
        '''
        Checks if the inputs are valid.
        '''
        if len(self.bank_code) != 4:
            raise ValueError('Bank code must be 4 characters long')
        if len(self.country_code) != 2:
            raise ValueError('Country code must be 2 characters long')
        if len(str(self.prefix_number)) > 6:
            raise ValueError('Prefix number must be up to 6 characters long')
        if len(str(self.account_number)) < 2 or len(str(self.account_number)) > 10:
            raise ValueError('Account number must be at least 2 and up to 10 characters long')
        
        return None

    def calculate_iban_checksum(self, iban: str) -> str:
        '''
        Calculates the IBAN checksum using the MOD-97-10 algorithm.
        
        Parameters
        ----------
        iban : str
            A string of 24 characters long, which is a concatenation of the country code, the check digits, the bank code, and the account identifier.
            
        Returns
        -------
        check_sum_digits : str
            A string of 2 characters long, which is the IBAN checksum.
        '''
        # Replace the two check digits by 00 (e.g., CZ00 for the CZ).
        iban = iban[:2] + '00' + iban[4:]
    
        # Move the four initial characters to the end of the string.
        iban = iban[4:] + iban[:4]
        
        # Replace the letters in the string with digits, expanding the string as necessary, such that A or a = 10, B or b = 11, and Z or z = 35. Each alphabetic character is therefore replaced by 2 digits
        iban = re.sub(r'[A-Z]', lambda x: str(ord(x.group()) - 55), iban)

        # Calculate mod-97 of the new number, which results in the remainder.
        remainder = self.mod_97(str(iban))

        # Subtract the remainder from 98 and use the result for the two check digits. If the result is a single-digit number, pad it with a leading 0 to make a two-digit number.
        check_sum_digits = '{:0>2}'.format(98 - remainder)
        
        return check_sum_digits

    def mod_97(self, iban: int) -> int:
        '''
        Calculates the remainder of the division of the IBAN number by 97.

        Parameters
        ----------
        iban : int
            An IBAN number.
            
        Returns
        -------
        remainder : int
            The remainder of the division of the IBAN number by 97.
        '''
        iban_array = self.number_to_array(iban)

        while self.array_to_number(iban_array) > 97:
            remainder = self.array_to_number(iban_array[:9]) % 97
            iban_array = iban_array[9:]

            if len(self.number_to_array(remainder)) == 1:
                iban_array = self.number_to_array(remainder) + iban_array
                print(iban_array)
            elif len(self.number_to_array(remainder)) == 2:
                iban_array = self.number_to_array(remainder) + iban_array
                print(iban_array)

        return remainder
    
    def number_to_array(self, n: int) -> list:
        '''
        Returns an array of digits of a number.
        
        Parameters
        ----------
        n : int
            A number.
            
        Returns
        -------
        array : list
            An array of digits of a number.
        '''
        return [int(digit) for digit in str(n)]
    
    def array_to_number(self, array: list) -> int:
        '''
        Returns a number from an array of digits.

        Parameters
        ----------
        array : list
            An array of digits of a number.

        Returns
        -------
        n : int
            A number.
        '''
        return int(''.join(map(str, array)))
    
    def make_iban(self) -> str:
        '''
        Returns a string of 24 characters long, which is the IBAN number.
        '''
        check_sum = self.calculate_iban_checksum(self.make_iban_without_checksum())

        return self.iban[:2] + check_sum + self.iban[4:]