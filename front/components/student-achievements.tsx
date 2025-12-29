"use client"

import { useState } from "react"
import { CertificateModal } from "./certificate-modal"

type CertificateItem = {
  id: number
  title: string
  year: string
  image: string
  category: "teachers" | "students"
  level: "district" | "city"
}

export default function StudentAchievements() {
  const [modalOpen, setModalOpen] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(0)
  const [currentCategory, setCurrentCategory] = useState<"students" | "teachers">("students")
  const [currentLevel, setCurrentLevel] = useState<"district" | "city">("district")

  const certificates: CertificateItem[] = [
    {
      id: 1,
      title: 'Сертификат 1',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/1.jpg",
    },
    {
      id: 2,
      title: 'Сертификат 2',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/2.jpg",
    },
    {
      id: 3,
      title: 'Сертификат 3',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/3.jpg",
    },
    {
      id: 4,
      title: 'Сертификат 4',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/4.jpg",
    },
    {
      id: 5,
      title: 'Сертификат 5',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/5.jpg",
    },
    {
      id: 6,
      title: 'Сертификат 6',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/6.jpg",
    },
    {
      id: 7,
      title: 'Сертификат 7',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/7.jpg",
    },
    {
      id: 8,
      title: 'Сертификат 8',
      year: '2023',
      category: 'students',
      level: 'district',
      image: "/student/8.jpg",
    },
  ]

  return (
    <section id="student-achievements" className="py-16 md:py-24 px-4 bg-gray-50">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-primary mb-12 text-center">Оқушылардың жетістіктері</h2>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-4">
          {certificates.map((cert, index) => (
            <button
              key={cert.id}
              onClick={() => {
                setCurrentLevel(cert.level)
                const filtered = certificates.filter(c => c.category === currentCategory && c.level === cert.level)
                const idx = filtered.findIndex(c => c.id === cert.id)
                setSelectedIndex(idx === -1 ? 0 : idx)
                setModalOpen(true)
              }}
              className="relative overflow-hidden rounded-lg shadow-md hover:shadow-lg transition-all hover:scale-105 group cursor-pointer bg-gray-100 aspect-square"
            >
              <img
                src={cert.image || "/placeholder.svg"}
                alt={cert.title}
                className="w-full h-full object-cover group-hover:brightness-75 transition-all duration-300"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent flex items-end opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-full p-2 md:p-3 text-white text-xs md:text-sm font-semibold line-clamp-2">
                  {cert.title}
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {modalOpen && (
        <CertificateModal
          isOpen={modalOpen}
          onClose={() => setModalOpen(false)}
          certificates={certificates}
          currentIndex={selectedIndex}
          onNavigate={setSelectedIndex}
          currentCategory={currentCategory}
          onCategoryChange={setCurrentCategory}
          currentLevel={currentLevel}
          onLevelChange={setCurrentLevel}
        />
      )}
    </section>
  )
}
