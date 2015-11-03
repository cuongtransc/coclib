#-*- coding: utf-8 -*-

# tracking: Tracking
#
# Copyright (C) 20012-2014 coclib
# Authors: Tran Huu Cuong <tranhuucuong91@gmail.com>
# URL:     http://tranhuucuong91.wordpress.com/
# License: BSD

from __future__ import print_function

import sqlite3
from . import config
from coclib.alert import send_alert

import bs4

import sys

if sys.version_info < (3, 0):
    from urllib2 import urlopen, Request
    from urlparse import urljoin
else:
    from urllib.request import urlopen, Request
    from urllib.parse import urljoin

import base64

import sys
import time

import traceback


class Tracking(object):

    """Tracking change website"""

    def __init__(self, name, url, pattern, headers={},
                 emails=['lalahahaaa@gmail.com'], time_retry=3600,
                 is_log=True, log_path='/var/log/tracking_change', is_loop=False):
        self.name = name
        self.url = url
        self.pattern = pattern
        self.headers = headers
        self.emails = emails
        self.time_retry = time_retry
        self.is_log = is_log
        self.log_path = log_path
        self.is_loop = is_loop

    def start(self):
        # Set output
        if self.is_log:
            fout = open('%s/%s.log' % (self.log_path, self.name), 'a')
        else:
            fout = sys.stdout
        # Connect to database server

        try:
            db = sqlite3.connect('%s/%s' % (config.PATH_DB, config.SQLITE3_DB),
                                 detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            db.row_factory = sqlite3.Row
            cur = db.cursor()
        except Exception as e:
            fout.write(
                '%s [ERROR] %s\n%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'),
                                         'Failed to connect to database!', e))
            fout.close()
            return 1

        # Create table
        table = 'id INTEGER PRIMARY KEY, insert_date TEXT'
        for i in self.pattern:
            table += ', %s TEXT' % i

        cur.execute("CREATE TABLE IF NOT EXISTS %s(%s)" % (self.name, table))

        # Make a request
        #rq = urllib2.Request(self.url, headers=self.headers)
        rq = Request(self.url, headers=self.headers)

        try:
            # while True:
                #html = urllib2.urlopen(rq).read()
                html = urlopen(rq).read()
                bs4html = bs4.BeautifulSoup(html)

                # tnew   :   t new
                # told   :   t old
                # tupdate:   t update

                tnew = {}
                for key in self.pattern.keys():
                    p = self.pattern[key]
                    t = bs4html.find(p['name'], p['attrs'])

                    if not t:
                        print("Don't find %s:%s." % (p['name'], p['attrs']))
                        raise Exception

                    for i in t('a'):
                        i['href'] = urljoin(self.url, i.get('href'))
                    for i in t('img'):
                        i['src'] = urljoin(self.url, i.get('src'))

                    t = unicode(t)

                    i = t.find('<script')
                    while i != -1:
                        j = t.find('</script>') + 9
                        t = t.replace(t[i:j], '')

                        i = t.find('<script')

                    tnew[key] = t

                try:
                    cur.execute(
                        'SELECT * FROM %s ORDER BY id DESC LIMIT 1' % self.name)
                    told = dict(cur.fetchone())
                except:
                    told = {}

                tupdate = {}
                for key in self.pattern:
                    if base64.decodestring(told.get(key, '')).decode('utf-8') != tnew.get(key):
                        tupdate[key] = tnew.get(key)

                if tupdate != {}:
                    # send email alert
                    content = u''
                    for key in tupdate:
                        content += '------- %s -------\n%s\n\n' % (
                            key, tupdate[key])

                    fout.write('%s %s\n' % (
                        time.strftime('%Y-%m-%d %H:%M:%S'), "Have a update!"))
                    for email in self.emails:
                        send_alert('%s update!' % (
                            self.name), content, email)

                    # update database
                    # tnew['insert_date'] = datetime.datetime.now()
                    cur.execute(
                        '''INSERT INTO %s(%s, insert_date) VALUES('%s','%s')'''
                        % (self.name, ','.join(tnew.keys()),
                            "', '".join([base64.encodestring(i.encode('utf-8'))
                                        for i in tnew.values()]),
                           time.strftime('%Y-%m-%d %H:%M:%S')))
                    db.commit()
                else:
                    fout.write('%s %s\n' % (
                        time.strftime('%Y-%m-%d %H:%M:%S'), 'Have not update!'))

                # if not self.is_loop:
                #     break

                # time.sleep(self.time_retry)

        except Exception as e:
            print(e)
            for filename, lineno, function, text in traceback.extract_tb(sys.exc_info()[2]):
                print(filename, lineno, function, text)
        finally:
            fout.close()

    def stop(self):
        pass
