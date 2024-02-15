import neis as ns
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta


def create_meal_image(schedule, meal_data, output_folder='images'):
    import os
    os.makedirs(output_folder, exist_ok=True)
    meal_data = {"아침": meal_data[0], "점심": meal_data[1], "저녁": meal_data[2]}

    title_font_size = 75
    title_font = ImageFont.truetype("fonts/GmarketSansTTFBold.ttf", title_font_size)

    meal_font_size = 50
    meal_font = ImageFont.truetype("fonts/GmarketSansTTFMedium.ttf", meal_font_size)

    schedule_font_size = 55
    schedule_font = ImageFont.truetype("fonts/GmarketSansTTFMedium.ttf", schedule_font_size)

    for meal, items in meal_data.items():
        w, h = 1080, 1080
        x, y = 50, 50
        image = Image.new('RGB', (w, h), 'white')
        draw = ImageDraw.Draw(image)

        draw.text((x, y), f'{datetime.now().strftime('%m/%d')} ({meal})', fill='black', font=title_font)
        draw.text((x + 480, y + 13), f'- {schedule}', fill='black', font=schedule_font)
        y += title_font_size + 50

        for item in items:
            draw.text((x, y), item, fill='black', font=meal_font)
            y += meal_font_size + 23

        filename = os.path.join(output_folder, f'{meal.lower()}_menu.jpeg')
        image.save(filename, format='JPEG')


def create_schedule_image(school_name, output_folder='images'):
    import os
    os.makedirs(output_folder, exist_ok=True)

    week_start = datetime.today() - timedelta(days=datetime.today().weekday())
    this_week = [(week_start + timedelta(days=i)).strftime('%Y%m%d') for i in range(7)]
    week_schedule = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        week_schedule[i], _ = ns.get_info(school_name, this_week[i])

    title_font_size = 75
    title_font = ImageFont.truetype("fonts/GmarketSansTTFBold.ttf", title_font_size)
    
    date_font_size = 45
    date_font = ImageFont.truetype("fonts/GmarketSansTTFBold.ttf", date_font_size) 

    schedule_font_size = 45
    schedule_font = ImageFont.truetype("fonts/GmarketSansTTFMedium.ttf", schedule_font_size)

    w, h = 1080, 1080
    x, y = 50, 50
    image = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(image)

    draw.text((x + 75, y), f'{this_week[0][4:6]}/{this_week[0][6:]}~{this_week[6][4:6]}/{this_week[6][6:]} 학사일정', fill='black', font=title_font)
    y += title_font_size + 43

    for i in range(7):
        _, _, datewidth, _ = draw.textbbox((0, 0), text=f'{this_week[i][4:6]}/{this_week[i][6:]}', font=date_font)
        date_x = (w - datewidth) // 2
        draw.text((date_x, y), f'{this_week[i][4:6]}/{this_week[i][6:]}', fill='black', font=date_font)
        y += date_font_size + 18
        _, _, textwidth, _ = draw.textbbox((0, 0), text=f'{week_schedule[i]}', font=schedule_font)
        text_x = (w - textwidth) // 2
        draw.text((text_x, y), f'{week_schedule[i]}', fill='black', font=schedule_font)
        y += schedule_font_size + 18

    image.save(os.path.join(output_folder, 'schedule.jpeg'), format='JPEG')


def get_current_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y%m%d")

    return formatted_date
