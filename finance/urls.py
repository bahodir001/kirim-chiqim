from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from finance.views import home_view


schema_view = get_schema_view(
    openapi.Info(
        title="Income/Expense Tracker API",
        default_version='v1',
        description="Kirim va chiqimlar uchun avtomatik API hujjat",
        contact=openapi.Contact(email="bahodir@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include('users.urls')),
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('incomes/', include('income.urls')),
    path('expenses/', include('expenses.urls')),
    path('exports/', include('exports.urls')),
    path('api/users/', include('users.urls')),
    path('api/incomes/', include('income.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/stats/', include('stats.urls')),
    path('api/exports/', include('exports.urls')),

    # Swagger va Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
