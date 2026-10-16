# Tối ưu lập lịch đa máy

Ứng dụng Flask phục vụ học tập và so sánh năm nhóm thuật toán lập lịch: **Greedy, Genetic Algorithm (GA), Branch and Bound (B&B), Tabu Search (TS) và CP-SAT**. LPT, EDD và WSPT là ba quy tắc ưu tiên trong nhóm Greedy.

## Bài toán

Có n công việc và m máy song song giống nhau. Mỗi công việc có mã `id`, thời lượng `p`, hạn hoàn thành `d` và trọng số `w`.

- Mọi công việc sẵn sàng tại thời điểm 0.
- Mỗi việc chạy liên tục trên đúng một máy; các việc trên cùng máy không chồng lấn.
- Không xét thời gian thiết lập, quan hệ trước–sau hoặc hỏng máy.
- Thời lượng và các mốc lập lịch tính theo **giờ**; thời gian chạy thuật toán tính theo **giây**.

Mục tiêu là tối thiểu tổng độ trễ có trọng số:

```text
C_i = S_i + p_i
T_i = max(0, C_i - d_i)
F   = Σ w_i × T_i
```

`S_i` là giờ bắt đầu, `C_i` là giờ hoàn thành. Hạn là hạn mềm: hoàn thành sau hạn vẫn được phép nhưng chịu phạt. Hoàn thành sớm không tạo độ trễ âm.

**Makespan** là `max(C_i)`, chỉ dùng để báo cáo. Lịch có makespan nhỏ hơn chưa chắc có F nhỏ hơn; F = 0 không có nghĩa là chưa tìm được lịch.

## Tính năng

### Phòng thử nghiệm thuật toán

Tab mặc định có lựa chọn số máy, số việc, mức hạn và tham số GA. Sau khi sinh dữ liệu, bảng hiển thị đúng bộ việc dùng để chạy. Kết quả gồm F, makespan, runtime, nhận xét và Gantt của năm thuật toán.

Các ô tốt nhất và thao tác chính dùng highlight xanh lá sáng. Công việc trễ trên Gantt có màu đỏ, dấu `!` và viền nét đứt. Có thể chọn thanh công việc bằng chuột hoặc bàn phím để xem chi tiết.

### Lý thuyết thuật toán

Giải thích bài toán, ký hiệu, quy tắc ưu tiên, công thức, các bước thực hiện, ví dụ tính tay, cây B&B, toán tử GA, dấu vết TS và mô hình CP-SAT. Có mục lục nội bộ và tài liệu tham khảo học thuật.

Chuyển tab không tải lại trang, không gọi lại thuật toán và giữ nguyên dữ liệu, cấu hình, kết quả, biểu đồ. Dùng mũi tên trái/phải, Home và End để chuyển tab bằng bàn phím.

## Cài đặt và chạy

Đã kiểm tra với **Python 3.11**. Sử dụng terminal tại thư mục gốc dự án.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Mở [http://127.0.0.1:5000](http://127.0.0.1:5000). Để tránh dùng nhầm môi trường Python, các lệnh trên gọi trực tiếp Python trong `.venv`.

Phụ thuộc chính được ghim trong `requirements.txt`: Flask 3.0.3 và OR-Tools 9.15.6755. Nếu thiếu OR-Tools, CP-SAT báo `UNAVAILABLE` cùng hướng dẫn cài, các thuật toán khác vẫn chạy.

`app.py` chạy Flask ở chế độ phát triển, không phải cấu hình triển khai production. Font Be Vietnam Pro tải từ Google Fonts; khi không truy cập được mạng, giao diện dùng font hệ thống dự phòng.

## Thuật toán và giới hạn

| Nhóm | Cách hoạt động | Mặc định / giới hạn |
| --- | --- | --- |
| Greedy | Chạy LPT, EDD, WSPT rồi chọn lịch có F thấp nhất | Hòa F giữ quy tắc trước theo thứ tự LPT → EDD → WSPT; runtime là tổng ba lượt |
| GA | Hoán vị công việc, giải mã vào máy rảnh sớm nhất, lai ghép và đổi chỗ | Quần thể 60; 120 thế hệ; xác suất lai 0,8; đột biến 0,1 |
| B&B | Duyệt thứ tự công việc và cách phân máy, cắt nhánh bằng cận dưới, loại máy đối xứng | Chỉ chạy khi n ≤ 10; tối đa 5 giây; khởi tạo bằng EDD |
| TS | Khởi tạo theo hạn, đổi chỗ hai việc, tabu theo cặp và ngoại lệ khi cải thiện tốt nhất | Tối đa 100 vòng, thời hạn cấm 7 vòng |
| CP-SAT | Biến thời điểm, chọn máy, optional interval và NoOverlap; tối thiểu F | Giới hạn tìm kiếm 10 giây |

Greedy, GA và TS không mặc nhiên bảo đảm tối ưu. B&B chỉ chứng minh tối ưu khi hoàn tất tìm kiếm; hết giờ trả lịch tốt nhất với `TIME_LIMIT`. CP-SAT chỉ có `optimal=true` khi trạng thái là `OPTIMAL`; `FEASIBLE` chỉ xác nhận đã có lịch.

CP-SAT yêu cầu p, d, w là số nguyên, không chấp nhận bool hoặc float kể cả `1.0`; p và w không âm, d có thể âm. Các hàm thuật toán khác chưa có lớp kiểm tra dữ liệu đầy đủ khi gọi trực tiếp; nên dùng dữ liệu đúng miền bài toán. GA được dùng trong miền tham số giao diện hợp lệ, không hỗ trợ tùy ý mọi giá trị quần thể/số thế hệ.

## Sinh dữ liệu theo tải máy

Backend là nơi duy nhất sinh dữ liệu: p nguyên từ 3–20 giờ, w nguyên từ 1–5. Đặt:

```text
H = max(p lớn nhất, tổng p / số máy)
```

| Mức hạn | Khoảng d |
| --- | --- |
| Chặt | 0,5H–0,9H |
| Vừa (mặc định) | 0,8H–1,2H |
| Rộng | 1,2H–1,8H |

Cận dưới làm tròn lên và ít nhất bằng p của việc; cận trên làm tròn xuống, nâng bằng cận dưới nếu cần. Mức chặt tăng khả năng trễ, không bảo đảm mọi bộ đều có F > 0. Đổi mức hạn rồi bấm **Sinh dữ liệu** để áp dụng cho bộ mới.

## Cấu trúc mã nguồn

```text
app.py                         Khởi tạo Flask
requirements.txt               Phụ thuộc Python
scheduling/
  jobs.py                      Sinh dữ liệu
  metrics.py                   Tính F, makespan và độ trễ
  greedy.py                    LPT, EDD, WSPT
  genetic.py                   GA, decoder và toán tử di truyền
  branch_and_bound.py          B&B
  tabu_search.py               TS
  cp_sat.py                    Mô hình OR-Tools
  service.py                   Điều phối, đo runtime, tạo kết quả
web/routes.py                  Trang chủ và API
templates/
  index.html                   Header, hai tab và phòng thử nghiệm
  theory.html                  Nội dung lý thuyết và ví dụ
static/
  app.js                       Tương tác thử nghiệm và Gantt
  tabs.js                      Chuyển tab và mục lục lý thuyết
  style.css                    Theme, typography, responsive
  theory_examples.json         Dữ liệu minh họa đã kiểm chứng
scripts/
  build_theory_examples.py      Sinh lại dữ liệu minh họa ngoại tuyến
```

Các thư mục trên cần được giữ trong Git. `static/theory_examples.json` cần có khi khởi động trang chủ; không bỏ qua file này như một file tạm.

## API

- `GET /`: giao diện hai tab.
- `POST /api/generate`: nhận `machines`, `jobs` (số việc), `deadline_level` (`tight`, `medium`, `wide`).
- `POST /api/run`: nhận `machines`, danh sách `jobs`, `population`, `generations`, `crossover`, `mutation`.

Kết quả chạy giữ các khóa `greedy`, `lpt`, `ga`, `bb`, `ts`, `cp_sat`. Khóa `lpt` riêng được giữ để tương thích, không phải nhóm thứ sáu trong bảng so sánh. CP-SAT trả thêm `status`, `best_bound`, `optimal`; khi chưa có lịch, `objective` và `schedule` là `null`, không phải 0. Service dùng `time.perf_counter()` để đo runtime và tính lại chỉ số từ lịch khả thi.

## Dữ liệu minh họa và kiểm tra

Ví dụ lý thuyết được chuẩn bị trước, không chạy solver khi chuyển tab. Để sinh lại sau khi thay đổi thuật toán:

```powershell
.\.venv\Scripts\python.exe scripts/build_theory_examples.py
```

Script cần OR-Tools, dùng GA seed 2718 và khôi phục trạng thái ngẫu nhiên sau khi chạy. Trên bộ năm việc, hai máy: LPT = 93, EDD = 48, WSPT = 86; GA, B&B, TS và CP-SAT đều đạt 48. Vét cạn độc lập xác nhận tối ưu là 48.

**Theo cấu hình Git hiện tại, thư mục `tests/` được bỏ qua và không đi kèm bản clone mới.** Nếu bộ kiểm thử vẫn có trên máy phát triển, chạy:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
node tests/test_frontend.cjs
node tests/test_tabs.cjs
```

Bộ kiểm tra cục bộ gồm tính hợp lệ của lịch, tính lại F, đối chiếu vét cạn, trường hợp biên, thiếu OR-Tools, API, các ví dụ và việc chuyển tab giữ trạng thái. Đã kiểm tra giao diện bằng viewport desktop/mobile giả lập; chưa thay thế thử thiết bị thật, kiểm toán accessibility đầy đủ hoặc đo hiệu năng quy mô lớn.

## Quy tắc Git

`.gitignore` bỏ qua `tests/`, môi trường ảo, cache Python/kiểm thử, cấu hình IDE, công cụ trợ lý cục bộ (`.agents/`, `.codex/`), file môi trường riêng, log và thư mục build. Các file bị bỏ qua vẫn giữ trên máy. `.env.example` có thể được theo dõi để cung cấp mẫu cấu hình không chứa bí mật.

Thay đổi `.gitignore` không tự ngừng theo dõi file đã commit; cần bỏ chúng khỏi Git index, không xóa khỏi ổ đĩa.
