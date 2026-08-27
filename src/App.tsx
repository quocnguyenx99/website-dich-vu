import { HashRouter, Navigate, Route, Routes } from 'react-router-dom'
import SiteHeader from './components/SiteHeader'
import SiteFooter from './components/SiteFooter'
import LegacyPage from './pages/LegacyPage'
import { siteRoutes } from './routes'

function Shell({ children }: { children: React.ReactNode }) {
  return <div className="min-h-screen bg-white text-on-background flex flex-col"><SiteHeader /><div className="flex-1">{children}</div><SiteFooter /></div>
}

export default function App() {
  return <HashRouter>
    <Shell>
      <Routes>
        {siteRoutes.map(route => (
          <Route key={route.path} path={route.path} element={<LegacyPage pageKey={route.pageKey} />} />
        ))}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Shell>
  </HashRouter>
}
