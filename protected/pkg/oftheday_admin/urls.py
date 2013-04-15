import views

URLS = [
    (r'^/?$', views.index),
    (r'^new/?$', views.new_input),
    (r'^(\d+)/edit/?$', views.edit),
    (r'^reset/?$', views.reset_db),
    (r'^login/?$', views.login),
    (r'^logout/?$', views.logout),
]
