from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def homepage(request):
    return render(request, 'index.html')
