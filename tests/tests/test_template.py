# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jinja2 import Environment, PackageLoader

from django.template import Template, Context
from django.test import TestCase

from pipeline.jinja2.ext import PipelineExtension

from tests.utils import pipeline_settings


class JinjaTest(TestCase):
    def setUp(self):
        self.env = Environment(extensions=[PipelineExtension], loader=
            PackageLoader('pipeline', 'templates'))

    def test_no_package(self):
        template = self.env.from_string(u"""{% compressed_css "unknow" %}""")
        self.assertEqual(u'', template.render())
        template = self.env.from_string(u"""{% compressed_js "unknow" %}""")
        self.assertEqual(u'', template.render())

    def test_package_css(self):
        template = self.env.from_string(u"""{% compressed_css "screen" %}""")
        self.assertEqual(u'<link href="/static/screen.css" rel="stylesheet" type="text/css" />', template.render())

    def test_package_css_disabled(self):
        with pipeline_settings(PIPELINE_ENABLED=False):
            template = self.env.from_string(u"""{% compressed_css "screen" %}""")
            self.assertEqual(u'''<link href="/static/pipeline/css/first.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/second.css" rel="stylesheet" type="text/css" />
<link href="/static/pipeline/css/urls.css" rel="stylesheet" type="text/css" />''', template.render())

    def test_package_js(self):
        template = self.env.from_string(u"""{% compressed_js "scripts" %}""")
        self.assertEqual(u'<script   type="text/css" src="/static/scripts.css" charset="utf-8"></script>', template.render())


class DjangoTest(TestCase):
    def render_template(self, template):
        return Template(template).render(Context())

    def test_compressed_empty(self):
        rendered = self.render_template(u"""{% load compressed %}{% compressed_css "unknow" %}""")
        self.assertEqual(u"", rendered)

    def test_compressed_css(self):
        rendered = self.render_template(u"""{% load compressed %}{% compressed_css "screen" %}""")
        self.assertEqual(u'<link href="/static/screen.css" rel="stylesheet" type="text/css" />', rendered)

    def test_compressed_js(self):
        rendered = self.render_template(u"""{% load compressed %}{% compressed_js "scripts" %}""")
        self.assertEqual(u'<script   type="text/css" src="/static/scripts.css" charset="utf-8"></script>', rendered)
