import datetime
import os, sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from pywebcopy import save_webpage
import re
from urllib.parse import urljoin


def fetchPages(args):
    for i in range(1, len(args)):
        try:
            requestedUrl = args[i]
            var = str(args[i])[:-1]
            var = var.split("//")
            requestedUrl = requests.get(requestedUrl)
            with open(var[1] + ".html", "w") as f:
                f.write(requestedUrl.text)

            with open(var[1] + ".txt", "w") as f:
                f.write("Site: %s\nnum_links: %s\nimages: %s\nlast_fetch: %s\n" % (
                    var[1], len(requestedUrl.text.split("href")) - 1, len(requestedUrl.text.split("img")),
                    datetime.now(timezone.utc).strftime('%a %b %d %Y %H:%M %Z')))
        except:
            print("Error while downloading html")


def meta(websiteName):
    try:
        var = websiteName.split("//")
        file = open(var[1] + ".txt", "r")
        for line in file.readlines():
            print(line)
    except:
        print("No such file exists")


def savePage(url, pagepath='page'):
    def soupfindnSave(pagefolder, tag2find='img', inner='src'):
        """saves on specified `pagefolder` all tag2find objects"""
        if not os.path.exists(pagefolder):  # create only once
            os.mkdir(pagefolder)
        for res in soup.findAll(tag2find):  # images, css, etc..
            try:
                if not res.has_attr(inner):  # check if inner tag (file object) exists
                    continue  # may or may not exist
                filename = re.sub('\W+', '', os.path.basename(res[inner]))  # clean special chars
                fileurl = urljoin(url, res.get(inner))
                filepath = os.path.join(pagefolder, filename)
                # rename html ref so can move html and folder of files anywhere
                res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                if not os.path.isfile(filepath):  # was not downloaded
                    with open(filepath, 'wb') as file:
                        filebin = session.get(fileurl)
                        file.write(filebin.content)
            except Exception as exc:
                print(exc, file=sys.stderr)
        return soup

    session = requests.Session()
    # ... whatever other requests config you need here
    response = session.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    pagepath, _ = os.path.splitext(pagepath)  # avoid duplicate .html
    pagefolder = pagepath + '_files'  # page contents
    soup = soupfindnSave(pagefolder, 'img', 'src')
    soup = soupfindnSave(pagefolder, 'link', 'href')
    soup = soupfindnSave(pagefolder, 'script', 'src')
    with open(pagepath + '.html', 'wb') as file:
        file.write(soup.prettify('utf-8'))
    return soup

if __name__ == '__main__':
    try:
        if sys.argv[1] == '--metadata':
            meta(sys.argv[2])
        else:
            savePage('http://developers-core.com', 'developers')
    except:
        print("Unknown arguments")
