import re
import base64


def extract_base64_font(html_path, output_file):
    """
    Get base64 encoding from html to generate ttf file
    :param html_path: captured html file
    :param output_file: generated ttf file
    :return: None
    """
    with open(html_path,'r',encoding="utf-8") as f:
        html_content = f.read()

    # Regular expression to extract base64 strings for font/ttf
    base64_pattern = r"base64,([A-Za-z0-9+/=]+)\)"
    base64_code = re.findall(base64_pattern,html_content)

    if base64_code:
        # Decode the first base64 match (assuming you want the first occurrence)
        decoded_font = base64.b64decode(base64_code[2])

        # Write the decoded content to a .ttf file
        with open(output_file, 'wb') as ttf_file:
            ttf_file.write(decoded_font)
        print(f"Font saved to {output_file}")
    else:
        print("No base64-encoded font found.")



