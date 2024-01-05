from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)

from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Post
from .utils import AuthorOrAdminMixin, AuthorMixin, CommentMixin


PAGINATION = 10


class IndexListView(ListView):
    model = Post
    form_class = PostForm
    template_name = 'blog/index.html'
    queryset = Post.objects.get_post_list()
    paginate_by = PAGINATION


class PostCreateView(LoginRequiredMixin, AuthorMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['pub_date'] = timezone.now()
        return initial

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostUpdateView(
    LoginRequiredMixin,
    AuthorMixin,
    AuthorOrAdminMixin,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(
    LoginRequiredMixin,
    AuthorMixin,
    AuthorOrAdminMixin,
    DeleteView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('blog:profile')
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            raise PermissionDenied
        if 'delete' in request.path:
            return self.delete(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(DetailView):
    model = Post
    form_class = PostForm
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        post_id = self.kwargs.get(self.pk_url_kwarg)
        return Post.objects.filter(pk=post_id)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_published and self.request.user != obj.author:
            raise Http404('Страница не найдена')
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = CommentForm()
        context['comments'] = post.comments.all()
        context['post_id'] = post.id
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class ProfilePostListView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATION

    def get_queryset(self):
        self.user = self.get_user()
        if (
            self.request.user.is_authenticated
            and self.request.user == self.user
        ):
            return Post.objects.filter(author=self.user)
        else:
            return Post.objects.get_post_list().filter(author=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user
        return context

    def get_user(self):
        username = (
            self.kwargs.get('username', None)
            or self.request.user.username
        )
        return get_object_or_404(User, username=username)


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'category'
    paginate_by = PAGINATION

    def get_queryset(self):
        posts = Post.objects.get_post_list().all()
        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return posts.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CommentCreateView(
    CommentMixin,
    LoginRequiredMixin,
    AuthorMixin,
    CreateView
):

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(
    CommentMixin,
    LoginRequiredMixin,
    AuthorOrAdminMixin,
    UpdateView
):
    pass


class CommentDeleteView(
    CommentMixin,
    LoginRequiredMixin,
    AuthorOrAdminMixin,
    DeleteView
):
    pass
