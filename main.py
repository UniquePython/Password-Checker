import requests
import hashlib
from colorama import Fore, init, Style

init(autoreset=True)

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char
    res = requests.get(url)
    status_code = res.status_code
    if status_code != 200:
        raise RuntimeError(Fore.RED + f"Error fetching {status_code}, check the API and try again!" + Style.RESET_ALL)
    return res

def hacked_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0

def hacked_api_check(password):
    hashed_password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    head, tail = hashed_password[:5], hashed_password[5:]
    response = request_api_data(head)
    return hacked_count(response, tail)

def check_password_strength(password):
    min_length = 8
    requires_uppercase = True
    requires_lowercase = True
    requires_numbers = True
    requires_special_characters = True

    score = 0
    if len(password) >= min_length:
        score += 1
    if any(char.isupper() for char in password) and requires_uppercase:
        score += 1
    if any(char.islower() for char in password) and requires_lowercase:
        score += 1
    if any(char.isdigit() for char in password) and requires_numbers:
        score += 1
    if any(char in "!@#$%^&*()-_=+{}[]|:;\"'<>,.?/~" for char in password) and requires_special_characters:
        score += 1
    
    if score >= 4:
        return "strong"
    elif score >= 2:
        return "moderate"
    else:
        return "weak"

def suggest_password_improvement(password):
    suggestions = []
    if len(password) < 8:
        suggestions.append("Length should be at least 8 characters.")
    if not any(char.isupper() for char in password):
        suggestions.append("Include at least one uppercase letter.")
    if not any(char.islower() for char in password):
        suggestions.append("Include at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        suggestions.append("Include at least one number.")
    if not any(char in "!@#$%^&*()-_=+{}[]|:;\"'<>,.?/~" for char in password):
        suggestions.append("Include at least one special character.")
    return suggestions

def main():
    while True:
        password = input(Fore.YELLOW + "Enter your password (or type 'exit' to quit): " + Style.RESET_ALL)
        if password.lower() == 'exit':
            break
        count = hacked_api_check(password)
        if count:
            print(Fore.RED + f"Your password '{password}' was hacked {count} times. Change your password IMMEDIATELY!" + Style.RESET_ALL)
            strength = check_password_strength(password)
            print(Fore.YELLOW + "Password strength:", strength + Style.RESET_ALL)
            if strength == "weak":
                print(Fore.GREEN + "Suggestions for improvement:" + Style.RESET_ALL)
                for suggestion in suggest_password_improvement(password):
                    print(Fore.BLUE + "-", suggestion + Style.RESET_ALL)
                break
            break
        else:
            print(Fore.GREEN + f"Your password '{password}' was not hacked. It is secure and safe to use.")
            print()
            break

if __name__ == "__main__":
    main()