"use client"

import { useState, useEffect } from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { apiService, HeroSlide } from '@/lib/api'

export default function Hero() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [slides, setSlides] = useState<HeroSlide[]>([])

  const fallbackSlides: HeroSlide[] = [
    {
      id: 0,
      image: "/modern-school-students.jpg",
      title: "№59 Мектеп гимназиясына қош келдіңіз",
      subtitle: "Болашақтың лидерлерін қалыптастыратын білім ордасы",
      order: 1,
    },
    {
      id: 1,
      image: "/students-learning-in-classroom-together.jpg",
      title: "Сапалы білім беру",
      subtitle: "Озық технологиялар мен ынталы мұғалімдерден құралған білім ордасы",
      order: 2,
    },
    {
      id: 2,
      image: "/diverse-students-teamwork-achievement.jpg",
      title: "Жетістіктің жолы",
      subtitle: "әрбір оқушының жеке қабілеті ашылып, жан-жақты дамытылады",
      order: 3,
    },
  ]

  useEffect(() => {
    let mounted = true
    apiService.getHeroSlides().then(data => {
      if (!mounted) return
      if (Array.isArray(data) && data.length > 0) setSlides(data)
      else setSlides(fallbackSlides)
    }).catch(() => setSlides(fallbackSlides))

    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % Math.max(1, slides.length))
    }, 5000)
    return () => { mounted = false; clearInterval(timer) }
  }, [])

  useEffect(() => {
    // reset currentSlide if slides changed
    setCurrentSlide(0)
  }, [slides])

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length)
  }

  const visibleSlides = slides.length ? slides : fallbackSlides

  return (
    <section id="hero" className="relative pt-16 w-full h-screen overflow-hidden">
      {/* Carousel */}
      <div className="relative w-full h-full">
        {visibleSlides.map((slide, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentSlide ? "opacity-100" : "opacity-0"
            }`}
          >
            <img src={slide.image || "/placeholder.svg"} alt={slide.title} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-black/40" />
            <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
              <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-white mb-4 text-balance">{slide.title}</h1>
              <p className="text-lg sm:text-xl md:text-2xl text-white/90 max-w-2xl text-balance">{slide.subtitle}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Navigation Buttons */}
      <button
        onClick={prevSlide}
        className="absolute left-4 sm:left-8 top-1/2 -translate-y-1/2 z-20 bg-primary/80 hover:bg-primary text-white p-2 sm:p-3 rounded-full transition-colors"
        aria-label="Previous slide"
      >
        <ChevronLeft size={24} />
      </button>
      <button
        onClick={nextSlide}
        className="absolute right-4 sm:right-8 top-1/2 -translate-y-1/2 z-20 bg-primary/80 hover:bg-primary text-white p-2 sm:p-3 rounded-full transition-colors"
        aria-label="Next slide"
      >
        <ChevronRight size={24} />
      </button>

      {/* Dots */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-20 flex gap-2">
        {visibleSlides.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-3 h-3 rounded-full transition-all ${
              index === currentSlide ? "bg-white w-8" : "bg-white/50 hover:bg-white/75"
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>
    </section>
  )
}
