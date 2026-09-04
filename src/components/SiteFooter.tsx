import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { footerHtml } from '../footerHtml'

export default function SiteFooter() {
  const ref = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()
  useEffect(() => {
    const root = ref.current
    if (!root) return
    const email = Array.from(root.querySelectorAll<HTMLElement>('span'))
      .find(element => element.textContent?.trim() === 'info@chinhnhan.vn')
    if (email) email.textContent = 'cskh@chinhnhan.vn'
    const anchors = Array.from(root.querySelectorAll<HTMLAnchorElement>('a'))
    const routes: Record<string,string> = {
      'Bảo trì & Helpdesk':'/dich-vu/bao-tri',
      'Cho thuê thiết bị':'/dich-vu/thue-thiet-bi',
      'Thi công mạng':'/dich-vu/thi-cong',
      'Sửa chữa tận nơi':'/dich-vu/sua-chua',
      'Về Chính Nhân':'/',
      'Câu hỏi thường gặp':'/tin-tuc/chi-tiet',
      'Thủ thuật - Tin tức':'/tin-tuc',
      'Tuyển dụng':'/tuyen-dung'
    }
    const cleanups = anchors.map(a => {
      const text = (a.textContent || '').trim()
      const path = routes[text]
      if (path) a.href = `#${path}`
      const fn=(e: Event) => { if(path){e.preventDefault();navigate(path)} }
      a.addEventListener('click',fn); return () => a.removeEventListener('click',fn)
    })
    return () => cleanups.forEach(fn => fn())
  }, [navigate])
  return <div className="site-footer" ref={ref} dangerouslySetInnerHTML={{__html: footerHtml}} />
}
