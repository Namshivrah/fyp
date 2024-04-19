'''
from .views import get_region_from_request
from .utils import set_database_for_region
import logging

class AdminRegionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin'):
            # Extract the region from the request or user session
            region = get_region_from_request(request)

            # Use the region to set the database alias for this request
            if region is not None:
                set_database_for_region(region)

            logging.info(f"Admin request intercepted for region {region}")

        response = self.get_response(request)
        return response


    def set_database_for_region(region):
        # Implement logic to set the database alias based on the region
        # Use Django's `using` attribute to set the database alias for the request
        region = request.GET.get('region') or request.POST.get('region')

        # You can also consider extracting the region from the user session or any other source

        return region
'''