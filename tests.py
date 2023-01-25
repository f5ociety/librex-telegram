from api import librex


datas = librex.request("gentoo")


for data in datas:
    if "special_response" in data:
        print(data["special_response"]["response"])
    else:
        print(data["title"], data["url"], data["description"])
