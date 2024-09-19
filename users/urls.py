from . import views, apps


app_name = apps.UsersConfig.name.replace("apps.","")

urlpatterns = [
    #llamar a las Url como: 'users:index' 
]