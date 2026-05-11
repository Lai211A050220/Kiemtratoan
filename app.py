"""
Ung dung Tao De Kiem Tra Toan
- Cho phep chon lop, hinh thuc, thoi gian
- Tao de thi ngau nhien voi cau hoi trac nghiem va tu luan
- Xuat file PDF voi ho tro Unicode tieng Viet
"""

import os
import io
import zipfile
import random

import requests
import streamlit as st
from fpdf import FPDF


# === HAM TAI FONT === #
# Ham nay tai font DejaVu Sans tu GitHub ve thu muc fonts/ neu chua co
def tai_font():
    """Tai font DejaVu Sans (Regular va Bold) tu GitHub ve thu muc fonts/"""
    thu_muc_font = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
    os.makedirs(thu_muc_font, exist_ok=True)

    font_regular = os.path.join(thu_muc_font, "DejaVuSans.ttf")
    font_bold = os.path.join(thu_muc_font, "DejaVuSans-Bold.ttf")

    # Chi tai neu file chua ton tai
    if os.path.exists(font_regular) and os.path.exists(font_bold):
        return thu_muc_font

    # Tai file zip tu GitHub
    url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()

        # Giai nen cac file font can thiet
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for ten_file in z.namelist():
                if ten_file.endswith("DejaVuSans.ttf"):
                    with z.open(ten_file) as f:
                        with open(font_regular, "wb") as out:
                            out.write(f.read())
                elif ten_file.endswith("DejaVuSans-Bold.ttf"):
                    with z.open(ten_file) as f:
                        with open(font_bold, "wb") as out:
                            out.write(f.read())
    except Exception as e:
        st.error(f"Loi khi tai font: {e}")
        return None

    # Kiem tra lai sau khi tai xong
    if not os.path.exists(font_regular) or not os.path.exists(font_bold):
        st.error("Tai font khong thanh cong. Vui long thu lai.")
        return None

    return thu_muc_font


# === HAM TAO CAU HOI === #
# Tao cac cau hoi toan hoc mau theo lop va hinh thuc
def tao_cau_hoi_trac_nghiem(lop, so_cau):
    """Tao danh sach cau hoi trac nghiem theo lop"""
    cau_hoi_list = []

    # Ngan hang cau hoi mau theo lop
    ngan_hang = {
        "Lớp 6": [
            "Tính giá trị biểu thức: 12 + 5 × 3 - 8 =",
            "Tìm ƯCLN của 24 và 36:",
            "Số nào sau đây chia hết cho cả 2 và 3?",
            "Phân số tối giản của 12/18 là:",
            "Tính: (-5) + 8 - (-3) =",
            "Tìm BCNN của 6 và 8:",
            "Kết quả của 2³ × 3² là:",
            "Số đối của -7 là:",
            "Tìm x biết: x + 5 = 12",
            "Hình chữ nhật có chiều dài 8cm, chiều rộng 5cm. Chu vi là:",
        ],
        "Lớp 7": [
            "Tính: √49 + √16 =",
            "Giá trị của |−5| + |3| =",
            "Tỉ lệ thức nào sau đây đúng?",
            "Hai đường thẳng song song khi và chỉ khi:",
            "Tam giác có ba cạnh 3, 4, 5 là tam giác gì?",
            "Tính: (-2)³ × (-1)⁵ =",
            "Số hữu tỉ nào nằm giữa 1/3 và 1/2?",
            "Góc đối đỉnh có tính chất gì?",
            "Đại lượng y tỉ lệ thuận với x theo hệ số k=3. Khi x=5 thì y=",
            "Tổng ba góc trong tam giác bằng:",
        ],
        "Lớp 8": [
            "Phân tích đa thức thành nhân tử: x² - 9 =",
            "Rút gọn phân thức: (x²-1)/(x+1) =",
            "Nghiệm của phương trình 2x + 6 = 0 là:",
            "Hình thang cân có tính chất gì?",
            "Diện tích hình thoi có hai đường chéo 6cm và 8cm là:",
            "Giải bất phương trình: 3x - 9 > 0",
            "Tính thể tích hình hộp chữ nhật 3×4×5 cm:",
            "Khai triển (a+b)² =",
            "Đường trung bình của tam giác có tính chất:",
            "Giá trị của biểu thức x²+2x+1 tại x=-1 là:",
        ],
        "Lớp 9": [
            "Rút gọn: √12 + √27 - √3 =",
            "Nghiệm của phương trình x² - 5x + 6 = 0 là:",
            "Đường tròn (O;R) có chu vi bằng:",
            "Hàm số y = 2x - 1 cắt trục Ox tại điểm có tọa độ:",
            "sin²α + cos²α =",
            "Hệ phương trình x+y=5, x-y=1 có nghiệm:",
            "Tiếp tuyến của đường tròn vuông góc với:",
            "Góc nội tiếp bằng nửa:",
            "Diện tích hình quạt bán kính R, góc n° là:",
            "Phương trình bậc hai có delta < 0 thì:",
        ],
    }

    # Dap an mau cho cac cau hoi
    lua_chon_mau = {
        "Lớp 6": [
            ["19", "27", "23", "21"],
            ["6", "12", "8", "4"],
            ["12", "15", "18", "20"],
            ["2/3", "3/4", "4/6", "6/9"],
            ["6", "-6", "4", "16"],
            ["24", "48", "12", "6"],
            ["72", "36", "18", "12"],
            ["7", "-7", "1/7", "-1/7"],
            ["x = 7", "x = 17", "x = -7", "x = 5"],
            ["26 cm", "40 cm", "13 cm", "30 cm"],
        ],
        "Lớp 7": [
            ["11", "13", "9", "15"],
            ["8", "2", "-2", "5"],
            ["2/3 = 4/6", "1/2 = 3/5", "2/5 = 3/7", "4/7 = 8/15"],
            ["Có một cặp góc so le trong bằng nhau", "Cắt nhau", "Vuông góc", "Trùng nhau"],
            ["Vuông", "Cân", "Đều", "Nhọn"],
            ["8", "-8", "2", "-2"],
            ["5/12", "2/5", "2/7", "1/4"],
            ["Bằng nhau", "Bù nhau", "Kề nhau", "Phụ nhau"],
            ["15", "8", "2", "25"],
            ["180°", "360°", "90°", "270°"],
        ],
        "Lớp 8": [
            ["(x-3)(x+3)", "(x-3)²", "(x+3)²", "x(x-9)"],
            ["x-1", "x+1", "x²-1", "1/(x+1)"],
            ["x = -3", "x = 3", "x = 6", "x = -6"],
            ["Hai đường chéo bằng nhau", "Hai cạnh bên bằng nhau", "Cả A và B", "Không có tính chất đặc biệt"],
            ["24 cm²", "48 cm²", "14 cm²", "32 cm²"],
            ["x > 3", "x < 3", "x > -3", "x < -3"],
            ["60 cm³", "12 cm³", "20 cm³", "45 cm³"],
            ["a²+2ab+b²", "a²+b²", "a²-2ab+b²", "(a+b)(a-b)"],
            ["Song song và bằng nửa cạnh thứ ba", "Vuông góc với cạnh thứ ba", "Bằng cạnh thứ ba", "Song song với cạnh thứ ba"],
            ["0", "4", "1", "-1"],
        ],
        "Lớp 9": [
            ["4√3", "5√3", "6√3", "2√3"],
            ["x=2, x=3", "x=-2, x=-3", "x=1, x=6", "x=-1, x=-6"],
            ["2πR", "πR²", "πR", "4πR"],
            ["(1/2; 0)", "(0; -1)", "(1; 0)", "(-1/2; 0)"],
            ["1", "0", "2", "-1"],
            ["x=3, y=2", "x=2, y=3", "x=5, y=0", "x=0, y=5"],
            ["Bán kính tại tiếp điểm", "Dây cung", "Đường kính", "Cát tuyến"],
            ["Số đo cung bị chắn", "Góc ở tâm", "Đường kính", "Bán kính"],
            ["πR²n/360", "2πRn/360", "πRn/180", "πR²n/180"],
            ["Vô nghiệm", "Có 2 nghiệm", "Có 1 nghiệm", "Có vô số nghiệm"],
        ],
    }

    ds_cau_hoi = ngan_hang.get(lop, ngan_hang["Lớp 6"])
    ds_lua_chon = lua_chon_mau.get(lop, lua_chon_mau["Lớp 6"])

    # Tao danh sach chi muc va xao tron de ngau nhien hoa thu tu cau hoi
    indices = list(range(len(ds_cau_hoi)))
    random.shuffle(indices)

    for i in range(so_cau):
        # Voi so cau vuot qua ngan hang (du lieu mau), dung modulo nhung thu tu da xao tron
        idx = indices[i % len(ds_cau_hoi)]
        cau_hoi_list.append({
            "noi_dung": ds_cau_hoi[idx],
            "lua_chon": ds_lua_chon[idx],
            "dap_an": "A",  # Dap an dung luon la phan tu dau tien trong danh sach lua chon
        })

    return cau_hoi_list


def tao_cau_hoi_tu_luan(lop, so_cau):
    """Tao danh sach cau hoi tu luan theo lop"""
    cau_hoi_list = []

    ngan_hang = {
        "Lớp 6": [
            "Tìm tất cả các ước của 36. Cho biết 36 có bao nhiêu ước?",
            "Tính giá trị biểu thức: A = 15 × 23 + 15 × 77 - 15 × 100",
            "Ba bạn An, Bình, Chi có tổng cộng 120 viên bi. Biết số bi An gấp đôi Bình, số bi Chi bằng 1/3 số bi An. Tìm số bi mỗi bạn.",
            "Tìm x biết: (2x + 1) × 3 = 27",
            "Vẽ hình và tính chu vi, diện tích hình chữ nhật có chiều dài 12cm, chiều rộng 7cm.",
        ],
        "Lớp 7": [
            "Chứng minh rằng tổng ba góc trong một tam giác bằng 180°.",
            "Cho tam giác ABC cân tại A, đường cao AH. Chứng minh BH = HC.",
            "Tính giá trị biểu thức: M = |2x - 3| + |x + 1| tại x = -2",
            "Hai đại lượng x và y tỉ lệ thuận. Khi x = 4 thì y = 12. Tìm y khi x = 7.",
            "Vẽ đồ thị hàm số y = 2x - 1 trên mặt phẳng tọa độ.",
        ],
        "Lớp 8": [
            "Phân tích đa thức thành nhân tử: P = x³ - 3x² + 3x - 1",
            "Giải phương trình: (x+2)/(x-2) - (x-2)/(x+2) = 16/(x²-4)",
            "Cho hình bình hành ABCD. Gọi M, N lần lượt là trung điểm AB và CD. Chứng minh AMCN là hình bình hành.",
            "Tính thể tích và diện tích toàn phần của hình lăng trụ đứng có đáy là tam giác vuông cạnh 3cm, 4cm, 5cm và chiều cao 10cm.",
            "Giải bất phương trình và biểu diễn tập nghiệm: 2(x-1) - 3(x+2) < 4x - 5",
        ],
        "Lớp 9": [
            "Giải hệ phương trình: 2x + 3y = 7 và x - 2y = -3",
            "Cho đường tròn (O;R) và điểm A nằm ngoài đường tròn. Kẻ hai tiếp tuyến AB, AC. Chứng minh OA là trung trực của BC.",
            "Rút gọn biểu thức: P = (√x + 1)/(√x - 1) - (√x - 1)/(√x + 1) + 4√x/(x-1) với x > 0, x ≠ 1",
            "Một thửa đất hình chữ nhật có chu vi 40m. Nếu tăng chiều dài 3m và giảm chiều rộng 2m thì diện tích tăng 4m². Tìm kích thước thửa đất.",
            "Vẽ đồ thị hàm số y = x² và y = 2x - 1 trên cùng hệ trục. Tìm tọa độ giao điểm.",
        ],
    }

    ds_cau_hoi = ngan_hang.get(lop, ngan_hang["Lớp 6"])

    # Tao danh sach chi muc va xao tron de ngau nhien hoa thu tu cau hoi
    indices = list(range(len(ds_cau_hoi)))
    random.shuffle(indices)

    for i in range(so_cau):
        # Voi so cau vuot qua ngan hang (du lieu mau), dung modulo nhung thu tu da xao tron
        idx = indices[i % len(ds_cau_hoi)]
        cau_hoi_list.append({
            "noi_dung": ds_cau_hoi[idx],
        })

    return cau_hoi_list


# === HAM TINH DIEM === #
# Chia diem deu cho cac cau, phan du cho cau cuoi
def tinh_diem(tong_cau, tong_diem=100):
    """Tinh diem cho moi cau hoi, tong diem = 100"""
    if tong_cau == 0:
        return []
    diem_moi_cau = tong_diem // tong_cau
    phan_du = tong_diem - diem_moi_cau * tong_cau
    ds_diem = [diem_moi_cau] * tong_cau
    # Phan du chia cho cac cau cuoi
    for i in range(phan_du):
        ds_diem[tong_cau - 1 - i] += 1
    return ds_diem


# === HAM TAO PDF === #
# Tao file PDF voi ho tro Unicode tieng Viet
class PDFKiemTra(FPDF):
    """Lop PDF tu dinh nghia voi footer ban quyen"""

    def __init__(self, font_path, font_bold_path):
        super().__init__()
        self.font_path = font_path
        self.font_bold_path = font_bold_path

    def header(self):
        pass  # Khong can header mac dinh

    def footer(self):
        """Footer ban quyen hien thi o cuoi moi trang"""
        self.set_y(-20)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, "Bản quyền của Nguyễn Kim Thu - Trường Phùng Hưng", align="C")


def tao_pdf(lop, thoi_gian_phut, cau_trac_nghiem, cau_tu_luan, diem_trac_nghiem, diem_tu_luan):
    """Tao file PDF de kiem tra voi font DejaVu Sans ho tro tieng Viet"""
    thu_muc_font = tai_font()

    # Kiem tra font da duoc tai chua
    if thu_muc_font is None:
        return None

    font_path = os.path.join(thu_muc_font, "DejaVuSans.ttf")
    font_bold_path = os.path.join(thu_muc_font, "DejaVuSans-Bold.ttf")

    # Kiem tra font da duoc tai chua
    if not os.path.exists(font_path) or not os.path.exists(font_bold_path):
        st.error("Khong tim thay font. Vui long thu lai.")
        return None

    # Khoi tao PDF voi margin rong va auto page break
    pdf = PDFKiemTra(font_path, font_bold_path)
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=25)

    # Them font DejaVu Sans ho tro Unicode tieng Viet
    pdf.add_font("DejaVu", "", font_path)
    pdf.add_font("DejaVu", "B", font_bold_path)

    pdf.add_page()

    # Chieu rong kha dung = trang A4 (210mm) - margin trai (15) - margin phai (15) = 180mm
    w = pdf.w - pdf.l_margin - pdf.r_margin

    # Tieu de
    so_lop = lop.replace("Lớp ", "")
    pdf.set_font("DejaVu", "B", 13)
    pdf.multi_cell(w, 8, f"ĐỀ KIỂM TRA TOÁN - LỚP {so_lop}\nTHỜI GIAN: {thoi_gian_phut} PHÚT", align="C")
    pdf.ln(4)

    # Thong tin chung
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(w, 6, "Tổng điểm: 100 điểm", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    so_thu_tu = 1

    # Phan trac nghiem
    if cau_trac_nghiem:
        pdf.set_font("DejaVu", "B", 11)
        pdf.cell(w, 8, "PHẦN I: TRẮC NGHIỆM", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        for i, cau in enumerate(cau_trac_nghiem):
            diem = diem_trac_nghiem[i]
            pdf.set_font("DejaVu", "B", 10)
            pdf.multi_cell(w, 6, f"Câu {so_thu_tu} ({diem} điểm): {cau['noi_dung']}")

            pdf.set_font("DejaVu", "", 9)
            lua_chon = cau["lua_chon"]
            # Hien thi moi lua chon tren 1 dong rieng de tranh loi tran ngang
            for j, lc in enumerate(lua_chon):
                nhan = chr(65 + j)  # A, B, C, D
                pdf.cell(5, 5, "")  # Thut le
                pdf.multi_cell(w - 5, 5, f"{nhan}. {lc}")
            pdf.ln(2)
            so_thu_tu += 1

    # Phan tu luan
    if cau_tu_luan:
        pdf.set_font("DejaVu", "B", 11)
        phan = "II" if cau_trac_nghiem else "I"
        pdf.cell(w, 8, f"PHẦN {phan}: TỰ LUẬN", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        for i, cau in enumerate(cau_tu_luan):
            diem = diem_tu_luan[i]
            pdf.set_font("DejaVu", "B", 10)
            pdf.multi_cell(w, 6, f"Câu {so_thu_tu} ({diem} điểm): {cau['noi_dung']}")
            pdf.ln(3)
            so_thu_tu += 1

    # Xuat PDF ra bytes
    return bytes(pdf.output())


# === GIAO DIEN STREAMLIT === #
# Cau hinh trang va thanh ben (sidebar)
st.set_page_config(page_title="Tạo Đề Kiểm Tra Toán", page_icon="📐", layout="wide")
st.title("📐 Tạo Đề Kiểm Tra Toán")
st.markdown("---")

# Thanh ben - cau hinh de thi
st.sidebar.header("⚙️ Cấu hình đề thi")

# Chon lop
lop = st.sidebar.selectbox("Chọn lớp:", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"])

# Chon hinh thuc thi
hinh_thuc = st.sidebar.radio("Hình thức:", ["Trắc nghiệm", "Tự luận", "Kết hợp"])

# Thanh truot ty le chi hien khi chon "Ket hop"
ty_le_trac_nghiem = 70  # Gia tri mac dinh
if hinh_thuc == "Kết hợp":
    ty_le_trac_nghiem = st.sidebar.slider(
        "Tỷ lệ trắc nghiệm:",
        min_value=30,
        max_value=90,
        value=70,
        step=5,
        format="%d%%",
        help="Phần trăm câu hỏi trắc nghiệm trong đề"
    )
    ty_le_tu_luan = 100 - ty_le_trac_nghiem
    st.sidebar.info(f"{ty_le_trac_nghiem}% Trắc nghiệm - {ty_le_tu_luan}% Tự luận")

# Chon thoi gian va so cau
thoi_gian_lua_chon = st.sidebar.selectbox(
    "Thời gian - Số câu:",
    ["15 phút - 20 câu", "60 phút - 50 câu", "90 phút - 70 câu"]
)

# Phan tich thoi gian va so cau tu lua chon
phan_tach = thoi_gian_lua_chon.split(" - ")
thoi_gian_phut = int(phan_tach[0].replace(" phút", ""))
tong_cau = int(phan_tach[1].replace(" câu", ""))

# Hien thi thong tin da chon
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Lớp:** {lop}")
st.sidebar.markdown(f"**Hình thức:** {hinh_thuc}")
st.sidebar.markdown(f"**Thời gian:** {thoi_gian_phut} phút")
st.sidebar.markdown(f"**Tổng số câu:** {tong_cau}")

# === XU LY TAO DE THI === #
# Nut tao de thi
if st.button("🎯 Tạo đề thi", type="primary"):
    with st.spinner("Đang tạo đề thi..."):
        # Tinh so cau trac nghiem va tu luan
        if hinh_thuc == "Trắc nghiệm":
            so_trac_nghiem = tong_cau
            so_tu_luan = 0
        elif hinh_thuc == "Tự luận":
            so_trac_nghiem = 0
            so_tu_luan = tong_cau
        else:  # Ket hop
            so_trac_nghiem = round(tong_cau * ty_le_trac_nghiem / 100)
            so_tu_luan = tong_cau - so_trac_nghiem

        # Tao cau hoi
        cau_trac_nghiem = tao_cau_hoi_trac_nghiem(lop, so_trac_nghiem)
        cau_tu_luan = tao_cau_hoi_tu_luan(lop, so_tu_luan)

        # Tinh diem cho moi cau
        ds_diem = tinh_diem(tong_cau, 100)
        diem_trac_nghiem = ds_diem[:so_trac_nghiem]
        diem_tu_luan = ds_diem[so_trac_nghiem:]

        # Hien thi xem truoc de thi
        st.success("✅ Đã tạo đề thi thành công!")
        st.markdown("---")

        # Xem truoc phan trac nghiem
        if cau_trac_nghiem:
            st.subheader("PHẦN I: TRẮC NGHIỆM")
            for i, cau in enumerate(cau_trac_nghiem):
                diem = diem_trac_nghiem[i]
                st.markdown(f"**Câu {i+1} ({diem} điểm):** {cau['noi_dung']}")
                cols = st.columns(4)
                for j, lc in enumerate(cau["lua_chon"]):
                    cols[j].write(f"{chr(65+j)}. {lc}")

        # Xem truoc phan tu luan
        if cau_tu_luan:
            phan = "II" if cau_trac_nghiem else "I"
            st.subheader(f"PHẦN {phan}: TỰ LUẬN")
            offset = so_trac_nghiem
            for i, cau in enumerate(cau_tu_luan):
                diem = diem_tu_luan[i]
                st.markdown(f"**Câu {offset + i + 1} ({diem} điểm):** {cau['noi_dung']}")

        # Tao PDF
        pdf_bytes = tao_pdf(lop, thoi_gian_phut, cau_trac_nghiem, cau_tu_luan, diem_trac_nghiem, diem_tu_luan)

        if pdf_bytes:
            # Nut tai xuong PDF
            st.markdown("---")
            st.download_button(
                label="📥 Tải xuống PDF",
                data=pdf_bytes,
                file_name=f"de_kiem_tra_toan_{lop.replace(' ', '_')}_{thoi_gian_phut}phut.pdf",
                mime="application/pdf",
            )
