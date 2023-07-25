from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    DeleteView, 
    UpdateView
    )

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.template.loader import get_template

from xhtml2pdf import pisa

# Create your views here.

def index(request):
    return render(request, 'syllabook/index.html')

def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'syllabook/home.html', context)

def about(request):
    return render(request, 'syllabook/about.html')

class PostListView(ListView):
    model = Post
    template_name = 'syllabook/home.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    
    fields = [
        
    'course_code', 'course_name','credits','contact_hours',
    'instructor','position','textbook','other_supplementary_material',
    'course_description','prerequisites','corequisites','course_classification',
    'course_objective','course_outcomes','student_outcome_addressed_by_the_course',
    'course_topics','prepared','noted','marked'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = [
    
    'course_code', 'course_name','credits','contact_hours',
    'instructor','position','textbook','other_supplementary_material',
    'course_description','prerequisites','corequisites','course_classification',
    'course_objective','course_outcomes','student_outcome_addressed_by_the_course',
    'course_topics','prepared','noted','marked'
    
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/home/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def create(LoginRequiredMixin, request):
    return render(request, 'syllabook/create.html')

def template_pdf(request,pdf_id):
    
    model = Post

    context = {
        'posts' : Post.objects.all().filter(id = pdf_id)
    }

    template_path = 'syllabook/template_pdf.html'

    reponse = HttpResponse(content_type='application/pdf')
    reponse['Content-Disposition'] = 'filename="syllabus.pdf"'
    template = get_template(template_path)
    html = template.render(context)


    pisa_status = pisa.CreatePDF(
        html, dest=reponse
    )

    if pisa_status.err:
        return HttpResponse('We had some error <pre> ' + html + '</pre>')
    
    return reponse