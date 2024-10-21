from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse, reverse_lazy
from anon_website.forms import LoginForm, SignupForm, TryForm
from django.conf import settings
from TextAnonymisationEngine.Engine.Lang import Lang
import requests

def home_redirect_view(request):
    return redirect(reverse('anon_website:home'))

@login_required(login_url=reverse_lazy('web_auth:login'))
def anonymise_view(request):
    context = {'languages': []}
    for lang in Lang:
        context['languages'].append({"value" : lang.value, 
                                     "name" : lang.name})
    
    context['api_token'] = "f5c40137f2af0d3b7462eb20a131f7526ad9e3f1"


    return render(request, 'anon_website/anonymise.html', context=context)

def try_view(request):
    form = TryForm()
    context = {'form': form,
               'api_token': settings.API_FREE_KEY}
    
    return render(request, 'anon_website/try.html', context=context)

def home_view(request):
    return render(request, 'anon_website/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('anonymise')  # Redirect to a success page.
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    context = {'form': form,
               'link': reverse('login'),
               'title': 'Login',
               'button': 'Login',
               'show_signup': True}
    return render(request, 'anon_website/login_template.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            if password != password_confirm:
                form.add_error(None, 'Passwords do not match')
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                return redirect('login')
    elif request.method == 'GET':
        form = SignupForm()
            

    context = {'form': 'form',
                'link': reverse('signup'),
                'title': 'Sign Up',
                'button': 'Sign Up',
                'show_signup': False}
    return render(request, 'anon_website/login_template.html', context)

def finished_registration_view(request):
    return redirect(reverse('anon_website:home'))

@login_required(login_url=reverse_lazy('web_auth:login'))
def recent_view(request):
    link = settings.API_URL + 'tasks/'
    headers = {'Authorization': 'Token ' + 'f5c40137f2af0d3b7462eb20a131f7526ad9e3f1'}
    response = requests.get(link, headers=headers)
    if response.status_code == 200:
        task_data = response.json()
    else:
        task_data = []

    tasks_since_last_midnight = []

    current_time = datetime.now()
    last_midnight = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    previous_midnight = last_midnight - timedelta(days=1)

    for task in task_data:
        creation_time = datetime.strptime(task['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if creation_time > previous_midnight:
            tasks_since_last_midnight.append(task)

    tasks_parced = []
    for task in tasks_since_last_midnight:
        task_id = task.get('id')
        output_file = task.get('output_file')

        if output_file is None:
            continue

        file_id = output_file.get('id')
        file_name = output_file.get('name')
        if file_id is None or file_name is None:
            continue
        
        task_creation_time = datetime.strptime(task['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        time_delta = current_time - task_creation_time
        file_day = "Today" if time_delta.days < 1 else "Yesterday"
        file_time = task_creation_time.strftime('%H:%M')

        tasks_parced.append({'task_id': task_id,
                             'file_id': file_id,
                             'file_name': file_name,
                             'file_day': file_day,
                             'file_time': file_time})
        
    context = {'tasks': tasks_parced,
               'api_token': 'f5c40137f2af0d3b7462eb20a131f7526ad9e3f1'}
        

    
    return render(request, 'anon_website/recent.html', context=context)