"use client"

import { useState, useEffect } from "react"
import { CertificateModal } from "./certificate-modal"
import { apiService, Certificate } from "@/lib/api"

export function Achievements() {
    const [activeTab, setActiveTab] = useState<"teachers" | "students">("teachers")
    const [activeLevel, setActiveLevel] = useState<"district" | "city">("district")
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [currentIndex, setCurrentIndex] = useState(0)
    const [certificates, setCertificates] = useState<Certificate[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        loadCertificates();
    }, []);

    const loadCertificates = async () => {
        try {
            setLoading(true);
            const data = await apiService.getCertificates();
            setCertificates(data);
        } catch (error) {
            console.error('Error loading certificates:', error);
        } finally {
            setLoading(false);
        }
    };

    const displayedCertificates = certificates
        .filter((cert) => cert.category === activeTab)
        .filter((cert) => cert.level === activeLevel);

    const handleCertificateClick = (certificate: Certificate) => {
        const index = certificates.findIndex((cert) => cert.id === certificate.id)
        setCurrentIndex(index)
        setIsModalOpen(true)
    }

    const handleCategoryChange = (category: "teachers" | "students") => {
        setActiveTab(category)
        const firstCertIndex = certificates.findIndex((cert) => cert.category === category)
        if (firstCertIndex !== -1) {
            setCurrentIndex(firstCertIndex)
        }
    }

    if (loading) {
        return (
            <section id="Achievements" className="py-20 px-8">
                <div className="max-w-7xl mx-auto text-center">
                    <p className="text-[#1a237e]/60">Жүктелуде...</p>
                </div>
            </section>
        );
    }

    return (
        <section id="Achievements" className="py-20 px-8">
            <div className="max-w-7xl mx-auto">
                {/* Main Category Toggle */}
                <div className="mb-8">
                    <div className="relative inline-flex items-center gap-4 p-2 border-4 border-[#007dfc] rounded-full mx-auto left-1/2 -translate-x-1/2">
                        <button
                            onClick={() => handleCategoryChange("teachers")}
                            className={`px-8 py-3 rounded-full transition-all ${
                                activeTab === "teachers" ? "bg-[#007dfc] text-white" : "text-[#1a237e]/50 hover:text-[#1a237e]"
                            }`}
                        >
                            Мұғалімдердің жетістіктері
                        </button>
                        <button
                            onClick={() => handleCategoryChange("students")}
                            className={`px-8 py-3 rounded-full transition-all ${
                                activeTab === "students" ? "bg-[#007dfc] text-white" : "text-[#1a237e]/50 hover:text-[#1a237e]"
                            }`}
                        >
                            Оқушылардың жетістіктері
                        </button>
                    </div>
                </div>

                {/* Level Filter */}
                <div className="mb-8 flex justify-center">
                    <div className="inline-flex items-center gap-3 bg-white rounded-full p-1.5 shadow-md">
                        <button
                            onClick={() => setActiveLevel("district")}
                            className={`px-6 py-2 rounded-full transition-all ${
                                activeLevel === "district" ? "bg-[#F64C00] text-white" : "text-[#1a237e] hover:bg-gray-100"
                            }`}
                        >
                            Аудан деңгейіндегі жетістіктер
                        </button>
                        <button
                            onClick={() => setActiveLevel("city")}
                            className={`px-6 py-2 rounded-full transition-all ${
                                activeLevel === "city" ? "bg-[#F64C00] text-white" : "text-[#1a237e] hover:bg-gray-100"
                            }`}
                        >
                            Қала деңгейіндегі жетістіктер
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {displayedCertificates.map((certificate) => (
                        <button
                            key={certificate.id}
                            onClick={() => handleCertificateClick(certificate)}
                            className="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-2xl transition-all transform hover:-translate-y-2 group"
                        >
                            <div className="aspect-[1/1] overflow-hidden bg-[#efefef]">
                                <img
                                    src={certificate.image}  // Убираем добавление URL, так как это уже сделано в api.ts
                                    alt={certificate.title}
                                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                                    onError={(e) => {
                                        // Fallback если изображение не загрузилось
                                        e.currentTarget.src = '/placeholder.svg';
                                    }}
                                />
                            </div>
                        </button>
                    ))}
                </div>

                {displayedCertificates.length === 0 && (
                    <div className="text-center py-12">
                        <p className="text-[#1a237e]/60">Әзірге сертификаттар жоқ</p>
                    </div>
                )}
            </div>

            <CertificateModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                certificates={certificates}
                currentIndex={currentIndex}
                onNavigate={setCurrentIndex}
                currentCategory={activeTab}
                onCategoryChange={handleCategoryChange}
            />
        </section>
    )
}