from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course
from django.views.generic.detail import DetailView


class SuserRegistrationView(CreateView):
    template_name = 'susers/suser/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('suser_course_list')
    
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],password=cd['password1'])
        login(self.request, user)
        return result

class SuserEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.susers.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('suser_course_detail',args=[self.course.id])

class SuserCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'susers/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(susers__in=[self.request.user])

class SuserCourseDetailView(DetailView):
    model = Course
    template_name = 'susers/course/detail.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(susers__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context