import requests
import tkinter as tk
import customtkinter as ctk
from ctypes import windll
from PIL import Image

cities = ['Canberra', 'Sydney', 'Adelaide', 'Melbourne', 'Brisbane', 'Perth', 'Hobart', 'Darwin',
          'Townsville city', 'Geelong', 'Wollongong', 'Cairns', 'Wagga wagga', 'Newcastle', 'Ballarat',
          'Launceston', 'Toowoomba', 'Bendigo', 'Mackay', 'Warrnambool', 'Hervey Bay', 'Nowra', 'Bathurst',
          'Albury', 'Lismore', 'Gladstone central', 'Gold coast', 'Port macquarie', 'Tamworth', 'Whyalla',
          'Burnie', 'Armidale', 'Maryborough', 'Rockhampton city', 'Swan hill', 'Port augusta',
          'Murray bridge', 'Grafton', 'Horsham', 'Dubbo', 'Coffs harbour', 'Lithgow', 'Devonport',
          'Bundaberg central', 'Albany', 'Central coast', 'Bunbury', 'Geraldton', 'Esperance', 'Busselton',
          'Alice springs']


class EntryScreen:

    def __init__(self, master):
        self.root = master
        self.root.geometry('600x800')
        self.root.maxsize(600, 800)
        self.root.minsize(600, 800)
        self.root.title('Australian City Weather')
        self.root.configure(bg='#818c91')
        windll.shcore.SetProcessDpiAwareness(1)

        self.entry_frame = tk.Frame(self.root, bg='#5b6b80')
        self.entry_frame.pack(fill=tk.BOTH,
                              expand=True,
                              pady=20,
                              padx=20)

        ctk.CTkLabel(self.entry_frame,
                     text='Australian City Weather',
                     font=('Sans', 30, 'bold'),
                     text_color='white',
                     bg_color='transparent').pack(pady=40)

        ctk.CTkLabel(self.entry_frame,
                     font=('Sans', 25, 'bold'),
                     text='City Name',
                     text_color='#cacccf',
                     bg_color='transparent').pack(pady=10)

        name_var = tk.StringVar()
        self.entry_box = ctk.CTkEntry(self.entry_frame,
                                      bg_color='transparent',
                                      fg_color='#a1b1c4',
                                      width=230,
                                      border_color='white',
                                      font=('Sans', 20, 'bold'),
                                      text_color='black',
                                      textvariable=name_var)
        self.entry_box.pack()

        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:18])

        name_var.trace("w", lambda *args: character_limit(name_var))

        ctk.CTkButton(self.entry_frame,
                      text='Search',
                      font=('Sans', 18, 'bold'),
                      height=40,
                      width=150,
                      command=lambda: self.display(name_var)).pack(padx=10, pady=30)

        self.entry_box.bind('<Return>', lambda event: self.display(name_var))

    def display(self, city_name):
        self.entry_box.configure(state='disabled')
        if city_name.get().capitalize() in cities:
            self.entry_frame.destroy()
            data = get_weather(city_name.get())
            DisplayPage(self.root, data)
        else:
            self.entry_box.configure(state='normal')


class DisplayPage:

    def __init__(self, master, data):
        self.root = master
        self.display_frame = tk.Frame(self.root, bg='#6f8996')
        self.display_frame.pack(fill=tk.BOTH,
                                expand=True,
                                pady=20,
                                padx=20)

        ctk.CTkLabel(self.display_frame,
                     text=f'{data['name']}',
                     bg_color='transparent',
                     font=('Sans', 35, 'bold'),
                     text_color='white').grid(row=0, column=0, columnspan=4, pady=10,
                                              sticky='s')
        ctk.CTkLabel(self.display_frame,
                     text=f'{data['weather'][0]['description']}',
                     bg_color='transparent',
                     font=('Sans', 20),
                     text_color='#d1d1d1').grid(row=1, column=0, columnspan=4, sticky='n')

        ctk.CTkLabel(self.display_frame,
                     text=f'{round(data['main']['temp'])}°C',
                     bg_color='transparent',
                     font=('Sans', 35, 'bold'),
                     text_color='white').grid(row=2, column=0, columnspan=4, pady=10, sticky='n')

        ctk.CTkLabel(self.display_frame,
                     bg_color='transparent',
                     fg_color='white',
                     width=350,
                     height=6,
                     corner_radius=90,
                     font=('Sans', 1)).grid(row=3, column=0, columnspan=4, pady=20, padx=10)

        img = ctk.CTkImage(light_image=Image.open('transparent_image_thermo_hot.png'), size=(50, 85))
        thing = ctk.CTkLabel(self.display_frame, image=img, text='')
        thing.grid(row=4, column=0, sticky='e', padx=15)

        ctk.CTkLabel(self.display_frame,
                     text=f'{round(data['main']['temp_max'])}°C',
                     bg_color='transparent',
                     font=('Sans', 25, 'bold'),
                     text_color='red').grid(row=4, column=1, columnspan=1, pady=10, sticky='w')

        img = ctk.CTkImage(light_image=Image.open('transparent_image_thermo_cold.png'), size=(50, 85))
        thing = ctk.CTkLabel(self.display_frame, image=img, text='')
        thing.grid(row=5, column=0, sticky='e', padx=15)

        ctk.CTkLabel(self.display_frame,
                     text=f'{round(data['main']['temp_min'])}°C',
                     bg_color='transparent',
                     font=('Sans', 25, 'bold'),
                     text_color='blue').grid(row=5, column=1, columnspan=1, pady=10, sticky='w')

        img = ctk.CTkImage(light_image=Image.open('humidity.webp'), size=(76, 82))
        thing = ctk.CTkLabel(self.display_frame, image=img, text='')
        thing.grid(row=4, column=2, sticky='e', padx=15)

        hums = round(data['main']['humidity'])

        def check_humid(humid):
            low, medium, high = '#ded1b8', '#ded1b8', '#e09d1f'
            if humid <= 55:
                return low
            if humid <= 65:
                return medium
            return high

        ctk.CTkLabel(self.display_frame,
                     text=f'{hums}%',
                     bg_color='transparent',
                     font=('Sans', 25, 'bold'),
                     text_color=f'{check_humid(hums)}').grid(sticky='w', row=4, column=3, pady=10)

        img = ctk.CTkImage(light_image=Image.open('transparent_image_pressure.png'), size=(70, 70))
        thing = ctk.CTkLabel(self.display_frame, image=img, text='')
        thing.grid(row=5, column=2, sticky='e', padx=20)

        ctk.CTkLabel(self.display_frame,
                     text=f'{round(data['main']['pressure'])} hPa',
                     bg_color='transparent',
                     font=('Sans', 23),
                     text_color='#cccccc').grid(sticky='w', row=5, column=3)

        ctk.CTkButton(self.display_frame,
                      text='Back',
                      bg_color='transparent',
                      fg_color='#81aadb',
                      text_color='white',
                      width=150,
                      font=('Sans', 20, 'bold'),
                      hover_color='#6da0de',
                      command=self.back_to_homepage).grid(row=6, column=0, columnspan=4, pady=30)

    def back_to_homepage(self):
        self.display_frame.destroy()
        EntryScreen(self.root)


def get_weather(city):
    api_key = '23bac0d141867e8cd3a782db608baf01'
    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city},AUSTRALIA&appid={api_key}'
    geo_response = requests.get(geo_url)
    lat = str(geo_response.json()[0]['lat'])
    lon = str(geo_response.json()[0]['lon'])
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?appid=23bac0d141867e8cd3a782db608baf01&lat={lat}&lon={lon}&units=metric')
    return response.json()


if __name__ == '__main__':
    root = tk.Tk()
    EntryScreen(root)
    root.mainloop()





