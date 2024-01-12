from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
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
from .authorship import AuthorOrAdminMixin, AuthorMixin
from .comment_handling import CommentMixin
from .post_handling import PostAccessMixin, PostContextData


PAGINATION = 10


class IndexListView(ListView):
    model = Post
    form_class = PostForm
    template_name = 'blog/index.html'
    queryset = Post.objects.get_published_posts()
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
    PostContextData,
    DeleteView
):

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    raise_exception = True

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = PostForm(instance=post)
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostDetailView(
    PostAccessMixin,
    PostContextData,
    DetailView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
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
        if self.request.user == self.user:
            return Post.objects.get_all_posts(author=self.user)
        return Post.objects.get_published_posts(author=self.user)

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


class CategoryPostListView(SingleObjectMixin, ListView):
    model = Post
    paginate_by = PAGINATION
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        category = super().get_object(queryset=queryset)
        if not category.is_published:
            raise Http404("Категория неопубликована.")
        return category

    def get_queryset(self):
        self.object = self.get_object(queryset=Category.objects.all())
        return Post.objects.get_published_posts(category=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context


class CommentCreateView(
    CommentMixin,
    LoginRequiredMixin,
    AuthorMixin,
    PostAccessMixin,
    CreateView
):

    def form_valid(self, form):
        try:
            post = Post.objects.get(pk=self.kwargs.get('post_id'))
        except Post.DoesNotExist:
            raise Http404(
                "Вы не можете добавлять комментарии к несуществующему посту."
            )
        form.instance.post = post
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
