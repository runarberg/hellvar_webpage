import views

URLS = [
    (r'^/?$', views.index),
    (r'^post/(\d+)/?$', views.post_permalink)
]
