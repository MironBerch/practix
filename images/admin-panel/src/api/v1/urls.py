from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('schema/', include('api.v1.schema.urls')),
]
