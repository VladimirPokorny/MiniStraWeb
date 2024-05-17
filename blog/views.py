from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .forms import MinistrantForm
from .models import Ministrant
from camp.models import SummerCampInfo, BankAccount

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Ministrant
from .forms import MinistrantForm
from camp.models import SummerCampInfo, BankAccount

from io import BytesIO
from reportlab.pdfgen import canvas

from datetime import datetime
from utils import email_notifier


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

    def ministrant_detail(request, pk):
        ministrant = get_object_or_404(Ministrant, pk=pk)
        bank_account = BankAccount.objects.first()
        summer_camp_price = SummerCampInfo.objects.first().price
        return render(request, 'ministrant_detail.html', {'ministrant': ministrant, 'bank_account': bank_account, 'summer_camp_price': summer_camp_price})


class MinistrantCreateView(LoginRequiredMixin, CreateView):
    model = Ministrant
    form_class = MinistrantForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        email_notifier.EmailNotifier(form.instance).send_email()
        return response


class MinistrantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ministrant
    form_class = MinistrantForm

    def test_func(self):
        ministrant = self.get_object()
        if self.request.user == ministrant.author:
            return True
        return False


class AllMinistrantListView(ListView):
    model = Ministrant
    template_name = 'blog/all_ministrants.html'
    context_object_name = 'ministrants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime(2023, 7, 23)
        return context


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

def send_inform_email(request, pk):
    ministrant = get_object_or_404(Ministrant, pk=pk)
    notifier = email_notifier.EmailNotifier(ministrant)
    notifier.send_email()

    return render(request, 'ministrant_detail.html', {'ministrant': ministrant})