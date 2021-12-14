from django import forms
from allauth.account.forms import SignupForm # 追加
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Ocupation


class ProfileForm(forms.Form):
    name = forms.CharField(max_length=30, label='ニックネーム')
    max_listening = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(495)], label='ベストリスニングスコア')
    max_reading = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(495)], label='ベストリーディングスコア')
    first_listening = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(495)], label='最初のリスニングスコア')
    first_reading = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(495)], label='最初のリーディングスコア')
    ocupation_data = Ocupation.objects.all()
    ocupation_choice = {}
    for ocupation in ocupation_data:
        ocupation_choice[ocupation] = ocupation
    ocupation = forms.ChoiceField(label='職業', widget=forms.Select, choices=list(ocupation_choice.items()))
    content = forms.CharField(widget=forms.Textarea(),label='自己紹介')
    icon = forms.ImageField(label='イメージ画像', required=False)

class SignupUserForm(SignupForm):
    name = forms.CharField(max_length=30, label='ニックネーム')

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user