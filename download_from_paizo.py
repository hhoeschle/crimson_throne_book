import urllib2
import urllib
from StringIO import StringIO
import gzip
import os
from bs4 import BeautifulSoup
from lxml import etree


def clean_text(text):
    if text:
        text = text.strip().replace(u'\u201c', '{\\itshape``').replace(u'\u201d', '}\'\'')
        text = text.replace(u'\u2019', '\'').replace(u'\u2018', '\'').replace(u'\u2013', '--')
        text = text.replace(u'\xe9', '\\\'e').replace(u'\u2026', '\\ldots')
        text = text.replace(u'\xef', '\\"i').replace(u'\xeb', '\\"e').replace(u'\u2014', '--')
        text = text.replace(u'\xc2', '\\S').replace(u'\xe7', '\\c{c}')
    else:
        text = ''
    return text


def get_image(url):
    name = url.split('/')[-1].split('?')[0].strip()
    img_name = os.path.join('images',  name + '.jpg').replace('\\', '/').strip()
    img_path = os.path.join(os.getcwd(), 'latex', 'images',  name + '.jpg')
    if os.path.isfile(img_path):
        print 'Image already downloaded'
        caption = open(img_path[:-4] + '.caption', 'r').readlines()[0].strip()
    else:
        print 'Get image from web'
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        html = soup.prettify("utf-8")
        html = html.replace('&', '&amp;').replace(' < ', '')
        with open('test.html', 'w') as f:
            f.write(html)
        root = etree.fromstring(html)
        print root
        print url
        expr = "//img[contains(@class,'dev-content-full')]"
        print expr
        img = root.xpath(expr)[0]
        print img, img.attrib
        urllib.urlretrieve(img.attrib['src'], img_path)
        caption = img.attrib['alt']
        print caption
        with open(img_path[:-4] + '.caption', 'w') as f:
            f.write(caption)
    print img_path, caption
    return img_name, caption.replace(' by MrVergee', '')


def transform(p):
    print "Transform", p
    res = ''
    figures = ''
    if (len(p.getchildren()) == 1 and p.getchildren()[0].tag == 'b' and p.text.strip() == ""):
        print p.getchildren()[0].tag
        print 'Found header'
        res = '\\section{{{0}}}\n\n'.format(p.getchildren()[0].text.strip())

    elif len(p.getchildren()) == 0:
        res += clean_text(p.text)
        res += '\\\\\n\n'
    else:
        res += clean_text(p.text)
        for pc in p.getchildren():
            if (pc.tag == 'a'
                    and pc.attrib['href'] != 'http://mrvergee.deviantart.com/gallery/'
                    and pc.attrib['href'] != 'http://mrvergee.deviantart.com/'
                    and 'paizo' not in pc.attrib['href']
                    and 'youtube' not in pc.attrib['href']
                    and 'wikipedia' not in pc.attrib['href']
                    and 'dropbox' not in pc.attrib['href']):
                print pc, pc.attrib, pc.text
                name, caption = get_image(pc.attrib['href'])
                print name, caption
                figures += '\\begin{figure}[h]\n'
                figures += '\t\\centering\n'
                figures += '\t\\includegraphics[width=0.4\\textwidth]{{{0}}}\n'.format(name[:-4] + '_mod.jpg')
                figures += '\t\\caption{{{0}}}\n'.format(caption)
                figures += '\t\\label{{fig:{0}}}\n'.format(name.split('/')[-1].split('.')[0])
                figures += '\\end{figure}\n\n'
                res += '\\hyperref[fig:{0}]{{ {1} }} '.format(
                    name.split('/')[-1].split('.')[0], clean_text(pc.text))
                res += clean_text(pc.tail) + ' '
            elif pc.tag == 'i':
                res += ' {\\itshape ' + clean_text(pc.text) + '} '
                res += clean_text(pc.tail) + ' '
            else:
                res += clean_text(pc.text) + ' '
    if figures != '':
        return res + '\\\\\n\n' + figures
    print res
    return res


for page in range(1, 8):
    file_name = 'html/pages_%02d.html' % page
    if os.path.isfile(file_name):
        html = open(file_name, "r").read()
    else:
        url = "http://paizo.com/threads/rzs2ps0m&page=%d" % page
        print url
        response = urllib2.urlopen(url)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            html = f.read()
        else:
            html = response.read()

        print html
        with open(file_name, 'w') as f:
            f.write(html)

    soup = BeautifulSoup(html, 'html.parser')
    html = soup.prettify("utf-8")

    with open(file_name, 'w') as f:
        f.write(html)
    # print html
    root = etree.fromstring(html)
    expr = "//div[contains(@id,'mprd_post')]"
    posts = root.xpath(expr)
    print posts, len(posts)
    count = 1
    for p in posts:
        print p, p.attrib
        time = p.xpath('.//time')[0].attrib['datetime']
        print time
        f_out = 'latex/downloaded/%s_%03d.tex' % (time[0:10], count)
        count += 1
        print f_out
        with open(f_out, 'w') as f:
            f.write('%!TEX root = ../crimson_throne_book_main.tex\n')
            f.write('% {0}\n'.format(time[0:10]))
            content = p.xpath('.//div[@class = "post-contents"]')[0]
            # print content
            for p in content.xpath('./p'):
                print p
                f.write(transform(p))
        # break
