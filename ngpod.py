#! /usr/bin/env python
import html.parser
import http.client
import os
import os.path
import urllib.parse
import urllib.request

class Parser(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.found = False  # is the searched tag found?
        self.image = None   # URL of the image

    def handle_starttag(self, tag, attrs):
        if self.image != None:
            return
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'primary_photo':
                    self.found = True
                    return
        elif tag == 'img' and self.found == True:
            for name, value in attrs:
                if name == 'src':
                    self.image = value
                    return

if __name__ == '__main__':
    # read HTML of the page with National Geographic picture of the day
    conn = http.client.HTTPConnection('photography.nationalgeographic.com')
    conn.request('GET', '/photography/photo-of-the-day')
    resp = conn.getresponse()
    resp = resp.read()
    resp = resp.decode()
    conn.close()
    # parse it to the URL of the image
    parser = Parser()
    parser.feed(resp)
    # download the content and store the image
    url = urllib.parse.urlparse(parser.image)
    name = os.path.basename(url.path)
    name = os.path.join('/tmp', name)
    with open(name, 'wb') as f:
        content = urllib.request.urlopen(parser.image)
        f.write(content.read())
    # set the wallpaper with awesome wm method
    os.system('awsetbg ' + name)
