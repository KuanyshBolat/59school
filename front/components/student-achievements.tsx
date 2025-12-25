"use client"

import { useState } from "react"
import CertificateModal from "./certificate-modal"

export default function StudentAchievements() {
  const [modalOpen, setModalOpen] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(0)

  const certificates = [
    {
      id: 1,
      image: "/student/1.jpg",
    },
    {
      id: 2,
      image: "/student/2.jpg",
    },
    {
      id: 3,
      image: "/student/3.jpg",
    },
    {
      id: 4,
      image: "/student/4.jpg",
    },
    {
      id: 5,
      image: "/student/5.jpg",
    },
    {
      id: 6,
      image: "/student/6.jpg",
    },
    {
      id: 7,
      image: "/student/7.jpg",
    },
    {
      id: 8,
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
                setSelectedIndex(index)
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
          certificates={certificates}
          selectedIndex={selectedIndex}
          onClose={() => setModalOpen(false)}
          onNavigate={setSelectedIndex}
        />
      )}
    </section>
  )
}
