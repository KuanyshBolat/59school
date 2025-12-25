"use client"

import { useEffect, useState } from 'react'
import { apiService } from '@/lib/api'

export default function Footer() {
  const [footer, setFooter] = useState<any | null>(null)
  const currentYear = new Date().getFullYear()

  const fallback = {
    title: '№59 Мектеп-гимназия',
    body: 'Балалардың болашағын ойлай отырып, озық білім беретін мектеп'
  }

  useEffect(() => {
    let mounted = true
    apiService.getFooter().then(data => {
      if (!mounted) return
      if (data) setFooter(data)
      else setFooter(fallback)
    }).catch(() => setFooter(fallback))
    return () => { mounted = false }
  }, [])

  const f = footer || fallback

  return (
    <footer className="bg-primary text-primary-foreground py-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* About */}
          <div>
            <h4 className="font-bold text-lg mb-4">{f.title}</h4>
            <p className="text-primary-foreground/80 text-sm">
              {f.body}
            </p>
          </div>
          {/* Quick Links */}
          <div>
            <h4 className="font-bold text-lg mb-4">Сілтемелер</h4>
            <ul className="space-y-2">
              <li>
                <a href="#about" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Мектеп туралы
                </a>
              </li>
              <li>
                <a href="#stats" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Статистика
                </a>
              </li>
              <li>
                <a href="#director" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Директор
                </a>
              </li>
              <li>
                <a href="#achievements" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Жетістіктер
                </a>
              </li>
            </ul>
          </div>
          {/* Services */}
          <div>
            <h4 className="font-bold text-lg mb-4">Қызмет</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Баланың дамуы
                </a>
              </li>
              <li>
                <a href="#" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Олимпиадалар
                </a>
              </li>
              <li>
                <a href="#" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Іс-шаралар
                </a>
              </li>
            </ul>
          </div>
          {/* Contact */}
          <div>
            <h4 className="font-bold text-lg mb-4">Байланыс</h4>
            <p className="text-primary-foreground/80 text-sm">+7 (727) 299‒52‒97</p>
            <p className="text-primary-foreground/80 text-sm">mektep59@almatybilim.kz</p>
            <p className="text-primary-foreground/80 text-sm">Алматы, Түрксіб ауданы</p>
          </div>
        </div>

        <div className="text-center">
          <p className="text-primary-foreground/80 text-sm">© {currentYear} {f.title}. Барлық құқықтар қорғалған.</p>
        </div>
      </div>
    </footer>
  )
}
