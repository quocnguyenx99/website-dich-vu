import type { PageKey } from './pageHtml'

export type SiteRoute = {
  path: string
  label: string
  pageKey: PageKey
}

export const siteRoutes: SiteRoute[] = [
  { path: '/', label: 'Trang chủ', pageKey: 'home' },
  { path: '/dich-vu/thue-thiet-bi', label: 'Cho thuê thiết bị', pageKey: 'rental' },
  { path: '/dich-vu/bao-tri', label: 'Bảo trì & IT Helpdesk', pageKey: 'maintenance' },
  { path: '/dich-vu/sua-chua', label: 'Sửa chữa tận nơi', pageKey: 'repair' },
  { path: '/dich-vu/thi-cong', label: 'Thi công & triển khai', pageKey: 'deployment' },
  { path: '/dich-vu/chi-tiet', label: 'Chi tiết dịch vụ', pageKey: 'service-detail' },
  { path: '/tin-tuc', label: 'Tin tức', pageKey: 'news' },
  { path: '/tin-tuc/chi-tiet', label: 'Chi tiết bài viết', pageKey: 'news-detail' },
  { path: '/tuyen-dung', label: 'Tuyển dụng', pageKey: 'careers' },
  { path: '/lien-he', label: 'Liên hệ', pageKey: 'contact' },
]

export const serviceRoutes = [
  { path: '/dich-vu/thue-thiet-bi', label: 'Cho thuê thiết bị', aliases: ['thuê thiết bị', 'cho thuê laptop', 'máy chiếu'] },
  { path: '/dich-vu/bao-tri', label: 'Bảo trì & IT Helpdesk', aliases: ['bảo trì', 'helpdesk'] },
  { path: '/dich-vu/thi-cong', label: 'Thi công & triển khai', aliases: ['thi công', 'camera', 'server'] },
  { path: '/dich-vu/sua-chua', label: 'Sửa chữa tận nơi', aliases: ['sửa chữa'] },
] as const

// Kept for callers that only need a compact path/label list.
export const demoRoutes = siteRoutes.map(({ path, label }) => [path, label] as const)
