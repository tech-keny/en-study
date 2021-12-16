from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser, Ocupation
from accounts.forms import ProfileForm, SignupUserForm
from django.shortcuts import render, redirect
from allauth.account import views
from app.models import Post





class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id )
        post_data = Post.objects.filter(author=request.user).order_by('-created')
        max_total = user_data.max_listening + user_data.max_reading
        first_total = user_data.first_listening + user_data.first_reading
        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'post_data': post_data,
            'max_total':max_total,
            'first_total':first_total
        })
class PostProfileView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user_data = CustomUser.objects.get(id=self.kwargs['pk'])
        post_data = Post.objects.filter(author=user_data).order_by('-created')
        max_total = user_data.max_listening + user_data.max_reading
        first_total = user_data.first_listening + user_data.first_reading
        return render(request, 'accounts/profile.html', {
            'user_data': user_data,
            'post_data': post_data,
            'max_total':max_total,
            'first_total':first_total
        })



class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'name': user_data.name,
                'max_listening': user_data.max_listening,
                'max_reading': user_data.max_reading,
                'first_listening': user_data.first_listening,
                'first_reading': user_data.first_reading,
                'ocupation': user_data.ocupation,
                'content': user_data.content,
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
            user_data.max_listening = form.cleaned_data['max_listening']
            user_data.max_reading = form.cleaned_data['max_reading']
            user_data.first_listening = form.cleaned_data['first_listening']
            user_data.first_reading = form.cleaned_data['first_reading']
            ocupation = form.cleaned_data['ocupation']
            ocupation_data = Ocupation.objects.get(name=ocupation)
            user_data.ocupation = ocupation_data
            user_data.content = form.cleaned_data['content']
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


