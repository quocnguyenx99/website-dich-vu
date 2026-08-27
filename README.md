# Chính Nhân Services Demo

Frontend demo được chuyển đổi từ bộ HTML Stitch do người dùng cung cấp.

## Stack

- Vite
- React
- TypeScript
- React Router (HashRouter để demo/deploy static không cần rewrite server)
- Tailwind CDN để giữ tối đa utility classes gốc của các file Stitch
- Material Symbols + Inter / Be Vietnam Pro

## Chạy local

```bash
npm install
npm run dev
```

Mở: `http://localhost:5173`

## Build

```bash
npm run build
npm run preview
```

## Routes

- `/#/` — Trang chủ
- `/#/dich-vu/thue-thiet-bi`
- `/#/dich-vu/bao-tri`
- `/#/dich-vu/sua-chua`
- `/#/dich-vu/thi-cong`
- `/#/dich-vu/chi-tiet`
- `/#/tin-tuc`
- `/#/tin-tuc/chi-tiet`
- `/#/tuyen-dung`
- `/#/lien-he`

## Kiến trúc demo

`SiteHeader` và `SiteFooter` là component dùng chung. Nội dung giữa trang được giữ sát HTML Stitch gốc để tránh redesign ngoài ý muốn; mỗi route render fragment HTML đã loại bỏ header/footer trùng lặp. Logic carousel và điều hướng CTA placeholder được gắn lại bằng React `useEffect`.

Đây là lựa chọn phù hợp cho **demo giao diện V1**: giữ fidelity với Stitch trước, rồi mới refactor sâu từng section thành React component thuần sau khi UI được duyệt.

## Lưu ý nguồn HTML

Hai file `Trang tin tức.html` và `trang chi tiết bài viết tin tức.html` trong bộ đầu vào là **giống hệt nhau**, vì vậy hiện `/tin-tuc` và `/tin-tuc/chi-tiet` hiển thị cùng một template bài viết. Khi có file listing tin tức riêng, thay page `news` là đủ.

Thư mục `references/original-html/` lưu nguyên bản 10 HTML đầu vào để đối chiếu.

## Asset

Logo Chính Nhân đã được local hóa trong `public/assets`. Hình ảnh nội dung do Stitch tạo vẫn dùng URL `googleusercontent.com`; khi chốt demo nên tải các ảnh này về local/CDN công ty để tránh phụ thuộc link ngoài.
