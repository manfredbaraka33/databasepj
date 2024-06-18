from django.urls import path

from . import views


from django.urls import path
from . import views

app_name = "hostelMS"
urlpatterns = [
  path('', views.hostel_view, name='index'), 
  path("preLogin", views.prelogin, name="prelogin"),
  path("login", views.login, name="login"),
  path("login2", views.login2, name="login2"),
  path("register", views.register, name="register"),
  path("studentDb", views.studentDb, name="studentDb"),
  path("employeeDb", views.employeeDb, name="employeeDb"),
  path("maintainace-issue", views.issue, name="issue"),
  path("maintainace-issuelist", views.issuelist, name="issuelist"),
  path('account',views.account,name="account"),
  path('account2',views.account2,name="account2"),
  path('approve/<int:maintainanceissue_id>/',views.approve,name="approve")
]
