from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def logging_out(request):
    return render(
        request,
        'users/logout.html'
    )

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("forum:post_feed")
    else:
        form = UserCreationForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form
        }
    )
