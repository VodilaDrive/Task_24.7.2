import os.path

from api import PetFriends
from settings import valid_email, valid_password



pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Джерси', animal_type='корги', age='5', pet_photo='images/corgi_1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_add_photo_of_pet_with_valid_data(pet_photo='images/Corgi_2.jpg'):
    """Проверяем возможность добавления фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception('ops')

def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Джерси", 'корги', '5', 'images/corgi_1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_pet_info(name='Джонник', animal_type='корги', age='6',):
    """Проверяем возможность обновляния информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name

def test_get_api_key_for_not_valid_user(email=valid_email, password=valid_password):
    """Проверяем возможность получить api ключ с не валидным пользователем"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_unsuccessful_add_new_pet(name='',animal_type='', age='',pet_photo='images/Corgi_4.jpg'):
    """Проверяем возможность при неуспешном добавлении питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_unsuccessful_create_pet_with_invalid_photo_format(name='Джерси', animal_type='корги', age='5', pet_photo='images/Corgi_3.gif'):
    """Проверяем, что при добавлении питомца с файлом неподдерживаемого формата (не JPG, JPEG или PNG) сервер вернет
    ошибку 400 и питомец не будет добавлен"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] == name

def test_add_new_pet_with_age_letter(name='Джонник', animal_type='корги', age='шесть', pet_photo= 'images/Corgi_2.jpg'):
    """Проверка невозможности добавления питомца с некорректным вводом age не цифрами а буквами"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age,pet_photo)
    assert status != 200
    assert result['age'] != age