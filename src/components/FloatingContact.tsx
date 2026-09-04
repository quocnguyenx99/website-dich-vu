import { useEffect, useState } from 'react'

export default function FloatingContact() {
  const [showScrollTop, setShowScrollTop] = useState(false)

  useEffect(() => {
    const updateVisibility = () => setShowScrollTop(window.scrollY >= window.innerHeight / 3)
    updateVisibility()
    window.addEventListener('scroll', updateVisibility, { passive: true })
    window.addEventListener('resize', updateVisibility)
    return () => {
      window.removeEventListener('scroll', updateVisibility)
      window.removeEventListener('resize', updateVisibility)
    }
  }, [])

  return <aside className="floating-contact" aria-label="Kênh liên hệ nhanh">
    <a className="floating-contact__button floating-contact__button--facebook" href="https://www.facebook.com/" target="_blank" rel="noreferrer" aria-label="Facebook Chính Nhân">
      <span className="floating-contact__ping" aria-hidden="true" />
      <img className="floating-contact__social-icon" src="/assets/chinh-nhan/icon-facebook.png" alt="" aria-hidden="true" />
      <span className="floating-contact__label">Facebook</span>
    </a>
    <a className="floating-contact__button floating-contact__button--zalo" href="https://zalo.me/" target="_blank" rel="noreferrer" aria-label="Zalo Chính Nhân">
      <span className="floating-contact__ping" aria-hidden="true" />
      <img className="floating-contact__social-icon" src="/assets/chinh-nhan/icon-zalo.png" alt="" aria-hidden="true" />
      <span className="floating-contact__label">Chat Zalo</span>
    </a>
    <a className="floating-contact__button floating-contact__button--hotline" href="tel:1900571200" aria-label="Gọi hotline tư vấn 1900 571 200">
      <span className="floating-contact__ping" aria-hidden="true" />
      <span className="material-symbols-outlined" aria-hidden="true">call</span>
      <span className="floating-contact__label">1900 571 200</span>
    </a>
    <button className={`floating-contact__button floating-contact__scroll-top${showScrollTop ? ' is-visible' : ''}`} type="button" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} aria-label="Lên đầu trang" tabIndex={showScrollTop ? 0 : -1}>
      <span className="material-symbols-outlined" aria-hidden="true">keyboard_arrow_up</span>
      <span className="floating-contact__label">Lên đầu trang</span>
    </button>
  </aside>
}
