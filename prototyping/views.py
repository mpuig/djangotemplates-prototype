# Copyright (c) 2009 Shrubbery Software
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import re
import operator

from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlquote
from django.utils.safestring import mark_safe


class Template(object):

    re_template_file = re.compile('[^.].*[^~]$')
    re_title = re.compile(r'\{#\s*(?P<title>.*?)\s*(\((?P<label>[^)]+)\))?\s*#\}')

    title_getter = operator.attrgetter('title')

    def __init__(self, name, filename):
        self.name = self.title = name
        self.filename = filename
        self.label = None
        self.inspect()

    def inspect(self):
        """Retrieve title and label from the template."""
        with file(self.filename) as fp:
            first_line = fp.readline()
            match = self.re_title.match(first_line)
            if match:
                self.title = match.group('title')
                self.label = match.group('label') or None

    def __repr__(self):
        return '<Template name=%s title=%s>' % (self.name, self.title)

    @property
    def url(self):
        return '/%s' % urlquote(self.name)

    @classmethod
    def collect(cls):
        # If there is template with same name in two or more directories,
        # only include the first.
        seen = set()
        templates = []
        for template_dir in settings.TEMPLATE_DIRS:
            files = [name for name in os.listdir(template_dir) \
                     if name not in seen and \
                     cls.re_template_file.match(name) and \
                     os.path.isfile(os.path.join(template_dir, name))]
            for name in files:
                filename = os.path.join(template_dir, name)
                template = cls(name, filename)
                templates.append(template)
        #templates.sort(key=cls.title_getter)
        return templates


def process(request, template_name=None, extra_context=None,
            title=u'Prototypes'):
    """Depending on the parameters, this view either lists all
    templates, or serves the specified."""

    templates = Template.collect()
    if not template_name: # List all templates
        context = {'templates': templates, 'title': title}
        return render_to_response('prototyping/templates.html',
                    RequestContext(request, context))
    else: # Show the desired template
        for template in templates:
            if template.name == template_name:
                login = request.GET.get('login', 'false')
                url = request.META.get('PATH_INFO')
                if extra_context is None:
                    extra_context = dict()
                extra_context['return_link'] = mark_safe("""
                    <a href="/" id="back-to-templates">Back to templates</a>
                """)
                
                extra_context['login'] = login!='true'
                
                if login=='true':
                    
                    extra_context['change_login_link'] = mark_safe("""
                        <a href="%s" id="switch-login">Login</a>
                    """ % url.replace('.html', '.html?login=false'))
                else:
                    extra_context['change_login_link'] = mark_safe("""
                        <a href="%s" id="switch-login">Logout</a>
                    """ % url.replace('.html', '.html?login=true'))
                
                return render_to_response(template.name,
                            RequestContext(request, extra_context))
        raise Http404('Template not found')
