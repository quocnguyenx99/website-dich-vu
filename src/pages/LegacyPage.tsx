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

const formatServicePrices = (html: string) => html.replace(
  /<div class="service-price-summary[^"]*">\s*<span[^>]*>Giá dịch vụ<\/span>\s*<span[^>]*>(Từ )?([^<]+)<\/span>\s*<\/div>/g,
  (_, from: string | undefined, amount: string) => {
    const fullPrice = `${from || ''}${amount}`
    const contactClass = from ? '' : ' service-price-summary--contact'
    return `<div class="service-price-summary${contactClass}" aria-label="Giá dịch vụ: ${fullPrice}">
<span class="service-price-label">Giá dịch vụ</span>
<span class="service-price-line">${from ? '<span class="service-price-from">Từ</span>' : ''}<span class="service-price-amount">${amount}</span></span>
</div>`
  },
)

const prepareLegacyHtml = (pageKey: PageKey, html: string) => {
  let cleaned = formatServicePrices(stripExportNotes(html))
  if (pageKey === 'deployment') {
    cleaned = cleaned
      .replace('YÊU CẦU BÁO GIÁ', 'Khám phá dịch vụ')
      .replace('TÌM HIỂU THÊM', 'Tìm hiểu thêm')
  }
  if (pageKey === 'careers') {
    cleaned = cleaned.replace(
      /<!-- Job Card 1 -->[\s\S]*?<!-- CTA Section -->/,
      `<!-- Job Card 1 -->
<article class="career-job-card bg-surface rounded-xl shadow-[0_4px_20px_rgba(0,0,0,0.05)] border border-surface-variant hover:border-b-2 hover:border-b-primary-container hover:shadow-lg transition-all duration-300 p-6 md:p-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 group">
  <div class="flex-1">
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="bg-surface-variant text-on-surface-variant px-3 py-1 rounded-full font-label-md text-xs">Kỹ thuật</span>
      <span class="bg-surface-variant text-on-surface-variant px-3 py-1 rounded-full font-label-md text-xs">TP.HCM</span>
      <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full font-label-md text-xs flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">group</span>2 vị trí</span>
    </div>
    <h3 class="font-headline-sm text-headline-sm text-on-surface group-hover:text-primary transition-colors mb-4">Nhân viên Kỹ thuật Hỗ trợ Phần cứng/Mạng</h3>
    <ul class="space-y-2 font-body-sm text-body-sm text-on-surface-variant list-none">
      <li class="flex items-start gap-2"><span class="material-symbols-outlined text-primary-container text-lg shrink-0">check_circle</span>Lương thỏa thuận.</li>
      <li class="flex items-start gap-2"><span class="material-symbols-outlined text-primary-container text-lg shrink-0">check_circle</span>Địa điểm làm việc: Hồ Chí Minh.</li>
      <li class="flex items-start gap-2"><span class="material-symbols-outlined text-primary-container text-lg shrink-0">check_circle</span>Kinh nghiệm: 2 năm.</li>
    </ul>
  </div>
  <div class="w-full md:w-auto mt-4 md:mt-0 flex flex-col gap-3 items-end">
    <button class="w-full md:w-auto bg-primary-container text-white px-8 py-3 rounded-lg font-label-md text-label-md hover:bg-orange-600 transition-colors shadow-sm text-center">Xem chi tiết</button>
    <span class="font-body-sm text-body-sm text-on-surface-variant">Hạn nộp: 30/09/2026</span>
  </div>
</article>
<!-- CTA Section -->`,
    )
  }
  if (pageKey !== 'contact') return cleaned
  return cleaned.replace(
    /(<img[^>]*data-location="Ho Chi Minh City"[^>]*src=")[^"]+("[^>]*>)/,
    '$1/assets/contact-map-detailed.png$2',
  )
}

const normalizedText = (element: Element) => (element.textContent || '')
  .replace(/\s+/g, ' ')
  .trim()
  .toLocaleLowerCase('vi')

const homeServiceRouteById: Record<string, string> = {
  'home-service-rental': '/dich-vu/thue-thiet-bi',
  'home-service-maintenance': '/dich-vu/bao-tri',
  'home-service-deployment': '/dich-vu/thi-cong',
  'home-service-repair': '/dich-vu/sua-chua',
  'home-service-outsourcing': '/dich-vu/bao-tri',
}

const consultationServiceOptions: Record<string, string[]> = {
  'Cho thuê thiết bị': [
    'Cho thuê máy in A3', 'Cho thuê máy photocopy', 'Cho thuê máy photocopy màu', 'Cho thuê PC',
    'Cho thuê máy in', 'Cho thuê máy chiếu', 'Cho thuê màn hình', 'Cho thuê laptop',
    'Cho thuê server', 'Cho thuê máy in màu',
  ],
  'Thi công & lắp đặt': [
    'Cấu hình Server', 'Camera giám sát văn phòng', 'Dịch vụ tháo lắp camera',
    'Dịch vụ lắp đặt camera', 'Thi công camera giám sát',
  ],
  'Sửa chữa tận nơi': ['Sửa máy tính giá rẻ', 'Dịch vụ sửa chữa máy in'],
  'Bảo trì & IT Helpdesk': [
    'Dịch vụ bảo trì máy in', 'Dịch vụ bảo trì máy tính', 'Bảo trì máy chủ',
    'Bảo trì máy tính để bàn / xách tay', 'Bảo trì hệ thống mạng',
  ],
  'Thuê IT Outsourcing': ['IT Helpdesk tại chỗ', 'IT Helpdesk từ xa', 'Quản trị hệ thống IT', 'Nhân sự IT thuê ngoài'],
}

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

    const selectCleanups = Array.from(root.querySelectorAll<HTMLFormElement>('form')).flatMap(form => {
      const serviceSelect = Array.from(form.querySelectorAll<HTMLSelectElement>('select')).find(select =>
        select.name === 'serviceCategory'
        || Array.from(select.options).some(option => normalizedText(option).includes('yêu cầu dịch vụ')),
      )
      if (!serviceSelect) return []

      const subServiceSelect = document.createElement('select')
      subServiceSelect.name = 'subService'
      subServiceSelect.required = true
      subServiceSelect.disabled = true
      subServiceSelect.className = serviceSelect.className
      subServiceSelect.setAttribute('aria-label', 'Dịch vụ cần tư vấn')

      serviceSelect.name = 'serviceCategory'
      serviceSelect.required = true
      serviceSelect.setAttribute('aria-label', 'Danh mục dịch vụ')
      serviceSelect.replaceChildren(new Option('Danh mục dịch vụ *', ''))
      Object.keys(consultationServiceOptions).forEach(category => serviceSelect.add(new Option(category, category)))

      const updateSubServices = () => {
        const services = consultationServiceOptions[serviceSelect.value] || []
        subServiceSelect.replaceChildren(new Option('Chọn dịch vụ cụ thể *', ''))
        services.forEach(service => subServiceSelect.add(new Option(service, service)))
        subServiceSelect.disabled = services.length === 0
      }
      updateSubServices()
      serviceSelect.addEventListener('change', updateSubServices)
      serviceSelect.insertAdjacentElement('afterend', subServiceSelect)
      return [() => {
        serviceSelect.removeEventListener('change', updateSubServices)
        subServiceSelect.remove()
      }]
    })

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
      if (pageKey === 'home' && /xem chi tiết/.test(text)) {
        const serviceSection = control.closest<HTMLElement>('[id^="home-service-"]')
        const servicePath = serviceSection ? homeServiceRouteById[serviceSection.id] : undefined
        if (servicePath) {
          event.preventDefault()
          navigate(servicePath)
          return
        }
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
      selectCleanups.forEach(cleanup => cleanup())
    }
  }, [location.pathname, location.state, navigate, page.title, pageKey])

  return <div ref={rootRef} dangerouslySetInnerHTML={{ __html: prepareLegacyHtml(pageKey, page.html) }} />
}
