# Generated by Django 4.1.2 on 2023-04-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='province',
            field=models.CharField(choices=[('ho_chi_minh', 'TP. Hồ Chí Minh'), ('ha_noi', 'Hà Nội'), ('da_nang', 'Đà Nẵng'), ('hai_phong', 'Hải Phòng'), ('can_tho', 'Cần Thơ'), ('cao_bang', 'Cao Bằng'), ('an_giang', 'An Giang'), ('bac_giang', 'Bắc Giang'), ('bac_kan', 'Bắc Kạn'), ('bac_lieu', 'Bạc Liêu'), ('bac_ninh', 'Bắc Ninh'), ('ben_tre', 'Bến Tre'), ('binh_dinh', 'Bình Định'), ('binh_duong', 'Bình Dương'), ('binh_phuoc', 'Bình Phước'), ('binh_thuan', 'Bình Thuận'), ('ca_mau', 'Cà Mau'), ('cao_bang', 'Cao Bằng'), ('dak_lak', 'Đắk Lắk'), ('dak_nong', 'Đắk Nông'), ('dien_bien', 'Điện Biên'), ('dong_nai', 'Đồng Nai'), ('dong_thap', 'Đồng Tháp'), ('gia_lai', 'Gia Lai'), ('ha_giang', 'Hà Giang'), ('ha_nam', 'Hà Nam'), ('ha_tinh', 'Hà Tĩnh'), ('hai_duong', 'Hải Dương'), ('hau_giang', 'Hậu Giang'), ('hoa_binh', 'Hòa Bình'), ('hung_yen', 'Hưng Yên'), ('khanh_hoa', 'Khánh Hòa'), ('kien_giang', 'Kiên Giang'), ('kon_tum', 'Kon Tum'), ('lai_chau', 'Lai Châu'), ('lam_dong', 'Lâm Đồng'), ('lang_son', 'Lạng Sơn'), ('lao_cai', 'Lào Cai'), ('long_an', 'Long An'), ('nam_dinh', 'Nam Định'), ('nghe_an', 'Nghệ An'), ('ninh_binh', 'Ninh Bình'), ('ninh_thuan', 'Ninh Thuận'), ('phu_tho', 'Phú Thọ'), ('quang_binh', 'Quảng Bình'), ('quang_nam', 'Quảng Nam'), ('quang_ngai', 'Quảng Ngãi'), ('quang_ninh', 'Quảng Ninh'), ('quang_tri', 'Quảng Trị'), ('soc_trang', 'Sóc Trăng'), ('son_la', 'Sơn La'), ('tay_ninh', 'Tây Ninh'), ('thai_binh', 'Thái Bình'), ('thai_nguyen', 'Thái Nguyên'), ('thanh_hoa', 'Thanh Hóa'), ('thua_thien_hue', 'Thừa Thiên Huế'), ('tien_giang', 'Tiền Giang'), ('tra_vinh', 'Trà Vinh'), ('tuyen_quang', 'Tuyên Quang'), ('vinh_long', 'Vĩnh Long'), ('vinh_phuc', 'Vĩnh Phúc'), ('yen_bai', 'Yên Bái')], default='ha_noi', max_length=20),
        ),
    ]
