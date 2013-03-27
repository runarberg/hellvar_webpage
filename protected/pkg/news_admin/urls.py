import views

URLS = [
    (r'^/?$', views.index),
    (r'^login/?$', views.login),
    (r'^logout/?$', views.logout),
    (r'^posts/?$', views.posts),
    (r'^new_post/?$', views.new_post),
    (r'^posts/(\d+)/?$', views.post_detail),
    (r'^(\d+)/edit/?$', views.edit_post),
]
