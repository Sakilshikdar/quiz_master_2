
from django.shortcuts import render, redirect
from .import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
# Create your views here.
from django.urls import reverse_lazy
# from car.models import Post
from django.contrib.auth.models import User


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def register(request):
    if request.method == "POST":
        signup_form = forms.RegistrationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            confirm_link = f"https://quiz-master-7or3.onrender.com/author/login/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string(
                'confirm_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return redirect('check')
    else:
        signup_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form': signup_form, 'type': 'Register'})


def checkmail(request):

    message = "Check your mail for confirmation"
    return render(request, 'check.html', {'message': message})


class LoginView(LoginView):
    template_name = 'register.html'

    def get_success_url(self):
        return reverse_lazy('homepage')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successful')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Logged information is incorrect')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context


@login_required
def profile(request):
    return render(request, 'profile.html', {'type': 'Profile'})


def user_logout(request):
    logout(request)
    return redirect('user_login')


@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_form = forms.changeUserForm(
            request.POST, instance=request.user)
        if profile_form.is_valid():
            # data = Post.objects.filter(author=request.user)
            profile_form.save()
            messages.success(request, 'profile update successfully')
            return redirect('profile')
    else:
        profile_form = forms.changeUserForm(instance=request.user)
    return render(request, 'update_profile.html', {'data': profile_form, })


def change_pass(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Password changed successfully')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_pass.html', {'data': form, })
