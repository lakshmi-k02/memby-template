import os
from bs4 import BeautifulSoup

def html_to_php_array(html_content):
    """Convert HTML structure to PHP array format like create-audience.php"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Title
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Untitled Page'

    # Excerpt
    excerpt_tag = soup.select_one('.excerpt p')
    excerpt = excerpt_tag.get_text(strip=True) if excerpt_tag else ''

    sections = []

    # Images
    for img in soup.find_all('img'):
        sections.append({
            'type': 'image',
            'src': img.get('src', ''),
            'alt': img.get('alt', '')
        })

    # Headings
    for heading in soup.find_all(['h2', 'h3']):
        sections.append({
            'type': 'heading',
            'id': heading.get('id', heading.get_text(strip=True).lower().replace(' ', '-')),
            'text': heading.get_text(strip=True)
        })

    # Tables
    for table in soup.find_all('table'):
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []
        for tr in table.find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells:
                rows.append(cells)
        if headers or rows:
            sections.append({
                'type': 'table',
                'headers': headers,
                'rows': rows
            })

    # Lists
    for ul in soup.find_all(['ul', 'ol']):
        items = [li.get_text(strip=True) for li in ul.find_all('li')]
        if items:
            sections.append({
                'type': 'list',
                'items': items
            })

    # Build PHP content
    php_content = "<?php\n"
    php_content += "// Auto-generated file from converter\n\n"
    php_content += "$page_content = [\n"
    php_content += f"    'title' => '{title}',\n"
    php_content += f"    'excerpt' => '{excerpt}',\n"
    php_content += f"    'updated' => date('F Y'),\n"
    php_content += f"    'sections' => [\n"

    for sec in sections:
        if sec['type'] == 'image':
            php_content += f"        [ 'type' => 'image', 'src' => '{sec['src']}', 'alt' => '{sec['alt']}' ],\n"
        elif sec['type'] == 'heading':
            php_content += f"        [ 'type' => 'heading', 'id' => '{sec['id']}', 'text' => '{sec['text']}' ],\n"
        elif sec['type'] == 'table':
            php_content += f"        [ 'type' => 'table', 'headers' => {sec['headers']}, 'rows' => {sec['rows']} ],\n"
        elif sec['type'] == 'list':
            php_content += f"        [ 'type' => 'list', 'items' => {sec['items']} ],\n"

    php_content += "    ]\n];\n\n"
    php_content += "function renderContent($content, $viewType = 'desktop') {\n"
    php_content += "    // Add rendering logic similar to create-audience.php\n"
    php_content += "}\n"
    php_content += "?>\n"

    return php_content


def convert_folder(folder_path):
    """Convert all .php files in the folder to structured format"""
    for filename in os.listdir(folder_path):
        if filename.endswith('.php'):
            full_path = os.path.join(folder_path, filename)
            with open(full_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            new_php = html_to_php_array(html_content)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_php)
            print(f"✅ Converted: {filename}")


if __name__ == "__main__":
    folder = input("Enter folder path with PHP files: ").strip()
    if os.path.isdir(folder):
        convert_folder(folder)
    else:
        print("❌ Folder not found")
