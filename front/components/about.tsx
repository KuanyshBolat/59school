"use client"

import { useEffect, useState } from 'react'
import { apiService } from '@/lib/api'

export default function About() {
  const [about, setAbout] = useState<any | null>(null)

  const fallback = {
    title: 'Мектеп туралы',
    body: '№50 мектеп-гимназия – балалардың толыққанды дамуы мен озық білім алуына бағытталған заманауи орталық',
    image: '/123.JPG',
    title_color: '#000000',
    body_color: '#333333'
  }

  useEffect(() => {
    let mounted = true
    apiService.getAbout().then(data => {
      if (!mounted) return
      if (data) setAbout(data)
      else setAbout(fallback)
    }).catch(() => setAbout(fallback))
    return () => { mounted = false }
  }, [])

  const data = about || fallback

  return (
    <section id="about" className="py-16 md:py-24 px-4 bg-white">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-primary mb-4" style={{ color: data.title_color }}>{data.title}</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-balance" style={{ color: data.body_color, whiteSpace: 'pre-wrap' }}>
            {data.body}
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="relative">
            <div className="rounded-3xl overflow-hidden shadow-2xl">
              <div className="absolute inset-0 bg-black/15 rounded-3xl"></div>
              <img
                src={data.image || '/123.JPG'}
                alt="Мектеп"
                className="w-full h-[400px] object-cover"
              />
              <div className="absolute bottom-8 left-8 right-8 text-white">
                <p className="text-[32px] mb-4">Біздің миссия</p>
                <p className="text-[20px]">
                  Ұлттық құндылықтарға бейімделген халықаралық тәжірибені енгізу арқылы сапалы білім беру ортасын құру
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="mb-6 flex gap-2">
              <div className="w-2 h-1 bg-white rounded-full"></div>
              <div className="w-4 h-1 bg-white rounded-full"></div>
              <div className="w-10 h-1 bg-white rounded-full"></div>
              <div className="w-28 h-1 bg-white rounded-full"></div>
            </div>
            <h3 className="text-[#1a237e] mb-8">
              Білім беру үдерісінің негізгі <span className="text-[#007dfc]">артықшылықтары</span>
            </h3>
            <ul className="space-y-4 text-[#1a237e]">
              <li className="flex items-start gap-3">
                <span className="text-[#007dfc] mt-1">✓</span>
                <span>Оқытуда озық әдіс-тәсілдер қолданылады</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-[#007dfc] mt-1">✓</span>
                <span>Балалардың сыни ойлау қабілеті дамытылады</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-[#007dfc] mt-1">✓</span>
                <span>Жүйелі топтық жұмыс әдісі енгізілген</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-[#007dfc] mt-1">✓</span>
                <span>Ата-аналармен тұрақты және тиімді байланыс орнатылған</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  )
}
