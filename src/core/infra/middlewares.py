from django.http import JsonResponse


# Health Check 미들웨어
class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path_info == '/minigame/health':
            return JsonResponse('GOGO MiniGame Service OK', safe=False)
        return self.get_response(request)