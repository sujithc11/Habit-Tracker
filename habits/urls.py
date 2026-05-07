from django.urls import path
from .views import dashboard,add_habit,complete_habit,signup,delete_habit

urlpatterns = [
    path('', dashboard),
    path('add/', add_habit),
    path('complete/<int:id>/', complete_habit),
    path('signup/', signup),
    path('delete/<int:id>/', delete_habit),

]