from django.shortcuts import render
from django.views import generic
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login, logout
from .models import Project, Dataset
from .forms import UserForm
from .models import AQI
from django.http import HttpResponse


def load_aqi(request):
    aqi = AQI()
    df = aqi.load_aqi()
    return HttpResponse(df.dtypes)


def save_aqi(request):
    aqi = AQI()
    aqi.save_aqi()
    return HttpResponse('Saved')


class ProjectsView(generic.ListView):
    template_name = 'discovery/projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(generic.DetailView):
    template_name = 'discovery/project.html'
    model = Project


class DatasetView(generic.DetailView):
    model =Dataset


def datasets(request):
    if not request.user.is_authenticated():
        return render(request, 'discovery/login.html')
    else:
        # aqi = AQI()
        # dss = aqi.load_aqi().collect()
        # dataset_list = [ds.asDict() for ds in dss]
        dataset_list = Dataset.objects.filter(user=request.user)
        return render(request, 'discovery/datasets.html', {
            'datasets': dataset_list,
        })


def projects(request):
    if not request.user.is_authenticated():
        return render(request, 'discovery/login.html')
    else:
        project_list = Project.objects.filter(user=request.user)
        query = request.GET.get('q')
        if query:
            project_list = project_list.filter(Q(name__icontains=query)).distinct()
            return render(request, 'discovery/projects.html', {
                'projects': project_list,
            })
        else:
            return render(request, 'discovery/projects.html', {
                'projects': project_list,
            })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                project_list = Project.objects.filter(user=request.user)
                return render(request, 'discovery/projects.html', {'projects': project_list})
            else:
                return render(request, 'discovery/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'discovery/login.html', {'error_message': 'Invalid login'})
    return render(request, 'discovery/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                project_list = Project.objects.filter(user=request.user)
                return render(request, 'discovery/index.html', {'projects': project_list})
    context = {
        "form": form,
    }
    return render(request, 'discovery/register.html', context)


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'discovery/login.html', context)
