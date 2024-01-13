from django.urls import include, path

from . import views

app_name = 'blog'

posts_patterns = [
    path(
        'create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'edit/',
        views.PostUpdateView.as_view(),
        name='edit_post'
    ),
    path(
        'delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        '',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'edit_comment/<int:pk>/',
        views.CommentUpdateView.as_view(),
        name='edit_comment'
    ),
    path(
        'delete_comment/<int:pk>/',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
    ),
    path(
        'comment/',
        views.create_comment,
        # views.CommentCreateView.as_view(),
        name='add_comment'
    ),
]

profile_patterns = [
    path(
        'edit/',
        views.ProfileUpdateView.as_view(),
        name='edit_profile'
    ),
    path(
        '<str:username>/',
        views.ProfilePostListView.as_view(),
        name='profile'
    ),
]

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/', include(posts_patterns)),
    path('posts/<int:post_id>/', include(posts_patterns)),
    path('profile/', include(profile_patterns)),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostListView.as_view(),
        name='category_posts'
    ),
]
