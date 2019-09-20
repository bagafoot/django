from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# posts = [
#     {
#         'author':'bekirniyaz',
#         'title':'blog post 1',
#         'content':'First Post content',
#         'date_posted':'August 23,2018'
#     },
# {
#         'author':'zakirpiyaz',
#         'title':'blog post 2',
#         'content':'Second Post content',
#         'date_posted':'August 23,2018'
#     }
# ]

# ctrl+alt+y

def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title': 'About'})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):      #form_valid metodunu ovveride ederek authoru mevcut user dan cekiyoruz
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):      #form_valid metodunu ovveride ederek authoru mevcut user dan cekiyoruz
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False