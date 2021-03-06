from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PodEnrollForm, DiscussionForm, CommentForm
from django.views.generic.list import ListView
from pods.models import Pod, Discussion, Comment
from django.views.generic.detail import DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse 
from pods.views import PodDetailView



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
        module = Permission.objects.filter(content_type__app_label='pods',content_type__model='module')
        comment = Permission.objects.filter(content_type__app_label='pods',content_type__model='comment')
        content = Permission.objects.filter(content_type__app_label='pods',content_type__model='content')
        discussion = Permission.objects.filter(content_type__app_label='pods',content_type__model='discussion')
        file = Permission.objects.filter(content_type__app_label='pods',content_type__model='file')
        image = Permission.objects.filter(content_type__app_label='pods',content_type__model='image')
        pod = Permission.objects.filter(content_type__app_label='pods',content_type__model='pod')
        text = Permission.objects.filter(content_type__app_label='pods',content_type__model='text')
        taggittag = Permission.objects.filter(content_type__app_label='taggit',content_type__model='tag')
        taggittaggetitem = Permission.objects.filter(content_type__app_label='taggit',content_type__model='taggeditem')
        
        for i in range(4):
            user.user_permissions.add(module[i],
                                      comment[i],
                                      content[i],
                                      discussion[i],
                                      file[i],
                                      image[i],
                                      pod[i],
                                      text[i],
                                      taggittag[i],
                                      taggittaggetitem[i]      
                                        )
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
        stuff = get_object_or_404(Pod, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id):
            liked = True

        context['liked'] = liked
        context['total_likes'] = total_likes
        # get pod object
        pod = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = pod.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = pod.modules.all()[0]
        return context


class AddDiscussionView(CreateView):
    model = Discussion
    form_class = DiscussionForm
    template_name: str = "susers/pod/add_discussion.html"
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.pod_id = self.kwargs['pk']
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('suser_pod_detail',args=[self.kwargs['pk']])

class DiscussionDetailView(DetailView):
    model = Discussion
    template_name = 'susers/pod/detail_discussion.html'
##comment
    form = CommentForm

    def post(self, request,pk, *args, **kwargs):
        
        form = CommentForm(request.POST)
        
        if form.is_valid():
            discussion = self.get_object()
            form.instance.author_id = self.request.user.id
            form.instance.discussion_id = self.kwargs['pk']
            form.save()
            
            return HttpResponseRedirect(reverse("discussion_detail", args=[str(pk)]))

    def get_context_data(self, **kwargs):

        discussion_comments_count = Comment.objects.all().filter(discussion=self.object.id).count
        discussion_comments = Comment.objects.all().filter(discussion=self.object.id)
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form,
            'discussion_comments': discussion_comments,
            'discussion_comments_count': discussion_comments_count,
        })
       
        return context


    


