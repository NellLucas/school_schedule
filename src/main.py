import draw
import neis as ns
import utility as util
import schedule
import time
from instagrapi import Client
from datetime import datetime


upload_time = "00:05"
school_name = "능주고등학교"
MAX_RETRIES = 3
RETRY_INTERVAL = 600
account_data = util.get_id()
ACCOUNT_USERNAME = account_data["id"]
ACCOUNT_PASSWORD = account_data["pw"]


def login_instagram(USERNAME, PASSWORD):
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    print("Login Successful")
    return cl


def fetch_image(school_name):
    global date
    date = datetime.now()
    schedules, meal_data = ns.get_info(school_name, util.get_fomatted_date(date))
    clean_meal_data = {key: [util.remove_numbers(menu_item) for menu_item in value] for key, value in meal_data.items()}
    draw.create_meal_image(schedules, clean_meal_data, date)
    draw.create_schedule_image(school_name, date)


def upload_images(cl):
    upload_img = ["images/아침_menu.jpeg", "images/점심_menu.jpeg", "images/저녁_menu.jpeg", "images/schedule.jpeg"]
    cl.album_upload(paths=upload_img, caption=f'{date.strftime("%Y/%m/%d")}의 급식 및 학사일정입니다.')
    time.sleep(5)
    print("Upload Completed in ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def upload_instagram():
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            cl = login_instagram(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
            fetch_image(school_name)
            upload_images(cl)
            return
        except Exception as e:
            print(f"Upload failed by {e}. Retrying in 10 minutes...")
            time.sleep(RETRY_INTERVAL)
            retry_count += 1
        finally:
            if 'cl' in locals():
                cl.logout()
                print("Logout Successful")

    print("Max retry count reached. Upload failed.")


schedule.every().day.at(upload_time).do(upload_instagram)


try:
    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    pass
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"An error occurred: {e}")
