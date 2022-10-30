from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.


# Authentication verifies a user is who they claim to be.
# Authorization determines what an authenticated user is allowed to do.
class IndexView(generic.TemplateView):
    template_name = "playground/auth/index.html"


class UsersIndexView(generic.TemplateView):
    template_name = "playground/auth/users/index.html"
    extra_context = {"users_context": {}}

    def get(self, request, *args, **kwargs):
        self.extra_context["users_context"].update({
            "users": User.objects.all(),
            "settings": self._get_settings()
        })

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        extra_context = {}

        created_user = self._create_user(request)
        extra_context.update({
            "created_user": created_user
        })

        self.extra_context["users_context"].update(extra_context)

        return redirect('playground:auth-users')

    def _create_user(self, request):
        user_details = {
            "username": request.POST["username"],
            "email": request.POST["email"] if "email" in request.POST else None,
            "password": request.POST["password"],
            "first_name": request.POST["first-name"] if "first-name" in request.POST else None,
            "last_name": request.POST["last-name"] if "last-name" in request.POST else None,
            "is_staff": True if "is-staff" in request.POST and request.POST["is-staff"] == "on" else False
        }

        return User.objects.create_user(**user_details)

    def _get_settings(self):
        return {
            "KEY": "VALUE"
        }


class UserPasswordView(generic.DetailView):
    model = User

    def post(self, request, *args, **kwargs):
        extra_context = {}
        user = self.get_object()

        current_password = request.POST['current-password']
        new_password = request.POST['new-password']

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            extra_context.update({
                "update_password": {"status": "set new password"}
            })
        else:
            extra_context.update({
                "update_password": {"status": "invalid current password"}
            })

        request.session["users_context"] = extra_context

        return redirect('playground:auth-user', user.pk)


class UserView(generic.DetailView):
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
    template_name = "playground/auth/users/user.html"
    extra_context = {"users_context": {}}

    def get(self, request, *args, **kwargs):
        if 'users_context' in request.session:
            self.extra_context["users_context"].update(request.session['users_context'])
            del request.session['users_context']
        else:
            self.extra_context["users_context"]["update_password"]["status"].clear()

        return super().get(request, *args, **kwargs)


class UserDeleteConfirmView(generic.DeleteView):
    model = User
    success_url = reverse_lazy('playground:auth-users')
