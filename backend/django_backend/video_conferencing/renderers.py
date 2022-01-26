import json

from rest_framework.renderers import JSONRenderer


class ConferenceJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    
    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'conference': data,
        })


class MemberJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'member': data,
        })
    