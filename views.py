from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CauLacBo, ThanhVien, SuKien
from django.http import HttpResponseForbidden
from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from .models import (CauLacBo, ThanhVien, SuKien, HoSoSinhVien, DangKyCLB, DangKySuKien,TinNhanCLB
                     )
import pandas as pd
from django.contrib import messages
# ======================
# TRANG CHỦ
# ======================
def home(request):

    tong_clb = CauLacBo.objects.count()
    tong_tv = ThanhVien.objects.count()
    tong_sk = SuKien.objects.count()

    return render(
        request,
        'club/home.html',
        {
            'tong_clb': tong_clb,
            'tong_tv': tong_tv,
            'tong_sk': tong_sk,
        }
    )


# ======================
# DANH SÁCH CLB
# ======================
@login_required
def clubs(request):

    profile = HoSoSinhVien.objects.filter(
        user=request.user
    ).first()

    if profile and profile.clb_quan_ly:

        clb = profile.clb_quan_ly

        # GỬI TIN NHẮN
        if request.method == "POST":

            noi_dung = request.POST.get(
                "noi_dung"
            )

            if noi_dung:

                TinNhanCLB.objects.create(
                    clb=clb,
                    nguoi_gui=profile,
                    noi_dung=noi_dung
                )

                return redirect("clubs")

        profile = HoSoSinhVien.objects.get(
        user=request.user
        )

        clb = profile.clb_quan_ly

        thanh_vien = HoSoSinhVien.objects.filter(
            clb=clb
        )
        return render(
            request,
        'club/clb_dashboard.html',
        {
        'clb': clb,
        'thanh_vien': thanh_vien
        }
        )


    ds_clb = CauLacBo.objects.all()

    return render(
        request,
        'club/clubs.html',
        {
            'ds_clb': ds_clb
        }
    )

# ======================
# SỰ KIỆN
# ======================
@login_required
def events(request):

    ds_sk = SuKien.objects.all()

    profile = HoSoSinhVien.objects.filter(
        user=request.user
    ).first()

    return render(
        request,
        'club/events.html',
        {
            'ds_sk': ds_sk,
            'profile': profile
        }
    )


@login_required
def upload_ds_sukien(request, sukien_id):

    sk = SuKien.objects.get(id=sukien_id)

    if request.method == 'POST':

        file = request.FILES.get('excel_file')

    if not file:

        messages.error(
            request,
            "Vui lòng chọn file Excel"
        )

    return redirect(
            f'/sukien/{sk.id}/thanhvien/'
        )

    try:

        # Bỏ dòng "DANH SÁCH SINH VIÊN"
        df = pd.read_excel(
            file,
            header=1
        )

        for _, row in df.iterrows():

            mssv = str(
                row['Mã sinh viên']
            ).strip()

            if not mssv or mssv == 'nan':
                continue

            try:

                sv = HoSoSinhVien.objects.get(
                    mssv=mssv
                )

                DangKySuKien.objects.get_or_create(
                    sinh_vien=sv,
                    su_kien=sk,
                    defaults={
                        'trang_thai': 'Đã duyệt'
                    }
                )

            except HoSoSinhVien.DoesNotExist:

                print(
                    f"Không tìm thấy MSSV: {mssv}"
                )

                continue

        messages.success(
            request,
            "Upload danh sách thành công"
        )

    except Exception as e:

        messages.error(
            request,
            f"Lỗi upload: {e}"
        )

    return redirect(
    f'/sukien/{sk.id}/thanhvien/'
)
# ======================
# QUẢN LÝ SỰ KIỆN
# ======================


@login_required
def quanly_sukien(request):

    profile = HoSoSinhVien.objects.get(
        user=request.user
    )

    clb = profile.clb_quan_ly

    ds_su_kien = SuKien.objects.all()

    return render(
        request,
        'club/quanly_sukien.html',
        {
            'ds_su_kien': ds_su_kien
        }
    )


@login_required
def them_sukien(request):

    profile = HoSoSinhVien.objects.get(
        user=request.user
    )

    clb = profile.clb_quan_ly

    if request.method == "POST":

        SuKien.objects.create(
        ten_su_kien=request.POST.get("ten_su_kien"),
        ngay_to_chuc=request.POST.get("ngay_to_chuc"),
        dia_diem=request.POST.get("dia_diem"),
        mo_ta=request.POST.get("mo_ta")
        )

        return redirect("events")

    return render(
    request,
    "club/them_sukien.html",
    {
        "clb": clb
    }
    )


@login_required
def sua_sukien(request, id):

    profile = HoSoSinhVien.objects.filter(
    user=request.user
    ).first()

    if not (
    request.user.is_superuser
    or (profile and profile.clb_quan_ly)
    ):
        return HttpResponseForbidden("Bạn không có quyền")

    sk = SuKien.objects.get(id=id)

    if request.method == "POST":

        sk.ten_su_kien = request.POST.get(
        "ten_su_kien"
    )

    sk.ngay_to_chuc = request.POST.get(
        "ngay_to_chuc"
    )

    sk.dia_diem = request.POST.get(
        "dia_diem"
    )

    sk.mo_ta = request.POST.get(
        "mo_ta"
    )

    if profile and profile.clb_quan_ly:
        sk.clb = profile.clb_quan_ly

    sk.save()

    return redirect("events")

    return render(
        request,
        "club/sua_sukien.html",
        {
            "sk": sk
        }
    )
@login_required
def xoa_sukien(request, id):

    profile = HoSoSinhVien.objects.filter(
    user=request.user
    ).first()

    if not (
    request.user.is_superuser
    or (profile and profile.clb_quan_ly)
    ):
        return HttpResponseForbidden("Bạn không có quyền")
    sk = SuKien.objects.get(id=id)

    sk.delete()

    return redirect('events')

@login_required
def xoa_thanh_vien(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền")

    tv = ThanhVien.objects.get(id=id)

    tv.delete()

    return redirect('thanh_vien')

@login_required
def thanhvien_sukien(request, id):

    sk = SuKien.objects.get(id=id)

    ds_dangky = DangKySuKien.objects.filter(
        su_kien=sk
    )

    return render(
        request,
        'club/thanhvien_sukien.html',
        {
            'su_kien': sk,
            'ds_dangky': ds_dangky
        }
    )

@login_required
def duyet_sukien(request, id):

    dk = DangKySuKien.objects.get(id=id)

    dk.trang_thai = "Đã duyệt"

    dk.save()

    return redirect(
        f'/sukien/{dk.su_kien.id}/thanhvien/'
    )

@login_required
def tuchoi_sukien(request, id):

    dk = DangKySuKien.objects.get(id=id)

    dk.trang_thai = "Từ chối"

    dk.save()

    return redirect(
        f'/sukien/{dk.su_kien.id}/thanhvien/'
    )
# ======================
# ĐĂNG KÝ CLB
# ======================
from django.contrib import messages

@login_required
def register(request):

    ds_clb = CauLacBo.objects.all()

    if request.method == "POST":

        clb_id = request.POST.get("clb")

        sinh_vien = HoSoSinhVien.objects.get(
            user=request.user
        )

        clb = CauLacBo.objects.get(
            id=clb_id
        )

        if not DangKyCLB.objects.filter(
            sinh_vien=sinh_vien,
            clb=clb
        ).exists():

            DangKyCLB.objects.create(
                sinh_vien=sinh_vien,
                clb=clb
            )

            messages.success(
                request,
                f"🎉 Đăng ký tham gia {clb.ten_clb} thành công!"
            )

        else:

            messages.warning(
                request,
                f"⚠️ Bạn đã tham gia {clb.ten_clb} rồi!"
            )

        return redirect("profile")

    return render(
        request,
        "club/register.html",
        {
            "ds_clb": ds_clb
        }
    )




# ======================
# THÀNH VIÊN
# ======================
@staff_member_required
def thanh_vien(request):

    q = request.GET.get('q')

    ds_tv = HoSoSinhVien.objects.all()

    if q:
        ds_tv = ds_tv.filter(
        ho_ten__icontains=q
    )

    ds_clb = CauLacBo.objects.all()

    return render(
    request,
    'club/thanh_vien.html',
    {
        'ds_tv': ds_tv,
        'ds_clb': ds_clb
    }
)

from .models import CauLacBo, DangKyCLB

@login_required
def thanh_vien_clb(request, id):

    clb = CauLacBo.objects.get(id=id)

    ds_tv = HoSoSinhVien.objects.filter(
        clb=clb
    )

    return render(
        request,
        'club/thanh_vien_clb.html',
        {
            'clb': clb,
            'ds_tv': ds_tv
        }
    )

@login_required
def duyet_thanh_vien(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền")

    dk = DangKyCLB.objects.get(id=id)

    dk.trang_thai = "Đã duyệt"

    dk.save()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def them_thanh_vien(request):

    profile = HoSoSinhVien.objects.get(
        user=request.user
    )

    if not profile.clb_quan_ly:
        return redirect('clubs')
    
    if request.method == "POST":

        ho_ten = request.POST.get("ho_ten")
        mssv = request.POST.get("mssv")
        lop = request.POST.get("lop")
        khoa = request.POST.get("khoa")
        email = request.POST.get("email")
        password = request.POST.get("password")
        vai_tro = request.POST.get("vai_tro")
        

        user = User.objects.create_user(
            username=mssv,
            email=email,
            password=password
        )

        if vai_tro == "Admin":
            user.is_staff = True
            user.is_superuser = True

        elif vai_tro == "CanBo":
            user.is_staff = True

        user.save()

        profile = HoSoSinhVien.objects.get(
    user=request.user
)

    HoSoSinhVien.objects.create(
    user=user,
    ho_ten=ho_ten,
    lop=lop,
    khoa=khoa,
    email=email,
    vai_tro=vai_tro,
    clb=profile.clb_quan_ly
)
    return redirect("thanh_vien")



# ======================
# ĐĂNG NHẬP
# ======================
def login_view(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('profile')

        message = "Sai tài khoản hoặc mật khẩu"

    return render(
        request,
        'club/login.html',
        {'message': message}
    )


# ======================
# ĐĂNG XUẤT
# ======================
def logout_view(request):
    logout(request)
    return redirect('home')


# ======================
# DASHBOARD
# ======================
@login_required
def dashboard(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền truy cập")

    tong_clb = CauLacBo.objects.count()
    tong_tv = ThanhVien.objects.count()
    tong_sk = SuKien.objects.count()

    ds_clb = CauLacBo.objects.order_by('-id')[:5]
    ds_sk = SuKien.objects.order_by('-id')[:5]

    return render(
        request,
        'club/dashboard.html',
        {
            'tong_clb': tong_clb,
            'tong_tv': tong_tv,
            'tong_sk': tong_sk,
            'ds_clb': ds_clb,
            'ds_sk': ds_sk
        }
    )

@login_required
def clb_dashboard(request):

    profile = HoSoSinhVien.objects.get(user=request.user)

    return render(
        request,
        'club/clb_dashboard.html',
        {
            'profile': profile
        }
    )


# ======================
# QUẢN LÝ CLB
# ======================

@login_required
def quanly_clb(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền")

    ds_clb = CauLacBo.objects.all()

    return render(
        request,
        'club/quanly_clb.html',
        {'ds_clb': ds_clb}
    )


@login_required
def them_clb(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền")

    if request.method == 'POST':

        CauLacBo.objects.create(
            ten_clb=request.POST.get('ten_clb'),
            mo_ta=request.POST.get('mo_ta'),
            hinh_anh=request.FILES.get('hinh_anh')
        )

    return redirect('clubs')

    return render(
        request,
        'club/them_clb.html'
    )


@login_required
def sua_clb(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền")

    clb = CauLacBo.objects.get(id=id)

    if request.method == "POST":

        clb.ten_clb = request.POST.get("ten_clb", clb.ten_clb)

        mo_ta = request.POST.get("mo_ta")

        if mo_ta:
            clb.mo_ta = mo_ta

        if request.FILES.get("hinh_anh"):
            clb.hinh_anh = request.FILES["hinh_anh"]

        profile = HoSoSinhVien.objects.get(
            user=request.user
        )

        if not request.user.is_superuser:

            if profile.clb_quan_ly != clb:

                return HttpResponseForbidden(
                "Bạn không có quyền"
            )
        clb.save()

        return redirect("clubs")
 
    return render(
        request,
        "club/sua_clb.html",
        {"clb": clb}
    )


@login_required
def xoa_clb(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền")

    clb = CauLacBo.objects.get(id=id)

    clb.delete()

    return redirect('clubs')

@login_required
def phan_quyen_clb(request, id):

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    tv = HoSoSinhVien.objects.get(id=id)

    clb_id = request.POST.get("clb")

    tv.clb_quan_ly_id = clb_id

    tv.user.is_staff = True

    tv.user.save()

    tv.save()

    return redirect('thanh_vien')

@login_required
def tieu_su_clb(request):

    profile = HoSoSinhVien.objects.get(
        user=request.user
    )

    clb = profile.clb_quan_ly

    if request.method == 'POST':

        clb.gioi_thieu = request.POST.get(
            'gioi_thieu'
        )

        clb.save()

    return render(
        request,
        'club/tieu_su_clb.html',
        {
            'clb': clb
        }
    )

@login_required
def sua_tieu_su_clb(request):

    profile = HoSoSinhVien.objects.get(
        user=request.user
    )

    clb = profile.clb_quan_ly

    if request.method == 'POST':

        clb.gioi_thieu = request.POST.get(
            'gioi_thieu'
        )

        clb.save()

        messages.success(
            request,
            'Đã cập nhật tiểu sử CLB'
        )

        return redirect('clubs')

    return render(
        request,
        'club/sua_tieu_su_clb.html',
        {
            'clb': clb
        }
    )

# ======================
# ĐĂNG KÝ TÀI KHOẢN
# ======================
def register_user(request):

    message = ""

    if request.method == "POST":

        ho_ten = request.POST.get("ho_ten")
        mssv = request.POST.get("mssv")
        lop = request.POST.get("lop")
        khoa = request.POST.get("khoa")

        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email.endswith("@tnut.edu.vn"):

            message = "Email phải có đuôi @tnut.edu.vn"

        elif len(password) < 8:

            message = "Mật khẩu phải từ 8 ký tự trở lên"

        elif User.objects.filter(username=mssv).exists():

            message = "MSSV đã tồn tại"

        else:

            user = User.objects.create_user(
                username=mssv,
                email=email,
                password=password
            )

            HoSoSinhVien.objects.create(
                user=user,
                ho_ten=ho_ten,
                mssv=mssv,
                lop=lop,
                khoa=khoa,
                email=email
            )

            return redirect('login')

    return render(
        request,
        'club/register_user.html',
        {'message': message}
    )

@login_required
def profile(request):

    profile = HoSoSinhVien.objects.filter(
        user=request.user
    ).first()

    if not profile:

        return render(
            request,
            'club/profile.html',
            {
                'profile': None,
                'ds_clb': [],
                'ds_sukien': []
            }
        )

    ds_clb = DangKyCLB.objects.filter(
        sinh_vien=profile
    )

    ds_sukien = DangKySuKien.objects.filter(
        sinh_vien=profile
    )

    return render(
        request,
        'club/profile.html',
        {
            'profile': profile,
            'ds_clb': ds_clb,
            'ds_sukien': ds_sukien
        }
    )

@login_required
def dangky_sukien(request, id):

    profile = HoSoSinhVien.objects.get(
        user=request.user
    )

    sk = SuKien.objects.get(id=id)

    DangKySuKien.objects.get_or_create(
        sinh_vien=profile,
        su_kien=sk
    )

    return redirect('events')
# ======================
# PHÂN QUYỀN ADMIN
# ======================
@login_required
def cap_quyen_admin(request, user_id):

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = User.objects.get(id=user_id)

    user.is_staff = True
    user.is_superuser = True

    user.save()

    return redirect('thanh_vien')

@login_required
def doi_quyen(request, user_id):

    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = User.objects.get(id=user_id)

    vai_tro = request.POST.get("vai_tro")

    if vai_tro == "Admin":

        user.is_staff = True
        user.is_superuser = True

    elif vai_tro == "CanBo":

        user.is_staff = True
        user.is_superuser = False

    else:

        user.is_staff = False
        user.is_superuser = False

        try:

            hs = HoSoSinhVien.objects.get(
                user=user
            )

            hs.clb_quan_ly = None

            hs.save()

        except:
            pass

    user.save()

    return redirect("thanh_vien")

@login_required
def phan_cong_clb(request, id):

    if not request.user.is_superuser:
        return redirect('home')

    tv = HoSoSinhVien.objects.get(id=id)

    clb_id = request.POST.get('clb_id')

    if clb_id:

        tv.clb_quan_ly = CauLacBo.objects.get(
            id=clb_id
        )

    else:

        tv.clb_quan_ly = None

    tv.save()

    return redirect('thanh_vien')

