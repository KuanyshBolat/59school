export default function Director() {
  return (
      <section id="director" className="py-20 px-8 bg-gradient-to-br from-white to-[#f6f6f6]">
          <div className="max-w-7xl mx-auto">
              <div className="grid md:grid-cols-2 gap-12 items-center">
                  <div className="relative">
                      <div className="absolute inset-0 bg-black/5 rounded-full blur-2xl"></div>
                      <div className="relative w-[460px] h-[460px] mx-auto rounded-full overflow-hidden border-8 border-white shadow-2xl">
                          <img
                              src= "/school-director-professional-portrait.jpg"
                              alt="Асан Ержанұлы"
                              className="w-full h-[135%] object-cover object-center -mt-5"
                          />
                      </div>
                      <div className="text-center mt-8">
                          <p className="text-white text-[32px]">Асан Ержанұлы</p>
                      </div>
                  </div>

                  <div className="text-[#1a237e] space-y-6">
                      <p>
                          <span className="text-[#007dfc]">Мектебімізде озық әдіс-тәсілдер қолданылады, сыни ойлау қалыптасады</span>, топтық жұмыс дағдылары дамиды және ата-аналармен тұрақты байланыс ерекше назарда ұсталады.
                      </p>
                      <p>
                          Біз балалардың білімді, жауапты, өз ойын еркін жеткізе алатын, болашаққа сеніммен қадам басатын тұлға болып қалыптасуына жағдай жасаймыз.
                      </p>
                      <p>
                          Сіздермен бірлесе отырып, биік мақсаттарға бірге жетеміз деп сенемін.
                      </p>
                      <p className="pt-4">Ізгі тілекпен,</p>
                      <p>
                          <span>Асан Ержанұлы, </span>
                          <span className="text-[#007dfc]">директор</span>
                      </p>
                  </div>
              </div>
          </div>
      </section>
  )
}
