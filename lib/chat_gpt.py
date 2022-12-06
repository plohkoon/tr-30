import requests
from .constants import OPENAI_PASSWORD, OPENAI_USERNAME, OPENAI_ACCESS_TOKEN
from uuid import uuid4 as uuid
import json
from urllib.parse import urlencode, urlparse, parse_qsl


####
# Inspired by:
# https://github.com/labteral/chatgpt-python/blob/master/chatgpt/chatgpt.py
####

class ChatGpt:
    def __init__(self):
        self.oauth()

    def oauth(self):
        # These are initialized from when I logged in once.
        # TODO: I should really OAuth these separately for each instance
        self._conversation_id = "178847ec-5385-48ae-96c1-d681d673543a"
        self._message_id = "cccccad2-479c-45eb-be03-6f96780abbae"
        self._parent_message_id = "cccccad2-479c-45eb-be03-6f96780abbae"
        self._model_name = "text-davinci-002-render"

        self._access_token = OPENAI_ACCESS_TOKEN

        # csrf_res = requests.get("https://chat.openai.com/api/auth/csrf")
        # cookies = csrf_res.cookies

        # csrf_token = csrf_res.json()["csrfToken"]

        # chat_auth0_res = requests.post(
        #     "https://chat.openai.com/api/auth/signin/auth0?prompt=login",
        #     data={
        #         "callbackUrl": "/",
        #         "csrfToken": csrf_token,
        #         "json": True
        #     },
        #     cookies=cookies,
        #     allow_redirects=False
        # )
        # cookies.update(chat_auth0_res.cookies)

        # location = chat_auth0_res.headers["location"]
        # redirect_res = requests.get(
        #     location, cookies=cookies, allow_redirects=False)
        # cookies.update(redirect_res.cookies)

        # # location = f"https://auth0.openai.com{redirect_res.headers['location']}"
        # # redirect_res = requests.get(
        # #     location, cookies=cookies, allow_redirects=False)
        # # cookies.update(redirect_res.cookies)

        # location = f"https://auth0.openai.com{redirect_res.headers['location']}".replace(
        #     "identifier", "password")

        # full_url = urlparse(location)
        # query_string = parse_qsl(full_url.query)

        # state = [val for (key, val) in query_string if key == "state"][0]

        # auth_res = requests.post(
        #     location,
        #     data={
        #         "username": OPENAI_USERNAME,
        #         "password": OPENAI_PASSWORD,
        #         "state": state,
        #         "action": "default"
        #     },
        #     cookies=cookies,
        #     allow_redirects=False
        # )
        # cookies.update(auth_res.cookies)

        # print(auth_res.headers["location"], auth_res.status_code)

        # url = None
        # try:
        #     url = chat_auth0_res.json()["url"]
        # except:
        #     url = chat_auth0_res.url.replace("identifier", "password")

        # full_url = urlparse(url)
        # query_string = parse_qsl(full_url.query)

        # state = [val for (key, val) in query_string if key == "state"][0]

        # auth_res = requests.post(
        #     url,
        #     data={
        #         "username": OPENAI_USERNAME,
        #         "password": OPENAI_PASSWORD,
        #         "state": state,
        #         "action": "default"
        #     },
        #     cookies=cookies
        # )

        # print(auth_res.status_code, auth_res.text)

    #     auth0_params = urlencode({
    #         "client_id": "foo",
    #         "scope": "openid email profile offline_access model.request model.read organization.read",
    #         "response_type": "code",
    #         "redirect_uri": "https://chat.openai.com/api/auth/callback/auth0",
    #         "prompt": "login",
    #         "state": "foo",
    #         "code_challenge": "challenge",
    #         "code_challenge_method": "S256",
    #     })

    #     # res = requests.post(
    #     #     f"{self.oauth_url}?state={self.oauth_state}",
    #     #     data={
    #     #         "state": self.oauth_state,
    #     #         "username": OPENAI_USERNAME,
    #     #         "password": OPENAI_PASSWORD,
    #     #         "action": True
    #     #     }
    #     # )

    #     # print(res.text)

    #     # self._access_token = res.cookies.get("auth")

    #     self._access_token = "foo"

    def chat(self, message: str):
        self._parent_message_id = self._message_id
        self._message_id = str(uuid())

        url = "https://chat.openai.com/backend-api/conversation"

        payload = json.dumps(
            {
                "action": "next",
                "messages": [
                    {
                        "id": self._message_id,
                        "role": "user",
                        "content": {
                            "content_type": "text",
                            "parts": [message]
                        }
                    }
                ],
                "conversation_id": self._conversation_id,
                "parent_message_id": self._parent_message_id,
                "model": self._model_name
            }
        )

        headers = {
            "Accept": "text/event-stream",
            "Authorization": f"Bearer {self._access_token}"
        }

        response = requests.post(url, headers=headers,
                                 data=payload, stream=True)

        print(response.status_code)

        for line in response.iter_lines():
            if line:
                print(line)
                event = json.loads(line)

                message = event["data"]["message"]

                self._parent_message_id = self._message_id
                self._message_id = message["id"]

                parts = message["content"]["parts"]
                content = "\n".join(parts)
                content = content.replace(r"\n+", "\n")

                print("Content: ", content)
                yield content

        # payload = response.text

        # try:
        #     last_item = payload.split(('data:'))[-2]
        #     text_items = json.loads(last_item)['message']['content']['parts']
        #     text = '\n'.join(text_items)
        #     postprocessed_text = text.replace(r'\n+', '\n')
        #     return postprocessed_text
        # except IndexError:
        #     error_message = json.loads(payload)['detail']
        #     raise Exception(error_message)

    def reset(self):
        self._message_id = str(uuid())
        self._parent_message_id = str(uuid())
