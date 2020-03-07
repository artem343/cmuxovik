from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, AuthorUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Hello {username}, your account has been created! You can now log in.')
            return redirect('login')
        else:
            pass
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        a_form = AuthorUpdateForm(request.POST,
                                  request.FILES,
                                  instance=request.user.author)
        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(
                request, f'{request.user.username}, your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AuthorUpdateForm(instance=request.user.author)

    context = {
        'u_form': u_form,
        'a_form': a_form
    }
    return render(request, 'users/profile.html', context)
