#! python
# downloadXkcs.py - Downloads XKCD comics

import requests, os, bs4

url = 'http://xkcd.com/2472/'        # starting url

os.makedirs('xkcd', exist_ok=True)  # store comics in ./xkcd

while not url.endswith('#'):
    # download the page
    print('Downloding page %s...' % (url))
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # find the url of the comic image
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find the comic image')
    else:
        try:
            comicUrl = 'https:' + comicElem[0].get('src') #getting comic url and then downloading its image
            print('Downloading image %s.....' %(comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()

        except requests.exceptions.MissingSchema:
        #skip if not a normal image file
            prev = soup.select('a[rel="prev"]')[0]
            url = 'http://xkcd.com' + prev.get('href')
            continue

    # save the image to ./xkcd
    imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)), 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    # get the Prev button's url
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print('Done')

    