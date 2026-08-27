import newsRawHtml from '../references/original-html/news.html?raw'
import newsDetailRawHtml from '../references/original-html/news-detail.html?raw'
import type { PageKey } from './pageHtml'

type RawPage = { title: string; html: string }

const titleFrom = (source: string) => {
  const title = source.match(/<title>([\s\S]*?)<\/title>/i)?.[1] || 'Chính Nhân Technology'
  return title.replace(/&amp;/g, '&').trim()
}

const contentBetween = (source: string, startMarker: string, endMarker: string) => {
  const start = source.indexOf(startMarker)
  const end = source.indexOf(endMarker, start + startMarker.length)
  if (start < 0 || end < 0) return ''
  return source.slice(start + startMarker.length, end).trim()
}

const fromOriginalHtml = (
  source: string,
  pageClass: string,
  startMarker: string,
  endMarker: string,
): RawPage => ({
  title: titleFrom(source),
  html: `<div class="legacy-page ${pageClass} font-inter">${contentBetween(source, startMarker, endMarker)}</div>`,
})

export const rawPageOverrides: Partial<Record<PageKey, RawPage>> = {
  news: fromOriginalHtml(newsRawHtml, 'page-news', '<!-- Hero Section -->', '<!-- Footer -->'),
  'news-detail': fromOriginalHtml(newsDetailRawHtml, 'page-news-detail', '<!-- Main Content Area -->', '<!-- Footer -->'),
}
