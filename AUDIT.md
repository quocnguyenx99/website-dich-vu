# Audit bộ HTML Stitch

## 10 file nhận được

1. Trang home
2. Dịch vụ thuê thiết bị
3. Dịch vụ bảo trì & IT Helpdesk
4. Dịch vụ sửa chữa
5. Dịch vụ thi công
6. Trang chi tiết bài dịch vụ
7. Trang liên hệ
8. Trang tuyển dụng
9. Trang tin tức
10. Trang chi tiết bài viết tin tức

## Ghi nhận chính

- Các trang dùng chung Top Info Bar, Header, mega menu, CTA và Footer nên đã được gom thành shell dùng chung.
- Hệ màu gần như đồng nhất: `#ff6600` primary CTA, `#a33e00` primary dark, `#D32F2F` hotline, nền trắng/xám.
- Có sự pha trộn font Inter và Be Vietnam Pro giữa các HTML; project giữ override theo page để fidelity cao hơn.
- Bốn trang nhóm dịch vụ có cùng pattern Hero → Service cards → supporting sections → news carousel; đủ tốt để refactor tiếp thành một `ServiceCategoryPage` data-driven sau khi demo được duyệt.
- `Trang tin tức.html` và `trang chi tiết bài viết tin tức.html` trùng 100% byte-by-byte trong bộ nguồn hiện tại; chưa có listing tin tức riêng biệt.
- Một số HTML export có style fixed width/height ở thẻ `<html>`; project đã bỏ các ràng buộc export canvas này để responsive hoạt động.
- Một số CTA và links dùng `href="#"`; project gắn route demo hợp lý mà không sửa layout.
- Hình ảnh Stitch đang phụ thuộc Google-hosted URLs và nên được local hóa ở bước production.
