import { useState, type FocusEvent, type MouseEvent } from 'react'
import { Link, useLocation } from 'react-router-dom'

const serviceLinks = [
  { to: '/dich-vu/thue-thiet-bi', icon: 'devices', title: 'Cho thuê thiết bị', desc: 'Laptop, PC, Server, máy in...' },
  { to: '/dich-vu/bao-tri', icon: 'support_agent', title: 'Bảo trì & IT Helpdesk', desc: 'Quản trị hệ thống, hỗ trợ người dùng.' },
  { to: '/dich-vu/thi-cong', icon: 'construction', title: 'Thi công & triển khai', desc: 'Mạng LAN, Wifi, Server, Camera.' },
  { to: '/dich-vu/sua-chua', icon: 'home_repair_service', title: 'Sửa chữa tận nơi', desc: 'Khắc phục sự cố phần cứng, phần mềm.' },
]

function LanguageFlags({ mobile = false }: { mobile?: boolean }) {
  return <div className={`language-flags flex items-center ${mobile ? 'gap-3 px-3 py-2' : 'gap-2'}`} aria-label="Ngôn ngữ hiển thị">
    <img src="/assets/flags/vi.svg" alt="Tiếng Việt" title="Tiếng Việt" className="h-5 w-7 rounded-sm object-cover ring-2 ring-primary-container ring-offset-1" />
    <img src="/assets/flags/en.svg" alt="English" title="English" className="h-5 w-7 rounded-sm object-cover opacity-65" />
  </div>
}

export default function SiteHeader() {
  const { pathname } = useLocation()
  const [open, setOpen] = useState(false)
  const [openDropdown, setOpenDropdown] = useState<'about' | 'services' | 'news' | null>(null)
  const isActive = (prefix: string) => pathname === prefix || pathname.startsWith(prefix + '/')
  const navClass = (active = false) => `${active ? 'text-primary-container font-bold border-b-2 border-primary-container' : 'text-on-surface-variant hover:text-primary-container'} transition-colors pb-1`
  const closeMenus = () => {
    setOpen(false)
    setOpenDropdown(null)
  }
  const closeOnBlur = (event: FocusEvent<HTMLLIElement>) => {
    if (!event.currentTarget.contains(event.relatedTarget)) setOpenDropdown(null)
  }
  const onConsultClick = (event: MouseEvent<HTMLAnchorElement>) => {
    const form = Array.from(document.querySelectorAll<HTMLFormElement>('.legacy-page form'))
      .find(element => element.querySelector('input[type="tel"], textarea[name="message"], input[name="fullName"]'))
    closeMenus()
    if (!form) return
    event.preventDefault()
    form.scrollIntoView({ behavior: 'smooth', block: 'center' })
    form.querySelector<HTMLElement>('input, select, textarea')?.focus({ preventScroll: true })
  }

  return <>
    <div className="border-b border-outline-variant py-2 hidden md:block bg-white">
      <div className="max-w-container-max mx-auto px-margin-desktop flex justify-between items-center text-sm text-on-surface-variant py-2">
        <div className="flex items-center gap-6">
          <a href="tel:1900571200" className="flex items-center gap-2 font-black text-lg text-hotline-urgent"><span className="material-symbols-outlined text-[20px]">call</span>1900 571 200</a>
          <div className="w-px h-4 bg-outline-variant" />
          <a href="mailto:cskh@chinhnhan.vn" className="flex items-center gap-2"><span className="material-symbols-outlined text-[18px]">mail</span>cskh@chinhnhan.vn</a>
        </div>
        <span className="flex items-center gap-2"><span className="material-symbols-outlined text-[18px]">schedule</span>T2-T6: 8:00 - 17:30 | T7: 8:00 - 12:00</span>
      </div>
    </div>
    <nav className="bg-white sticky top-0 z-50 shadow-sm border-b border-outline-variant">
      <div className="flex justify-between items-center w-full px-margin-mobile md:px-margin-desktop max-w-container-max mx-auto h-20 md:h-24">
        <Link to="/" onClick={closeMenus} className="shrink-0"><img src="/assets/chinh-nhan-logo.png" alt="Chính Nhân Technology" className="h-9 md:h-10 object-contain" /></Link>
        <ul className="hidden lg:flex items-center gap-7 text-sm font-semibold">
          <li className="relative about-mega" onMouseEnter={() => setOpenDropdown('about')} onMouseLeave={() => setOpenDropdown(null)} onFocus={() => setOpenDropdown('about')} onBlur={closeOnBlur}>
            <Link onClick={closeMenus} className={`${navClass(pathname === '/')} flex items-center gap-1`} to="/">Giới thiệu <span className="material-symbols-outlined text-[18px]">keyboard_arrow_down</span></Link>
            <div className={`absolute top-full left-1/2 -translate-x-1/2 mt-4 w-60 bg-white rounded-lg shadow-[0_10px_30px_rgba(0,0,0,0.08)] border border-outline-variant p-2 flex-col z-50 ${openDropdown === 'about' ? 'flex' : 'hidden'}`}>
              <span aria-disabled="true" className="flex items-center justify-between gap-3 p-3 rounded-lg text-on-surface-variant"><span className="flex items-center gap-3"><span className="material-symbols-outlined text-primary-container">corporate_fare</span>Về Chính Nhân</span><small className="text-[10px] uppercase opacity-60">Sắp có</small></span>
              <span aria-disabled="true" className="flex items-center justify-between gap-3 p-3 rounded-lg text-on-surface-variant"><span className="flex items-center gap-3"><span className="material-symbols-outlined text-primary-container">engineering</span>Đội ngũ kỹ thuật</span><small className="text-[10px] uppercase opacity-60">Sắp có</small></span>
            </div>
          </li>
          <li className="relative group mega-menu-trigger" onMouseEnter={() => setOpenDropdown('services')} onMouseLeave={() => setOpenDropdown(null)} onFocus={() => setOpenDropdown('services')} onBlur={closeOnBlur}>
            <Link onClick={closeMenus} className={`${navClass(isActive('/dich-vu'))} flex items-center gap-1`} to="/dich-vu/thue-thiet-bi">Dịch vụ IT <span className="material-symbols-outlined text-[18px]">keyboard_arrow_down</span></Link>
            <div className={`mega-menu absolute top-full left-1/2 -translate-x-1/2 mt-4 w-[620px] bg-white rounded-lg shadow-[0_10px_30px_rgba(0,0,0,0.08)] border border-outline-variant p-6 grid-cols-2 gap-3 z-50 ${openDropdown === 'services' ? 'grid' : 'hidden'}`}>
              {serviceLinks.map(item => <Link onClick={closeMenus} key={item.to} to={item.to} className="group/item flex gap-4 p-4 rounded-lg hover:bg-surface-container transition-colors">
                <div className="w-12 h-12 rounded-full bg-primary-container/15 flex items-center justify-center text-primary-container"><span className="material-symbols-outlined">{item.icon}</span></div>
                <div><h4 className="font-semibold text-on-surface mb-1 group-hover/item:text-primary-container">{item.title}</h4><p className="text-sm font-normal text-on-surface-variant">{item.desc}</p></div>
              </Link>)}
            </div>
          </li>
          <li className="relative group news-mega" onMouseEnter={() => setOpenDropdown('news')} onMouseLeave={() => setOpenDropdown(null)} onFocus={() => setOpenDropdown('news')} onBlur={closeOnBlur}><Link onClick={closeMenus} className={`${navClass(isActive('/tin-tuc'))} flex items-center gap-1`} to="/tin-tuc">Thủ thuật - Tin tức <span className="material-symbols-outlined text-[18px]">keyboard_arrow_down</span></Link>
            <div className={`news-mega-menu absolute top-full left-1/2 -translate-x-1/2 mt-4 w-52 bg-white rounded-lg shadow-[0_10px_30px_rgba(0,0,0,0.08)] border border-outline-variant p-2 flex-col z-50 ${openDropdown === 'news' ? 'flex' : 'hidden'}`}>
              <Link onClick={closeMenus} to="/tin-tuc" className="flex items-center gap-3 p-3 rounded-lg hover:bg-surface-container"><span className="material-symbols-outlined text-primary-container">lightbulb</span>Thủ thuật</Link>
              <Link onClick={closeMenus} to="/tin-tuc" className="flex items-center gap-3 p-3 rounded-lg hover:bg-surface-container"><span className="material-symbols-outlined text-primary-container">newspaper</span>Tin tức</Link>
            </div>
          </li>
          <li><Link onClick={closeMenus} className={navClass(isActive('/tuyen-dung'))} to="/tuyen-dung">Tuyển dụng</Link></li>
          <li><Link onClick={closeMenus} className={navClass(isActive('/lien-he'))} to="/lien-he">Liên hệ</Link></li>
        </ul>
        <div className="hidden lg:flex items-center gap-4">
          <LanguageFlags />
          <Link to="/lien-he" state={{ scrollToConsultation: true }} onClick={onConsultClick} className="bg-primary-container text-white px-5 py-2.5 rounded-lg font-bold text-sm flex items-center gap-2 hover:bg-primary transition-all shadow-sm">Nhận tư vấn<span className="material-symbols-outlined text-[18px]">arrow_forward</span></Link>
        </div>
        <button aria-label="Mở menu" className="lg:hidden text-on-surface p-2" onClick={() => setOpen(v => !v)}><span className="material-symbols-outlined">{open ? 'close' : 'menu'}</span></button>
      </div>
      {open && <div className="lg:hidden border-t border-outline-variant bg-white px-4 py-4 shadow-lg">
        <div className="flex flex-col gap-2 max-w-container-max mx-auto">
          <Link onClick={closeMenus} to="/" className="p-3 rounded-lg hover:bg-surface-container">Trang chủ / Giới thiệu</Link>
          <div className="pl-6 text-sm text-on-surface-variant">Về Chính Nhân <span className="text-xs opacity-60">(Sắp có)</span></div>
          <div className="pl-6 text-sm text-on-surface-variant">Đội ngũ kỹ thuật <span className="text-xs opacity-60">(Sắp có)</span></div>
          <div className="px-3 pt-2 pb-1 text-xs uppercase tracking-wider text-on-surface-variant font-bold">Dịch vụ IT</div>
          {serviceLinks.map(item => <Link onClick={closeMenus} key={item.to} to={item.to} className="p-3 rounded-lg hover:bg-surface-container flex items-center gap-3"><span className="material-symbols-outlined text-primary-container">{item.icon}</span>{item.title}</Link>)}
          <Link onClick={closeMenus} to="/tin-tuc" className="p-3 rounded-lg hover:bg-surface-container">Thủ thuật - Tin tức</Link>
          <Link onClick={closeMenus} to="/tuyen-dung" className="p-3 rounded-lg hover:bg-surface-container">Tuyển dụng</Link>
          <LanguageFlags mobile />
          <Link onClick={onConsultClick} state={{ scrollToConsultation: true }} to="/lien-he" className="p-3 rounded-lg bg-primary-container text-white font-bold text-center mt-2">Nhận tư vấn</Link>
        </div>
      </div>}
    </nav>
  </>
}
