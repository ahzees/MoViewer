from authentication.models import SEX, CustomUser
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email")
    password = forms.CharField(
        max_length=90, label="Password", widget=forms.PasswordInput()
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password", "sex"]
        widgets = {
            "password": forms.PasswordInput(
                attrs={"label": "password", "placeholder": "Password"}
            ),
            "email": forms.EmailInput(attrs={"label": "Email", "placeholder": "Email"}),
            "first_name": forms.TextInput(
                attrs={"label": "First Name", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"label": "Last Name", "placeholder": "Last Name"}
            ),
        }

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ChangeUserForm(forms.Form):
    first_name = forms.CharField(max_length=99, required=False)
    last_name = forms.CharField(max_length=99, required=False)
    sex = forms.ChoiceField(choices=SEX, required=False)
    image = forms.FileField(required=False)
