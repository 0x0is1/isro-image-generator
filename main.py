import requests, json, random, os
from bs4 import BeautifulSoup as scraper

url = "https://www.isro.gov.in"

def get_links():
    links_array = []
    response = requests.get(url + "/media")
    soup = scraper(response.content, 'html.parser')
    data = soup.find_all("div", {"class": "views-bootstrap-grid-plugin-style"})
    links = data[0].find_all("div", {"class": "views-field views-field-title"})
    for link in links: links_array.append(link.find("a").get("href"))
    return links_array

def get_images():
    links = get_links()
    images = []
    for i in links:
        response = requests.get(url + i)
        soup = scraper(response.content, 'html.parser')
        images_data = soup.find_all("div", {"class": "field-items"})[1]
        for j in images_data.find_all("a"):
            images.append(j.get("href"))
    return images

def write_data():
    with open("a.json", "w") as f:
        data = {"images": get_images()}
        json.dump(data, f)

def get_ran_image():
    with open("a.json", "r") as f:
        data = json.load(f)
    if len(data["images"]) < 5:
        print("Getting images. Please wait few minutes")
        write_data()
    index = random.randint(0, len(data["images"])-1)
    #linux users can uncomment next comment to use as wallpaper chager
    #os.system("gsettings set org.gnome.desktop.background picture-uri " + data["images"][index])
    return index

#get_ran_image()