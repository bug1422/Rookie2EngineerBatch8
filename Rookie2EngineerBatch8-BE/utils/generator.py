from datetime import date
from utils.hash import hash_password

class Generator:
    def __init__(self):
        pass

    @staticmethod
    def generate_username(first_name: str, last_name: str) -> str:
        # Convert names to lowercase and take only the first word
        first_name_first_word = first_name.strip().lower().split()[0]
        # Split last name into words
        last_name_parts = last_name.strip().lower().split()
        
        # Get first letter of each word in last name
        last_name_initials = ''.join(word[0] for word in last_name_parts)
        
        # Combine first name with last name initials
        username = first_name_first_word + last_name_initials
        
        return username
    
    @staticmethod
    def generate_staff_code(count_all_users: int) -> str:
        return f"SD{count_all_users + 1:04d}"
    
    @staticmethod
    def generate_password(username: str, date_of_birth: date) -> str:
        # format: username@date_of_birth (ddmmyyyy)
        generated_password = f"{username}@{date_of_birth.strftime('%d%m%Y')}"
        return hash_password(generated_password)
    
    @staticmethod
    def generate_root_password(password: str) -> str:
        return hash_password(password)

    @staticmethod
    def generate_prefix(category_name: str) -> str:
        """Generate a prefix for the category based on its name."""
        words = category_name.split()
        if len(words) >= 2:
            # Take the first letter of the first two words
            prefix = ''.join(word[0].upper() for word in words[:2])
        else:
            # If there's only one word, take the first two letters
            prefix = category_name[:2].upper()
        return prefix
    @staticmethod
    def generate_asset_code(prefix: str, number: int) -> str:
        """Generate an asset code with the given prefix and 6-digit number."""
        return f"{prefix}{number:06d}"

    