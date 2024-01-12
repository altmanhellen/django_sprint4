from django.urls import reverse

from .forms import CommentForm
from .models import Comment


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
