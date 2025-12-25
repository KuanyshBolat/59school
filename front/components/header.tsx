"use client"
import { useState, useEffect } from "react"
import { Menu, X } from "lucide-react"
import Link from 'next/link'
import { apiService } from '@/lib/api'

export default function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [navigation, setNavigation] = useState<{name:string, href:string}[]>([])
  const [logo, setLogo] = useState<string | null>(null)

  const fallback = [
    { name: "Мектеп туралы", href: "#about" },
    { name: "Статистика", href: "#stats" },
    { name: "Директор", href: "#director" },
    { name: "Жетістіктер", href: "#Achievements" },
    { name: "Байланыс", href: "#contact" },
  ]

  useEffect(() => {
    let mounted = true
    apiService.getHeader().then(data => {
      if (!mounted) return
      if (data) {
        setLogo(data.logo || null)
        if (data.nav_links && Array.isArray(data.nav_links) && data.nav_links.length) {
          setNavigation(data.nav_links.map((n:any) => ({ name: n.name, href: n.href })))
        } else setNavigation(fallback)
      } else setNavigation(fallback)
    }).catch(() => setNavigation(fallback))
    return () => { mounted = false }
  }, [])

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href)
    element?.scrollIntoView({ behavior: "smooth" })
    setIsOpen(false)
  }

  return (
    <header className="fixed w-full top-0 z-50 bg-white shadow-md">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            {logo ? <img src={logo} alt="logo" className="h-10" /> : <div className="h-10 w-32 bg-gray-200" />}
          </div>

          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navigation.map((item) => (
                <a key={item.name} onClick={() => scrollToSection(item.href)} className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium cursor-pointer">
                  {item.name}
                </a>
              ))}
            </div>
          </div>

          <div className="-mr-2 flex md:hidden">
            <button onClick={() => setIsOpen(!isOpen)} className="bg-white p-2 rounded-md inline-flex items-center justify-center text-gray-400 hover:text-gray-500 hover:bg-gray-100">
              {isOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
      </nav>

      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            {navigation.map((item) => (
              <a key={item.name} onClick={() => scrollToSection(item.href)} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 cursor-pointer">
                {item.name}
              </a>
            ))}
          </div>
        </div>
      )}
    </header>
  )
}
