from django.shortcuts import render
from .forms import MemberForm

def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()  
    else:
        form = MemberForm()

    return render(request, 'members/form.html', {'form': form})
