"use client"

import { useEffect, useState } from "react"
import { X, ChevronLeft, ChevronRight } from "lucide-react"

interface Certificate {
    id: number
    title: string
    year: string
    image: string
    category: "teachers" | "students"
    level: "district" | "city"
}

interface CertificateModalProps {
    isOpen: boolean
    onClose: () => void
    certificates: Certificate[]
    currentIndex: number
    onNavigate: (index: number) => void
    currentCategory: "teachers" | "students"
    onCategoryChange: (category: "teachers" | "students") => void
}

export function CertificateModal({
                                     isOpen,
                                     onClose,
                                     certificates,
                                     currentIndex,
                                     onNavigate,
                                     currentCategory,
                                     onCategoryChange,
                                 }: CertificateModalProps) {
    const [currentLevel, setCurrentLevel] = useState<"district" | "city">("district")

    // Фильтруем сертификаты по текущей категории И уровню
    const filteredCertificates = certificates.filter(
        cert => cert.category === currentCategory && cert.level === currentLevel
    )

    useEffect(() => {
        const handleEscape = (e: KeyboardEvent) => {
            if (e.key === "Escape") onClose()
        }

        const handleArrow = (e: KeyboardEvent) => {
            if (e.key === "ArrowLeft" && currentIndex > 0) {
                onNavigate(currentIndex - 1)
            }
            if (e.key === "ArrowRight" && currentIndex < filteredCertificates.length - 1) {
                onNavigate(currentIndex + 1)
            }
        }

        if (isOpen) {
            document.addEventListener("keydown", handleEscape)
            document.addEventListener("keydown", handleArrow)
            document.body.style.overflow = "hidden"
        }

        return () => {
            document.removeEventListener("keydown", handleEscape)
            document.removeEventListener("keydown", handleArrow)
            document.body.style.overflow = "unset"
        }
    }, [isOpen, currentIndex, filteredCertificates.length, onClose, onNavigate])

    if (!isOpen) return null

    if (filteredCertificates.length === 0) {
        return (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4">
                <div className="relative w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden p-8">
                    <div className="bg-gradient-to-r from-[#1a237e] to-[#007dfc] p-4 -m-8 mb-4">
                        <div className="flex items-center justify-between">
                            <h3 className="text-white text-xl">Сертификаттар</h3>
                            <button
                                onClick={onClose}
                                className="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
                            >
                                <X className="w-6 h-6 text-white" />
                            </button>
                        </div>
                    </div>
                    <div className="text-center py-12">
                        <p className="text-[#1a237e]/60 text-lg">Бұл бөлімде сертификаттар жоқ</p>
                    </div>
                </div>
            </div>
        )
    }

    const currentCertificate = filteredCertificates[currentIndex] || filteredCertificates[0]

    const handlePrevious = () => {
        if (currentIndex > 0) {
            onNavigate(currentIndex - 1)
        }
    }

    const handleNext = () => {
        if (currentIndex < filteredCertificates.length - 1) {
            onNavigate(currentIndex + 1)
        }
    }

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 overflow-y-auto">
            <div className="relative w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden my-8">
                {/* Header */}
                <div className="bg-gradient-to-r from-[#1a237e] to-[#007dfc] p-4">
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-white text-xl">Сертификаттар</h3>
                        <button
                            onClick={onClose}
                            className="w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
                        >
                            <X className="w-6 h-6 text-white" />
                        </button>
                    </div>

                    {/* Category Toggle */}
                    <div className="flex gap-2 bg-white/10 rounded-full p-1 mb-3">
                        <button
                            onClick={() => {
                                onCategoryChange("teachers")
                                onNavigate(0)
                            }}
                            className={`flex-1 py-2 px-3 rounded-full transition-all text-sm ${
                                currentCategory === "teachers" ? "bg-white text-[#1a237e]" : "text-white hover:bg-white/20"
                            }`}
                        >
                            Мұғалімдердің жетістіктері
                        </button>
                        <button
                            onClick={() => {
                                onCategoryChange("students")
                                onNavigate(0)
                            }}
                            className={`flex-1 py-2 px-3 rounded-full transition-all text-sm ${
                                currentCategory === "students" ? "bg-white text-[#1a237e]" : "text-white hover:bg-white/20"
                            }`}
                        >
                            Оқушылардың жетістіктері
                        </button>
                    </div>

                    {/* Level Toggle */}
                    <div className="flex gap-2 bg-white/10 rounded-full p-1">
                        <button
                            onClick={() => {
                                setCurrentLevel("district")
                                onNavigate(0)
                            }}
                            className={`flex-1 py-2 px-3 rounded-full transition-all text-sm ${
                                currentLevel === "district" ? "bg-white text-[#1a237e]" : "text-white hover:bg-white/20"
                            }`}
                        >
                            Аудан деңгейі
                        </button>
                        <button
                            onClick={() => {
                                setCurrentLevel("city")
                                onNavigate(0)
                            }}
                            className={`flex-1 py-2 px-3 rounded-full transition-all text-sm ${
                                currentLevel === "city" ? "bg-white text-[#1a237e]" : "text-white hover:bg-white/20"
                            }`}
                        >
                            Қала деңгейі
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="p-4 max-h-[calc(100vh-280px)] overflow-y-auto">
                    {/* Certificate Image */}
                    <div className="relative bg-[#f6f6f6] rounded-xl overflow-hidden mb-4">
                        <img
                            src={currentCertificate.image || "/placeholder.svg"}
                            alt={currentCertificate.title}
                            className="w-full h-auto max-h-[400px] object-contain"
                        />
                    </div>

                    {/* Certificate Info */}
                    <div className="text-center mb-4">
                        <div className="inline-block px-3 py-1 bg-[#007dfc]/10 text-[#007dfc] rounded-full text-sm mb-2">
                            {currentCertificate.level === "district" ? "Аудан деңгейі" : "Қала деңгейі"}
                        </div>
                        <h4 className="text-[#1a237e] mb-1 text-lg">{currentCertificate.title}</h4>
                        <p className="text-[#1a237e]/60">{currentCertificate.year}</p>
                    </div>

                    {/* Navigation */}
                    <div className="flex items-center justify-between mb-4">
                        <button
                            onClick={handlePrevious}
                            disabled={currentIndex === 0}
                            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                                currentIndex === 0 ? "text-gray-400 cursor-not-allowed" : "text-[#007dfc] hover:bg-[#007dfc]/10"
                            }`}
                        >
                            <ChevronLeft className="w-5 h-5" />
                            <span>Алдыңғы</span>
                        </button>

                        <div className="text-[#1a237e]/60">
                            {currentIndex + 1} / {filteredCertificates.length}
                        </div>

                        <button
                            onClick={handleNext}
                            disabled={currentIndex === filteredCertificates.length - 1}
                            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                                currentIndex === filteredCertificates.length - 1
                                    ? "text-gray-400 cursor-not-allowed"
                                    : "text-[#007dfc] hover:bg-[#007dfc]/10"
                            }`}
                        >
                            <span>Келесі</span>
                            <ChevronRight className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Thumbnails */}
                    <div className="flex gap-2 overflow-x-auto pb-2">
                        {filteredCertificates.map((cert, index) => (
                            <button
                                key={cert.id}
                                onClick={() => onNavigate(index)}
                                className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all ${
                                    index === currentIndex
                                        ? "border-[#007dfc] ring-2 ring-[#007dfc]/30"
                                        : "border-gray-200 hover:border-[#007dfc]/50"
                                }`}
                            >
                                <img src={cert.image || "/placeholder.svg"} alt={cert.title} className="w-full h-full object-cover" />
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}