#!/usr/bin/env python

import requests
import json


BASE_URL = 'http://www.browserstack.com/screenshots'


class Screenshot(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def request(self, url=None, params=None, method='get'):
        if url:
            url = '%s/%s' % (BASE_URL, url)
        else:
            url = BASE_URL
        func = getattr(requests, method)
        headers = {}
        if method == 'post':
            headers = {'content-type': 'application/json'}
        r = func(
            url=url, data=json.dumps(params),
            auth=(self.username, self.password), headers=headers)
        if r.status_code == 200:
            return r.json()
        raise Exception(r.text)

    def get_browsers(self):
        """Get the list of available OS and browsers
        """
        url = 'browsers.json'
        return self.request(url)

    def add_screenshot(self, url, **kw):
        """Generate screenshots for a URL
        """
        params = {
            'url': url,
        }
        for k, v in kw.items():
            params[k] = v
        return self.request(params=params, method='post')

    def get_screenshot(self, job_id):
        """Get the status and data about the given job_id
        """
        url = '%s.json' % job_id
        return self.request(url)


def screenshot_to_html(response):
    """Generate a HTML page from the browserstack response

    It can be usefull to the hook script called by the callback
    """
    html = ['<html><body>']
    screenshots = response.pop('screenshots')
    html += ['<ul>']
    for k, v in response.items():
        html += ['<li>%s: %s</li>' % (k, v)]
    html += ['</ul>']
    for screenshot in screenshots:
        keys = screenshot.keys()
        html += ['<ul>']
        for k in keys:
            html += ['<li>%s: %s</li>' % (k, screenshot[k])]
        html += ['</ul>']
        if 'image_url' in screenshot:
            html += ['<img src="%s" />' % screenshot['image_url']]
    html += ['<br /><br />']
    html += ['</body></html>']
    return ''.join(html)
