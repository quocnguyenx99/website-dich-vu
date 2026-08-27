import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { footerHtml } from '../footerHtml'

export default function SiteFooter() {
  const ref = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()
  useEffect(() => {
    const root = ref.current
    if (!root) return
    const anchors = Array.from(root.querySelectorAll<HTMLAnchorElement>('a'))
    const routes: Record<string,string> = {
      'Bảo trì & Helpdesk':'/dich-vu/bao-tri',
      'Cho thuê thiết bị':'/dich-vu/thue-thiet-bi',
      'Thi công mạng':'/dich-vu/thi-cong',
      'Sửa chữa tận nơi':'/dich-vu/sua-chua',
      'Thủ thuật - Tin tức':'/tin-tuc',
      'Tuyển dụng':'/tuyen-dung'
    }
    const cleanups = anchors.map(a => {
      const fn=(e: Event) => { const t=(a.textContent||'').trim(); if(routes[t]){e.preventDefault();navigate(routes[t])} }
      a.addEventListener('click',fn); return () => a.removeEventListener('click',fn)
    })
    return () => cleanups.forEach(fn => fn())
  }, [navigate])
  return <div className="site-footer" ref={ref} dangerouslySetInnerHTML={{__html: footerHtml}} />
}
