import sys
import os
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("missing args")
    print(sys.argv[0] + "[search query]")
    sys.exit(1)

query = sys.argv[1]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.mangaworld.nz/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
}

def search_manga(keyword):
	params = {
	    'keyword': f'{keyword}',
	}
	response = requests.get('https://www.mangaworld.nz/archive', params=params, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	links = []
	for link in soup.find_all('a', class_='manga-title'):
	    links.append(link.get('href'))
	return links

def choose_manga(links):
    i = 0
    for link in links:
        manga_title = link[link.rfind('/') + 1:]
        print('['+str(i)+"] " + manga_title.title())
        i += 1
    while 1:
        choice = input("Choose a manga [n]: ")
        choice = int(choice)
        if choice > i - 1:
            print("Invalid answer")
            continue
        return links[choice]

def get_volumes(manga):
    response = requests.get(manga)
    soup = BeautifulSoup(response.text, 'html.parser')
    max_volumes = soup.find_all('p', class_="volume-name d-inline")[0].get_text()
    max_volumes = int(max_volumes[max_volumes.rfind(' ') + 1:])
    volumes = []
    chapters = []
    for volume_div in soup.find_all('div', class_="volume-element pl-2")[:max_volumes]:
        chapters = []
        for chapter in volume_div.find_all('a', class_="chap"):
            href = chapter.get('href')
            if "/read/" in href:
                chapters.append(href)
        chapters.reverse()  
        volumes.append(chapters)
    volumes.reverse()
    return volumes

def get_pages(chapter):
    response = requests.get(chapter)
    soup = BeautifulSoup(response.text, 'html.parser')
    for image in soup.find_all('img', class_='img-fluid'):
        src = image.get('src')
        if "capitolo" in src:
            first_page = src
    max_page = soup.find_all('option', value='0')[0].get_text()
    max_page = max_page[max_page.rfind('/') + 1:]
    max_page = int(max_page)
    pages = []
    for i in range(1, max_page + 1):
        pages.append(first_page[:first_page.rfind('/') + 1] + str(i) + first_page[first_page.rfind('.'):])
    return pages

def download_page(pages, chapter, volume):
    for i, url in enumerate(pages):  
        filename = f"volume{volume}_chapter{chapter}_{i + 1}.png"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Downloaded: {filename}")
                continue  

            # Try with alternative ext.
            print(f"⚠️ Error for {url}: {response.status_code}")
            print("🔁 Trying alternative url...")

            if url.endswith('.png'):
                alt_url = url[:-4] + '.jpg'
                alt_filename = filename.replace('.png', '.jpg')
            elif url.endswith('.jpg'):
                alt_url = url[:-4] + '.png'
                alt_filename = filename.replace('.png', '.jpg')  # fallback
            else:
                print("unable to change ext.")
                continue

            alt_response = requests.get(alt_url)
            if alt_response.status_code == 200:
                with open(alt_filename, 'wb') as f:
                    f.write(alt_response.content)
                print(f"✅ Downloaded alternative: {alt_filename}")
            else:
                print(f"❌ Alternative failed for {alt_url}: {alt_response.status_code}")

        except Exception as e:
            print(f"❌ Exception for {url}: {e}")


# MAIN

links   = search_manga(query)
manga   = choose_manga(links)
volumes = get_volumes(manga)


volumes_with_pages = []

for volume in volumes:
    chapters_with_pages = []
    for chapter_url in volume:
        pages = get_pages(chapter_url)  
        chapters_with_pages.append({
            'url': chapter_url,
            'pages': pages
        })
    volumes_with_pages.append(chapters_with_pages)

dir_name = manga[manga.rfind('/') + 1:].title()
os.mkdir(dir_name)
os.chdir(dir_name)

i = 1
j = 1
for volume in volumes_with_pages:
    for chapter in volume:
        download_page(chapter['pages'], str(i), str(j))
        i += 1
    j += 1

