from bs4 import BeautifulSoup
import requests
import sys

if len(sys.argv) < 2:
    print("missing args")
    manga = input("Inserisci il link di un manga: ")
else:
    manga = sys.argv[1]
    print(sys.argv[1])

chapters = []

def get_chapters_link(link):
    r = requests.get(manga, "html.parser")
    soup = BeautifulSoup(r.text, "lxml")
    for link in soup.find_all('a', 'chap'):
        if "/read/" in link.get('href'):
            chapters.append(link.get('href'))

get_chapters_link(manga)
chapters.reverse()

f = open("chapters.txt", "a")
for chapter in chapters:
    f.write(chapter + '\n')

f.close()

f = open("chapters.txt", "r")
print(f.read()) 
f.close()