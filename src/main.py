import draw
import neis as ns
import utility as util
import schedule
import time
from instagrapi import Client
from datetime import datetime


upload_time = "00:30"
school_name = "능주고등학교"
account_data = util.get_id()
ACCOUNT_USERNAME = account_data["id"]
ACCOUNT_PASSWORD = account_data["pw"]

cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
print("Login Successful")


def fetch_image():
    schedules, meal_data = ns.get_info(school_name, ns.get_current_date())
    clean_meal_data = {key: [util.remove_numbers(menu_item) for menu_item in value] for key, value in meal_data.items()}
    draw.create_meal_image(schedules, clean_meal_data)
    draw.create_schedule_image(school_name)


def upload_instagram():
    fetch_image()
    upload_img = ["images/아침_menu.jpeg", "images/점심_menu.jpeg", "images/저녁_menu.jpeg", "images/schedule.jpeg"]
    cl.album_upload(paths=upload_img, caption=f'{datetime.now().strftime("%Y/%m/%d")}의 급식 및 학사일정입니다.')
    time.sleep(5)
    print("Upload Completed in ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


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
finally:
    cl.logout()
    print("Logout Successful")
