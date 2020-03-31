from django.urls import path

from .views import home, scrape, get_ListProduct, detail_Product


app_name = 'scrapping'

urlpatterns = [
    path('', home, name='home'),
    path('scrapping-product/', scrape, name ='scrape'),
    path('detail-product/<int:my_id>', detail_Product, name ='detail'),
    path('list-product/', get_ListProduct, name ='list'),
]