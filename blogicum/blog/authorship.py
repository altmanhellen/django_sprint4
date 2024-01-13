from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

from .models import Post, Comment


class AuthorOrAdminMixin(UserPassesTestMixin):
    """Проверка, что пользователь - автор объекта или администратор."""

    model = None
    pk_url_kwarg = 'pk'

    def test_func(self):
        obj = self.get_object()
        return (
            obj.author == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        obj = self.get_object()
        post_id = self.kwargs.get('post_id')

        if post_id is None:
            raise PermissionDenied('Запрашиваемый пост не найден.')
        if isinstance(obj, Post) or isinstance(obj, Comment):
            return redirect(
                reverse('blog:post_detail',
                        kwargs={'post_id': post_id}
                        )
            )
        raise PermissionDenied(self.get_permission_denied_message())


class AuthorMixin:
    """Устанавливаем пользователя в качестве автора объекта."""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
