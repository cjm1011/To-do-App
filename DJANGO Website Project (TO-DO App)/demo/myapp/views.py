from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Tasks
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'myapp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args, **kwargs)

    
class TaskList(LoginRequiredMixin, ListView):
    model = Tasks
    context_object_name ='Tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tasks'] = context ['Tasks'].filter(user=self.request.user)
        context['count'] = context ['Tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('Search-area') or ''
        if search_input:
            context['Tasks'] = context['Tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Tasks
    context_object_name = 'Task'
    template_name ="myapp/tasks.html"

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Tasks
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')  # return to the list

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Tasks
    fields=['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Tasks
    context_object_name = 'Task'
    success_url = reverse_lazy('tasks')

