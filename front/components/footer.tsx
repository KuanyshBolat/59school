export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-primary text-primary-foreground py-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          {/* About */}
          <div>
            <h4 className="font-bold text-lg mb-4">№59 Мектеп-гимназия</h4>
            <p className="text-primary-foreground/80 text-sm">
              Балалардың болашағын ойлай отырып, озық білім беретін мектеп
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-bold text-lg mb-4">Сілтемелер</h4>
            <ul className="space-y-2">
              <li>
                <a href="#about" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Мектеп туралы
                </a>
              </li>
              <li>
                <a href="#director" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Директор
                </a>
              </li>
              <li>
                <a
                  href="#achievements"
                  className="text-primary-foreground/80 hover:text-white transition-colors text-sm"
                >
                  Жетістіктер
                </a>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-bold text-lg mb-4">Қызмет</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Баланың дамуы
                </a>
              </li>
              <li>
                <a href="#" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Олимпиадалар
                </a>
              </li>
              <li>
                <a href="#" className="text-primary-foreground/80 hover:text-white transition-colors text-sm">
                  Іс-шаралар
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold text-lg mb-4">Байланыс</h4>
            <ul className="space-y-2 text-sm">
              <li className="text-primary-foreground/80">+7 (727) 299‒52‒97</li>
              <li>
                <a
                  href="mailto:mektep59@almatybilim.kz"
                  className="text-primary-foreground/80 hover:text-white transition-colors"
                >
                  mektep59@almatybilim.kz
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-primary-foreground/20 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-primary-foreground/80 text-sm">
            © {currentYear} №59 Мектеп-гимназия. Барлық құқықтар сақталған.
          </p>
          
        </div>
      </div>
    </footer>
  )
}
