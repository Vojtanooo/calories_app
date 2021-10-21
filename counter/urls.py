from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bmr", views.bmr_calculator, name="bmr")

]