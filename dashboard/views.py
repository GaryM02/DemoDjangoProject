from django.shortcuts import render, redirect
from .models import Project
from profiles.models import Profile
from django.db.models import Q
from django.views.generic import ListView
from . import forms

# Create your views here.


class ProjectsList(ListView):
    model = Project
    template_name = 'dashboard/projects.html'
    context_object_name = 'qs'

    def get_queryset(self):

        profile = Profile.objects.get(user=self.request.user)
        
        query = self.request.GET.get('name')
        if query:
            qs = Project.objects.filter(Q(name__icontains=query) & Q(vendor=profile)|Q(client=profile))
            
            return qs
        else:
            qs = Project.objects.filter(Q(vendor=profile)|Q(client=profile))
            return qs
        # qs = Profile.objects.get_all_profiles(self.request.user)
        # print(qs[0].user.username)
        # return qs
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        context['is_empty'] = False
        
    
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True


        return context




def project_details(request, name):
    project = Project.objects.get(name=name)
    print(project)
    context={'project':project}
    return render(request, 'dashboard/viewproject.html', context)

def create_project_view(request):
    form = forms.ProjectForm()
    context = {'form':form}
    return render(request, 'dashboard/createproject.html', context)