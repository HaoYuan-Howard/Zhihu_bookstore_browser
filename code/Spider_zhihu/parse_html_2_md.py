import re
from bs4 import BeautifulSoup


def extract_paragraphs_to_md(html_path, md_output_file):
    """
    Get the novel content from HTML to generate md document
    :param html_path: captured html files
    :param md_output_file: saved novel content from html with p tags
    :return: None
    """
    with open(html_path, 'r', encoding="utf-8") as f:
        html_content = f.read()

    # Use BeautifulSoup to parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <p> tags
    paragraphs = soup.find_all('p')

    # Extract text content from each <p> tag and join them with line breaks
    content = '\n\n'.join([p.get_text() for p in paragraphs])

    # Write the content to a .md file
    with open(md_output_file, 'w', encoding="utf-8") as md_file:
        md_file.write(content)

    print(f"Content saved to {md_output_file}")



