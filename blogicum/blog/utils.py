from .querysets import FilteredQuerySet


def get_post_list(self):
    return (
        FilteredQuerySet(self).is_published()
    )
