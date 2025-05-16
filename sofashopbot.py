import functions, configs
from telegram import Update, ReplyKeyboardMarkup,  ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, \
    ConversationHandler

token = configs.TOKEN
ARTICULE, NAME, CONTACTS, ADDRESS, CASH_OR_CARD, CONFIRM = range(6)
articule_number = ""
fio = ""
contact_info = ""
address_data = ""
payment = ""

async def texting(update, context) -> None:
    chat_id = update.message.chat_id
    answer, image = functions.bot(update.message.text)
    if image and image != "":
        await context.bot.send_photo(chat_id=chat_id, photo=image, caption=answer)
    else: await update.message.reply_text(answer)

async def start(update, context) -> None:
    await update.message.reply_text("Здравствуйте! Давайте начнём наш диалог\nВведите /catalog, чтобы ознакомиться с нашими товарами\nВведите /order, если хотите сделать заказ\nВведите /faq, чтобы получить ответы на интересующие вопросы\nВведите /help, чтобы увидеть список доступных команд)")

async def help(update, context) -> None:
    await update.message.reply_text("Нужна помощь? Введите /start, чтобы начать\nВведите /faq, чтобы получить ответы на интересующие вопросы\nВведите /contacts для получения контактной информации\nВведите /catalog, чтобы ознакомиться с нашими товарами\nВведите /cart, чтобы добавить предмет в корзину\nВведите /order, если хотите сделать заказ")

async def faq(update, context) -> None:
    await update.message.reply_text("1) Что это за компания? \nSuperSofaShop - лучший мебельный магазин во всей Москве. Мы работаем с 2022 года, однако наше качество ничуть не уступает маститым производителям!\n"+
    "2) Почему именно мы?\nВ первую очередь, мы думаем о клиенте и предлагаем ему наилучшие варианты в соответствии с его потребностями. А во-вторых... все остальные)\n"+
                                    "3) Как нас найти? \nНаш магазин находится по адресу: г. Москва, ул. Галушки Борисова, д. 6. Будем рады вас видеть!\n"+
                                    "4) Как оформить у вас заказ?\nВы можете оформить заказ на нашем официальном сайте или здесь с помощью команды /order\n"+
                                    "5) Как осуществляется доставка?\nМы доставляем мебель в любую точку Москвы или Подмосковья. Доставка бесплатная.\n"+
                                    "6) Собираете ли вы мебель?\nМы осуществляем сборку мебели только по желанию клиента. Стоимость сборки зависит от сложности работ и высчитывается вместе с клиентом на предварительном созвоне.")

async def info(update, context) -> None:
    await update.message.reply_text("Телефон для связи: +799999999999\nНаша почта: sofa@shop.ru\nСайт sofashop.ru\nНаш адрес: г. Москва, ул. Галушки Борисова, д. 6")

async def catalog(update, context) -> None:
    cat = ""
    for i in configs.CATOLOG:
        cat += i + "\n"
    await update.message.reply_text(f"{cat}\nЧтобы узнать о товаре больше, введите его наименование, а я вам выдам всю информацию!")

async def order(update, context) -> int:
    if articule_number != "":
        await update.message.reply_text("Введите ФИО заказчика без запятых")
        return NAME
    await update.message.reply_text("Введите точное наименование артикула")
    return ARTICULE

async def articule(update, context) -> int:
    global articule_number
    articule_number = update.message.text
    await update.message.reply_text("Введите ФИО заказчика без запятых")
    return NAME

async def name(update, context) -> int:
    global fio
    fio = update.message.text
    await update.message.reply_text("Введите контактную информацию:\n-Либо номер телефона в формате +7**********\n-Либо адрес электронной почты в формате user@domain.ru")
    return CONTACTS

async def contacts(update, context) -> int:
    global contact_info
    contact_info = update.message.text
    await update.message.reply_text("Укажите адрес доставки")
    return ADDRESS

async def address(update, context) -> int:
    global address_data
    address_data = update.message.text
    reply_keyboard = [["Наличными", "Картой"]]
    await update.message.reply_text("Укажите способ оплаты", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Наличными или картой?"))
    return CASH_OR_CARD

async def cash_or_card(update, context) -> int:
    global payment, articule_number, fio, contact_info, address_data
    payment = update.message.text
    reply_keyboard = [["ДА", "НЕТ"]]
    await update.message.reply_text(f"Подтверждаете оформление заказа?\nДетали:\nФИО: {fio}\nАртикул: {articule_number}\nКонтакты: {contact_info}\nАдрес доставки: {address_data}\nОплата {payment.lower()}", reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder="ДА/НЕТ"))
    return CONFIRM

async def confirmation(update, context) -> int:
    yes_no = update.message.text
    global articule_number, fio, contact_info, address_data, payment
    if yes_no == "ДА":
        functions.orders_record(articule_number, fio, contact_info, address_data, payment)
        await update.message.reply_text("Благодарим за оформление! С вами свяжутся по деталям заказа)", reply_markup=ReplyKeyboardRemove())
    else:
        await update.message.reply_text("Вы отменили заказ!", reply_markup=ReplyKeyboardRemove())
    articule_number = ""
    fio = ""
    contact_info = ""
    address_data = ""
    payment = ""
    return ConversationHandler.END

async def cancel(update, context) -> int:
    global fio, articule_number, contact_info, address_data, payment
    fio = ""
    articule_number = ""
    contact_info = ""
    address_data = ""
    payment = ""
    await update.message.reply_text("Отмена заказа!")
    return ConversationHandler.END

async def cart(update, context) -> int:
    await update.message.reply_text("Введите наименование товара, а я добавлю его в корзину!")
    return 0

async def add_to_cart(update, context) -> int:
    a = update.message.text.lower()
    a = a[0].upper() + a[1:]
    global articule_number
    if a in configs.GOODS:
        if articule_number != "": articule_number += ", "
        articule_number += a
        await update.message.reply_text("Предмет успешно добавлен в корзину! Чтобы просмотреть корзину, введите /view")
    else:
        await update.message.reply_text("Извините, но такого предмета в каталоге нет(")
    return ConversationHandler.END

async def view_cart(update, context) -> None:
    global articule_number
    c = articule_number.split(", ")
    n = ""
    for i in c:
        n += f"{i}\n"
    await update.message.reply_text(f"Ваша корзина:\n{n}")

def main():
    print("Bot is started")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("catalog", catalog))
    application.add_handler(CommandHandler("contacts", info))
    application.add_handler(CommandHandler("faq", faq))
    application.add_handler(CommandHandler("view", view_cart))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("cart",cart)],
                                                states={0: {MessageHandler(filters.TEXT & ~filters.COMMAND, add_to_cart)}},
                                                fallbacks=[CommandHandler("add", add_to_cart)]))
    application.add_handler(ConversationHandler(entry_points=[CommandHandler("order", order)],
                                                states={ARTICULE: [MessageHandler(filters.TEXT & ~filters.COMMAND, articule)],
                                                    NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
                                                    CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, contacts)],
                                                    ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)],
                                                    CASH_OR_CARD: [MessageHandler(filters.Regex("^(Наличными|Картой)$"),cash_or_card)],
                                                    CONFIRM: [MessageHandler(filters.Regex("^(ДА|НЕТ)$"), confirmation)]},
                                                fallbacks=[CommandHandler("cancel", cancel)]))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texting))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()