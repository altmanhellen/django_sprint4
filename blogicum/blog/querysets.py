from django.db.models import QuerySet
from django.utils import timezone


class FilteredQuerySet(QuerySet):

    def is_published(self):
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
