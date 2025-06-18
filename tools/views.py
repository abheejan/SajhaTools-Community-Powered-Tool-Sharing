from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Tool
from .forms import ToolForm

class ToolListView(ListView):
    model = Tool
    template_name = 'tools/tool_list.html' 
    context_object_name = 'tools'
    ordering = ['-availability_status', '-posted_time']


class ToolDetailView(DetailView):
    model = Tool
    template_name = 'tools/tool_detail.html' 
    context_object_name = 'tool'


class ToolCreateView(LoginRequiredMixin, CreateView):
    """View for users to post a new tool."""
    model = Tool
    form_class = ToolForm
    template_name = 'tools/tool_form.html' 

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ToolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for tool owners to update their tool listing."""
    model = Tool
    form_class = ToolForm
    template_name = 'tools/tool_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Ensure the user trying to update the tool is the owner."""
        tool = self.get_object()
        return self.request.user == tool.owner


class ToolDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for tool owners to delete their tool listing."""
    model = Tool
    template_name = 'tools/tool_confirm_delete.html' 
    success_url = reverse_lazy('tool-list')

    def test_func(self):
        """Ensure the user trying to delete the tool is the owner."""
        tool = self.get_object()
        return self.request.user == tool.owner