from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Cmux
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages


def home(request):
    cmuxes = Cmux.objects.all()

    return render(request, 'cmuxovik/home.html')


class CmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/home.html'
    context_object_name = 'cmuxes'
    ordering = ['-ratings__average', '-created_at']
    paginate_by = 5


class UserCmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/user_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-ratings__average', '-created_at']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Cmux.objects.filter(author=user.author).order_by('-ratings__average', '-created_at')


class UnapprovedCmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/unapproved_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        return Cmux.objects.filter(is_approved=False).order_by('-created_at')


class CmuxDetailView(DetailView):
    model = Cmux


class CmuxCreateView(LoginRequiredMixin, CreateView):
    model = Cmux
    fields = ['text', 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class CmuxUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cmux
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

    def test_func(self):
        cmux = self.get_object()
        is_author = self.request.user.author == cmux.author
        is_moderator = self.request.user.author.is_moderator
        post_is_new = not cmux.is_approved
        if is_author and post_is_new:
            return True
        return False


class CmuxDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cmux
    success_url = '/'

    def test_func(self):
        cmux = self.get_object()
        is_author = self.request.user.author == cmux.author
        is_moderator = self.request.user.author.is_moderator
        post_is_new = not cmux.is_approved
        if (is_author and post_is_new) or is_moderator:
            return True
        return False


def approve_cmux(request, pk):
    cmux = Cmux.objects.get(pk=pk)
    cmux.is_approved = True
    cmux.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def test_func(self):
        is_moderator = self.request.user.author.is_moderator
        if (is_moderator) or is_moderator:
            return True
        return False


def unapproved_cmuxes_count():
    return Cmux.objects.filter(is_approved=False).count()
