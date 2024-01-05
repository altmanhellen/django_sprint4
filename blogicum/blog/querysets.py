from django.db import models
from django.utils import timezone


class FilteredQuerySet(models.QuerySet):

    def is_published(self):
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )


class PersonManager(models.Manager):

    def get_custom_queryset(self):
        return FilteredQuerySet(self.model, using=self._db)

    def get_post_list(self, category=None):
        queryset = self.get_custom_queryset().is_published()
        if category:
            queryset = queryset.filter(category=category)
        return queryset
