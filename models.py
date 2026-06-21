from django.db import models
from django.contrib.auth.models import User

class HoSoSinhVien(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    ho_ten = models.CharField(max_length=100)

    mssv = models.CharField(max_length=20)

    lop = models.CharField(max_length=50)

    khoa = models.CharField(max_length=100)

    email = models.EmailField()

    clb = models.ForeignKey(
        'CauLacBo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    clb_quan_ly = models.ForeignKey(
        'CauLacBo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quan_tri_vien'
    )

    ngay_sinh = models.DateField(
        null=True,
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatar/',
        null=True,
        blank=True
    )
    vai_tro = models.CharField(
        max_length=20,
        default='SinhVien'
    )
    
    def __str__(self):
        return self.ho_ten
    
   

class CauLacBo(models.Model):
    ten_clb = models.CharField(max_length=100)
    mo_ta = models.TextField()

    hinh_anh = models.ImageField(
    upload_to='clb/',
    blank=True,
    null=True
)
    gioi_thieu = models.TextField(
    null=True,
    blank=True
)
    def __str__(self):
        return self.ten_clb


class ThanhVien(models.Model):
    ho_ten = models.CharField(max_length=100)
    mssv = models.CharField(max_length=20)
    lop = models.CharField(max_length=20)
    email = models.EmailField()

    clb = models.ForeignKey(
        CauLacBo,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.ho_ten
    

class SuKien(models.Model):

    ten_su_kien = models.CharField(max_length=200)

    ngay_to_chuc = models.DateField()

    dia_diem = models.CharField(max_length=200)

    mo_ta = models.TextField()

    def __str__(self):
        return self.ten_su_kien

class DangKyCLB(models.Model):

    sinh_vien = models.ForeignKey(
        HoSoSinhVien,
        on_delete=models.CASCADE
    )

    clb = models.ForeignKey(
        CauLacBo,
        on_delete=models.CASCADE
    )

    ngay_dang_ky = models.DateTimeField(
        auto_now_add=True
    )

    trang_thai = models.CharField(
        max_length=20,
        default='Chờ duyệt'
    )

    def __str__(self):
        return f"{self.sinh_vien.ho_ten} - {self.clb.ten_clb}"
class DangKySuKien(models.Model):

    sinh_vien = models.ForeignKey(
        HoSoSinhVien,
        on_delete=models.CASCADE
    )

    su_kien = models.ForeignKey(
        SuKien,
        on_delete=models.CASCADE
    )

    trang_thai = models.CharField(
        max_length=20,
        default='Chờ duyệt'
    )

    ngay_dang_ky = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sinh_vien.ho_ten} - {self.su_kien.ten_su_kien}"

class FileThanhVienSuKien(models.Model):

    su_kien = models.ForeignKey(
        SuKien,
        on_delete=models.CASCADE
    )

    file_excel = models.FileField(
        upload_to='excel/'
    )

    ngay_upload = models.DateTimeField(
        auto_now_add=True
    )

class ThongBaoCLB(models.Model):

    clb = models.ForeignKey(
        CauLacBo,
        on_delete=models.CASCADE
    )

    tieu_de = models.CharField(max_length=200)

    noi_dung = models.TextField()

    ngay_tao = models.DateTimeField(
        auto_now_add=True
    )

class TaiLieuCLB(models.Model):

    clb = models.ForeignKey(
        CauLacBo,
        on_delete=models.CASCADE
    )

    ten_file = models.CharField(max_length=200)

    file = models.FileField(
        upload_to='tailieu/'
    )

    ngay_tao = models.DateTimeField(
        auto_now_add=True
    )

class TinNhanCLB(models.Model):

    clb = models.ForeignKey(
        CauLacBo,
        on_delete=models.CASCADE
    )

    nguoi_gui = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    noi_dung = models.TextField()

    ngay_gui = models.DateTimeField(
        auto_now_add=True
    )