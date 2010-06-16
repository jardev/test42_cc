from tests_42cc.tickets.models import HttpRequestLogEntry

class HttpRequestLoggerMiddleware:
    def process_request(self, request):
        log_entry = HttpRequestLogEntry()
        log_entry.host = request.get_host()
        log_entry.url = request.get_full_path()
        log_entry.method = request.method
        if request.user.is_authenticated():
            log_entry.user = request.user
        log_entry.save()
            
