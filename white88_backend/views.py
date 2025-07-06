from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Chào mừng đến với White88 API!",
        "api_endpoints": [
            "/api/taixiu/",
            "/api/bongda/",
            "/api/lode/"
        ]
    }) 