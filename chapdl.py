from bs4 import BeautifulSoup
import requests
import sys

if len(sys.argv) < 2:
    print("missing args")
    starting_url = input("inserisci il link del capitolo di un manga: ")
else:
    starting_url = sys.argv[1]
    print(sys.argv[1])

def get_page_link(link):
    r = requests.get(link, "html.parser")
    soup = BeautifulSoup(r.text, "lxml")
    return soup.find_all('img')[1].get('src')

def url_ok(url):
    try:
        response = requests.head(url)
         
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError as e:
        return e

def parse_links(pages, ext):
    i = 0
    while 1:
        next_link = pages[i].rsplit('.', 1)[0] + ext
        if i < 10:
            index = next_link.find(ext)
            next_link = next_link[:index - 1] + str(i + 1) + next_link[index:]
        elif i >= 10 and i < 100:
            index = next_link.find(ext)
            next_link = next_link[:index - 2] + str(i + 1) + next_link[index:]
        elif i >= 100 and i < 1000:
            index = next_link.find(ext)
            next_link = next_link[:index - 3] + str(i + 1) + next_link[index:]
        else:
            print("!TOO MANY CHAPTERS!")
            exit

        if (url_ok(next_link)):
            pages.append(next_link) 
            i += 1
            print("Parsing chapter " + str(i))
            continue

        if ext == ".jpg":
            # link convertito a .png
            alternative_next_link = next_link.rsplit('.', 1)[0] + ".png"
            if (url_ok(alternative_next_link)):
                pages.append(alternative_next_link) 
                i += 1
                print("Parsing chapter " + str(i))
                continue

        if ext == ".png":
            # link convertito a .jpg
            alternative_next_link = next_link.rsplit('.', 1)[0] + ".jpg"
            if (url_ok(alternative_next_link)):
                pages.append(alternative_next_link) 
                i += 1
                print("Parsing chapter " + str(i))
                continue

        break

pages = [get_page_link(starting_url)]

if(url_ok(pages[0]) != True):
    print("!INDEX ERROR!")
    exit

if pages[0][pages[0].rfind("."):] == ".jpg":
    ext = ".jpg"
elif pages[0][pages[0].rfind("."):] == ".png":
    ext = ".png"

parse_links(pages, ext)

f = open("output.txt", "a")
for page in pages:
    f.write(page + '\n')

f.close()

f = open("output.txt", "r")
print(f.read()) 
f.close()