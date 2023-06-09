from django.contrib import admin
from django.urls import path,include
from . import views
#from .views import Login_view, Register_view, test_view, book_appointment
app_name = "patient"
urlpatterns = [
    path('', views.home, name="home"),
    path('lienhe', views.lienhe, name="lienhe"),
    path('lienhe1', views.lienhe1, name="lienhe1"),
    path('hdsd', views.hdsd, name="hdsd"),
    path('hdsd1', views.hdsd1, name="hdsd1"),
    path('dangky', views.dangky, name="dangky"),
    path('dangnhap', views.dangnhap, name="dangnhap"),
    path('tintuc', views.tintuc, name="tintuc"),
    path('tintuc1', views.tintuc1, name="tintuc1"),
    path('thongbao', views.thongbao, name="thongbao"),
    path('thongbao1', views.thongbao1, name="thongbao1"),
    path('chuyenkhoa', views.chuyenkhoa, name="chuyenkhoa"),
    path('chuyenkhoa1', views.chuyenkhoa1, name="chuyenkhoa1"),
    path('home1', views.home1, name="home1"),
    path('khieunai', views.khieunai, name="khieunai"),
    path('khieunai1', views.khieunai1, name="khieunai1"),
    path('register', views.register, name="register"),
    path('user_login', views.user_login, name="user_login"),
    path('thongtin', views.thongtin, name="thongtin"),
    path('change_password', views.change_password, name="change_password"),
    path('chaomung', views.chaomung, name="chaomung"),
    #chuyên khoa
    path('xuongkhop', views.xuongkhop, name="xuongkhop"),
    path('xuongkhop1', views.xuongkhop1, name="xuongkhop1"),
    path('thankinh', views.thankinh, name="thankinh"),
    path('thankinh1', views.thankinh1, name="thankinh1"),
    path('tieuhoa', views.tieuhoa, name="tieuhoa"),
    path('tieuhoa1', views.tieuhoa1, name="tieuhoa1"),
    path('timmach', views.timmach, name="timmach"),
    path('timmach1', views.timmach1, name="timmach1"),
    path('taimuihong', views.taimuihong, name="taimuihong"),
    path('taimuihong1', views.taimuihong1, name="taimuihong1"),
    path('cotsong', views.cotsong, name="cotsong"),
    path('cotsong1', views.cotsong1, name="cotsong1"),
    path('dalieu', views.dalieu, name="dalieu"),
    path('dalieu1', views.dalieu1, name="dalieu1"),
    path('hohap', views.hohap, name="hohap"),
    path('hohap1', views.hohap1, name="hohap1"),
    path('nhakhoa', views.nhakhoa, name="nhakhoa"),
    path('nhakhoa1', views.nhakhoa1, name="nhakhoa1"),


    #chuyên khoa đặt khám
    path('xuongkhopdk', views.xuongkhopdk, name="xuongkhopdk"),
    path('xuongkhopdk1', views.xuongkhopdk1, name="xuongkhopdk1"),
    path('thankinhdk', views.thankinhdk, name="thankinhdk"),
    path('thankinhdk1', views.thankinhdk1, name="thankinhdk1"),
    path('tieuhoadk', views.tieuhoadk, name="tieuhoadk"),
    path('tieuhoadk1', views.tieuhoadk1, name="tieuhoadk1"),
    path('timmachdk', views.timmachdk, name="timmachdk"),
    path('timmachdk1', views.timmachdk1, name="timmachdk1"),
    path('taimuihongdk', views.taimuihongdk, name="taimuihongdk"),
    path('taimuihongdk1', views.taimuihongdk1, name="taimuihongdk1"),
    path('cotsongdk', views.cotsongdk, name="cotsongdk"),
    path('cotsongdk1', views.cotsongdk1, name="cotsongdk1"),
    path('dalieudk', views.dalieudk, name="dalieudk"),
    path('dalieudk1', views.dalieudk1, name="dalieudk1"),
    path('hohapdk', views.hohapdk, name="hohapdk"),
    path('hohapdk1', views.hohapdk1, name="hohapdk1"),
    path('nhakhoadk', views.nhakhoadk, name="nhakhoadk"),
    path('nhakhoa1dk', views.nhakhoadk1, name="nhakhoadk1"),

     # 5 chuyên khoa ngoài trang home
    path('xuongkhophome', views.xuongkhophome, name="xuongkhophome"),
    path('xuongkhophome1', views.xuongkhophome1, name="xuongkhophome1"),
    path('thankinhhome', views.thankinhhome, name="thankinhhome"),
    path('thankinhhome1', views.thankinhhome1, name="thankinhhome1"),
    path('tieuhoahome', views.tieuhoahome, name="tieuhoahome"),
    path('tieuhoahome1', views.tieuhoahome1, name="tieuhoahome1"),
    path('timmachhome', views.timmachhome, name="timmachhome"),
    path('timmachhome1', views.timmachhome1, name="timmachhome1"),
    path('taimuihonghome', views.taimuihonghome, name="taimuihonghome"),
    path('taimuihonghome1', views.taimuihonghome1, name="taimuihonghome1"),
    #bác sĩ 
    path('BsXuongkhop1/<int:id>', views.BsXuongkhop1, name="BsXuongkhop1"),
    path('BsXuongkhop2/<int:id>', views.BsXuongkhop2, name="BsXuongkhop2"),
    path('BsThankinh1/<int:id>', views.BsThankinh1, name="BsThankinh1"),
    path('BsThankinh2/<int:id>', views.BsThankinh2, name="BsThankinh2"),
    path('BsTieuhoa1/<int:id>', views.BsTieuhoa1, name="BsTieuhoa1"),
    path('BsTieuhoa2/<int:id>', views.BsTieuhoa2, name="BsTieuhoa2"),
    path('BsTimmach1/<int:id>', views.BsTimmach1, name="BsTimmach1"),
    path('BsTimmach2/<int:id>', views.BsTimmach2, name="BsTimmach2"),
    path('BsTaimuihong1/<int:id>', views.BsTaimuihong1, name="BsTaimuihong1"),
    path('BsTaimuihong2/<int:id>', views.BsTaimuihong2, name="BsTaimuihong2"),
    path('BsCotsong1/<int:id>', views.BsCotsong1, name="BsCotsong1"),
    path('BsCotsong2/<int:id>', views.BsCotsong2, name="BsCotsong2"),
    path('BsDalieu1/<int:id>', views.BsDalieu1, name="BsDalieu1"),
    path('BsDalieu2/<int:id>', views.BsDalieu2, name="BsDalieu2"),
    path('BsHohapphoi1/<int:id>', views.BsHohapphoi1, name="BsHohapphoi1"),
    path('BsHohapphoi2/<int:id>', views.BsHohapphoi2, name="BsHohapphoi2"),
    path('BsNhakhoa1/<int:id>', views.BsNhakhoa1, name="BsNhakhoa1"),
    path('BsNhakhoa2/<int:id>', views.BsNhakhoa2, name="BsNhakhoa2"),
    #login để đặt khám
    path('logindedatkham', views.logindedatkham, name="logindedatkham"),
    #thay đổi thông tin người dùng
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),

    #đặt khám
    path('datkham', views.datkham, name="datkham"),
    path('datkham1', views.datkham1, name="datkham1"),
    path('book_appointment', views.book_appointment, name="book_appointment"),
    path('book_appointment/<int:id>/<str:time>/', views.datkhamid0, name="book_appointment"),
    path('book_appointment1', views.book_appointment1, name="book_appointment1"),
    path('book_appointment1/<int:id>/<str:time>/', views.datkhamid, name="book_appointment1"),
    path('success', views.success, name="success"),
    #code tìm kiếm bác sĩ
    path('test-infos/<int:id>', views.thongtinBS, name="thongtinBS"),
    path('test-info/<int:id>', views.thongtinBS1, name="thongtinBS"),
    path('get-time-available/', views.get_time_available),
    path('check-available-to-book/', views.check_available_to_book),
    path('save-appoint/', views.save_appoint, name = "save-appoint"),
    path('logout/', views.logout_v, name = "logout"),
    ]

