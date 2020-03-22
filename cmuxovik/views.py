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
from django.contrib.auth.decorators import user_passes_test

from django.contrib.messages.views import SuccessMessageMixin
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

    def get_queryset(self):
        filter_params, exclude_params = {}, {}
        filter_params['is_active'] = True
        q = self.request.GET.get('search_text', None)
        if q:
            filter_params['text__icontains'] = q
        if self.request.user.is_anonymous or not self.request.user.author.is_moderator:
            exclude_params['is_approved'] = False
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by('-ratings__average', '-created_at')


class UserCmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/user_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-ratings__average', '-created_at']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        filter_params, exclude_params = {}, {}
        filter_params['is_active'] = True
        filter_params['author'] = user.author
        q = self.request.GET.get('search_text', None)
        if q:
            filter_params['text__icontains'] = q
        if self.request.user.is_anonymous or not self.request.user.author.is_moderator:
            exclude_params['is_approved'] = False
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by('-ratings__average', '-created_at')


class UnapprovedCmuxListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cmux
    template_name = 'cmuxovik/unapproved_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-created_at']
    paginate_by = 5

    def get_queryset(self):
        filter_params, exclude_params = {}, {}
        filter_params['is_active'] = True
        filter_params['is_approved'] = False
        q = self.request.GET.get('search_text', None)
        if q:
            filter_params['text__icontains'] = q
        if self.request.user.is_anonymous or not self.request.user.author.is_moderator:
            exclude_params['is_approved'] = False
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by('-ratings__average', '-created_at')

    def test_func(self):
        return self.request.user.author.is_moderator


class CmuxDetailView(DetailView):
    model = Cmux


class CmuxCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cmux
    fields = ['text', 'tags']
    success_message = "The cmux was successfully created!"

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class CmuxUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Cmux
    fields = ['text', 'tags']
    success_message = "The cmux was successfully updated!"

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

    def test_func(self):
        cmux = self.get_object()
        is_author = self.request.user.author == cmux.author
        is_moderator = self.request.user.author.is_moderator
        post_is_new = not cmux.is_approved
        if is_author and post_is_new and cmux.is_active:
            return True
        return False


class CmuxDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cmux
    success_message = "The cmux was successfully deleted."
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CmuxDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        cmux = self.get_object()
        is_author = self.request.user.author == cmux.author
        is_moderator = self.request.user.author.is_moderator
        post_is_new = not cmux.is_approved
        if (is_author and post_is_new and cmux.is_active) or is_moderator:
            return True
        return False


def is_moderator(user):
    return user.author.is_moderator


@user_passes_test(is_moderator)
def approve_cmux(request, pk):
    cmux = Cmux.objects.get(pk=pk)
    if cmux.is_approved:
        messages.warning(
            request, 'This cmux has already been approved.')
    else:
        cmux.is_approved = True
        cmux.save()
        messages.success(
            request, 'The cmux was approved!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def unapproved_cmuxes_count():
    return Cmux.objects.filter(is_approved=False).count()
