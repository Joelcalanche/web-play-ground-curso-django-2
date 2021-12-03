from django.urls import path
from . import views
from.views import PageListView, PageDetailView, PageCreate, PageUpdate, PageDelete
pages_patterns = ([
    
    # internamente esta clase apunta  un template de nombre: modelo_list.htnnl
    path('', PageListView.as_view(), name='pages'),
    # tenemos que ponerle pk ""primary key" para que vaya a buscar la instancia asociada
    
    # internamente esta clase apunta un template de nombre: modelo_detail.html
    path('<int:pk>/<slug:slug>/', PageDetailView.as_view(), name='page'),
    path('create/', PageCreate.as_view(), name='create'),
    path('update/<int:pk>/', PageUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', PageDelete.as_view(), name='delete'),
], 'pages')