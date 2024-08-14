
def replace_special_characters(text):
    # Define a dictionary for the characters and their replacements
    char_to_html = {
        '"': "'",  # Replace double quotes with single quotes
        '&': "&amp;",  # Replace ampersand with HTML entity
        '<': "&lt;",   # Replace less than with HTML entity
        '>': "&gt;",   # Replace greater than with HTML entity
        ':': "",       # Remove colon
        '|': "!",       # Replace pipe with exclamation mark
        "’": "'",      # Replace right single quotation mark with single quote
        "‘": "'",      # Replace left single quotation mark with single quote
        "��": "",      # Remove unknown characters
        "»": "",       # Remove right-pointing double angle quotation mark
        "–": "-",      # Replace en dash with hyphen
        "—": "-",      # Replace em dash with hyphen
        "&#39;": "'"   # Replace HTML entity for apostrophe with single quote
    }
    decoded_text = text


    for i in range(len(text)):
        if '&#39;' in text[i:i+5]:
            decoded_text = decoded_text.replace('&#39;', "'", char+5)
            
    # Replace each character in the dictionary with its replacement
    for char, replacement in char_to_html.items():
        decoded_text = decoded_text.replace(char, replacement)
    
    return decoded_text
