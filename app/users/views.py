# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from django.http import HttpResponse


class Users(View):
    testMessage = "this is a test"

    def get(self, request):
        return HttpResponse(self.testMessage)
