import os
import asyncio
import main as m
from selenium_driverless import webdriver
from selenium_driverless.types.by import By


async def main():
    options = webdriver.ChromeOptions()
    options.user_data_dir = os.path.join(os.getcwd(), "browserdata")
    options.auto_clean_dirs = False
    last_page = "about:blank"

    if not os.path.exists(options.user_data_dir) or not os.path.isdir(options.user_data_dir):
        os.mkdir(options.user_data_dir)
    
    async with webdriver.Chrome(options=options) as driver:
        await driver.get("https://google.com")
        await asyncio.sleep(1)
        await driver.get("https://case-battle.life")
        while True:
            await asyncio.sleep(1)
            try:
                url = await driver.current_url
                if url == last_page:
                    continue
                await asyncio.sleep(2)
                last_page = url
                if "/case/" not in url:
                    continue

                html = await driver.find_element(By.CLASS_NAME, "case-assets")
                html = await html.source

                case_price = await driver.find_element(By.CLASS_NAME, "footer-wrapper")
                case_price = await case_price.source
                case_price = case_price.split('<span class="__currency">')[1].split('</span>')[0]

                case_price = int(case_price.replace(" ", ""))

                items, counts = m.parse_items(html, case_price)
                real_count, bad_cases, good_cases = m.calculate_additional_stats(items, counts)
                max_loss = min([items[x][1] for x in items])

                result = f"""
Макс потеря денег: {case_price-max_loss} ({round(case_price*0.8, 2)-max_loss} PROMO 20%)

BAD DROPS: {bad_cases} ({int(bad_cases*100/real_count)}%)
GOOD DROPS: {good_cases} ({int(good_cases*100/real_count)}%)
"""
                await driver.execute_script("alert(arguments[0]);", result, timeout=300)
            except IndexError as e:
                await driver.execute_script(
                    "alert(arguments[0]);", 
                    "Ошибка! Обычно бывает при:\n Нет входа\n Вам хватает на кейс\n Лагает КБ\n Валюта - не рубли", 
                    timeout=300)
            except Exception:
                await driver.quit(clean_dirs=False)
                break


asyncio.run(main())
