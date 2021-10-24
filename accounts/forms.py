from django import forms
from allauth.account.forms import SignupForm # 追加


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='ニックネーム')
    department = forms.CharField(max_length=30, label='所属', required=False)
    icon = forms.ImageField(label='イメージ画像', required=False)

class SignupUserForm(SignupForm):
    name = forms.CharField(max_length=30, label='ニックネーム')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user