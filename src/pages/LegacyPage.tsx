import { useEffect, useRef } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { pageHtml, type PageKey } from '../pageHtml'
import { rawPageOverrides } from '../rawPageHtml'
import { serviceRoutes } from '../routes'

const exportNotes = new Set([
  'Top Info Bar',
  'TopNavBar',
  'TopNavBar Component',
  'Hero Section',
  'Hero Section (Thinner version)',
  'Core Commitments Section',
  'Service Category Section',
  'SLA Section (Dark) -> Now "Lý do chọn Chính Nhân"',
  'Testimonials Section',
  'Client Logo Wall',
  'Consultation Form Section',
  'News & Knowledge Section',
  'Main Content',
  'Main Content Area',
  'Main Content Canvas',
  'Footer',
  'Footer Component',
])

const stripExportNotes = (html: string) => html
  .split('\n')
  .filter(line => !exportNotes.has(line.trim()))
  .join('\n')

const prepareLegacyHtml = (pageKey: PageKey, html: string) => {
  const cleaned = stripExportNotes(html)
  if (pageKey !== 'contact') return cleaned
  return cleaned.replace(
    /(<img[^>]*data-location="Ho Chi Minh City"[^>]*src=")[^"]+("[^>]*>)/,
    '$1/assets/contact-map.jpg$2',
  )
}

const normalizedText = (element: Element) => (element.textContent || '')
  .replace(/\s+/g, ' ')
  .trim()
  .toLocaleLowerCase('vi')

export default function LegacyPage({ pageKey }: { pageKey: PageKey }) {
  const rootRef = useRef<HTMLDivElement>(null)
  const navigate = useNavigate()
  const location = useLocation()
  const page = rawPageOverrides[pageKey] || pageHtml[pageKey]

  useEffect(() => {
    document.title = page.title
    window.scrollTo({ top: 0, behavior: 'instant' as ScrollBehavior })
    const root = rootRef.current
    if (!root) return

    const consultationForm = Array.from(root.querySelectorAll<HTMLFormElement>('form'))
      .find(form => form.querySelector('input[type="tel"], textarea[name="message"], input[name="fullName"]'))
    if (location.state?.scrollToConsultation && consultationForm) {
      requestAnimationFrame(() => {
        consultationForm.scrollIntoView({ behavior: 'smooth', block: 'center' })
        consultationForm.querySelector<HTMLElement>('input, select, textarea')?.focus({ preventScroll: true })
      })
      navigate(location.pathname, { replace: true, state: null })
    }

    if (pageKey === 'home') {
      const homeServices = [
        { label: 'thuê thiết bị', id: 'home-service-rental' },
        { label: 'bảo trì & it helpdesk', id: 'home-service-maintenance' },
        { label: 'thi công camera & server', id: 'home-service-deployment' },
        { label: 'sửa chữa tận nơi', id: 'home-service-repair' },
        { label: 'thuê it outsourcing', id: 'home-service-outsourcing' },
      ]
      const serviceHeadings = Array.from(root.querySelectorAll<HTMLHeadingElement>('#dich-vu h3'))
      const categoryLinks = Array.from(root.querySelectorAll<HTMLAnchorElement>('#dich-vu > div:first-child a'))
      homeServices.forEach(item => {
        const heading = serviceHeadings.find(element => normalizedText(element).includes(item.label))
        const section = heading?.closest<HTMLElement>('.grid')
        const link = categoryLinks.find(element => normalizedText(element).includes(item.label.split(' & ')[0]))
        if (section) section.id = item.id
        if (link) link.href = `#${item.id}`
      })
    }

    // Preserve the original Stitch carousel behavior on the pages that contain it.
    const carousel = root.querySelector<HTMLElement>('#news-carousel')
    const prevBtn = root.querySelector<HTMLButtonElement>('#news-prev')
    const nextBtn = root.querySelector<HTMLButtonElement>('#news-next')
    const getScrollAmount = () => {
      const card = carousel?.querySelector<HTMLElement>('div')
      return card ? card.offsetWidth + 32 : (carousel?.offsetWidth || 0)
    }
    const onPrev = () => carousel?.scrollBy({ left: -getScrollAmount(), behavior: 'smooth' })
    const onNext = () => carousel?.scrollBy({ left: getScrollAmount(), behavior: 'smooth' })
    const updateButtons = () => {
      if (!carousel || !prevBtn || !nextBtn) return
      prevBtn.disabled = carousel.scrollLeft <= 0
      nextBtn.disabled = carousel.scrollLeft >= carousel.scrollWidth - carousel.clientWidth - 2
    }
    prevBtn?.addEventListener('click', onPrev)
    nextBtn?.addEventListener('click', onNext)
    carousel?.addEventListener('scroll', updateButtons)
    updateButtons()

    const scrollTo = (selector: string) => {
      const target = root.querySelector<HTMLElement>(selector)
      if (!target) return false
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      target.querySelector<HTMLElement>('input, select, textarea, button')?.focus({ preventScroll: true })
      return true
    }

    // One delegated handler keeps all imported HTML links and buttons connected.
    const onClick = (event: MouseEvent) => {
      const target = event.target as Element | null
      const control = target?.closest<HTMLAnchorElement | HTMLButtonElement>('a, button')
      if (!control || !root.contains(control)) return
      if (control.id === 'news-prev' || control.id === 'news-next') return

      const href = control instanceof HTMLAnchorElement ? control.getAttribute('href') || '' : ''
      const text = normalizedText(control)
      if (href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:')) return
      if (href.startsWith('#home-service-')) {
        event.preventDefault()
        scrollTo(href)
        return
      }
      if (href.startsWith('#') && href.length > 1) return

      if (/khám phá dịch vụ/.test(text)) {
        event.preventDefault()
        scrollTo('#dich-vu')
        return
      }
      if (/nhận tư vấn|yêu cầu báo giá|nhận báo giá|thuê ngay|ứng tuyển|gửi cv/.test(text)) {
        event.preventDefault()
        if (!scrollTo('form')) navigate('/lien-he')
        return
      }
      if (/liên hệ hotline/.test(text)) {
        event.preventDefault()
        window.location.href = 'tel:1900571200'
        return
      }
      if (/xem chi tiết/.test(text) && control.closest('#news-carousel')) {
        event.preventDefault()
        navigate('/tin-tuc/chi-tiet')
        return
      }
      if (pageKey === 'news' && (control.closest('article') || control.querySelector('h4') || (/xem thêm/.test(text) && control.closest('aside')))) {
        event.preventDefault()
        navigate('/tin-tuc/chi-tiet')
        return
      }
      if (/xem chi tiết|xem thêm|tìm hiểu thêm/.test(text)) {
        event.preventDefault()
        navigate('/dich-vu/chi-tiet')
        return
      }
      if (/tin tức|thủ thuật/.test(text)) {
        event.preventDefault()
        navigate('/tin-tuc')
        return
      }
      if (/trang chủ|về chính nhân/.test(text)) {
        event.preventDefault()
        navigate('/')
        return
      }
      const directService = serviceRoutes.find(route => route.aliases.some(alias => text.includes(alias)))
      if (directService) {
        event.preventDefault()
        navigate(directService.path)
        return
      }
      if (href === '#') event.preventDefault()
    }

    const onSubmit = (event: SubmitEvent) => {
      const form = event.target as HTMLFormElement
      if (!root.contains(form)) return
      event.preventDefault()
      let status = form.querySelector<HTMLElement>('.demo-form-status')
      if (!status) {
        status = document.createElement('p')
        status.className = 'demo-form-status'
        status.setAttribute('role', 'status')
        form.appendChild(status)
      }
      status.textContent = 'Dữ liệu đã được kiểm tra trên giao diện demo. Cần kết nối API để gửi yêu cầu thực tế.'
    }

    root.addEventListener('click', onClick)
    root.addEventListener('submit', onSubmit)

    return () => {
      prevBtn?.removeEventListener('click', onPrev)
      nextBtn?.removeEventListener('click', onNext)
      carousel?.removeEventListener('scroll', updateButtons)
      root.removeEventListener('click', onClick)
      root.removeEventListener('submit', onSubmit)
    }
  }, [location.pathname, location.state, navigate, page.title, pageKey])

  return <div ref={rootRef} dangerouslySetInnerHTML={{ __html: prepareLegacyHtml(pageKey, page.html) }} />
}
