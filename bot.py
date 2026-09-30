import os
import time
from playwright.sync_api import sync_playwright

def run_bot():
    # Вземане на бисквитката от настройките на облака (за сигурност)
    session_cookie = os.getenv("TICK_SESSION")
    
    if not session_cookie:
        print("ГРЕШКА: Липсва TICK_SESSION променлива в настройките!")
        return

    print("Стартиране на инкогнито сесия в облака...")
    
    with sync_playwright() as p:
        # Стартира браузър в скрит режим (headless=True), за да пести ресурс в облака
        browser = p.chromium.launch(headless=True)
        
        # Създаване на чист профил
        context = browser.new_context()
        
        # Ръчно вграждане на твоята сесия в браузъра на бота
        context.add_cookies([{
            'name': 'pterodactyl_session',
            'value': session_cookie,
            'domain': 'tickhosting.com',
            'path': '/',
            'secure': True,
            'http_only': True
        }])
        
        page = context.new_page()
        
        try:
            print("Влизане в контролния панел на TickHosting...")
            page.goto("https://tickhosting.com", timeout=60000)
            page.wait_for_load_state("networkidle")
            
            # Проверка дали сесията работи
            if "login" in page.url:
                print("ГРЕШКА: Твоята бисквитка е изтекла! Трябва да я вземеш наново от Edge.")
                return

            print("Намиране на бутона за подновяване...")
            # Търси бутона по неговия текст или клас
            renew_button = page.locator("text=Renew").first
            
            if renew_button.is_visible():
                print("Бутонът е намерен! Натискане...")
                renew_button.click()
                
                # Изисква се изчакване заради 10-секундната реклама на хостинга
                print("Изчакване 15 секунди за обработка на рекламата...")
                time.sleep(15)
                
                print("УСПЕХ: Сървърът с 8GB RAM беше подновен успешно!")
            else:
                print("ВНИМАНИЕ: Бутонът Renew не е активен в момента. Сървърът вероятно вече е подновен.")
                
        except Exception as e:
            print(f"Възникна грешка по време на изпълнението: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_bot()
