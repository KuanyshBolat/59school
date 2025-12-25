"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Phone, Mail, MapPin, Send } from "lucide-react"
import { apiService } from '@/lib/api'

export default function Contact() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  })
  const [loading, setLoading] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<"idle" | "success" | "error">("idle")
  const [statusMessage, setStatusMessage] = useState("")
  const [contact, setContact] = useState<any | null>(null)

  useEffect(() => {
    let mounted = true
    apiService.getContact().then(data => { if (!mounted) return; if (data) setContact(data) })
    .catch(() => {})
    return () => { mounted = false }
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setSubmitStatus("idle")

    try {
      const response = await fetch("/api/send-message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (response.ok) {
        setSubmitStatus("success")
        setStatusMessage("Хабарламаныз сәтті жіберілді!")
        setFormData({ name: "", email: "", message: "" })
        setTimeout(() => setSubmitStatus("idle"), 5000)
      } else {
        setSubmitStatus("error")
        setStatusMessage(data.error || "Жіберу кезінде ақау байқалды")
      }
    } catch (error) {
      console.error("[v0] Form submission error:", error)
      setSubmitStatus("error")
      setStatusMessage("Желілік ақау, кеінірек қайта жіберіп көрініз.")
    } finally {
      setLoading(false)
    }
  }

  const phone = contact?.phone || '+7 (727) 299‒52‒97'
  const email = contact?.email || 'mektep59@almatybilim.kz'
  const address = contact?.address || 'Алматы қаласы, Түрксіб ауданы, Т.Сауранбаев к-сі 12а'
  const textColor = contact?.text_color || '#333333'

  return (
    <section id="contact" className="py-16 md:py-24 px-4 bg-white">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-primary mb-12 text-center">Байланыс</h2>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Contact Info */}
          <div className="space-y-8">
            <h3 className="text-2xl font-bold text-foreground mb-6">Бізге хабарласыңыз</h3>

            <div className="flex gap-4" style={{ color: textColor }}>
              <div className="flex-shrink-0">
                <Phone className="w-6 h-6 text-accent mt-1" />
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Телефон</h4>
                <p className="text-muted-foreground">{phone}</p>
              </div>
            </div>

            <div className="flex gap-4" style={{ color: textColor }}>
              <div className="flex-shrink-0">
                <Mail className="w-6 h-6 text-accent mt-1" />
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Эл. пошта</h4>
                <p className="text-muted-foreground">{email}</p>
              </div>
            </div>

            <div className="flex gap-4" style={{ color: textColor }}>
              <div className="flex-shrink-0">
                <MapPin className="w-6 h-6 text-accent mt-1" />
              </div>
              <div>
                <h4 className="font-semibold text-foreground">Мекенжайымыз</h4>
                <p className="text-muted-foreground" style={{ whiteSpace: 'pre-wrap' }}>{address}</p>
              </div>
            </div>

            <div className="mt-8 rounded-lg overflow-hidden shadow-md h-96">
              <iframe
                id="map_63218287"
                frameBorder="0"
                width="100%"
                height="100%"
                title="Мектеб орналасқан жері"
                src="https://makemap.2gis.ru/widget?data=eJw1j91Kw0AQhd9lvA11s9n8glcRRQmlRaFU6UXojnV1mwnbqdiGvruTqHMzMGfOmW8GoGAxoL1H2iMHhweoXgfgU49QwR22fAwIEfSBegw86QNsyVMQ_UrpIn7TorNjPzrU43nJts7Uuhn7dWPrs2o-ll_zulTN7ZLL2qh1sTP0tJo_f96I1eJhG1zPjjoJkMH5obP4DVWs_usSwe4X8DSe_6NbkOtY9rckT7iu5Qk-z2alKXReRCaZJYnJknQjfmehMrm-bCLYt_2CDu734AC-ZZGmXZXGWmdJaVQZgR_lMS1ViYrzXBfKpFrwiPYCl0mogJP3q3dE_zJNORzx8gOOvWfy"
                sandbox="allow-modals allow-forms allow-scripts allow-same-origin allow-popups allow-top-navigation-by-user-activation"
              />
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <form onSubmit={handleSubmit} className="space-y-6 bg-muted p-8 rounded-lg">
              <h3 className="text-2xl font-bold text-foreground">Хабарлама жіберіңіз</h3>

              <div>
                <label htmlFor="name" className="block text-sm font-medium text-foreground mb-2">
                  Атыңыз
                </label>
                <input
                  type="text"
                  id="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Атыңыз"
                  className="w-full px-4 py-2 border border-border rounded-lg bg-white text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                  Эл. пошта
                </label>
                <input
                  type="email"
                  id="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  placeholder="example@email.com"
                  className="w-full px-4 py-2 border border-border rounded-lg bg-white text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  required
                  disabled={loading}
                />
              </div>

              <div>
                <label htmlFor="message" className="block text-sm font-medium text-foreground mb-2">
                  Хабарламасы
                </label>
                <textarea
                  id="message"
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  placeholder="Сіздің хабарламасы..."
                  rows={4}
                  className="w-full px-4 py-2 border border-border rounded-lg bg-white text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                  required
                  disabled={loading}
                />
              </div>

              {submitStatus === "success" && (
                <div className="p-3 bg-green-100 text-green-800 rounded-lg text-sm">{statusMessage}</div>
              )}
              {submitStatus === "error" && (
                <div className="p-3 bg-red-100 text-red-800 rounded-lg text-sm">{statusMessage}</div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-primary hover:bg-primary/90 disabled:bg-gray-400 text-primary-foreground font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
              >
                <Send size={18} />
                {loading ? "Жіберілуде..." : "Жіберіңіз"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  )
}
