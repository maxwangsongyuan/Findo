from django.urls import path
from . import adv1

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('a/', views.get_all_user_name, name='get_user_name'),
    path('ret/', views.redirect_to_admin),
    path('database/', views.runoob),
    path('insert/', views.insert),
    path('update/', views.update),
    path('delete/', views.delete),
    path('view/', views.view),

    path('viewStock/', views.runStock),
    path('viewStockDatabase/', views.viewStockDatabase),
    path('insertStock/', views.insertStock),
    path('deleteStock/', views.deleteStock),
    path('searchStockId/', views.searchStockId),
    path('searchStockPrice/', views.searchStockPrice),

    path('viewSFIDatabase/', views.viewSFIDatabase),
    path('insertSFI/', views.insertSFI),
    path('deleteSFI/', views.deleteSFI),
    path('updateSFI/', views.updateSFI),
    path('searchSFI/', views.searchSFI),
    path('viewSFI/', views.runSFI),
    path('searchStockIdViaSFI/', views.searchStockIdViaSFI),

    path('viewFPDatabase/', views.viewFPDatabase),
    path('insertFP/', views.insertFP),
    path('searchFP/', views.searchFP),
    path('viewFP/', views.runFP),

    # MongoDB
    path('all_users/', views.all_users),
    path('add_users_page/', views.run_add_user),
    path('insertUser/', views.insertUser),
    path('loginUser/', views.loginUser),
    path('userSaves/', views.userSaves),
    path('mySaves/', views.mySaves),
    path('logout/', views.logout),

    # Advance Function
    path('ad1/', views.ad1),
    path('ad1_page/', views.ad1_page),

]