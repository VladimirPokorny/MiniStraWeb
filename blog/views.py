from django.http import HttpResponse
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

from io import BytesIO
from reportlab.pdfgen import canvas


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


class AllMinistrantListView(ListView):
    model = Ministrant
    template_name = 'blog/all_ministrants.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'ministrants'



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


# class MinistrantPDFGenerator(LoginRequiredMixin, UserPassesTestMixin):
#     model = Ministrant

def generate_pdf(request, pk):
    ministrant = Ministrant.objects.get(pk=pk)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the BytesIO buffer as its "file"
    p = canvas.Canvas(buffer)

    # Set up the PDF content
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, "Birthname: {}".format(ministrant.birthname))
    p.drawString(100, 680, "Surename: {}".format(ministrant.surename))
    p.drawString(100, 660, "Birth Date: {}".format(ministrant.birth_date))
    # Add more fields as needed

    # Close the PDF object cleanly, and we're done
    p.showPage()
    p.save()

    # File buffer rewind
    buffer.seek(0)

    # Generate the response as a PDF file
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ministrant.pdf"'
    return response
