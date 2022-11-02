from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout

from accounts.models import User
from accounts.views import email_validation, login_user, account


class CheckEmailValidatedMiddleware(MiddlewareMixin):
    '''
    This middleware will check User Account Email Verifcation .
    '''

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
            if not request.path.startswith('/verify/email/') and not request.path.startswith('/resend-email/'):
                if request.path == reverse("logout"):
                    return
                print(view_func.__name__)
                print(login_user.__name__)
                if view_func.__name__ == login_user.__name__:
                    print('llllllllll')
                    return redirect("/")

                if view_func.__name__ == account.__name__  and not request.user.is_email_verified:
                    return redirect(reverse("email_validation"))
