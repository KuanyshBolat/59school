"use client"

import { useEffect, useState } from 'react'
import { apiService } from '@/lib/api'

export default function Director() {
  const [director, setDirector] = useState<any | null>(null)

  const fallback = {
    name: 'Асан Ержанұлы',
    title: 'директор',
    bio: 'Мектебімізде озық әдіс-тәсілдер қолданылады, сыни ойлау қалыптасады',
    image: '/school-director-professional-portrait.jpg',
    name_color: '#000000',
    bio_color: '#333333'
  }

  useEffect(() => {
    let mounted = true
    apiService.getDirector().then(data => {
      if (!mounted) return
      if (data) setDirector(data)
      else setDirector(fallback)
    }).catch(() => setDirector(fallback))
    return () => { mounted = false }
  }, [])

  const d = director || fallback
  const nameColor = d?.name_color || '#000000'
  const bioColor = d?.bio_color || '#333333'

  return (
      <section id="director" className="py-20 px-8 bg-gradient-to-br from-white to-[#f6f6f6]">
          <div className="max-w-7xl mx-auto">
              <div className="grid md:grid-cols-2 gap-12 items-center">
                  <div className="relative text-center md:text-left">
                      <div className="absolute inset-0 bg-black/5 rounded-full blur-2xl"></div>
                      <div className="relative mx-auto md:mx-0 w-40 sm:w-56 md:w-72 lg:w-[460px] aspect-square rounded-full overflow-hidden border-8 border-white shadow-2xl">
                          <img loading="lazy"
                              src={d.image}
                              alt={d.name}
                              className="w-full h-full object-cover object-center"
                          />
                      </div>
                      <div className="text-center mt-6 md:mt-8">
                          <p className="text-[24px] md:text-[32px] font-semibold" style={{ color: nameColor }}>{d.name}</p>
                      </div>
                  </div>

                  <div className="space-y-6">
                      <p style={{ color: bioColor, whiteSpace: 'pre-wrap' }}>
                        {d.bio}
                      </p>

                      <p className="pt-4">Ізгі тілекпен,</p>
                      <p>
                          <span style={{ color: nameColor }}>{d.name}, </span>
                          <span className="text-[#007dfc]">{d.title}</span>
                      </p>
                  </div>
              </div>
          </div>
      </section>
  )
}
