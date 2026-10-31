# 14. Thiết kế giao diện và trải nghiệm người dùng (UI/UX)

> Tài liệu này là **nguồn quy tắc duy nhất** cho mọi tác vụ giao diện của
> TrafficSign AI. Quy tắc được xây dựng theo bộ nguyên tắc **Design Pro
> Max** (Taste-Skill + UI/UX Pro Max), điều chỉnh cho bối cảnh đồ án:
> công cụ nhận diện biển báo, trình diễn học thuật, tính trung thực của
> kết quả quan trọng hơn hiệu ứng.
>
> Liên quan: `REQUIREMENTS.md` (FR-01..FR-12), `API_SPEC.md`,
> `DEMO_CHECKLIST.md`, `TESTING_EVALUATION.md`, `AGENTS.md`.

------------------------------------------------------------------------

## 14.0. Design Read và ba "núm vặn"

### 14.0.1. Design Read

> **Reading this as:** *Product UI / công cụ phân tích ảnh* cho *sinh
> viên, giảng viên và người dùng phổ thông Việt Nam*, với ngôn ngữ
> *rõ ràng -- đáng tin -- kỹ thuật vừa phải*, nghiêng về thẩm mỹ
> *Modern Minimalist + Industrial (đường kẻ mảnh, số liệu monospace)*,
> lấy cảm hứng từ hệ thống **biển báo giao thông** (hình dạng + màu
> mang ý nghĩa).

| Yếu tố | Kết luận |
| :--- | :--- |
| Loại trang | Ứng dụng công cụ (không phải landing page marketing) |
| Người dùng | Giảng viên chấm đồ án, sinh viên, người dùng phổ thông |
| Bối cảnh chính | Demo 5--7 phút trên máy chiếu, chạy local, không Internet |
| Tài sản thương hiệu | Chưa có logo/màu → tự định nghĩa ở mục 14.2 |
| Giá trị cốt lõi | Trung thực về độ tin cậy, dễ đọc, nhanh hiểu |

### 14.0.2. Ba núm vặn (khác baseline 8/6/4 của skill)

| Núm vặn | Giá trị | Lý do |
| :--- | :---: | :--- |
| `DESIGN_VARIANCE` | **4** | Công cụ cần bố cục ổn định, dự đoán được; chỉ trang *Đánh giá* dùng bento nhẹ |
| `MOTION_INTENSITY` | **3** | Chỉ micro-interaction có mục đích (phản hồi trạng thái, liên kết box ↔ thẻ). Không scroll choreography |
| `VISUAL_DENSITY` | **5** | Màn hình kết quả có nhiều thông tin (box, confidence, ý nghĩa, nguồn) nhưng phải đọc được trên máy chiếu |

### 14.0.3. Danh sách cấm (Anti-Default) áp dụng cho dự án

- ❌ Không dùng tím/violet "AI glow", gradient mesh, nền blob.
- ❌ Không hero căn giữa + 3 thẻ tính năng giống hệt nhau.
- ❌ Không mặc định Inter + Slate-900 (xem 14.3 -- dùng font hỗ trợ tốt
  tiếng Việt).
- ❌ Không ảnh chụp màn hình giả dựng bằng div; không ảnh do AI sinh
  được trình bày như *kết quả nhận diện thật*.
- ❌ Không vẽ biển báo giả bằng CSS/emoji. Ảnh biển chỉ dùng
  `image_url` có quyền sử dụng (`DATABASE.md` §8.2), nếu không có thì
  dùng glyph hình dạng nhóm (14.2.3).
- ❌ Không emoji làm icon UI (🚫 ⚠️ ✅).
- ❌ Không thanh tiến trình giả lập các bước xử lý (backend xử lý trong
  một request, frontend không biết tiến độ thật).
- ❌ Không ngôn ngữ phóng đại: "chính xác tuyệt đối", "AI thông minh nhận
  diện mọi biển".

------------------------------------------------------------------------

## 14.1. Nền tảng kỹ thuật giao diện

| Hạng mục | Quyết định | Ghi chú |
| :--- | :--- | :--- |
| Framework | React + TypeScript + Vite | Theo `AGENTS.md`, D-002 |
| Styling | **Vanilla CSS + CSS Modules + CSS custom properties** | Token tập trung tại `src/styles/tokens.css`. Không thêm Tailwind/UI kit lớn nếu nhóm chưa quyết định |
| Primitive truy cập | Tùy chọn `@radix-ui/react-*` (Dialog, Tabs, Tooltip, Slider) | Chỉ thêm khi cần, ghi vào `DECISIONS.md` |
| Icon | **Phosphor Icons** (`@phosphor-icons/react`), weight `regular`, size 20/24 | Một họ icon duy nhất, không trộn |
| Motion | CSS transitions; tùy chọn `motion` (Motion for React) cho stagger thẻ kết quả | Luôn tôn trọng `prefers-reduced-motion` |
| Font | Tự host (`@fontsource`) để chạy **offline** khi demo | `DEMO_CHECKLIST.md`: không phụ thuộc Internet |

Cấu trúc style đề xuất:

``` text
frontend/src/
├── styles/
│   ├── tokens.css      # màu, font, spacing, radius, shadow, motion
│   ├── base.css        # reset, typography mặc định, focus ring
│   └── utilities.css   # một số tiện ích nhỏ (visually-hidden, stack)
├── components/         # mỗi component có .tsx + .module.css
└── pages/
```

------------------------------------------------------------------------

## 14.2. Màu sắc

### 14.2.1. Nguyên tắc

1. **Một màu nhấn duy nhất (One Accent Rule):** *Teal tín hiệu*
   `#0F766E`. Không trùng nghĩa với màu nhóm biển báo (đỏ/vàng/xanh
   dương), tránh người xem hiểu nhầm nút bấm là biển báo.
2. **Màu biển báo là màu dữ liệu, không phải màu thương hiệu.** Chỉ dùng
   cho chip nhóm, viền bounding box và thẻ kết quả.
3. **Khóa một theme (Theme Lock):** MVP dùng **giao diện sáng**. Lý do:
   máy chiếu làm mất độ tương phản của theme tối; ảnh đường phố hiển thị
   trung thực hơn trên nền trung tính sáng. Không xen section tối giữa
   trang sáng.
4. **WCAG AA:** chữ thường ≥ 4.5:1, chữ lớn ≥ 3:1. Không chỉ dùng màu để
   truyền đạt trạng thái -- luôn kèm icon + chữ.
5. Độ bão hòa màu nhấn < 80%; không dùng gradient trang trí.

### 14.2.2. Bảng token

``` css
/* src/styles/tokens.css */
:root {
  /* Nền & bề mặt — trung tính zinc, tránh bẫy be/nâu */
  --color-bg:            #FAFAFA;
  --color-surface:       #FFFFFF;
  --color-surface-2:     #F4F4F5;
  --color-border:        #E4E4E7;
  --color-border-strong: #D4D4D8;

  /* Chữ */
  --color-text:          #18181B; /* 17.7:1 trên trắng */
  --color-text-muted:    #52525B; /* 7.7:1 */
  --color-text-subtle:   #71717A; /* 4.8:1 — chỉ cho chú thích */

  /* Màu nhấn duy nhất */
  --color-accent:        #0F766E; /* 5.5:1 với chữ trắng */
  --color-accent-hover:  #115E59;
  --color-accent-soft:   #CCFBF1;
  --color-accent-ink:    #134E4A;
  --color-focus:         #0F766E;

  /* Màu nhóm biển báo (dữ liệu) */
  --sign-prohibitory:      #C8102E; /* Biển cấm — 5.9:1 */
  --sign-prohibitory-soft: #FDECEE;
  --sign-danger:           #F2B705; /* Biển nguy hiểm — CHỈ làm nền/viền */
  --sign-danger-ink:       #8A6100; /* chữ trên nền trắng — 5.5:1 */
  --sign-danger-soft:      #FEF6D8;
  --sign-mandatory:        #0B5CAD; /* Biển hiệu lệnh — 6.7:1 */
  --sign-mandatory-soft:   #E7F0FA;
  --sign-guide:            #1E3A8A; /* Biển chỉ dẫn */
  --sign-guide-soft:       #E8ECF7;
  --sign-unknown:          #52525B; /* Chưa có trong catalog */

  /* Trạng thái hệ thống */
  --status-uncertain:      #B45309; /* Cần xác minh — 5.0:1 */
  --status-uncertain-soft: #FEF3C7;
  --status-error:          #B91C1C;
  --status-error-soft:     #FEE2E2;
  --status-info:           #0369A1;
  --status-info-soft:      #E0F2FE;
}
```

> Trạng thái "đã nhận diện" **không** dùng xanh lá ăn mừng. Dùng trung
> tính + icon `CheckCircle` để tránh tạo cảm giác kết quả chắc chắn
> đúng (nguyên tắc trung thực của đồ án).

### 14.2.3. Mã hóa nhóm biển báo: Màu + Hình dạng + Chữ

| Nhóm (`group_name`) | Màu token | Glyph hình dạng | Nhãn chip |
| :--- | :--- | :--- | :--- |
| Biển cấm | `--sign-prohibitory` | Vòng tròn có gạch chéo | "Biển cấm" |
| Biển nguy hiểm/cảnh báo | `--sign-danger` (chữ `--sign-danger-ink`) | Tam giác | "Nguy hiểm" |
| Biển hiệu lệnh | `--sign-mandatory` | Hình tròn đặc | "Hiệu lệnh" |
| Biển chỉ dẫn | `--sign-guide` | Hình vuông/chữ nhật | "Chỉ dẫn" |
| Không có trong catalog | `--sign-unknown` | Dấu hỏi | "Chưa có thông tin" |

Glyph là SVG trừu tượng (hình học), **không** mô phỏng biển báo cụ thể.

### 14.2.4. Mức cảnh báo (`warning_level`)

| Giá trị | Token | Icon Phosphor | Nhãn |
| :--- | :--- | :--- | :--- |
| `high` | `--status-error` | `WarningOctagon` | Mức cao |
| `medium` | `--status-uncertain` | `Warning` | Trung bình |
| `low` | `--color-text-muted` | `Info` | Thấp |
| `info` | `--status-info` | `Info` | Thông tin |

------------------------------------------------------------------------

## 14.3. Typography

### 14.3.1. Cặp font

| Vai trò | Font | Lý do |
| :--- | :--- | :--- |
| Heading + Body | **Be Vietnam Pro** (400/500/600/700) | Thiết kế cho tiếng Việt, dấu thanh chồng (ở, ữ, ặ) hiển thị chuẩn; tránh mặc định Inter |
| Số liệu, mã | **JetBrains Mono** (400/500) | `sign_code`, confidence, `processing_ms`, `request_id`, bảng metrics; có hỗ trợ tiếng Việt |

Không dùng serif. Không dùng quá 2 họ font.

### 14.3.2. Thang chữ

``` css
:root {
  --font-sans: "Be Vietnam Pro", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --text-xs:   0.75rem;  /* 12px — chú thích, nguồn */
  --text-sm:   0.875rem; /* 14px — nhãn, meta */
  --text-base: 1rem;     /* 16px — body tối thiểu */
  --text-lg:   1.125rem; /* 18px — tiêu đề thẻ */
  --text-xl:   1.375rem; /* 22px — tiêu đề section */
  --text-2xl:  1.75rem;  /* 28px — tiêu đề trang */
  --text-3xl:  2.5rem;   /* 40px — tiêu đề trang Quét ảnh */
}
```

Quy tắc:
- Tiêu đề lớn: `letter-spacing: -0.02em; line-height: 1.1`. Với tiếng
  Việt, **không** dùng `line-height` < 1.1 để dấu không bị cắt.
- Body: `line-height: 1.6; color: var(--color-text-muted); max-width: 65ch`.
- Số liệu dùng `font-variant-numeric: tabular-nums` để cột thẳng hàng.
- Confidence hiển thị dạng phần trăm số nguyên (`0.93` → `93%`); bảng
  metrics giữ 3 chữ số thập phân như log gốc, không làm tròn quá mức
  (`REPORT_GUIDE.md`).

------------------------------------------------------------------------

## 14.4. Spacing, radius, shadow, motion tokens

``` css
:root {
  /* Spacing — lưới 4px */
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px; --space-4: 16px;
  --space-5: 20px; --space-6: 24px;  --space-8: 32px; --space-10: 40px;
  --space-12: 48px; --space-16: 64px; --space-24: 96px;

  /* Radius — vừa phải, không "bong bóng" */
  --radius-sm: 6px; --radius-md: 10px; --radius-lg: 14px; --radius-full: 999px;

  /* Shadow — tinh tế, dựa vào border là chính */
  --shadow-sm: 0 1px 2px rgb(24 24 27 / 0.06);
  --shadow-md: 0 4px 12px rgb(24 24 27 / 0.08);

  /* Motion */
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --dur-fast:    120ms;
  --dur-base:    200ms;
  --dur-slow:    320ms;

  /* Layout */
  --nav-height: 64px;
  --content-max: 1280px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

------------------------------------------------------------------------

## 14.5. Kiến trúc thông tin và điều hướng

### 14.5.1. Sơ đồ trang

| Route | Tên trang | Mức độ | Yêu cầu liên quan |
| :--- | :--- | :--- | :--- |
| `/` | **Quét ảnh** | Must | FR-01..FR-09, FR-11 |
| `/signs` | Tra cứu biển báo | Should | `GET /signs` |
| `/signs/:id` | Chi tiết biển báo | Should | `GET /signs/{id}` |
| `/history` | Lịch sử quét | Should | FR-10, `GET /history` |
| `/evaluation` | Đánh giá mô hình | Must (demo bước 7) | `TESTING_EVALUATION.md` |
| `/about` | Giới thiệu & nguồn | Should | FR-12 |

Trang chưa triển khai **ẩn khỏi nav**, không để link chết.

### 14.5.2. Thanh điều hướng

- Desktop: cao **64px**, một dòng, ≤ 5 liên kết: *Quét ảnh · Tra cứu ·
  Lịch sử · Đánh giá · Giới thiệu*.
- Bên phải nav: **chỉ báo trạng thái model** từ `GET /health`:
  - `model_loaded = true` → chấm trung tính + "Model sẵn sàng" +
    `model_version` (mono, `--text-xs`).
  - `false` / lỗi mạng → chấm `--status-error` + "Model chưa sẵn sàng".
    Nút tải ảnh bị vô hiệu kèm giải thích (TC-10).
- Mobile (< 768px): logo + chỉ báo model ở top bar; **bottom nav ≤ 5
  tab**, icon + nhãn, mỗi tab ≥ 44×44px.
- Liên kết hiện tại: `aria-current="page"`, gạch chân 2px màu nhấn.

### 14.5.3. Footer

Một dòng cố định nội dung: *"Prototype phục vụ học tập. Không thay thế
việc quan sát biển báo thực tế."* + link *Giới thiệu & nguồn*.

------------------------------------------------------------------------

## 14.6. Trang Quét ảnh (màn hình chính)

### 14.6.1. Trạng thái ban đầu (chưa chọn ảnh)

Áp dụng quy tắc *Hero Viewport Fit* cho công cụ: toàn bộ vùng tải ảnh
phải nằm trong viewport đầu tiên (`min-height: 100dvh` trừ nav, không
dùng `100vh`; padding trên ≤ 96px).

Text stack tối đa 4 phần tử:
1. Tiêu đề (≤ 2 dòng): **"Nhận diện biển báo giao thông từ ảnh"**
2. Mô tả (≤ 20 từ): *"Tải ảnh đường phố lên để phát hiện biển báo và
   xem ý nghĩa, khuyến nghị đã được kiểm chứng."*
3. Vùng thao tác: **Dropzone** + tab *Tải ảnh / Chụp ảnh* (camera chỉ
   hiện khi hỗ trợ).
4. Dòng quyền riêng tư (`--text-sm`, icon `ShieldCheck`): *"Ảnh được xử
   lý trong bộ nhớ và không được lưu mặc định."*

Không đặt danh sách tính năng, logo đối tác hay số liệu trong vùng này.
Danh sách lớp được hỗ trợ đặt **bên dưới** dưới dạng link "Xem các biển
báo hệ thống hỗ trợ (N lớp)" → `/signs`.

**Dropzone:**
- Kích thước tối thiểu 320×200px, viền nét đứt `--color-border-strong`,
  icon `UploadSimple` 32px.
- Nhãn: *"Kéo thả ảnh vào đây hoặc **Chọn ảnh**"*; dòng phụ: *"JPG, PNG
  · tối đa {MAX_MB} MB"* (giá trị đọc từ cấu hình, không hardcode).
- Toàn vùng là `<label>` cho `<input type="file" accept="image/jpeg,image/png">`
  → bấm được, focus được bằng bàn phím.
- Hover/drag-over: nền `--color-accent-soft`, viền liền `--color-accent`.
- Kiểm tra sơ bộ phía client (định dạng, dung lượng) để phản hồi nhanh;
  **backend vẫn là nơi quyết định** (`ARCHITECTURE.md` §3.4).

**Tùy chọn nâng cao** (thu gọn mặc định, `<details>`):
- *Ngưỡng confidence* -- slider 0.05--0.95, nhãn **phía trên**, hiển thị
  giá trị mono, helper: *"Server có thể giới hạn giá trị này."*
  Dùng để minh họa câu hỏi nghiên cứu về ngưỡng (`PROJECT_OVERVIEW.md`
  §1.10).
- *Lưu vào lịch sử* -- switch, **mặc định tắt** (D-007), helper nói rõ
  sẽ lưu gì (metadata, không lưu ảnh gốc).

### 14.6.2. Trạng thái đang xử lý

- Hiển thị ảnh xem trước (object URL) mờ 60% + overlay *"Đang phân tích
  ảnh…"* với spinner nhỏ và **bộ đếm thời gian thực** (giây). Không
  hiển thị các bước giả.
- Cột kết quả hiện **skeleton** 2 thẻ, giữ đúng kích thước để không gây
  CLS.
- Nút gửi chuyển `aria-busy="true"`, vô hiệu để tránh gửi trùng.
- Vùng `aria-live="polite"` thông báo "Đang phân tích ảnh".

### 14.6.3. Trạng thái có kết quả

Bố cục desktop (≥ 1200px): lưới 12 cột, **ảnh 7 cột (sticky) · danh
sách kết quả 5 cột**. Tablet: 6/6. Mobile: xếp dọc, ảnh trước.

**Thanh tóm tắt** (trên cùng cột kết quả):
`2 biển báo được phát hiện · 184 ms · Model v{version}` -- số liệu mono.
Ghi chú `--text-xs`: *"Thời gian xử lý phía server."*

**Khung ảnh kết quả (`ResultCanvas`):**
- Hiển thị ảnh gốc + **lớp SVG overlay** vẽ bounding box từ `bbox`
  trong JSON. SVG dùng `viewBox="0 0 {image.width} {image.height}"` nên
  tọa độ pixel gốc tự co giãn theo khung, không cần tự quy đổi.
- `annotated_image` từ API dùng cho nút *Tải ảnh kết quả* và chế độ so
  sánh; overlay SVG phục vụ tương tác.
- Khung giữ tỷ lệ bằng `aspect-ratio: {width} / {height}` → không CLS.
- Box: viền 3px màu nhóm (`vector-effect: non-scaling-stroke`), góc
  vuông; detection cần xác minh dùng **viền nét đứt**.
- Nhãn box: chip đặc màu nhóm, chữ tương phản đạt AA, nội dung
  `{số thứ tự} · {confidence}%` (ví dụ `1 · 93%`). Không đặt tên dài
  lên ảnh.
- Segmented control *Kết quả / Ảnh gốc* (FR "so sánh ảnh" -- Could).
- Nút phụ: *Tải ảnh kết quả* · *Quét ảnh khác*.

**Liên kết box ↔ thẻ:** hover/focus một box làm nổi thẻ tương ứng và
ngược lại (thẻ khác giảm opacity 0.5, box được chọn dày 4px). Box là
phần tử focus được (`tabindex="0"`, `role="button"`,
`aria-label="Biển 1: {tên}, độ tin cậy 93%"`). Click box cuộn tới thẻ.

**Thẻ kết quả (`DetectionCard`)** -- thứ tự nội dung:

1. Hàng đầu: số thứ tự (khớp nhãn box) · ảnh/glyph nhóm 40px · **tên
   biển** (`--text-lg`, 600) · chip nhóm.
2. Hàng meta: `sign_code` (mono) · **Confidence meter** (thanh ngang 4px
   + số `93%`).
3. **Ý nghĩa** (`meaning`).
4. **Khuyến nghị** (`recommended_action`) trong khối nền
   `--color-surface-2`, icon theo `warning_level` + nhãn mức.
5. Chân thẻ: *Nguồn:* `source` · *Kiểm tra ngày:* `source_checked_at`
   (`--text-xs`) · link *Xem chi tiết* → `/signs/:id`.

**Biến thể thẻ theo nghiệp vụ (bắt buộc):**

| Điều kiện | Hiển thị | Quy tắc |
| :--- | :--- | :--- |
| `verification_required = false`, có catalog | Thẻ đầy đủ như trên | -- |
| `verification_required = true` (confidence < ngưỡng) | Viền trái 3px `--status-uncertain`, badge `Question` **"Kết quả chưa chắc chắn"**, tiêu đề đổi thành *"Có thể là: {tên}"* | FR-09, quy tắc nghiệp vụ 2. Không trình bày như khẳng định |
| Class không có trong catalog | Glyph dấu hỏi, tiêu đề `class_name`, thông báo *"Nhãn này chưa có thông tin được kiểm chứng trong catalog."* **Không hiển thị** ý nghĩa/khuyến nghị | FR-06, TC-11, quy tắc nghiệp vụ 1 |

Sắp xếp thẻ: theo confidence giảm dần; số thứ tự gán theo thứ tự này.
Thẻ xuất hiện với stagger 60ms, dịch 8px, `--ease-out` (tắt khi reduced
motion).

**Khối giới hạn** (cuối cột, luôn hiện, thu gọn được):
*"Kết quả chỉ mang tính tham khảo. Ngữ cảnh đường và biển phụ có thể
thay đổi ý nghĩa. Không phát hiện biển báo không có nghĩa là ảnh không
có biển báo."*

### 14.6.4. Trạng thái không phát hiện (`detection_count = 0`)

- Không hiển thị box hay thẻ giả (FR-08).
- Empty state trong cột kết quả: icon `MagnifyingGlass`, tiêu đề
  **"Không phát hiện biển báo trong phạm vi hỗ trợ"**, mô tả: *"Biển có
  thể quá nhỏ, bị che, thiếu sáng hoặc không thuộc {N} lớp hệ thống hỗ
  trợ."*
- Hành động: *Thử ảnh khác* (primary) · *Xem các lớp hỗ trợ* (link).

### 14.6.5. Trạng thái lỗi (ánh xạ từ `API_SPEC.md` §7.6)

Lỗi hiển thị **ngay tại dropzone** (inline), không chỉ toast. Icon
`WarningCircle`, màu `--status-error`, có hành động khắc phục.

| Code | Thông điệp hiển thị | Hành động |
| :--- | :--- | :--- |
| `INVALID_IMAGE` | Không thể đọc ảnh. Tệp có thể bị hỏng. | Chọn ảnh khác |
| `FILE_TOO_LARGE` | Ảnh vượt quá {MAX_MB} MB. | Chọn ảnh nhỏ hơn |
| `UNSUPPORTED_MEDIA_TYPE` | Chỉ hỗ trợ ảnh JPG hoặc PNG. | Chọn ảnh khác |
| `INVALID_PARAMETER` | Tùy chọn không hợp lệ. Đã khôi phục mặc định. | Thử lại |
| `INFERENCE_ERROR` | Đã xảy ra lỗi khi phân tích ảnh. | Thử lại |
| `MODEL_NOT_READY` | Model chưa sẵn sàng. Vui lòng chờ hoặc kiểm tra server. | Kiểm tra lại |
| Lỗi mạng | Không kết nối được tới server. | Thử lại |

- Hiển thị `request_id` (mono, `--text-xs`, có nút sao chép) để đối chiếu
  log. **Không** hiển thị stack trace hay đường dẫn nội bộ.
- Thông điệp: nói chuyện gì xảy ra + làm gì tiếp; không đổ lỗi người dùng.

### 14.6.6. Chụp ảnh từ camera (FR-11, Could)

- Tab *Chụp ảnh* chỉ hiển thị khi `navigator.mediaDevices` có sẵn và
  trang chạy HTTPS/localhost; nếu không, tab hiện ở trạng thái vô hiệu
  với tooltip giải thích.
- Luồng: Bật camera (người dùng chủ động bấm) → xem trực tiếp → *Chụp* →
  xem lại → *Dùng ảnh này* / *Chụp lại*. Không tự động gửi.
- Từ chối quyền: hướng dẫn bật lại trong trình duyệt + gợi ý dùng *Tải
  ảnh*.
- Tắt stream ngay khi rời tab hoặc đã chụp.

------------------------------------------------------------------------

## 14.7. Các trang khác

### 14.7.1. Tra cứu biển báo (`/signs`)

- Ô tìm kiếm có **label phía trên** ("Tìm theo tên hoặc mã biển"),
  debounce 300ms, đồng bộ query `q` lên URL.
- Bộ lọc nhóm: segmented chip *Tất cả · Cấm · Nguy hiểm · Hiệu lệnh · Chỉ
  dẫn* (mỗi chip có glyph hình dạng).
- Lưới thẻ: 4 cột desktop / 2 tablet / 1 mobile. Thẻ: ảnh/glyph,
  tên, `sign_code`, chip nhóm. Ảnh `loading="lazy"` + kích thước cố định.
- Phân trang theo `page`/`page_size`; nút ≥ 44px.
- Empty: *"Không tìm thấy biển báo phù hợp."* + *Xóa bộ lọc*.

### 14.7.2. Chi tiết biển báo (`/signs/:id`)

Bố cục dọc, độ rộng đọc ≤ 72ch: breadcrumb → ảnh + tên + mã + nhóm →
Ý nghĩa → Khuyến nghị → Nguồn pháp lý (`legal_source`) + ngày kiểm tra
+ ngày cập nhật. Thiếu nguồn → không hiển thị phần diễn giải pháp lý.

### 14.7.3. Lịch sử quét (`/history`, Should)

- Bảng: Thời gian · Tên tệp · Số biển · Thời gian xử lý (ms) · Trạng
  thái. Số căn phải, mono.
- Mobile: chuyển sang danh sách thẻ, không cuộn ngang bảng.
- Bộ lọc thời gian/lớp (Should) đặt trên bảng, label phía trên.
- Empty: *"Chưa có lịch sử. Lịch sử chỉ được ghi khi bật 'Lưu vào lịch
  sử' lúc quét."*
- Nếu tính năng tắt ở server → ẩn route khỏi nav.

### 14.7.4. Đánh giá mô hình (`/evaluation`)

Trang duy nhất dùng **bento grid** (Variance 4 → bento nhẹ, đều đặn):

| Ô | Nội dung | Kích thước |
| :--- | :--- | :--- |
| 1 | Thông tin thí nghiệm: dataset + phiên bản, số ảnh/instance test, model, ngưỡng conf/IoU, thiết bị | 2 cột |
| 2--6 | Precision · Recall · F1 · mAP@0.5 · mAP@0.5:0.95 (số mono lớn + nhãn) | 1 cột mỗi ô |
| 7 | Latency: trung vị/trung bình + số lần đo, tách preprocess/inference/postprocess | 2 cột |
| 8 | Confusion matrix (`confusion_matrix.png` thật) | 2 cột |
| 9 | PR curve (`PR_curve.png` thật) | 2 cột |
| 10 | Bảng chỉ số theo lớp | toàn chiều rộng |

Quy tắc:
- Số ô = số nội dung thực có; **không để ô trống**. Ít nhất 2 ô chứa
  hình thật (confusion matrix, PR curve).
- Dữ liệu đọc từ `evaluation.json`/`results.csv`. Nếu chưa có: hiển thị
  *"Chưa có kết quả đánh giá trên tập test độc lập"* -- **tuyệt đối
  không** điền số mẫu (`AGENTS.md`: không tạo số liệu giả).
- Ghi rõ "Đánh giá trên tập test độc lập, ngưỡng chọn trên validation".
- Mục *Ví dụ thành công và thất bại*: lưới ảnh thật kèm nhãn thật, dự
  đoán, confidence, nguyên nhân khả dĩ (`TESTING_EVALUATION.md` §9.4).
  Không chỉ chọn ảnh đẹp.

### 14.7.5. Giới thiệu & nguồn (`/about`)

Thứ tự: Mục đích & phạm vi → Danh sách lớp hỗ trợ → Giới hạn đã biết →
Nguồn dữ liệu (tên, URL, license, ngày truy cập) → Nguồn pháp lý (văn
bản, ngày kiểm tra) → Công nghệ & phiên bản model.
Không dùng bố cục zigzag ảnh trái/chữ phải quá 2 section liên tiếp; ưu
tiên một cột văn bản dễ đọc.

------------------------------------------------------------------------

## 14.8. Thư viện component và trạng thái

Mỗi component tương tác phải có đủ: **default · hover · focus-visible ·
active · disabled · loading** (nếu áp dụng).

| Component | Ghi chú bắt buộc |
| :--- | :--- |
| `Button` (primary/secondary/ghost) | Cao 44px (sm: 36px chỉ desktop), nhãn 1 dòng ≤ 3 từ; `:active` → `transform: translateY(1px) scale(0.98)`; **một primary mỗi viewport** |
| `IconButton` | Bắt buộc `aria-label`; vùng chạm 44×44 |
| `Dropzone` | Xem 14.6.1; trạng thái idle / drag-over / validating / error |
| `ResultCanvas` | Overlay SVG, aspect-ratio cố định, box focus được |
| `DetectionCard` | 3 biến thể (14.6.3); skeleton cùng kích thước |
| `ConfidenceMeter` | Thanh + số; `role="meter"` + `aria-valuenow`; màu theo trạng thái, không chỉ dựa vào màu |
| `SignGroupChip` | Glyph + màu + chữ |
| `StatusBadge` | Model ready / not ready / uncertain |
| `EmptyState` | Icon + tiêu đề + mô tả + 1 hành động |
| `InlineError` | Icon + thông điệp + hành động + `request_id` |
| `Skeleton` | Shimmer nhẹ 1.2s; tĩnh khi reduced motion |
| `Toast` | Chỉ cho thông báo phụ (đã sao chép, đã tải về); không dùng cho lỗi chính |

Focus ring toàn cục:

``` css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
/* Không bao giờ dùng outline: none mà không có thay thế */
```

------------------------------------------------------------------------

## 14.9. Motion

Nguyên tắc: **chuyển động phải có lý do** (phản hồi, liên kết, thứ tự).

| Tương tác | Hiệu ứng | Thời lượng |
| :--- | :--- | :--- |
| Hover nút/thẻ | Đổi nền/viền | `--dur-fast` |
| Bấm nút | translateY(1px) scale(0.98) | `--dur-fast` |
| Box xuất hiện | `stroke-dashoffset` vẽ viền | `--dur-slow` |
| Thẻ kết quả xuất hiện | opacity 0→1, y 8→0, stagger 60ms | `--dur-base` |
| Liên kết box ↔ thẻ | Độ dày viền + opacity thẻ khác | `--dur-base` |
| Chuyển trang | Không animation (công cụ cần nhanh) | -- |

Nếu dùng Motion for React cho stagger, tham khảo mẫu `RevealStagger`
trong skill nhưng thay `whileInView` bằng `animate` (thẻ hiển thị ngay
khi có kết quả) và luôn kiểm tra `useReducedMotion()`.
Không dùng GSAP/scroll-pinning cho dự án này.

------------------------------------------------------------------------

## 14.10. Responsive

| Breakpoint | Bố cục |
| :--- | :--- |
| < 768px | Một cột; bottom nav; ảnh kết quả full-width, thẻ bên dưới; bảng → thẻ |
| 768--1199px | Quét ảnh 6/6; lưới tra cứu 2 cột; bento 2 cột |
| ≥ 1200px | Quét ảnh 7/5 (ảnh sticky); lưới tra cứu 4 cột; bento 4 cột |

- Mọi hàng nhiều cột **phải có** layout mobile được định nghĩa rõ.
- Kiểm thử chính trên desktop hiện đại (`REQUIREMENTS.md` §2.3); mobile
  ở mức dùng được.
- Kiểm tra riêng **độ phân giải máy chiếu 1280×720** và zoom 125%:
  vùng tải ảnh và nút chính phải thấy được không cần cuộn.

------------------------------------------------------------------------

## 14.11. Truy cập (Accessibility) -- WCAG 2.1 AA

- Toàn bộ luồng *chọn ảnh → gửi → đọc kết quả* thực hiện được bằng bàn
  phím.
- Ảnh kết quả có `alt` tóm tắt: *"Ảnh kết quả: phát hiện 2 biển báo --
  1. {tên} 93%, 2. {tên} 71% (chưa chắc chắn)."* Danh sách thẻ là phương
  án tương đương văn bản.
- Thay đổi trạng thái (đang xử lý, hoàn tất, lỗi) được thông báo qua
  `aria-live="polite"`; lỗi chặn dùng `role="alert"`.
- Sau khi có kết quả, focus chuyển tới tiêu đề tóm tắt kết quả.
- Tiêu đề trang theo cấp: một `<h1>` mỗi trang, không nhảy cấp.
- `lang="vi"` trên `<html>`; `<title>` riêng từng trang
  ("Quét ảnh · TrafficSign AI").
- Vùng chạm ≥ 44×44px, khoảng cách giữa các đích ≥ 8px.
- Không có tương tác chỉ dựa vào hover.

------------------------------------------------------------------------

## 14.12. Hiệu năng

- Xem trước ảnh bằng `URL.createObjectURL` và `revokeObjectURL` khi
  không dùng nữa.
- Mọi ảnh có kích thước/aspect-ratio dành sẵn → CLS < 0.1.
- Ảnh catalog: WebP, `loading="lazy"`, `decoding="async"`.
- Font tự host, `font-display: swap`, chỉ subset `latin` + `vietnamese`.
- Không tải thư viện biểu đồ chỉ để hiện confusion matrix/PR curve --
  dùng ảnh PNG đã sinh khi đánh giá.

------------------------------------------------------------------------

## 14.13. Văn phong và microcopy

| Nguyên tắc | Nên | Không nên |
| :--- | :--- | :--- |
| Trung thực về độ tin cậy | "Có thể là: Cấm đi ngược chiều (58%)" | "Đây chắc chắn là biển cấm đi ngược chiều" |
| Không tư vấn pháp lý | "Biển này báo hiệu…" (theo catalog) | "Bạn sẽ bị phạt nếu…" |
| Không phóng đại | "Nhận diện {N} lớp biển báo đã chọn" | "Nhận diện mọi biển báo Việt Nam" |
| Lỗi có hướng xử lý | "Ảnh vượt quá 10 MB. Hãy chọn ảnh nhỏ hơn." | "Lỗi 413" |
| Nhãn nút ngắn | "Chọn ảnh", "Thử lại", "Xem chi tiết" | "Nhấn vào đây để tải ảnh của bạn lên" |

- Dùng tiếng Việt có dấu đầy đủ; thuật ngữ kỹ thuật giữ nguyên khi cần
  (confidence → "độ tin cậy", bounding box → "khung", mAP giữ nguyên).
- Nội dung ý nghĩa/khuyến nghị **chỉ lấy từ catalog** (D-006); frontend
  không tự viết hay sửa nội dung pháp lý.
- Khi demo dùng dữ liệu ghi sẵn, giao diện phải có nhãn *"Dữ liệu ghi
  sẵn"* (`DEMO_CHECKLIST.md` §12.4).

------------------------------------------------------------------------

## 14.14. Ma trận truy vết UI ↔ yêu cầu ↔ kiểm thử

| Trạng thái/màn hình | FR | TC | Mục |
| :--- | :--- | :--- | :--- |
| Dropzone + kiểm tra client | FR-01, FR-02 | TC-04, TC-05 | 14.6.1 |
| Khung + nhãn + confidence | FR-04, FR-05 | TC-01, TC-02 | 14.6.3 |
| Thẻ thông tin & cảnh báo | FR-06, FR-07 | TC-01 | 14.6.3 |
| Không phát hiện | FR-08 | TC-03, TC-07 | 14.6.4 |
| Chưa chắc chắn | FR-09 | TC-08, TC-09 | 14.6.3 |
| Class thiếu catalog | FR-06 | TC-11 | 14.6.3 |
| Lỗi ảnh/model | FR-02 | TC-05, TC-06, TC-10 | 14.6.5 |
| Lịch sử | FR-10 | -- | 14.7.3 |
| Camera | FR-11 | -- | 14.6.6 |
| Giới thiệu & nguồn | FR-12 | -- | 14.7.5 |

Dùng bảng này khi chụp màn hình cho Chương 5 của báo cáo.

------------------------------------------------------------------------

## 14.15. Checklist trước khi bàn giao một tác vụ UI

- [ ] Đã đọc tài liệu này và các mục FR liên quan.
- [ ] Không có dấu hiệu "AI slop": không tím/glow, không Inter mặc định,
      không ảnh/biển báo giả, không emoji làm icon.
- [ ] Chỉ dùng token trong `tokens.css`; không mã màu rời rạc.
- [ ] Một màu nhấn; màu nhóm biển chỉ dùng cho dữ liệu biển báo.
- [ ] Trang Quét ảnh: dropzone và nút chính thấy được trong viewport đầu
      (kể cả 1280×720).
- [ ] Đủ trạng thái: đang xử lý, có kết quả, không phát hiện, chưa chắc
      chắn, thiếu catalog, lỗi (từng mã lỗi).
- [ ] Không hiển thị kết quả giả hoặc số liệu đánh giá giả.
- [ ] Nhãn nút 1 dòng, contrast ≥ 4.5:1, có phản hồi `:active`.
- [ ] Icon một họ (Phosphor), cùng weight.
- [ ] Layout mobile (< 768px) cho mọi hàng nhiều cột.
- [ ] Focus ring hiển thị, `aria-label` cho icon button, tôn trọng
      `prefers-reduced-motion`.
- [ ] Ảnh có kích thước dành sẵn, ảnh catalog lazy-load.
- [ ] Văn phong không khẳng định tuyệt đối, không tư vấn pháp lý.
- [ ] Đã kiểm thử thủ công trên trình duyệt và ghi lại phần chưa kiểm
      chứng (`AGENTS.md`).
