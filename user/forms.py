from django import forms
# formlarımızı djangoda hazır bir model olan formdan türeteceğiz
from .models import Profile, User

# formlarımızı djangoda hazır bir model olan formdan türeteceğiz

class ProfileForm(forms.ModelForm):
    email=forms.EmailField(widget=forms.EmailInput())
    confirm_email=forms.EmailField(widget=forms.EmailInput())
    biografi= forms.Textarea()

    class Meta:
        model = Profile
        fields = [
            'image',
            'first_name',
            'last_name',
            'role',
            'location',            
            'birthdate',
            'education',
            'language',
            'profession',
            'phone',
            'email',
            'biography',
        ]

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        bio = cleaned_data.get("biography")

        if email != confirm_email:
            raise forms.ValidationError(
                "Emails must match!"
            )

        if len(bio) < 10:
            raise forms.ValidationError(
                "Biography must be 10 characters or longer!"
            )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length= 50, label ='User')
    password = forms.CharField(max_length= 20, label = 'Password', widget= forms.PasswordInput)
    confirm = forms.CharField(max_length= 20, label = 'Password Confirmation', widget= forms.PasswordInput)

    # password ile confirm eşleşip eşleimediğini kontrol etmek için djangonun önerdiği clean fonksiyonunu kullanacağız

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if User.objects.filter(username=username).exists():
            print("username")
            raise forms.ValidationError(u'Username "%s" is already in use!' % username)
        if password and confirm and password != confirm:
            raise forms.ValidationError('Password and confirm do not match')

        values = {
            'username': username,
            'password': password
        }
        return values


class LoginForm(forms.Form):
    username = forms.CharField(label = 'User')
    password = forms.CharField(label = 'Password', widget= forms.PasswordInput)


