import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters
import asyncio
import random
from AppToken import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

milk_factories = [
    ["Улица Белого потока, 10", "Молокозавод 'Белый поток'"],
    ["Природный проезд, 5", "Молокозавод 'Куркуля'"],
    ["Молочная улица, 12", "Молокозавод 'АгроМолоко'"],
    ["Поляна 1-й, 7", "Молокозавод 'Золотая ферма'"],
    ["Зимний бульвар, 4", "Молокозавод 'Снежный дол'"],
    ["Луговая улица, 9", "Молокозавод 'Луговое молоко'"],
    ["Полевая дорога, 13", "Молокозавод 'АгроМир'"],
    ["Горный проезд, 8", "Молокозавод 'Молочная горка'"],
    ["Северный переулок, 3", "Молокозавод 'Северное молоко'"],
    ["Вершки 4-й, 6", "Молокозавод 'Вершки и корешки'"],
    ["Лесной путь, 11", "Молокозавод 'Лесной ключ'"],
    ["Деревенская улица, 15", "Молокозавод 'Деревенский вкус'"],
    ["Молочная площадь, 14", "Молокозавод 'Молочная звезда'"],
    ["Крайняя улица, 21", "Молокозавод 'Молочный край'"],
    ["Облачная улица, 16", "Молокозавод 'Нежное облако'"],
    ["Белое золото, 18", "Молокозавод 'Белое золото'"],
    ["Горный проезд, 23", "Молокозавод 'Горное молоко'"],
    ["Молочный мост, 22", "Молокозавод 'Молочный союз'"],
    ["Вкусная аллея, 30", "Молокозавод 'Поляна вкуса'"],
    ["Сельская дорога, 25", "Молокозавод 'Сельское молоко'"],
    ["Речная улица, 28", "Молокозавод 'Речное утро'"],
    ["АгроДеревня, 5", "Молокозавод 'АгроДеревня'"],
    ["Полевая аллея, 27", "Молокозавод 'Вкусное поле'"],
    ["Солнечная площадь, 29", "Молокозавод 'Солнце Луга'"],
    ["Белый хутор, 34", "Молокозавод 'Белый хутор'"],
    ["Молочные дали, 6", "Молокозавод 'Молочные дали'"],
    ["Фермерская улица, 3", "Молокозавод 'Фермерский вкус'"],
    ["Сливочный проезд, 31", "Молокозавод 'Сливочный мир'"],
    ["Здоровье 8-й, 20", "Молокозавод 'Здоровое молоко'"],
    ["Утренний бульвар, 24", "Молокозавод 'Белоснежное утро'"],
    ["Коровкин переулок, 17", "Молокозавод 'Коровкин дом'"],
    ["Сливочная долина, 2", "Молокозавод 'Сливочная долина'"],
    ["Премиум улица, 18", "Молокозавод 'Премиум молоко'"],
    ["ЭкоМолоко, 9", "Молокозавод 'ЭкоМолоко'"],
    ["Лунная ферма, 11", "Молокозавод 'Лунная ферма'"],
    ["Родные поля, 10", "Молокозавод 'Родные поля'"],
    ["Молоко жизни, 8", "Молокозавод 'Молоко жизни'"],
    ["Исток, 14", "Молокозавод 'Молочный источник'"],
    ["Сливки села, 3", "Молокозавод 'Сливки села'"],
    ["Молочная страна, 5", "Молокозавод 'Молочная страна'"],
    ["Снежное утро, 7", "Молокозавод 'Снежное утро'"],
    ["Душистая улица, 13", "Молокозавод 'Душистое молоко'"],
    ["Луговая свежесть, 12", "Молокозавод 'Луговая свежесть'"],
    ["Солнечное пастбище, 4", "Молокозавод 'Солнечное пастбище'"],
    ["Гармония вкуса, 9", "Молокозавод 'Гармония вкуса'"],
    ["Белая корова, 16", "Молокозавод 'Белая корова'"],
    ["Родной вкус, 8", "Молокозавод 'Родной вкус'"],
    ["Кремовый рай, 6", "Молокозавод 'Кремовый рай'"],
    ["Ароматный луг, 18", "Молокозавод 'Ароматный луг'"],
    ["Нежный поток, 12", "Молокозавод 'Нежный поток'"]
]

farms = [
    "Ферма 'Золотой плуг'",
    "Ферма 'Родная земля'",
    "Ферма 'Солнечный сад'",
    "Ферма 'Зеленая поляна'",
    "Ферма 'Сельский дом'",
    "Ферма 'Серебряный источник'",
    "Ферма 'Лесное чудо'",
    "Ферма 'Родной хутор'",
    "Ферма 'Зорька'",
    "Ферма 'Молочная лагуна'",
    "Ферма 'Деревенская сказка'",
    "Ферма 'Светлый край'",
    "Ферма 'Коровий рай'",
    "Ферма 'Сочные травы'",
    "Ферма 'Сельская звезда'",
    "Ферма 'Лесной домик'",
    "Ферма 'Долина жизни'",
    "Ферма 'Куркульский уголок'",
    "Ферма 'Утренний свет'",
    "Ферма 'Молочная тропа'",
    "Ферма 'Край родной'",
    "Ферма 'Пастбище здоровья'",
    "Ферма 'Вкус природы'",
    "Ферма 'Сельская ширь'",
    "Ферма 'Коровий ключ'",
    "Ферма 'Здоровая жизнь'",
    "Ферма 'Утренний ручей'",
    "Ферма 'Молочная радуга'",
    "Ферма 'Пастбище счастья'",
    "Ферма 'Белая долина'",
    "Ферма 'Деревенский рассвет'",
    "Ферма 'Поле мечты'",
    "Ферма 'Родной угол'",
    "Ферма 'Солнечный простор'",
    "Ферма 'Жемчужный луг'",
    "Ферма 'Белоснежная поляна'",
    "Ферма 'Молочная ферма'",
    "Ферма 'Тихий вечер'",
    "Ферма 'Горное пастбище'",
    "Ферма 'Молочный путь'",
    "Ферма 'Счастливый дом'",
    "Ферма 'Коровье поле'",
    "Ферма 'Деревенская идиллия'",
    "Ферма 'Лесной край'",
    "Ферма 'Сливочные просторы'",
    "Ферма 'Родной пастух'",
    "Ферма 'Молочный уголок'",
    "Ферма 'Чистая роса'",
    "Ферма 'Белый утес'",
    "Ферма 'Родная ферма'",
    "Ферма 'Лунное поле'"
]

hours_milk = ['18', '19']
minutes = ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'] 

hours_farm = ['20', '21']



# Храним временные данные для примера
data = {
    "фермеры": {},
    "молокозаводы": {},
}

async def start(update: Update, context: CallbackContext):
    buttons = [["Я фермер", "Я сотрудник молокозавода", "Помощь"]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Кто вы?", reply_markup=reply_markup)

async def farmer_start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Добрый день! Укажите название вашей фермы:",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data["role"] = "фермер"
    context.user_data["step"] = "название_фермы"

async def factory_start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Добрый день! Укажите название вашего молокозавода:",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data["role"] = "молокозавод"
    context.user_data["step"] = "название_завода"
    
async def factory_help(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Добрый день! Опишите кратко вашу проблему.",
        reply_markup=ReplyKeyboardRemove()
    )
    context.user_data["role"] = "помощь"

async def handle_response(update: Update, context: CallbackContext):
    role = context.user_data.get("role")
    step = context.user_data.get("step")

    if role == "фермер":
        if step == "название_фермы":
            context.user_data["название_фермы"] = update.message.text
            context.user_data["step"] = "адрес_фермы"
            await update.message.reply_text("Укажите адрес вашей фермы:")
        elif step == "адрес_фермы":
            context.user_data["адрес_фермы"] = update.message.text
            context.user_data["step"] = "количество_сыворотки"
            await update.message.reply_text("Укажите, сколько литров сыворотки вам необходимо на завтра(только число)")
            await update.message.reply_text("Если вы укажете, количество литров менее 100, будет оформлен самовывоз")
        elif step == "количество_сыворотки":
            context.user_data["количество_сыворотки"] = update.message.text
            await update.message.reply_text(
                "Спасибо, данные отправлены на обработку в WheyWay. Ожидайте ответа."
            )
            await asyncio.sleep(4)
            fabric = random.choice(milk_factories)
            if int(update.message.text) >= 100:
                await update.message.reply_text(
                    f"{fabric[1]} предоставит вам {context.user_data['количество_сыворотки']} литров сыворотки. "
                    f"Ожидайте молоковоз с {random.choice(hours_farm)}:{random.choice(minutes)}"
                )
            elif int(update.message.text) < 100:
                
                await update.message.reply_text(
                    f"{fabric[1]} предоставит вам {context.user_data['количество_сыворотки']} литров сыворотки. "
                    f"Ожидаем вас с {random.choice(hours_milk)}:{random.choice(minutes)}, по адресу {fabric[0]}"
                )
            else:
                await update.message.reply_text("Количество литров сыворотки должно быть > 0")
                
            context.user_data.clear()
            await update.message.reply_text("Вы можете создать новую заявку, отправив /start.")

    elif role == "молокозавод":
        if step == "название_завода":
            context.user_data["название_завода"] = update.message.text
            context.user_data["step"] = "адрес_завода"
            await update.message.reply_text("Укажите адрес вашего молокозавода:")
        elif step == "адрес_завода":
            context.user_data["адрес_завода"] = update.message.text
            context.user_data["step"] = "количество_сыворотки"
            await update.message.reply_text("Укажите, сколько литров сыворотки у вас осталось сегодня (только число)")
        elif step == "количество_сыворотки":
            unfilled = True
            max_сыворотки = int(update.message.text)
            random_amount = random.randint(1, max_сыворотки)
            context.user_data["количество_сыворотки"] = max_сыворотки
            
            if max_сыворотки >= 100 and max_сыворотки < 300:
                random_nums_farms = 2
            elif max_сыворотки >= 300 and max_сыворотки < 1000:
                random_nums_farms = 3
            elif max_сыворотки >= 1000:
                random_nums_farms = 4
            else:
                random_nums_farms = 0
                
            await update.message.reply_text(
                    "Спасибо, данные отправлены на обработку в WheyWay. Ожидайте ответа."
                )
            
            if random_nums_farms != 0:
                for i in range(random_nums_farms):
                    if i == random_nums_farms-1:
                        await asyncio.sleep(random.randint(1, 5))
                        if max_сыворотки > 100:
                            await update.message.reply_text(
                                f"Спасибо, сегодня с {random.choice(hours_milk)}:{random.choice(minutes)} отгрузите {max_сыворотки} литров сыворотки. "
                                f"Она будет отправлена на предприятие: {random.choice(farms)}."
                            )
                        else:
                            await update.message.reply_text(
                                f"Спасибо, сегодня с {random.choice(hours_milk)}:{random.choice(minutes)} предприятие {random.choice(farms)} отгрузит у вас {max_сыворотки} литров сыворотки. "
                            )
                    else:
                        random_amount = random.randint(1, int(max_сыворотки*0.5))
                        max_сыворотки -= random_amount
                        if random_amount > 100:
                            await asyncio.sleep(random.randint(1, 5))
                            await update.message.reply_text(
                                f"Спасибо, сегодня с {random.choice(hours_milk)}:{random.choice(minutes)} отгрузите {random_amount} литров сыворотки. "
                                f"Она будет отправлена на предприятие: {random.choice(farms)}."
                            )
                        else:
                            await update.message.reply_text(
                                f"Спасибо, сегодня с {random.choice(hours_milk)}:{random.choice(minutes)} предприятие {random.choice(farms)} отгрузит у вас {random_amount} литров сыворотки. "
                            )
            else:
                await update.message.reply_text(
                    "Извините, количество сыворотки должно быть более 100 литров, с уважением, WheyWay."
                )
                    
            context.user_data.clear()
            await update.message.reply_text("Вы можете создать новую заявку, отправив /start.")

    elif role == "помощь":
        await update.message.reply_text(
            "Сообщение отправлено в службу поддержки WheyWay. Мы скоро вам ответим."
        )
        await asyncio.sleep(7)
        await update.message.reply_text(
            f"Ваше обращение зарегистрировано. Номер вашего обращения: {random.randint(10000000, 99999999)}"
        )
        context.user_data.clear()
        await update.message.reply_text("Вы можете создать новую заявку, отправив /start.")

    else:
        await update.message.reply_text("Пожалуйста, выберите, кто вы: фермер, молокозавод или нужна помощь.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text(["Я фермер"]), farmer_start))
    app.add_handler(MessageHandler(filters.Text(["Я сотрудник молокозавода"]), factory_start))
    app.add_handler(MessageHandler(filters.Text(["Помощь"]), factory_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    
    app.run_polling()

if __name__ == "__main__":
    main()
