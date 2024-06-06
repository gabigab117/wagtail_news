from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from account.forms import SignUpForm
from homepage.models import IndexPage


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            index = IndexPage.objects.get(slug="index")
            return redirect(index.url)
    else:
        form = SignUpForm()
    return render(request, "account/signup.html", context={"form": form})


class UserLoginView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        index = IndexPage.objects.get(slug="index")
        return index.url


@require_POST
def logout_view(request):
    logout(request)
    index = IndexPage.objects.get(slug="index")
    return redirect(index.url)
