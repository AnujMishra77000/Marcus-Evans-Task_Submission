from django.http import JsonResponse
from django.conf import settings
import logging


logger = logging.getLogger(__name__)



class MaintananceMiddleware:
    ERROR_THRESHOLD = 5
    error_count = 0
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if getattr(settings,"MAINTENANCE_MODE", False):
          return JsonResponse({"error": "site is under maintenance. Please try again later."}, status=503)          
        
        response = self.get_response(request)

        if response.status_code >= 400:
            self.error_count +=1
            logger.error(f"API Error Detected! Count: {self.error_count}")

            if self.error_count >= self.ERROR_THRESHOLD:
                settings.MAINTENANCE_MODE = True
                logger.critical("Maintenance mode activate due to repeated errors!")
        else:
            self.error_count= 0

        return response                         