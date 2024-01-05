from django.urls import include, path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/', include([
        path(
            'create/',
            views.PostCreateView.as_view(),
            name='create_post'
        ),
        path(
            '<int:post_id>/',
            views.PostDetailView.as_view(),
            name='post_detail'
        ),
        path(
            '<int:post_id>/edit/',
            views.PostUpdateView.as_view(),
            name='edit_post'
        ),
        path(
            '<int:post_id>/delete/',
            views.PostDeleteView.as_view(),
            name='delete_post'
        ),
        path(
            '<int:post_id>/edit_comment/<int:pk>/',
            views.CommentUpdateView.as_view(),
            name='edit_comment'
        ),
        path(
            '<int:post_id>/delete_comment/<int:pk>/',
            views.CommentDeleteView.as_view(),
            name='delete_comment'
        ),
        path(
            '<int:post_id>/comment/',
            views.CommentCreateView.as_view(),
            name='add_comment'
        ),
    ])),
    path('profile/', include([
        path(
            'edit/',
            views.ProfileUpdateView.as_view(),
            name='edit_profile'
        ),
        path(
            '<slug:username>/',
            views.ProfilePostListView.as_view(),
            name='profile'
        ),
    ])),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostListView.as_view(),
        name='category_posts'
    ),
]
