from django.conf import global_settings
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.views import generic, View


# Create your views here.


# Django provides full support for anonymous sessions.
# It stores data on the server side and abstracts the sending and receiving of cookies.
# To use cookies-based sessions, set the SESSION_ENGINE setting
# to "django.contrib.sessions.backends.signed_cookies".
class IndexView(generic.TemplateView):
    template_name = "playground/sessions.html"
    extra_context = {"session": {}}

    def get(self, request, *args, **kwargs):
        if Session.objects.filter(session_key=request.session.session_key).exists():
            model = Session.objects.get(session_key=request.session.session_key)
        else:
            model = ""

        self.extra_context["session"].update({
            "model": model,
            "object": request.session,
            "dict": dict(request.session),
            "settings": self._get_settings()
        })

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        extra_session_context = {}

        set_item_key, set_item_value = request.POST.get("set-item-key"), request.POST.get("set-item-value")

        if set_item_key and set_item_value:
            request.session[set_item_key] = set_item_value

        get_item_key = request.POST.get("get-item-key")

        if get_item_key:
            get_item_value = request.session[get_item_key]
            extra_session_context.update({
                "get_item": {"key": get_item_key, "value": get_item_value}
            })
        else:
            extra_session_context.update({
                "get_item": {"key": "", "value": ""}
            })

        delete_item_key = request.POST.get("delete-item-key")

        if delete_item_key:
            del request.session[delete_item_key]
            extra_session_context.update({
                "delete_item": {"status": f"deleted {delete_item_key}"}
            })
        else:
            extra_session_context.update({
                "delete_item": {"status": ""}
            })

        set_expiry_value = request.POST.get("set-expiry-value")

        if set_expiry_value:
            if set_expiry_value.isdigit():
                set_expiry_value = int(set_expiry_value)
            request.session.set_expiry(set_expiry_value)

        self.extra_context["session"].update(extra_session_context)

        return self.get(request, *args, **kwargs)

    def _get_settings(self):
        return {
            "SESSION_CACHE_ALIAS": global_settings.SESSION_CACHE_ALIAS,
            "SESSION_COOKIE_AGE": global_settings.SESSION_COOKIE_AGE,
            "SESSION_COOKIE_DOMAIN": global_settings.SESSION_COOKIE_DOMAIN,
            "SESSION_COOKIE_HTTPONLY": global_settings.SESSION_COOKIE_HTTPONLY,
            "SESSION_COOKIE_NAME": global_settings.SESSION_COOKIE_NAME,
            "SESSION_COOKIE_PATH": global_settings.SESSION_COOKIE_PATH,
            "SESSION_COOKIE_SAMESITE": global_settings.SESSION_COOKIE_SAMESITE,
            "SESSION_COOKIE_SECURE": global_settings.SESSION_COOKIE_SECURE,
            "SESSION_ENGINE": global_settings.SESSION_ENGINE,
            "SESSION_EXPIRE_AT_BROWSER_CLOSE": global_settings.SESSION_EXPIRE_AT_BROWSER_CLOSE,
            "SESSION_FILE_PATH (default: tempfile.gettempdir())": global_settings.SESSION_FILE_PATH,
            "SESSION_SAVE_EVERY_REQUEST": global_settings.SESSION_SAVE_EVERY_REQUEST,
            "SESSION_SERIALIZER": global_settings.SESSION_SERIALIZER
        }


class ClearView(View):
    def post(self, request):
        request.session.clear()

        return redirect('playground:sessions')


class FlushView(View):
    def post(self, request):
        request.session.flush()

        return redirect('playground:sessions')


class TestCookieView(View):
    def post(self, request):
        if "set-test-cookie" in request.POST:
            request.session.set_test_cookie()
        elif "delete-test-cookie" in request.POST:
            request.session.delete_test_cookie()

        return redirect('playground:sessions')


class ClearExpiredView(View):
    # Django does not provide automatic purging of expired sessions.
    # Therefore, it’s your job to purge expired sessions on a regular basis.
    # Django provides a clean-up management command for this purpose: clearsessions.
    # It’s recommended to call this command on a regular basis, for example as a daily cron job.
    def post(self, request):
        request.session.clear_expired()

        return redirect('playground:sessions')


class CycleKeyView(View):
    def post(self, request):
        request.session.cycle_key()

        return redirect('playground:sessions')


class ModifiedView(View):
    def post(self, request):
        request.session.modified = True

        return redirect('playground:sessions')
