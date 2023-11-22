from django.utils.deprecation import MiddlewareMixin
from django.conf import settings




class CompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        company = request.headers.get('company')
        if not company:
            raise Exception('Company header is missing')
        request.company = company
