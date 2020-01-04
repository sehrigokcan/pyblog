from django.shortcuts import render, redirect,get_object_or_404
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

@login_required(login_url="user:login")
def profile(request):
    """Display User Profile"""
    profile = request.user.profile
    return render(request, 'profile.html', {
        'profile': profile
    })


@ login_required(login_url="user:login")
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        messages.success(request, "Updated the Profile Successfully!")
        return redirect('user:profile')

    return render(request, 'edit_profile.html', {
        'form': form,
        'profile': profile
    })



def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid(): 
        # bu method forms.py'deki clean fonksiyonunu çağırıyor. Eğer sorgulama doğru ise TRUE yanlış ise FALSE döndürüyor.
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
            # forms.py'den verileri alıyoruz
        
        newUser = User(username = username)
            # user modelden obje oluşturuyoruz.
        newUser.set_password(password)
            # passwordü şifreliyoruz
        newUser.save()
            # yeni kullanıcıyı kaydediyoruz
        login(request, newUser)
            # Kaydedilen yeni kullanıcıyı login yapıyoruz
        messages.info(request,'You have successfully registered.')
            # success-->yeşil bir bar içinde uyarı
            # warning-->kırmızı bir bar içinde uyarı

        return redirect('index') 
            # path('', views.index, name='index') urls.py(article) index'e redirect yaptık.
   
    context = {
        'form': form
    }
     # eğer if sorgusu FALSE ise form aynı sayfada yeniden görüntülenecek
    return render(request, 'register.html', context)

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        'form' : form
    }

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username = username , password = password)
            # bir değişkene atama yaptık ve bu veriler databasede kayıtlımı diye sorgulanıyor.

        if user is None:
            messages.info(request, 'Invalid user name or password')
            return render(request, 'loginuser.html', context)
                # giriş başarısız, tekrar login sayfasına döndürdü
     
        messages.success(request, username.capitalize()+', login successful')
            # if bloğuna girmedi yani giriş başarılı

        login(request, user)
            # user değişkenine atanan veriler ile login fonk. sayesinde giriş yapıldı

        return redirect('index')
            # giriş başarılı ana sayfaya yönlendiriliyor

    return render(request, 'loginuser.html', context)
        # 54. stır ile aynı durum. bu bölümde if sorgusu başarlı durum için kurgulanıp else durumu olarak bu satır alınabilir

def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('index')

