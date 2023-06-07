from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Ministrant
from .forms import MinistrantForm


def home(request):
    context = {
        'ministrants': Ministrant.objects.all()
    }
    return render(request, 'blog/home.html', context)


class MinistrantListView(ListView):
    model = Ministrant
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'ministrants'
    ordering = ['-time_stamp']
    paginate_by = 5


class UserMinistrantListView(ListView):
    model = Ministrant
    template_name = 'blog/user_ministrants.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'ministrants'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ministrant.objects.filter(author=user).order_by('-time_stamp')


class MinistrantDetailView(DetailView):
    model = Ministrant


class MinistrantCreateView(LoginRequiredMixin, CreateView):
    model = Ministrant
    form_class = MinistrantForm
    # fields = ['birthname', 'surename', 'birth_date', 'address', 'town', 'town_zip']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MinistrantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ministrant
    form_class = MinistrantForm
    # fields = ['title', 'content']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        ministrant = self.get_object()
        if self.request.user == ministrant.author:
            return True
        return False


class MinistrantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ministrant
    success_url = '/'

    def test_func(self):
        ministrant = self.get_object()
        if self.request.user == ministrant.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def page_not_found(request, exception):
    return render(request, '404.html', {'title': 'Page Not Found :('})
