from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from django.http import HttpResponseRedirect
from django.urls import path
from .tasks import send_email

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    change_list_template = "users_list.html"

    def changelist_view(self, request, extra_context=None):
        """
        this method first process notify action. if exists do it and return back to list view. otherwise continue old method
        :param request:
        :param extra_context:
        :return:
        """
        if request.method == 'POST' and request.POST.get("notify") in ["all", "selected"]:
            if request.POST.get("notify") == "all":
                self.notify_all(request)
            else:
                self.notify_custom(request)
                # set method to get to avoid processing actions
                request.mutable = True
                request.method = 'GET'
        return super(CustomUserAdmin, self).changelist_view(request, extra_context)

    def notify_all(self, request):
        """
        get list of all email address and send email to them all
        :param request:
        :return:
        """
        email_address = list(User.objects.all().values_list('email', flat=True))
        send_email.delay('notification', 'email content', email_address)
        self.message_user(request, "all user are notified")

    def notify_custom(self, request):
        """
        process post list of users and send notification email to all of them
        :param request:
        :return:
        """
        selected_users = request.POST.getlist("_selected_action")
        email_address = User.objects.filter(pk__in=selected_users).values('email')
        send_email.delay('notification', 'email content', email_address)
        self.message_user(request, "an email notification sent to users")
