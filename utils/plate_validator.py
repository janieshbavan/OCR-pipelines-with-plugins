# """
# License Plate Validator Module
# Validates and corrects Indian license plate numbers
# """

# import re


# class PlateValidator:
#     """Validator for Indian license plate format"""
    
#     # Indian state codes
#     STATE_CODES = {
#         "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL", 
#         "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TG", 
#         "TS", "TR", "UP", "UK", "WB", "AN", "CH", "DD", "DL", "JK", "LA", "LD", 
#         "PY", "BH"
#     }
    
#     def __init__(self):
#         """Initialize plate validator"""
#         pass
    
#     def validate_format(self, text):
#         """
#         Validate Indian license plate format: AA##AA#### or AA##A####
        
#         Args:
#             text: License plate text to validate
            
#         Returns:
#             True if valid format, False otherwise
#         """
#         if not text or len(text) < 7:
#             return False
        
#         # Pattern: 2 letters + 2-3 digits + 1-2 letters + 4 digits
#         pattern = r'^([A-Z]{2})(\d{2,3})([A-Z]{1,2})(\d{4})$'
#         match = re.match(pattern, text)
        
#         if not match:
#             return False
        
#         # Check if state code is valid
#         state_code = match.group(1)
#         return state_code in self.STATE_CODES
    
#     def smart_correct(self, text):
#         """
#         Apply smart character correction based on position
#         Format: AA##AA#### or AA##A####
        
#         Args:
#             text: License plate text to correct
            
#         Returns:
#             Corrected text
#         """
#         if not text or len(text) < 7:
#             return text
        
#         chars = list(text.upper())
        
#         for i, char in enumerate(chars):
#             # State code positions (0-1) - should be letters only
#             if i < 2:
#                 if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
#                     if char == '0': chars[i] = 'O'
#                     elif char == '1': chars[i] = 'I'
#                     elif char == '2': chars[i] = 'Z'
#                     elif char == '5': chars[i] = 'S'
#                     elif char == '8': chars[i] = 'B'
#                     elif char == '6': chars[i] = 'G'
            
#             # District code positions (2-3) - should be numbers only
#             elif i in [2, 3]:
#                 if char == 'O': chars[i] = '0'
#                 elif char == 'I': chars[i] = '1'
#                 elif char == 'B': chars[i] = '8'
#                 elif char == 'S': chars[i] = '5'
#                 elif char == 'G': chars[i] = '6'
#                 elif char == 'Z': chars[i] = '2'
#                 elif char == 'D': chars[i] = '0'
#                 elif char == 'Q': chars[i] = '0'
            
#             # Series letter positions (4-5) - should be letters only
#             elif i in [4, 5]:
#                 if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
#                     if char == '0': chars[i] = 'O'
#                     elif char == '1': chars[i] = 'I'
#                     elif char == '2': chars[i] = 'Z'
#                     elif char == '5': chars[i] = 'S'
#                     elif char == '8': chars[i] = 'B'
#                     elif char == '6': chars[i] = 'G'
            
#             # Vehicle number positions (6+) - should be numbers only
#             else:
#                 if char == 'O': chars[i] = '0'
#                 elif char == 'I': chars[i] = '1'
#                 elif char == 'B': chars[i] = '8'
#                 elif char == 'S': chars[i] = '5'
#                 elif char == 'G': chars[i] = '6'
#                 elif char == 'Z': chars[i] = '2'
#                 elif char == 'D': chars[i] = '0'
#                 elif char == 'Q': chars[i] = '0'
        
#         return "".join(chars)
    
#     def remove_prefix_before_state_code(self, text):
#         """
#         Remove any characters before a valid state code
        
#         Args:
#             text: Text to process
            
#         Returns:
#             Text starting from valid state code
#         """
#         if not text or len(text) < 2:
#             return text
        
#         # Find first occurrence of valid state code
#         for i in range(len(text) - 1):
#             potential_state = text[i:i+2]
#             if potential_state in self.STATE_CODES:
#                 return text[i:]
        
#         return text
    
#     def validate_and_correct(self, text):
#         """
#         Validate and correct license plate text
        
#         Args:
#             text: Raw OCR text
            
#         Returns:
#             Validated and corrected plate number or None if invalid
#         """
#         if not text:
#             return None
        
#         # Remove prefix before state code
#         cleaned = self.remove_prefix_before_state_code(text)
        
#         # Apply smart correction
#         corrected = self.smart_correct(cleaned)
        
#         # Try to extract plate pattern
#         pattern = r'([A-Z]{2})(\d{2,3})([A-Z]{1,2})(\d{4})'
#         match = re.search(pattern, corrected)
        
#         if match:
#             plate = "".join(match.groups())
#             if self.validate_format(plate):
#                 return plate
        
#         return None
    
#     def get_state_name(self, state_code):
#         """
#         Get state name from state code
        
#         Args:
#             state_code: 2-letter state code
            
#         Returns:
#             State name or "Unknown"
#         """
#         state_names = {
#             'TN': 'Tamil Nadu', 'KA': 'Karnataka', 'MH': 'Maharashtra',
#             'DL': 'Delhi', 'GJ': 'Gujarat', 'RJ': 'Rajasthan',
#             'UP': 'Uttar Pradesh', 'WB': 'West Bengal', 'AP': 'Andhra Pradesh',
#             'KL': 'Kerala', 'TS': 'Telangana', 'TG': 'Telangana',
#             'BR': 'Bihar', 'MP': 'Madhya Pradesh', 'PB': 'Punjab',
#             'HR': 'Haryana', 'HP': 'Himachal Pradesh', 'JK': 'Jammu & Kashmir',
#             'AS': 'Assam', 'OR': 'Odisha', 'GA': 'Goa',
#             'CH': 'Chandigarh', 'AN': 'Andaman & Nicobar', 'DD': 'Daman & Diu'
#         }
#         return state_names.get(state_code, 'Unknown')
"""
License Plate Validator Module
Validates and corrects Indian license plate numbers
"""

import re


class PlateValidator:
    """Validator for Indian license plate format"""
    
    # Indian state codes with common ones first (for priority)
    STATE_CODES = {
        "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL", 
        "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TG", 
        "TS", "TR", "UP", "UK", "WB", "AN", "CH", "DD", "DL", "JK", "LA", "LD", 
        "PY", "BH"
    }
    
    # Priority order for state codes (most common first)
    PRIORITY_STATES = [
        "TN","MH", "DL", "KA", "UP", "GJ", "RJ", "WB", "AP", "TS", "TG", 
        "BR", "MP", "PB", "HR", "KL", "NL", "AR", "AS", "GA", "HP", "JK",
        "CH", "AN", "DD", "LD", "PY", "SK", "TR", "UK", "BH"
    ]
    
    # Valid district code ranges by state (simplified)
    # Most states have district codes from 01-99
    VALID_DISTRICT_RANGES = {
        'TN': (1, 99),  # Tamil Nadu: 01-99
        'MH': (1, 99),  # Maharashtra: 01-99
        'DL': (1, 99),  # Delhi: 01-99
        'KA': (1, 99),  # Karnataka: 01-99
        'NL': (1, 99),  # Nagaland: 01-99 (but less common)
        # Add more specific ranges if needed
    }
    
    def __init__(self):
        """Initialize plate validator"""
        pass
    
    def validate_format(self, text):
        """
        Validate Indian license plate format: AA##AA#### or AA##A####
        
        Args:
            text: License plate text to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if not text or len(text) < 7:
            return False
        
        # Pattern: 2 letters + 2-3 digits + 1-2 letters + 4 digits
        pattern = r'^([A-Z]{2})(\d{2,3})([A-Z]{1,2})(\d{4})$'
        match = re.match(pattern, text)
        
        if not match:
            return False
        
        # Check if state code is valid
        state_code = match.group(1)
        return state_code in self.STATE_CODES
    
    def extract_state_code_from_text(self, text):
        """
        Extract state code from OCR text (even if not at beginning)
        
        Args:
            text: OCR text
            
        Returns:
            State code if found, else None
        """
        # Only look for valid state codes
        for state_code in self.PRIORITY_STATES:
            if state_code in text:
                return state_code
        return None
    
    def is_valid_district_code(self, state_code, district_code):
        """
        Check if district code is valid for the state
        
        Args:
            state_code: 2-letter state code
            district_code: District number (string)
            
        Returns:
            True if valid, False otherwise
        """
        if not district_code.isdigit():
            return False
        
        district_num = int(district_code)
        
        # Get valid range for the state
        if state_code in self.VALID_DISTRICT_RANGES:
            min_district, max_district = self.VALID_DISTRICT_RANGES[state_code]
            return min_district <= district_num <= max_district
        
        # Default: district should be between 01-99
        return 1 <= district_num <= 99
    
    def smart_correct(self, text):
        """
        Apply smart character correction based on position
        Format: AA##AA#### or AA##A####
        
        Args:
            text: License plate text to correct
            
        Returns:
            Corrected text
        """
        if not text or len(text) < 7:
            return text
        
        chars = list(text.upper())
        
        for i, char in enumerate(chars):
            # State code positions (0-1) - should be letters only
            if i < 2:
                if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if char == '0': chars[i] = 'O'
                    elif char == '1': chars[i] = 'I'
                    elif char == '2': chars[i] = 'Z'
                    elif char == '5': chars[i] = 'S'
                    elif char == '8': chars[i] = 'B'
                    elif char == '6': chars[i] = 'G'
            
            # District code positions (2-3) - should be numbers only
            elif i in [2, 3]:
                if char == 'O': chars[i] = '0'
                elif char == 'I': chars[i] = '1'
                elif char == 'B': chars[i] = '8'
                elif char == 'S': chars[i] = '5'
                elif char == 'G': chars[i] = '6'
                elif char == 'Z': chars[i] = '2'
                elif char == 'D': chars[i] = '0'
                elif char == 'Q': chars[i] = '0'
            
            # Series letter positions (4-5) - should be letters only
            elif i in [4, 5]:
                if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if char == '0': chars[i] = 'O'
                    elif char == '1': chars[i] = 'I'
                    elif char == '2': chars[i] = 'Z'
                    elif char == '5': chars[i] = 'S'
                    elif char == '8': chars[i] = 'B'
                    elif char == '6': chars[i] = 'G'
            
            # Vehicle number positions (6+) - should be numbers only
            else:
                if char == 'O': chars[i] = '0'
                elif char == 'I': chars[i] = '1'
                elif char == 'B': chars[i] = '8'
                elif char == 'S': chars[i] = '5'
                elif char == 'G': chars[i] = '6'
                elif char == 'Z': chars[i] = '2'
                elif char == 'D': chars[i] = '0'
                elif char == 'Q': chars[i] = '0'
        
        return "".join(chars)
    
    def remove_prefix_before_state_code(self, text):
        """
        Remove any characters before a valid state code
        
        Args:
            text: Text to process
            
        Returns:
            Text starting from valid state code
        """
        if not text or len(text) < 2:
            return text
        
        # Find first occurrence of valid state code
        for i in range(len(text) - 1):
            potential_state = text[i:i+2]
            if potential_state in self.STATE_CODES:
                return text[i:]
        
        return text
    
    def reconstruct_full_plate(self, text, state_code=None):
        """
        Reconstruct full plate number when state code is missing or misplaced
        
        Args:
            text: OCR text (might be missing state code)
            state_code: Optional state code to prepend
            
        Returns:
            Reconstructed plate number
        """
        # If state code provided, use it
        if state_code:
            # Remove any existing state code from text
            clean_text = text
            for sc in self.STATE_CODES:
                clean_text = clean_text.replace(sc, '')
            
            # Clean the remaining text
            cleaned = re.sub(r'[^A-Z0-9]', '', clean_text.upper())
            
            # Try to extract district code, series, and number
            # Format: (district 2-3 digits) + (series 1-2 letters) + (number 4 digits)
            pattern = r'^(\d{2,3})([A-Z]{1,2})(\d{4})$'
            match = re.search(pattern, cleaned)
            
            if match:
                district = match.group(1)
                series = match.group(2)
                number = match.group(3)
                
                # Validate district code for this state
                if self.is_valid_district_code(state_code, district):
                    return f"{state_code}{district}{series}{number}"
                else:
                    print(f"District code {district} invalid for state {state_code}")
            
            return None
        return None
    
    def try_all_state_codes(self, text):
        """
        Try all possible state codes to find the best match
        
        Args:
            text: OCR text (like "23BH7438")
            
        Returns:
            Best matching plate or None
        """
        # Clean the text
        cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # Extract district, series, number parts
        # The text should already have district+series+number (e.g., "23BH7438")
        # where district=23, series=BH, number=7438
        
        # Try to parse the pattern
        pattern = r'^(\d{2,3})([A-Z]{1,2})(\d{4})$'
        match = re.search(pattern, cleaned)
        
        if not match:
            return None
        
        district = match.group(1)
        series = match.group(2)
        number = match.group(3)
        
        print(f"Parsed - District: {district}, Series: {series}, Number: {number}")
        
        # Try each state code in priority order
        for state_code in self.PRIORITY_STATES:
            # Skip NL if we suspect it's wrong (you can add specific exclusions)
            # For this specific case, prioritize TN over NL
            if state_code == 'NL' and 'TN' in self.PRIORITY_STATES:
                # Continue checking TN first
                continue
            
            # Check if district code is valid for this state
            if self.is_valid_district_code(state_code, district):
                plate = f"{state_code}{district}{series}{number}"
                if self.validate_format(plate):
                    print(f"Found valid plate with {state_code}: {plate}")
                    return plate
        
        return None
    
    def validate_and_correct(self, text):
        """
        Validate and correct license plate text
        
        Args:
            text: Raw OCR text
            
        Returns:
            Validated and corrected plate number or None if invalid
        """
        if not text:
            return None
        
        # Debug print
        print(f"Validator received: '{text}'")
        
        # FIRST: Check if this is a plate without state code (like "23BH7438")
        # Try to reconstruct by adding possible state codes
        reconstructed = self.try_all_state_codes(text)
        if reconstructed:
            return reconstructed
        
        # SECOND: Try to find state code in the text
        state_code = self.extract_state_code_from_text(text)
        
        if state_code:
            print(f"Found state code in text: {state_code}")
            reconstructed = self.reconstruct_full_plate(text, state_code)
            if reconstructed:
                print(f"Reconstructed plate: {reconstructed}")
                if self.validate_format(reconstructed):
                    return reconstructed
        
        # THIRD: Try standard approach (state code at beginning)
        # Remove prefix before state code
        cleaned = self.remove_prefix_before_state_code(text)
        
        # Apply smart correction
        corrected = self.smart_correct(cleaned)
        
        # Try to extract plate pattern
        pattern = r'([A-Z]{2})(\d{2,3})([A-Z]{1,2})(\d{4})'
        match = re.search(pattern, corrected)
        
        if match:
            plate = "".join(match.groups())
            if self.validate_format(plate):
                return plate
        
        # FOURTH: Try to clean and re-validate without expecting state code at start
        cleaned_all = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # Look for pattern anywhere in the string
        pattern_flexible = r'([A-Z]{2})(\d{2,3})([A-Z]{1,2})(\d{4})'
        match = re.search(pattern_flexible, cleaned_all)
        
        if match:
            plate = "".join(match.groups())
            if self.validate_format(plate):
                return plate
        
        return None
    
    def get_state_name(self, state_code):
        """
        Get state name from state code
        
        Args:
            state_code: 2-letter state code
            
        Returns:
            State name or "Unknown"
        """
        state_names = {
            'TN': 'Tamil Nadu', 'KA': 'Karnataka', 'MH': 'Maharashtra',
            'DL': 'Delhi', 'GJ': 'Gujarat', 'RJ': 'Rajasthan',
            'UP': 'Uttar Pradesh', 'WB': 'West Bengal', 'AP': 'Andhra Pradesh',
            'KL': 'Kerala', 'TS': 'Telangana', 'TG': 'Telangana',
            'BR': 'Bihar', 'MP': 'Madhya Pradesh', 'PB': 'Punjab',
            'HR': 'Haryana', 'HP': 'Himachal Pradesh', 'JK': 'Jammu & Kashmir',
            'AS': 'Assam', 'OR': 'Odisha', 'GA': 'Goa',
            'CH': 'Chandigarh', 'AN': 'Andaman & Nicobar', 'DD': 'Daman & Diu',
            'NL': 'Nagaland'  # Nagaland, not Netherlands
        }
        return state_names.get(state_code, 'Unknown')