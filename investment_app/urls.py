from django.urls import path
from .views import WeightList, PriceList, PortfolioWeightDetail, PortfolioValueDetail, cargar_datos

urlpatterns = [
    path('weights/', WeightList.as_view(), name='weight-list'),
    path('prices/', PriceList.as_view(), name='price-list'),
    path('portfolio/<int:portafolio_id>/weights/', PortfolioWeightDetail.as_view(), name='portfolio-weights'),
    path('portfolio/<int:portafolio_id>/values/', PortfolioValueDetail.as_view(), name='portfolio-values'),
    path('cargar-datos/', cargar_datos, name='cargar-datos'),
]