export default function Stats() {
  const stats = [
    { number: "1420", label: "Оқушылар" },
    { number: "104", label: "Мұғалімдер" },
    { number: "9", label: "Жыл мектепке" },
    { number: "200+", label: "Жетістіктер" },
  ]

  return (
    <section id="stats" className="py-16 md:py-24 px-4 bg-primary">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl md:text-5xl font-bold text-white mb-2">{stat.number}</div>
              <p className="text-primary-foreground/80 text-lg">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
