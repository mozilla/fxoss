class XForwardedForMiddleware():
    def process_request(self, request):
        if "HTTP_X_FORWARDED_FOR" in request.META.keys():
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]
