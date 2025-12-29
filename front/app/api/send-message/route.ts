import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { name, email, message } = await request.json()

    // Telegram Bot API параметры
    const botToken = process.env.TELEGRAM_BOT_TOKEN
    const chatId = process.env.TELEGRAM_CHAT_ID

    if (!botToken || !chatId) {
      console.error("[v0] Telegram credentials not set in environment")
      return NextResponse.json({ error: "Telegram credentials not configured" }, { status: 500 })
    }

    // Форматирование сообщения
    const telegramMessage = `
📧 Новое сообщение с сайта школы

👤 Имя: ${name}
📨 Email: ${email}
💬 Сообщение: ${message}
    `.trim()

    // Отправка в Telegram
    const telegramResponse = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        chat_id: chatId,
        text: telegramMessage,
        parse_mode: "HTML",
      }),
    })

    if (!telegramResponse.ok) {
      const error = await telegramResponse.json()
      console.error("[v0] Telegram API error:", error)
      return NextResponse.json({ error: "Ошибка при отправке сообщения" }, { status: 500 })
    }

    return NextResponse.json({ success: true, message: "Сообщение успешно отправлено" }, { status: 200 })
  } catch (error) {
    console.error("[v0] Error sending message:", error)
    return NextResponse.json({ error: "Внутренняя ошибка сервера" }, { status: 500 })
  }
}
