from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from movies.views import MovieListView, MovieDetailView
from users.views import UserSignupHTMLView, review_delete, review_create

urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', UserSignupHTMLView.as_view(), name='signup_html'),
    
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('reviews/<int:pk>/delete/', review_delete, name='review_delete'),
    path('movies/<int:movie_id>/reviews/create/', review_create, name='review_create'),

    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/movies/', include('movies.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/', include('comments.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]