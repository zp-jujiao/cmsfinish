from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


# class Mymiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         url = request.path
#         if url.startswith("/admin") and not url.endswith("login/"):
#             username = request.session.get("admin")
#             if username:
#                 pass
#             else:
#                 if url!="/admin/loginHandler/":
#                     return redirect("/admin/login/")
#                 elif url=="/admin/loginHandler/" and request.POST.get("username")==None:
#                     return redirect("/admin/login/")
