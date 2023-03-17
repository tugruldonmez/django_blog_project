from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin#giriş yapmadan post paylaşılmaya çalışılırsa giriş ekranına yönlendirir giriş yaptıktan sonra direkt forma gönderir
from django.contrib.auth.mixins import UserPassesTestMixin#Postu sadece atan kişinin güncellemesini sağlar
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView   
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5#paginate_by yandaki değer kadar objeyi bir sayfaya sığdırır

class UserPostListView(ListView):
    model=Post
    template_name='blog/user_posts.html'
    context_object_name='posts'
    paginate_by=5#paginate_by yandaki değer kadar objeyi bir sayfaya sığdırır

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))#eğer link barına var olmayan user id girilip postlar görüntülenmeye çalışılırsa 404 hatası versin
        return Post.objects.filter(author=user).order_by('-date_posted')#eğer link barına var olan user id girilirse paylaştığı postları göstersin

class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title', 'content']
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)#bu fonksiyon post paylaşırken paylaşılan postun giriş yapmış kullanıcıya ait olduğunu belirtir(bu fonksiyon olmazsa post paylaşılamaz id hatası verir)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Post
    fields=['title', 'content']
    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):#Postu atan kişiyle güncellemek isteyen kişi aynı mı diye kontrol eden fonk.
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Post
    success_url='/'#  '/' komutu programı ilk sayfaya gönderir

    def test_func(self):#Postu atan kişiyle silmek isteyen kişi aynı mı diye kontrol eden fonk.
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False 

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})