from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

from .forms import CommentForm
from .models import Post, Comment


class AuthorOrAdminMixin(UserPassesTestMixin):
    """Проверка, что пользователь является
    автором объекта или администратором.
    """

    model = None
    pk_url_kwarg = 'pk'

    def test_func(self):
        obj = self.get_object()
        if isinstance(obj, Post):
            return obj.author == (
                self.request.user or self.request.user.is_superuser
            )
        elif isinstance(obj, Comment):
            return obj.author == (
                self.request.user or self.request.user.is_superuser
            )
        return False

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(reverse('login'))
        post_id = self.kwargs.get('post_id')
        if not self.test_func():
            if isinstance(self.get_object(), Post):
                return HttpResponseRedirect(
                    reverse(
                        'blog:post_detail',
                        kwargs={'post_id': post_id}
                    )
                )
            elif isinstance(self.get_object(), Comment):
                return HttpResponseRedirect(
                    reverse(
                        'blog:post_detail',
                        kwargs={'post_id': post_id}
                    )
                )
        raise PermissionDenied(self.get_permission_denied_message())


class AuthorMixin:
    """Устанавливаем пользователя, отправившего форму,
    в качестве автора объекта.
    """

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentMixin:
    """Миксин для общих операций с моделью Comment."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )
