import random
import time
import os
import logging

import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from button_kb import kb_inline_call

# # webhook settings
# WEBHOOK_HOST = 'https://194.67.205.94'
# WEBHOOK_PATH = ''
# WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
#
# # webserver settings
# WEBAPP_HOST = 'localhost'  # or ip
# WEBAPP_PORT = 3001

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)
# dp.middleware.setup(LoggingMiddleware())

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")


# @dp.message_handler()
# async def echo(message: types.Message):
#     # Regular request
#     # await bot.send_message(message.chat.id, message.text)
#
#     # or reply INTO webhook
#     return SendMessage(message.chat.id, message.text)


@dp.message_handler(lambda x: x.text in ['Start', 'start', '/start'])
async def push_button(message: types.Message):
    button = ['По одной карте', 'По трём картам', 'Start', 'Гороскоп']
    k_b = ReplyKeyboardMarkup(resize_keyboard=True).add(*button)
    await message.answer(f'Приветствую {message.from_user.username}, выберете карту чтобы узнать свою судьбу',
                         reply_markup=k_b)


@dp.message_handler(lambda message_x: message_x.text in ['По одной карте'])
async def run_taro(message: types.Message):
    await message.answer('Минуту происходит магия...')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    link = f'https://www.astrocentr.ru/index.php?przd=taro&str=len'
    browser.get(link)
    time.sleep(1)
    msg = browser.find_element(By.CLASS_NAME, "title1").text
    img1 = browser.find_element(By.CSS_SELECTOR, ".fsdiv > img.topleft").get_attribute("src")
    msg_full = browser.find_element(By.CSS_SELECTOR, ".fsdiv").text
    browser.quit()
    await bot.send_photo(message.from_user.id, img1, f"<b>Ваша карта: {msg}</b>", parse_mode='html')
    await bot.send_message(message.from_user.id, f"{msg_full}")


@dp.message_handler(lambda message_x: message_x.text in ['По трём картам'])
async def run_taro(message: types.Message):
    await message.answer('Минуту происходит магия...')
    await message.delete()

    list_sub = ['1. Влияние прошлого в связи с заданным вопросом', '2. Влияние настоящего в связи с заданным вопросом',
                '3. Результат']
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    link = f'https://www.astrocentr.ru/index.php?przd=taro&str=3cards'
    browser.get(link)
    time.sleep(1)
    for i in range(3):
        browser.find_element(By.ID, f'd{random.randint(1, 78)}').click()
    time.sleep(3)
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html, 'lxml')
    fi1 = soup.findAll('fieldset')
    try:
        for i in range(3):
            link = 'https://www.astrocentr.ru' + fi1[i].find('div', class_='fsdiv').find('img', class_='topleft').get(
                'src')
            title = fi1[i].find('div', class_='fsdiv').find('span', class_='title1').text
            description = fi1[i].find('div', class_='fsdiv').text
            await bot.send_photo(message.from_user.id, link,
                                 f"{list_sub[i]}")
            await bot.send_message(message.from_user.id, f"<b>Ваша карта {i + 1}:\n{title}\n\n{description}</b>",
                                   parse_mode='html')
    except Exception as e:
        print(e)
        await message.answer('Если все карты не загрузились, попробуйте еще раз!')


@dp.message_handler(lambda x: x.text in ['гороскоп', 'Гороскоп'])
async def bootom_horoscope(message: types.Message):
    await bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=kb_inline_call)


@dp.callback_query_handler(lambda callback: True)
async def callback_worker(callback: types.CallbackQuery):
    zodiac = {'Овен': 'aries', 'Телец': 'taurus', 'Близнецы': 'gemini',
              'Рак': 'cancer', 'Лев': 'leo', 'Дева': 'virgo',
              'Весы': 'libra', 'Скорпион': 'scorpio', 'Стрелец': 'sagittarius',
              'Козерог': 'capricorn', 'Водолей': 'aquarius', 'Рыбы': 'pisces'
              }
    await callback.answer('Минуту происходит магия...')
    for k, v in zodiac.items():
        if callback.data == k:
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            link = f'https://www.elle.ru/astro/{v}/day/'
            browser.get(link)
            time.sleep(1)
            msg = browser.find_element(By.CLASS_NAME, "articleParagraph").text
            browser.quit()
            await bot.send_message(callback.from_user.id, f'<b>Знак зодиака {k.upper()}</b>\n {msg}', parse_mode='html')


# async def on_startup(dp):
#     await bot.set_webhook(WEBHOOK_URL)
#
#
# async def on_shutdown(dp):
#     await bot.delete_webhook()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# if __name__ == '__main__':
#     aiogram.executor.start_webhook(
#         dispatcher=dp,
#         webhook_path=WEBHOOK_PATH,
#         on_startup=on_startup,
#         on_shutdown=on_shutdown,
#         skip_updates=True,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#     )