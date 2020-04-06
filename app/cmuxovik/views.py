from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Cmux, Tag
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
from django.urls import resolve
from django.db import IntegrityError
from django.utils.translation import gettext as _


class CmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/home.html'
    context_object_name = 'cmuxes'
    paginate_by = 10

    def get_queryset(self):
        # Filtering
        filter_params, exclude_params = {}, {}
        filter_params['is_active'] = True
        q = self.request.GET.get('search_text', None)
        if q:
            filter_params['text__icontains'] = q
        if self.request.user.is_anonymous or not self.request.user.author.is_moderator:
            exclude_params['is_approved'] = False
        # Ordering
        # TODO: sometimes doesnt work just after the migration when switching locale
        url_name = resolve(self.request.path).url_name
        if url_name == 'cmuxovik-best':
            order_by_list = ['-ratings__average', '-created_at']
        else:
            order_by_list = ['-created_at']
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by(*order_by_list)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Homepage')
        return context


class UserCmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/user_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-ratings__average', '-created_at']
    paginate_by = 10

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
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by(
            '-ratings__average', '-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{_('Cmuxes by')} {self.kwargs.get('username')}"
        return context


class TagCmuxListView(ListView):
    model = Cmux
    template_name = 'cmuxovik/tag_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-ratings__average', '-created_at']
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        filter_params, exclude_params = {}, {}
        filter_params['is_active'] = True
        filter_params['tags__id'] = tag.id
        q = self.request.GET.get('search_text', None)
        if q:
            filter_params['text__icontains'] = q
        if self.request.user.is_anonymous or not self.request.user.author.is_moderator:
            exclude_params['is_approved'] = False
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by(
            '-ratings__average', '-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(pk=self.kwargs.get('pk'))
        context['title'] = f"{_('Cmuxes by tag')} {context['tag']}"
        return context


class UnapprovedCmuxListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cmux
    template_name = 'cmuxovik/unapproved_cmuxes.html'
    context_object_name = 'cmuxes'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        filter_params, exclude_params = {}, {}
        filter_params['is_active'] = True
        filter_params['is_approved'] = False
        q = self.request.GET.get('search_text', None)
        if q:
            filter_params['text__icontains'] = q
        if self.request.user.is_anonymous or not self.request.user.author.is_moderator:
            exclude_params['is_approved'] = False
        return Cmux.objects.filter(**filter_params).exclude(**exclude_params).order_by(
            '-ratings__average', '-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Unapproved cmuxes')
        return context

    def test_func(self):
        return self.request.user.author.is_moderator


class CmuxDetailView(DetailView):
    model = Cmux


class CmuxCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cmux
    fields = ['text', 'tags']
    success_message = _("The cmux was successfully created!")

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('text', _("This cmux already exists."))
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CmuxCreateView, self).get_context_data(**kwargs)
        context['tags_exist'] = Tag.objects.count() > 0
        context['mode'] = 'create'
        return context


class CmuxUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Cmux
    fields = ['text', 'tags']
    success_message = _("The cmux was successfully updated!")

    def test_func(self):
        cmux = self.get_object()
        is_author = self.request.user.author == cmux.author
        is_moderator = self.request.user.author.is_moderator
        # Author can change unapproved cmuxes, Moderator can change all cmuxes
        if (is_author and cmux.is_active and not cmux.is_approved) or is_moderator:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(CmuxUpdateView, self).get_context_data(**kwargs)
        context['tags_exist'] = Tag.objects.count() > 0
        context['mode'] = 'update'
        return context


class CmuxDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cmux
    success_message = _("The cmux was successfully deleted.")
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
            request, _('This cmux has already been approved.'))
    else:
        cmux.is_approved = True
        cmux.save()
        messages.success(
            request, _('The cmux was approved!'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def unapproved_cmuxes_count():
    return Cmux.objects.filter(is_approved=False).count()


def error_404(request, exception):
    data = {}
    return render(request, 'cmuxovik/404.html', data)


def error_500(request):
    data = {}
    return render(request, 'cmuxovik/500.html', data)


def error_403(request, exception):
    data = {}
    return render(request, 'cmuxovik/404.html', data)


def error_400(request, exception):
    data = {}
    return render(request, 'cmuxovik/500.html', data)
