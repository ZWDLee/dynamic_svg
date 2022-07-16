from rest_framework.renderers import JSONRenderer

class custom_renderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            if isinstance(data, dict):
                msg = data.pop('message', '请求成功')
                code = data.pop('code', renderer_context['response'].status_code)
            else:
                msg = '请求成功'
                code = renderer_context['response'].status_code
            ret = {
                'msg': msg,
                'code': code,
                'data': data
            }

            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)