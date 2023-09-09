import tkinter as tk
import random
import numpy as np
import copy
import os
from PIL import Image, ImageTk

class puzzle_game:
    def __init__(self):
        self.root = tk.Tk()
        self.buttons = []
        self.choose_move=[]
        self.next_moves=[]
        self.move_number=0
        self.level = 0
        self.difficult_selec()
        self.root.mainloop()
    def interface_olustur(self):
        self.buton_sayi_siralama()
        for i in range(self.level):
            row = []
            for j in range(self.level):
                if self.button_number[i][j] !=self.button_number[-1][-1]:
                    button = tk.Button(self.root, text=self.button_number[i][j] + 1, width=10, height=2, bg="red",fg="white",disabledforeground="white",state="disabled")
                    button.grid(row=i, column=j,padx=5,pady=5)  
                    button["command"] = lambda button=button: self.on_button_click(button) 
                    row.append(button)
                else:
                    button = tk.Button(self.root, text="", width=10, height=2, bg="red",fg="white",disabledforeground="white")
                    button.grid(row=i, column=j,padx=5,pady=5)  
                    button["command"] = lambda button=button: self.on_button_click(button) 
                    row.append(button)

            self.buttons.append(row)
    def interface_olustur_image(self):
        for i in range(self.level):
            row = []
            for j in range(self.level):
                # Buton için resim dosyası yükleniyor
                image_file = self.random_image_files[i*self.level + j]
                dizin = os.getcwd() + self.adress + image_file
                
                # Resim dosyası yükleniyor ve ImageTk nesnesine dönüştürülüyor
                image = Image.open(dizin)
                photo = ImageTk.PhotoImage(image)
                if (image_file != '16.png' and self.form == 2) or (image_file != '1.png' and self.form == 1):
                # Resimli buton oluşturuluyor
                    button = tk.Button(self.root, state="disabled", image=photo,borderwidth=0)
                else:
                    button = tk.Button(self.root, state="normal", image=photo,borderwidth=0)
                button.image = photo
                button.grid(row=i, column=j)  
                button["command"] = lambda button=button: self.on_button_click(button)
                
                    
                row.append(button)

            self.buttons.append(row)
    def buton_sayi_siralama(self):
        
        number = self.level * self.level

        # 1-15 arası 15 sayı seç
        numbers = random.sample(range(1, number), number -1)

        # Numpy dizisi oluştur
        self.button_number = np.zeros((self.level, self.level), dtype=int)

        # Rastgele sayıları iki boyutlu diziye yerleştir
        self.button_number.flat[:len(numbers)] = numbers

    def next_move(self):
        for i in range(self.level):
            for j in range(self.level):
                if [i, j] in self.next_moves and [i, j] :
                    self.buttons[i][j].config(state="normal")
                else:
                    self.buttons[i][j].config(state="disabled")

    def on_button_click(self,button):
        self.empty_button_choose(button)
        self.next_move()
        self.hamle_degisimi()
        if self.form == 0: 
            self.button_color_control()
        self.move_number+=1          # hamle sayısı sayaci
        self.move_label.config(text=f"Hamle sayisi: {self.move_number}")

    def empty_button_choose(self,button):
        for i in range(len(self.buttons)):      # tıklanan butonun indeksi
            if button in self.buttons[i]:
                row = i
                col = self.buttons[i].index(button)
                break
        self.choose_move.append([row,col])
        self.next_moves = [[row - 1,col],[row + 1,col],[row,col -1],[row,col +1]]   # oynanabilecek hamlelerin konumları
        
    def hamle_degisimi(self):
        if len(self.choose_move) < 2:
            return
        button2 = self.buttons[self.choose_move[-1][-2]][self.choose_move[-1][-1]]
        button1 = self.buttons[self.choose_move[-2][-2]][self.choose_move[-2][-1]]
        if self.form == 0:
            button_text = button2["text"]
            button1["text"] = button_text
            button2["text"] = ""
        else:
            button_image = button2["image"]
            button2["image"] = button1["image"]
            button1["image"] = button_image
        
    def button_color_control(self):
        true_button_value = 0
        for i in range(self.level):
            for j in range(self.level):
                true_button_value+=1
                if self.buttons[i][j]["text"] == str(true_button_value):
                    self.buttons[i][j].config(background="green")
                else:
                    self.buttons[i][j].config(background="red")
    
    def difficult_selec(self):
            
        # option menu oluşturulması
        options = ["Level 1", "Level 2", "Level 3", "Level 4"]
        self.selected_option = tk.StringVar()
        self.selected_option.set(options[1])
        option = tk.OptionMenu(self.root, self.selected_option, *options)
        option.grid(row=5, column=0, columnspan=7)

        # seçim butonu oluşturulması
        button = tk.Button(self.root, text="Start",width=10, height=2,command=self.star_game_onclick)
        button.grid(row=11, column=0, columnspan=8)

        self.move_label = tk.Label(text=f"Hamle sayisi: {self.move_number}")
        self.move_label.grid(row=12, column=0,columnspan=8 )

    def star_game_onclick(self):
        if len(self.buttons) !=0:
            self.butonlari_sil()
        self.level_choose()
        self.buttons = []
        self.choose_move=[]
        self.next_moves=[]
        self.move_number=0
        if self.form == 0:
            self.interface_olustur()
        else:
            self.picture_desing()
            self.interface_olustur_image()
    def butonlari_sil(self):
        for i in range(self.level):
            for j in range(self.level):
                self.buttons[i][j].destroy()
        self.buttons = []
    def level_choose(self):
        if int(self.selected_option.get()[-1]) == 1:
            self.level = 3
            self.form = 0
        elif int(self.selected_option.get()[-1]) == 2:
            self.level = 4
            self.form = 0
        elif int(self.selected_option.get()[-1]) == 3:
            self.level = 3
            self.form = 1
            self.adress = '\\gorseller\\level3\\'
        elif int(self.selected_option.get()[-1]) == 4:
            self.level = 4
            self.form = 2
            self.adress = '\\gorseller\\level4\\'
    def picture_desing(self):
        if self.form == 2:
            # image_files listesi
            self.image_files = ["1.png", "2.png", "3.png", "4.png",
                        "5.png", "6.png", "7.png", "8.png",
                        "9.png", "10.png", "11.png", "12.png",
                        "13.png", "14.png", "15.png", "16.png"]

            # image_files listesinin kopyası
            self.random_image_files = copy.copy(self.image_files)

            # Kopyalanan listedeki elemanları rastgele karıştırma
            random.shuffle(self.random_image_files)
        elif self.form == 1:
            # image_files listesi
            self.image_files = ["1.png", "2.png", "3.png", "4.png",
                        "5.png", "6.png", "7.png", "8.png",
                        "9.png"]

            # image_files listesinin kopyası
            self.random_image_files = copy.copy(self.image_files)

            # Kopyalanan listedeki elemanları rastgele karıştırma
            random.shuffle(self.random_image_files)


dd=puzzle_game()

