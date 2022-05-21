from multiprocessing import context
from django.shortcuts import render
from .models import Pod, Discussion, Module, Content
from django.urls import reverse_lazy, reverse 
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from .forms import ModuleFormSet
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.views.generic.detail import DetailView
from susers.forms import PodEnrollForm
from django.http import HttpResponseRedirect


def LikeView(request, pk):
    pod = get_object_or_404(Pod, id=request.POST.get('pod_id'))
    liked= False
    if pod.likes.filter(id=request.user.id).exists():
        pod.likes.remove(request.user)
        liked= False
    else:    
        pod.likes.add(request.user)
        liked= True

    return HttpResponseRedirect(reverse('suser_pod_detail', args=[str(pk)]))


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerPodMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Pod
    fields = ['tags','title', 'file', 'slug', 'overview', ]
    success_url = reverse_lazy('manage_pod_list')

class OwnerPodEditMixin(OwnerPodMixin, OwnerEditMixin):
    template_name = 'pods/manage/pod/form.html'

class ManagePodListView(OwnerPodMixin, ListView):
    template_name = 'pods/manage/pod/list.html'
    permission_required = 'pods.view_pod'

class PodCreateView(OwnerPodEditMixin, CreateView):
    permission_required = 'pods.add_pod'
    pass

class PodUpdateView(OwnerPodEditMixin, UpdateView):
    permission_required = 'pods.change_pod'
    pass

class PodDeleteView(OwnerPodMixin, DeleteView):
    template_name = 'pods/manage/pod/delete.html'
    permission_required = 'pods.delete_pod'


#module addition and edit view
class PodModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'pods/manage/module/formset.html'
    pod = None

    def get_formset(self, data=None):
 
        return ModuleFormSet(instance=self.pod, data=data)
    
    def dispatch(self, request, pk):

        self.pod = get_object_or_404(Pod,id=pk,owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        
        formset = self.get_formset()
        return self.render_to_response({'pod': self.pod,'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_pod_list')
        return self.render_to_response({'pod': self.pod,'formset': formset})


#Content addition to modules
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'pods/manage/content/form.html'

    #checking the model name(text, video, image, file)
    def get_model(self, model_name):
        
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='pods',model_name=model_name)
        return None
    #building a dynamic form
    def get_form(self, model, *args, **kwargs):

        Form = modelform_factory(model, exclude=['owner','order','created','updated'])
        return Form(*args, **kwargs)

    #receives URL parameters and stores the corresponding module,model,content as class attributes
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,id=module_id,pod__owner=request.user)

        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,id=id,owner=request.user)
        
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,instance=self.obj,data=request.POST,files=request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,item=obj)

            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,'object': self.obj})

#for deleting contents
class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,id=id,module__pod__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'pods/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,id=module_id,pod__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin,
    JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, pod__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class ContentOrderView(CsrfExemptMixin,
    JsonRequestResponseMixin,View):
    
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__pod__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

#for viewing pods

class PodListView(TagMixin, ListView):
    model = Pod
    template_name = 'pods/pod/list.html'
    queryset= Pod.objects.all()
    context_object_name = 'pods'

class TagListView(TagMixin, ListView):
    model = Pod
    template_name = 'pods/pod/list.html'
    context_object_name = 'pods'

    def get_queryset(self):
        return Pod.objects.filter(tags__slug=self.kwargs.get('tag_slug'))
    

class PodDetailView(DetailView):
    model = Pod
    template_name = 'pods/pod/detail.html'
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Pod, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        context['enroll_form'] = PodEnrollForm(initial={'pod':self.object})
        context['total_likes'] = total_likes
        
        return context

## Search Function


    
def search_pods(request):

    if request.method == "POST":
        searched = request.POST['searched']
        pods = Pod.objects.filter(title__contains = searched)
        return render(request, 
        'pods/search_pods.html', 
        {'searched' : searched, 'pods': pods})
    
    else:
        return render(request, 'pods/search_pods.html', {})

