from django import forms
# formlarımızı djangoda hazır bir model olan formdan türeteceğiz

class RegisterForm(forms.Form):
    username = forms.CharField(max_length= 50, label ='User')
    password = forms.CharField(max_length= 20, label = 'Password', widget= forms.PasswordInput)
    confirm = forms.CharField(max_length= 20, label = 'Password Confirmation', widget= forms.PasswordInput)

# password ile confirm eşleşip eşleimediğini kontrol etmek için djangonun önerdiği clean fonksiyonunu kullanacağız

def clean(self):
    username = self.cleaned_data.get('username')
    password = self.cleaned_data.get('password')
    confirm = self.cleaned_data.get('confirm')

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


