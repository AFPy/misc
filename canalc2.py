# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from chut import console_script
from subprocess import call

event = "http://www.canalc2.tv/video.asp?idEvenement=722"
host = "http://www.canalc2.tv/"


@console_script
def canalc2(args):
    """Usage: %prog"""
    doc = pq(url=event)
    for li in doc('ul.listeProgramme li').items():
        a = li('a')
        if not a.attr.href or not a.attr.href.startswith('video'):
            continue
        url = host + a.attr.href
        conf = pq(url=url + '&voir=oui')
        title = conf('span.titreGris10:eq(1)').text()
        title = title.strip(' .!')
        author = conf('span.interBleu10:eq(1)').text()
        if author is None:
            filename = u'{0}.mp4'.format(title)
        else:
            filename = u'{0} - {1}.mp4'.format(author, title)
        mp4 = pq(
            'http://www.canalc2.tv/clientlinux.asp?' + url.split('?')[1]
        )('td.titreEmission').text()
        call('mimms -r "{0}" "{1}"'.format(mp4, filename.encode('utf8')),
             shell=True)
