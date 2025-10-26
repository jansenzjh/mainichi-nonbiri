
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_slug(url):
    path = urlparse(url).path
    return path.strip('/').split('/')[-1]

def fetch_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', class_='post_content')
        return content_div
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    with open('links.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not os.path.exists('output'):
        os.makedirs('output')

    slugs = [get_slug(url) for url in urls]
    generated_files = []

    for i, url in enumerate(urls):
        slug = slugs[i]
        content_div = fetch_content(url)

        if content_div:
            for a_tag in content_div.find_all('a', class_='sounds'):
                audio_src = a_tag.get('data-file')
                if audio_src:
                    audio_tag = BeautifulSoup('<audio controls></audio>', 'html.parser').audio
                    audio_tag['src'] = audio_src
                    a_tag.replace_with(audio_tag)

            prev_slug = slugs[i - 1] if i > 0 else None
            next_slug = slugs[i + 1] if i < len(slugs) - 1 else None

            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slug}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="nav">
            {'<a href="' + prev_slug + '.html">Previous</a>' if prev_slug else ''}
            <a href="index.html">Index</a>
            {'<a href="' + next_slug + '.html">Next</a>' if next_slug else ''}
            <button id="mark-learning">Mark as Learning</button>
            <button id="clear-marker">Clear Marker</button>
            <button id="go-marker">Go to Marker</button>
        </div>
        {content_div.prettify()}
    </div>
    <script>
        document.getElementById('mark-learning').addEventListener('click', () => {{
            localStorage.setItem('learningMarker', window.location.href);
            alert('Page marked as learning!');
        }});

        document.getElementById('clear-marker').addEventListener('click', () => {{
            localStorage.removeItem('learningMarker');
            alert('Marker cleared!');
        }});

        document.getElementById('go-marker').addEventListener('click', () => {{
            const marker = localStorage.getItem('learningMarker');
            if (marker) {{
                window.location.href = marker;
            }} else {{
                alert('No marker set!');
            }}
        }});
    </script>
</body>
</html>
"""
            file_path = os.path.join('output', f'{slug}.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated_files.append(f'{slug}.html')
            print(f"Generated {file_path}")

    # Generate index.html
    index_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Index</h1>
        <ul>
"""
    for file in generated_files:
        index_content += f'            <li><a href="{file}">{file}</a></li>\n'
    index_content += """
        </ul>
    </div>
</body>
</html>
"""
    with open(os.path.join('output', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("Generated index.html")

if __name__ == '__main__':
    main()
