from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PodEnrollForm
from django.views.generic.list import ListView
from pods.models import Pod
from django.views.generic.detail import DetailView
##
from django.contrib.auth.models import Permission, User
from django.contrib.auth import get_user_model



class SuserRegistrationView(CreateView):
    template_name = 'susers/suser/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('suser_pod_list')
    
    
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        
        login(self.request, user)
        # bunu kullan
        permission = Permission.objects.filter(content_type__app_label='pods',content_type__model='module')
        user.user_permissions.add(permission[1])
        user.user_permissions.add(permission[2])
        user.user_permissions.add(permission[3])
        #
        return result


        

class SuserEnrollPodView(LoginRequiredMixin, FormView):
    pod = None
    form_class = PodEnrollForm

    def form_valid(self, form):
        self.pod = form.cleaned_data['pod']
        self.pod.susers.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('suser_pod_detail',args=[self.pod.id])

class SuserPodListView(LoginRequiredMixin, ListView):
    model = Pod
    template_name = 'susers/pod/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(susers__in=[self.request.user])

class SuserPodDetailView(DetailView):
    model = Pod
    template_name = 'susers/pod/detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(susers__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get pod object
        pod = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = pod.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = pod.modules.all()[0]
        return context