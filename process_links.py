
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
        title_h1 = soup.find('h1', class_='c-postTitle__ttl')
        content_div = soup.find('div', class_='post_content')
        return title_h1, content_div
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None

def main():
    with open('links.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not os.path.exists('output'):
        os.makedirs('output')

    slugs = [get_slug(url) for url in urls]
    generated_files = []

    for i, url in enumerate(urls):
        slug = slugs[i]
        title_h1, content_div = fetch_content(url)

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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <script defer src="https://umi.crazyhungry.party/script.js" data-website-id="515ea1ca-45c6-499c-b353-7f38a29336b1"></script>
</head>
<body>
    <div class="container">
        <div class="nav">
            <div class="nav-left">
                {'<a href="' + prev_slug + '.html" title="Previous"><i class="fas fa-arrow-left"></i></a>' if prev_slug else '<a class="disabled"><i class="fas fa-arrow-left"></i></a>'}
            </div>
            <div class="nav-center">
                <a href="index.html" title="Index"><i class="fas fa-list"></i></a>
                <button id="mark-learning" title="Mark"><i class="fas fa-bookmark"></i></button>
                <button id="go-marker" title="Go"><i class="fas fa-location-arrow"></i></button>
                <button id="clear-marker" title="Clear"><i class="fas fa-trash"></i></button>
            </div>
            <div class="nav-right">
                {'<a href="' + next_slug + '.html" title="Next"><i class="fas fa-arrow-right"></i></a>' if next_slug else '<a class="disabled"><i class="fas fa-arrow-right"></i></a>'}
            </div>
        </div>
        {title_h1.prettify() if title_h1 else ''}
        {content_div.prettify()}
    </div>
    <script src="script.js"></script>
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
