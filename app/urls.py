from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.new_question, name='new_question'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('tag/<str:tag>/', views.search_tag, name='tag'),
]
