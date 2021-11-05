

import bs4
import requests
from gitlab import Gitlab

def user_password_change(username, password):
    URL = "https://gitlab.example.com"
    SIGN_IN_URL = URL + "/users/sign_in"
    EDIT_PASSWORD_URL = URL+ "/-/profile/password"
    PRIVATE_TOKEN = "Personel Acces Token Value"

    result = True
    GITLAB_CONNECTION = Gitlab(URL, private_token=PRIVATE_TOKEN,api_version=4)
    GITLAB_CONNECTION.auth()
    user_info = GITLAB_CONNECTION.users.list(username=username)
    if user_info:
        try:
            user = user_info[0]
            user.password = password
            user.password_confirmation = password
            user.save()

            with requests.Session() as session:
                sign_in_page = session.get(SIGN_IN_URL)
                soup = bs4.BeautifulSoup(sign_in_page.text, 'html.parser')
                token = soup.find('meta', dict(name='csrf-token'))['content']
                data = {'user[login]': username,
                        'user[password]': password,
                        'authenticity_token': token}

                login_in_page = session.post(SIGN_IN_URL, data=data)
                if "Invalid login or password." in login_in_page.text:
                    print("giris bilgileri hatali")
                    result = False
                else:
                    soup = bs4.BeautifulSoup(login_in_page.text, 'html.parser')
                    csrf_token = soup.find('meta', dict(name='csrf-token'))['content']
                    new_token = csrf_token

                    data1 = {'user[current_password]': password,
                            'user[password]': password,
                            'user[password_confirmation]': password,
                            'authenticity_token': new_token
                            }

                    password_edit_in_page = session.post(EDIT_PASSWORD_URL, data=data1)

                    if "Password successfully changed" in password_edit_in_page.text:
                        print("parola guncellendi")
                    else:
                        print("current password hatali girildi.")
                        result=False
        except Exception as ex:
            result=False
    else:
        print("user kayitli degil")
        result = False
    return result

is_updated = user_password_change("sevgi","sevgi2332")
print(is_updated)
