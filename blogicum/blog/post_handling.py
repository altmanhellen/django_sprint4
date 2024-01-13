from django.http import Http404
from django.views.generic.detail import SingleObjectMixin


class PostAccessMixin(SingleObjectMixin):

    def get_object(self, queryset=None):
        self.post = super().get_object(queryset=queryset)
        if queryset is None:
            queryset = self.model.objects
        if (
            (self.post not in queryset.get_published_posts())
            and (
                not self.request.user.is_superuser
            ) and (
                self.post.author != self.request.user
            )
        ):
            raise Http404('Страница не найдена')
        return self.post


class PostContextData:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all()
        context['post_id'] = post.id
        context['post'] = post
        return context
