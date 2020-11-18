import requests
from bs4 import BeautifulSoup
import csv
import sys

def check_rows(data):
    rows = ['Kira', 'İlan no', 'Son Güncelleme Tarihi', 'İlan Durumu', 'Konut Şekli', 'Oda + Salon Sayısı', 'Brüt / Net M2', 'Bulunduğu Kat', 'Bina Yaşı', 'Isınma Tipi', 'Kat Sayısı', 'Eşya Durumu', 'Banyo Sayısı', 'Yapı Tipi', 'Yapının Durumu', 'Kullanım Durumu', 'Cephe ', 'Depozito', 'Yakıt Tipi']
    if len(data) != len(rows):
        print("Not enough")
        return False
    else:
        print("Checking row..")
        
        check_row = []
        for x in data:
            check_row.append(x)
        print(check_row)
        if rows == check_row:
            return True
        else:
            return False

all_data = []
s = requests.session()
try:
    links_file = sys.argv[1]
except IndexError:
    print("Lütfen link dosyası giriniz.")
    exit()
with open(links_file,"r") as fp:
    main_links = fp.readlines()

for main_link in main_links:
    try:
        main_link = main_link.strip()
        r = s.get(main_link)
        print("In link " + main_link)
        bs = BeautifulSoup(r.text,'html.parser')
        last_page = bs.find_all("li", {"class": "page-item"})[-1].text
        for page in range(1,int(last_page)):
            print(f"In page {page}")
            r = s.get(f"{main_link}?page={page}")
            bs = BeautifulSoup(r.text,'html.parser')
            # İlan linklerini al
            all_links_bs = bs.find_all("a", class_="card-link")
            all_links = []
            for link in all_links_bs:
                all_links.append("https://www.hurriyetemlak.com" + link["href"])
            
            # Linkleri gezerek bilgileri topla
            for link in all_links:
                r = s.get(link)

                bs = BeautifulSoup(r.text, 'html.parser')
                rent_bs = bs.find("p", class_="fontRB fz24 price")
                rent = rent_bs.text.strip()
                house_properties_bs = bs.find_all("ul", class_="adv-info-list")

                bs = BeautifulSoup(str(house_properties_bs[0]), 'html.parser')

                house_properties = bs.find_all("span")
                if len(house_properties) == 37:
                    net_m = house_properties[12].text
                    house_properties.pop(12)

                    data = {}
                    data["Kira"] = rent
                    for x in range(len(house_properties)):
                        if x % 2 == 0:
                            data[house_properties[x].text] = house_properties[x+1].text
                        else:
                            pass
                    data["Brüt / Net M2"] = data["Brüt / Net M2"] + net_m
                    if check_rows(data):
                        all_data.append(data)
                else:
                    
                    pass
    except Exception as e:
        print("Error : " + str(e))

rows = ['No','Kira', 'İlan no', 'Son Güncelleme Tarihi', 'İlan Durumu', 'Konut Şekli', 'Oda + Salon Sayısı', 'Brüt / Net M2', 'Bulunduğu Kat', 'Bina Yaşı', 'Isınma Tipi', 'Kat Sayısı', 'Eşya Durumu', 'Banyo Sayısı', 'Yapı Tipi', 'Yapının Durumu', 'Kullanım Durumu', 'Cephe ', 'Depozito', 'Yakıt Tipi']



# CSV dosyasına yaz
with open('house-data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(rows)
    counter = 0
    for data in all_data:
        row = []
        row.append(counter)
        for key_name in data:
            row.append(data[key_name])
        writer.writerow(row)
        counter += 1
        
