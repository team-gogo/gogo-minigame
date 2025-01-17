from django.http import JsonResponse


# MiniGame 서비스의 /minigame 프리픽스를 제거하는 미들웨어
class MiniGamePathPrefixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        prefix = '/minigame'

        if request.path.startswith(prefix):
            request.path_info = request.path[len(prefix):]
        
        return self.get_response(request)


# Health Check 미들웨어
class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info == '/health':
            return JsonResponse('GOGO MiniGame Service OK', safe=False)
        return self.get_response(request)