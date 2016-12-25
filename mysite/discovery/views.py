from django.shortcuts import render
from django.views import generic
from django.db.models.query_utils import Q
from .models import Project, Dataset


class ProjectsView(generic.ListView):
    template_name = 'discovery/projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(generic.DetailView):
    template_name = 'discovery/project.html'
    model = Project


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
        # else:
        #     return render(request, 'discovery/projects.html', {
        #         'projects': projects,
        #     })

