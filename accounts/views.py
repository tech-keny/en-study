from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from accounts.forms import ProfileForm, SignupUserForm
from django.shortcuts import render, redirect
from allauth.account import views
from app.models import Post





class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        post_data = Post.objects.filter(author=request.user)
        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'post_data': post_data
        })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'name': user_data.name,
                'department': user_data.department,
                'image': user_data.icon
            }
        )

        return render(request, 'accounts/profile_edit.html', {
            'form': form,
            'user_data': user_data
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.name = form.cleaned_data['name']
            user_data.department = form.cleaned_data['department']
            if request.FILES.get('icon'):
                user_data.icon = request.FILES.get('icon') #追加
            user_data.save()
            return redirect('profile')

        return render(request, 'accounts/profile.html', {
            'form': form
        })


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'

class LogoutView(views.LogoutView):
    template_name = 'accounts/logout.html'

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class SignupView(views.SignupView):
    template_name = 'accounts/signup.html'
    form_class = SignupUserForm


