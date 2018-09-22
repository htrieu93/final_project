from models.service import Service
import mlab
import wikipedia
from faker import *
from random import *

mlab.connect()

fake = Faker()

for i in range(10):
    print("Saving service", i + 1, "......")
    yob = randint(87,96)
    serv_name = fake.name()
    measurements = [randint(70,90), randint(60,70), randint(70,90)]
    gender = randint(0, 1)

    descriptions_female = ["ngoan hiền", "biết nấu ăn", "nhu mỳ", "dễ thương", "thích chụp ảnh", "lễ phép với gia đình", "biết đánh đàn", 
                    "trượt pa tanh", "biết chơi DOTA", "thích đọc sách", "thích du lịch", "thích quẩy", "thích đi ăn đêm", "yêu động vật",
                    "thích ngắm trời mưa", "yêu thích thể thao", "yêu thích trẻ con"]
    descriptions_male = ["thích chơi các trò chơi cảm giác mạnh", "biết nấu ăn", "thích chụp ảnh", "thích chơi ghita", 
                    "trượt pa tanh", "thích chơi bóng chuyền", "thích đọc sách", "thích du lịch", "thích đi ăn đêm", "yêu động vật",
                    "biết chơi bóng rổ", "cao to sáng láng", "đẹp zai", "ga-lăng", "chăm làm việc nhà"]
    
    image_female = ['female.jpg', 'hand.jpg', 'slide3.jpg', 'steel.jpg', 'woods.jpg']
    image_male = ['male.jpg', 'lightning.jpg', 'night.jpg', 'rocks.jpg', 'slide4.jpg', 'slide5.jpg']
    
    if gender == 1:
        new_service = Service(
            name = serv_name,
            yob = yob,
            gender = gender,
            height = randint(160, 170),
            phone = fake.phone_number(),
            address = fake.address(),
            status = randint(0, 1),
            measurements = measurements,
            descriptions = sample(descriptions_female, 3),
            image = '../static/image/female/' + choice(image_female)
        )
    else:
        new_service = Service(
            name = serv_name,
            yob = yob,
            gender = gender,
            height = randint(160, 180),
            phone = fake.phone_number(),
            address = fake.address(),
            status = randint(0, 1),
            measurements = measurements,
            descriptions = sample(descriptions_male, 3),
            image = '../static/image/male/' + choice(image_male)
        )

    new_service.save()