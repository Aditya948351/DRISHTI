from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm

class CustomLoginView(LoginView):
    template_name = 'PublicPages/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.role == 'citizen':
            return reverse_lazy('citizen_dashboard')
        elif user.role == 'officer':
            return reverse_lazy('officer_dashboard')
        elif user.role == 'dept_admin':
            return reverse_lazy('dept_dashboard')
        elif user.role == 'city_admin':
            return reverse_lazy('state_dashboard')
        elif user.role == 'super_admin':
            return reverse_lazy('national_dashboard')
        return reverse_lazy('home')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect based on role
            if user.role == 'citizen':
                return redirect('citizen_dashboard')
            elif user.role == 'officer':
                return redirect('officer_dashboard')
            elif user.role == 'dept_admin':
                return redirect('dept_dashboard')
            elif user.role == 'city_admin':
                return redirect('state_dashboard')
            elif user.role == 'super_admin':
                return redirect('national_dashboard')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'PublicPages/register.html', {'form': form})
