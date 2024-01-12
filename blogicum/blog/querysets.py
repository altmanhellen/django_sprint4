from django.db import models
from django.utils import timezone


class FilteredQuerySet(models.QuerySet):

    def is_published(self):
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )

    def all_posts(self):
        return self


class PersonManager(models.Manager):

    def get_queryset(self):
        return FilteredQuerySet(self.model, using=self._db)

    def get_published_posts(self, category=None, author=None):
        queryset = self.get_queryset().is_published()
        if category:
            queryset = queryset.filter(category=category)
        if author:
            queryset = queryset.filter(author=author)
        return queryset

    def get_all_posts(self, category=None, author=None):
        queryset = self.get_queryset().all_posts()
        if category:
            queryset = queryset.filter(category=category)
        if author:
            queryset = queryset.filter(author=author)
        return queryset
