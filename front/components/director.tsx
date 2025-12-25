 "use client"

import { useEffect, useState } from 'react'
import { apiService } from '@/lib/api'

export default function Director() {
  const [director, setDirector] = useState<any | null>(null)

  const fallback = {
    name: 'Асан Ержанұлы',
    title: 'директор',
    bio: 'Мектебімізде озық әдіс-тәсілдер қолданылады, сыни ойлау қалыптасады',
    image: '/school-director-professional-portrait.jpg'
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

  return (
      <section id="director" className="py-20 px-8 bg-gradient-to-br from-white to-[#f6f6f6]">
          <div className="max-w-7xl mx-auto">
              <div className="grid md:grid-cols-2 gap-12 items-center">
                  <div className="relative">
                      <div className="absolute inset-0 bg-black/5 rounded-full blur-2xl"></div>
                      <div className="relative w-[460px] h-[460px] mx-auto rounded-full overflow-hidden border-8 border-white shadow-2xl">
                          <img
                              src={d.image}
                              alt={d.name}
                              className="w-full h-[135%] object-cover object-center -mt-5"
                          />
                      </div>
                      <div className="text-center mt-8">
                          <p className="text-white text-[32px]">{d.name}</p>
                      </div>
                  </div>

                  <div className="text-[#1a237e] space-y-6">
                      <p>
                          <span className="text-[#007dfc]">{d.bio}</span>
                      </p>
                      <p>
                          Біз балалардың білімді, жауапты, өз ойын еркін жеткізе алатын, болашаққа сеніммен қадам басатын тұлға болып қалыптасуына жағдай жасаймыз.
                      </p>
                      <p>
                          Сіздермен бірлесе отырып, биік мақсаттарға бірге жетеміз деп сенемін.
                      </p>
                      <p className="pt-4">Ізгі тілекпен,</p>
                      <p>
                          <span>{d.name}, </span>
                          <span className="text-[#007dfc]">{d.title}</span>
                      </p>
                  </div>
              </div>
          </div>
      </section>
  )
}
