from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm, UserSubscription
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.models import Author, Category


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors'):
        authors_group.user_set.add(user)
        Author.objects.create(user=request.user)
    return redirect('news/')

# @login_required
# def subscribe_me(request):
# category_id = request.GET.get('category_id')
# try:
#  subscription = UserSubscription.objects.get(user=request.user, category=Category.objects.get(pk=category_id))
# except UserSubscription.DoesNotExist:
#  subscription = UserSubscription.objects.create(user=request.user, category=Category.objects.get(pk=category_id))
# return redirect(request.GET.get('path_info'))
