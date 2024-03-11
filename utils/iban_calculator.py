import re
from schwifty import IBAN



class IBANCalculator:
    def __init__(self, country_code: str, account_number: int, bank_code: str, prefix_number: int=None):
        self.country_code = country_code
        self.bank_code = bank_code
        self.account_number = account_number
        self.prefix_number = prefix_number

        self.check_lenght()
        
        #      0100    1 1576 0467 0277
        # CZ97 0100 0001 1576 0467 0277
        # XXYY BBBB PPPP PPPP PPPP PPPP

    def make_account_identifier(self):
        account_identifier = f'{str(self.prefix_number)}{str(self.account_number)}'
        # account_identifier = f'{str(self.prefix_number)}'
        # account_identifier = f'{str(self.account_number)}'
        return account_identifier.zfill(16)
    
    def make_iban(self):
        self.iban = None
        account_identifier = self.make_account_identifier()
        self.iban = f'{self.country_code}00{account_identifier}'
        return self.iban

    def check_lenght(self):
        if len(self.bank_code) != 4:
            raise ValueError('Bank code must be 4 characters long')
        if len(self.country_code) != 2:
            raise ValueError('Country code must be 2 characters long')
        if len(str(self.prefix_number)) > 6:
            raise ValueError('Prefix number must be up to 6 characters long')
        if len(str(self.account_number)) < 2 or len(str(self.account_number)) > 10:
            raise ValueError('Account number must be at least 2 and up to 10 characters long')

    def calculate_iban_checksum_with_prefix(self, iban: str):
        # Replace the two check digits by 00 (e.g., GB00 for the UK).
        iban = iban[:2] + '00' + iban[4:]
        print(iban)
    
        # Move the four initial characters to the end of the string.
        iban = iban[4:] + iban[:4]
        print(iban)
        
        # Replace the letters in the string with digits, expanding the string as necessary, such that A or a = 10, B or b = 11, and Z or z = 35. Each alphabetic character is therefore replaced by 2 digits
        iban = re.sub(r'[A-Z]', lambda x: str(ord(x.group()) - 55), iban)
        print(iban)

        # Convert the string to an integer (i.e. ignore leading zeroes).
        iban = int(iban)
        print(iban)

        # Calculate mod-97 of the new number, which results in the remainder.
        remainder = iban % 97
        print(remainder)

        # Subtract the remainder from 98 and use the result for the two check digits. If the result is a single-digit number, pad it with a leading 0 to make a two-digit number.
        check_digits = '{:0>2}'.format(98 - remainder)
        print(f'Check digits: {check_digits}')
        
        return check_digits

    def mod97(self, iban: int):
        # Starting from the leftmost digit of D, construct a number using the first 9 digits and call it N.[Note 3]
        number = int(str(iban)[:9])
        print(number)

        # Calculate N mod 97.
        remainder = number % 97

        # Construct a new 9-digit N by concatenating the above result (step 2) with the next 7 or 8 digits of D. If there are fewer than 7 digits remaining in D but at least one, then construct a new N, which will have less than 9 digits, from the above result (step 2) followed by the remaining digits of D
        if len(str(remainder)) < 9:
        new_number = int(str(remainder) + str(iban)[9:])

    
#     Calculate N mod 97.
#     Construct a new 9-digit N by concatenating the above result (step 2) with the next 7 or 8 digits of D. If there are fewer than 7 digits remaining in D but at least one, then construct a new N, which will have less than 9 digits, from the above result (step 2) followed by the remaining digits of D
#     Repeat steps 2–3 until all the digits of D have been processed

# The result of the final calculation in step 2 will be D mod 97 = N mod 97. 
        

if __name__ == '__main__':
    iban = IBANCalculator('CZ', 7604670277, "0100", 19)
    print(f'input iban: {iban.make_iban()}')
    print(iban.calculate_iban_checksum_with_prefix(iban.make_iban()))
    # 'CZ9701000001157604670277
    