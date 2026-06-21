from django.urls import path
from . import views
from club import views

urlpatterns = [

    # ======================
    # TRANG CHỦ
    # ======================
    path('', views.home, name='home'),

    # ======================
    # CLB
    # ======================
    path('clubs/', views.clubs, name='clubs'),
    path('quanly-clb/', views.quanly_clb, name='quanly_clb'),
    path('them-clb/', views.them_clb, name='them_clb'),
    path('sua-clb/<int:id>/', views.sua_clb, name='sua_clb'),
    path('xoa-clb/<int:id>/', views.xoa_clb, name='xoa_clb'),
    path('phan-quyen/<int:id>/', views.phan_quyen_clb, name='phan_quyen_clb'),
    path('phan-cong-clb/<int:id>/', views.phan_cong_clb, name='phan_cong_clb'),
    path('clb-dashboard/', views.clb_dashboard, name='clb_dashboard'),
    path('clb/sua-tieu-su/', views.sua_tieu_su_clb, name='sua_tieu_su_clb'),


    # ======================
    # SỰ KIỆN
    # ======================
    path('events/', views.events, name='events'),
    path('quanly-sukien/', views.quanly_sukien, name='quanly_sukien'),
    path('them-sukien/', views.them_sukien, name='them_sukien'),
    path('sua-sukien/<int:id>/', views.sua_sukien, name='sua_sukien'),
    path('xoa-sukien/<int:id>/', views.xoa_sukien, name='xoa_sukien'),
    path('sukien/<int:id>/thanhvien/', views.thanhvien_sukien, name='thanhvien_sukien'),
    path('duyet-sukien/<int:id>/', views.duyet_sukien, name='duyet_sukien'),
    path('tuchoi-sukien/<int:id>/', views.tuchoi_sukien, name='tuchoi_sukien'),
    path('sukien/<int:sukien_id>/upload/', views.upload_ds_sukien, name='upload_ds_sukien'),

    # ======================
    # THÀNH VIÊN
    # ======================
    path('thanh-vien/', views.thanh_vien, name='thanh_vien'),
    path('xoa-thanh-vien/<int:id>/', views.xoa_thanh_vien, name='xoa_thanh_vien'),
    path('thanh-vien/', views.thanh_vien_clb, name='thanh_vien_clb'),
    path('duyet-thanh-vien/<int:id>/',  views.duyet_thanh_vien, name='duyet_thanh_vien'),
    path('them-thanh-vien/', views.them_thanh_vien, name='them_thanh_vien'),
    path('cap-quyen-admin/<int:user_id>/', views.cap_quyen_admin, name='cap_quyen_admin'),
    path('doi-quyen/<int:user_id>/', views.doi_quyen, name='doi_quyen'),


    # ======================
    # ĐĂNG KÝ
    # ======================
    path('register/', views.register, name='register'),

    # ======================
    # TÀI KHOẢN
    # ======================
    path('register-user/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ======================
    # DASHBOARD
    # ======================
    path('dashboard/', views.dashboard, name='dashboard'),

    # ======================
    # HỒ SƠ SINH VIÊN
    # ======================
    path('profile/', views.profile, name='profile'),
    path('dangky-sukien/<int:id>/', views.dangky_sukien, name='dangky_sukien'),
]