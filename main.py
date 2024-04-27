from selenium import webdriver
from customtkinter import *
from _database_handler import AppDatabase
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import sqlite3
import time
import urllib
import json
import atexit


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())

db = AppDatabase("assets/data/app_database.db")

@atexit.register
def exit_handler() -> None:
    db.close()
    print("Exiting program")

def on_text_info_caller(texto: str) -> list:
    callers = []
    func_callers = ["(nome.contato)", "(email.contato)"]

    for i in func_callers:
        if i in texto:
            callers.append(i)

    return callers

def enviar_mensagem() -> None:
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://web.whatsapp.com/")

    while len(driver.find_elements_by_id("side")) < 1:
        time.sleep(1)

    contatos = [
        ['numero', 'nome', 'teste@outlook.com'],
        ['1', 'Maria', 'teste@gmail.com']
    ]

    texto = main_text_box.get('1.0', 'end-1c')

    for contato in contatos:
        numero, nome, email = contato
        
        callers = on_text_info_caller(texto)
        for i in callers:
            match callers:
                case "(nome.contato)":
                    texto = texto.replace(i, nome)
                case "(email.contato)":
                    texto = texto.replace(i, email)
            
        
        texto = urllib.parse.quote(texto)
        link = f"https://web.whatsapp.com/send?phone={numero}&text={texto}"
            # Formato de número sempre em (+55) 21 9....
        
        driver.get(link)
        while len(driver.find_elements_by_id("side")) < 1:
            time.sleep(1)
        driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.ENTER)
        time.sleep(10)

def character_counter(event) -> None:
    text_get = main_text_box.get('1.0', 'end-1c')

    text_lenght = len(text_get)
    func_lenght = len(on_text_info_caller(text_get))

    characters_counter_label.configure(
        text=f"{text_lenght} Caracteres\n{func_lenght} Funções   "
    )

def change_theme(_tema, button=None) -> str:
    global tema
    tema = _tema
    
    if tema == "light":
        set_appearance_mode("light")
        tema = "dark"
        tema_shown = "Escuro"
    elif tema == "dark":
        set_appearance_mode("dark")
        tema = "light"
        tema_shown = "Claro"

    if button:
        button.configure(text=f"Tema {tema_shown}")

    return tema

def language_alternator(language) -> None:
    if "PT-BR" in language:
        print("BRASIL")
    elif "EN-US" in language:
        print("USA")

# Returns to the main screen
def main_screen() -> None:
    left_bar.pack(side=LEFT, fill=Y)
    message_text.pack(expand=True, side=RIGHT, fill=BOTH)
    #pack_forget()

def contatos_screen():
    pass

def configs_tab():
    configs = CTkToplevel(app)
    configs.geometry("325x350")
    configs.title("Configurações")
    configs.minsize(width=325, height=350)
    configs.maxsize(width=325, height=350)

    def configs_navigate(*frames, tab = None) -> None:
        if not tab:
            return
        
        for frame in frames:
            frame.pack_forget()

        match tab:
            case "config":
                configs_theme_button.pack(
                    pady=10
                )
                models_button.pack(
                    pady=10
                )
                language_label.pack(
                )
                language_menu.pack(
                )
            case "add_model":
                add_model_tab()
            case "callables_tab":
                models_tab()
    
    def add_model_tab():
        model_textbox_frame = CTkFrame(master=configs, width=325, height=300)
        model_textbox_frame.pack(expand=True, fill=BOTH)

        model_bottom_frame = CTkFrame(master=configs, width=325, height=100)
        model_bottom_frame.pack(expand=True, side=BOTTOM, fill=BOTH)

        model_text_box = CTkTextbox(
            master=model_textbox_frame,
            width=325,
            height=250,
            font=("Arial", 12)
        )
        model_text_box.pack(
            expand=True,
            fill=BOTH
        )

        add_model_button = CTkButton(
            master=model_bottom_frame,
            text="Adicionar",
            width=65,
            corner_radius=64,
            border_width=2,
            command=lambda: None
        )
        add_model_button.pack(
            pady=10
        )

        go_back_button = CTkButton(
            master=model_bottom_frame,
            text="Voltar",
            width=65,
            corner_radius=64,
            border_width=2,
            command=lambda: configs_navigate(
                model_textbox_frame,
                model_bottom_frame,
                tab="callables_tab"
            )
        )
        go_back_button.pack(
            padx=5,
            side=LEFT
        )

    def models_tab(*buttons):
        callables_frame = CTkFrame(master=configs, width=325, height=300)
        callables_frame.pack(expand=True, fill=BOTH)

        add_callable_frame = CTkFrame(master=configs, width=325, height=100)
        add_callable_frame.pack(expand=True, side=BOTTOM, fill=BOTH)

        scrollable_frame = CTkScrollableFrame(callables_frame, width=325, height=250)
        scrollable_frame.pack(expand=True, fill=BOTH)

        for button in buttons:
            button.pack_forget()
        
        _lista_temp = [
            "esse",
            "aquele",
            "teste",

        ]

        _row = 0

        add_callable_button = CTkButton(
            master=add_callable_frame,
            text="Adicionar",
            corner_radius=64,
            border_width=2,
            command=lambda: configs_navigate(
                callables_frame,
                add_callable_frame,
                tab="add_model"
            )
        )
        add_callable_button.pack(
            pady=10
        )

        go_back_button = CTkButton(
            master=add_callable_frame,
            text="Voltar",
            width=65,
            corner_radius=64,
            border_width=2,
            command=lambda: configs_navigate(
                callables_frame,
                add_callable_frame,
                tab="config"
            )
        )
        go_back_button.pack(
            padx=5,
            side=LEFT
        )

        for i in _lista_temp:
            callable_options_test = CTkCheckBox(
                master=scrollable_frame,
                text=i
            )
            callable_options_test.grid(
                column=0,
                row=_row,
                padx=5,
                sticky=NSEW
            )
            callable_edit_button = CTkButton(
                master=scrollable_frame,
                text="",
                width=25,
                height=25,
                fg_color="#bfa304",
                hover_color="#bfa304"
            )
            callable_edit_button.grid(
                pady=10,
                column=1,
                row=_row,
                padx=15
            )
            callable_delete_button = CTkButton(
                master=scrollable_frame,
                text="",
                width=25,
                height=25,
                fg_color="#bf3f22",
                hover_color="#bf3f22"
            )
            callable_delete_button.grid(
                pady=10,
                column=2,
                row=_row
            )
            _row += 1

    configs_theme_button = CTkButton(
        master=configs,
        text=f"Tema {tema_shown}",
        corner_radius=64,
        border_width=2,
        command=lambda: change_theme(tema, configs_theme_button)
    )
    configs_theme_button.pack(
        pady=10,
    )
    
    models_button = CTkButton(
        master=configs,
        text="Models",
        corner_radius=64,
        border_width=2,
        command=lambda: models_tab(
            models_button,
            configs_theme_button,
            language_menu,
            language_label
        )
    )
    models_button.pack(
        pady=10
    )

    language_label = CTkLabel(
        master=configs,
        text="Idioma",
        text_color="#DCE4EE"
    )
    language_label.pack(
        pady=0
    )
    language_menu = CTkOptionMenu(
        master=configs,
        values=["Português [PT-BR]", "Inglês [EN-US]"],
        command=language_alternator
    )
    language_menu.pack(
        pady=0
    )
    language_menu.set("Inglês [EN-US]")

def teste() -> None:
    texto = main_text_box.get("1.0", "end-1c")
        
    callers = on_text_info_caller(texto)
    print(callers)
    for i in callers:
        match i:
            case "(nome.contato)":
                texto = texto.replace(i, 'NomeContato')
            case "(email.contato)":
                texto = texto.replace(i, 'EmailContato')

    print(texto)


app = CTk()
app.geometry("850x650")
app.title("app legal")
app.minsize(width=600, height=450)
set_appearance_mode("system")
set_default_color_theme("assets/configs/theme.json")

left_bar = CTkFrame(master=app, width=185, corner_radius=0)
left_bar.pack(side=LEFT, fill=Y)

message_text = CTkFrame(master=app, width=200, height=350)
message_text.pack(expand=True, side=RIGHT, fill=BOTH)

whatsapp_icon_png = Image.open("assets/icons/whatsapp-icon.png").resize((20, 20))

system_theme = AppearanceModeTracker.detect_appearance_mode()

if system_theme == 0:
    tema = "dark"
    tema_shown = "Escuro"
elif system_theme == 1:
    tema = "light"
    tema_shown = "Claro"

main_text_label = CTkLabel(
    master=message_text, text="Automatizar mensagens",
    font=("Helvetica", 24, "bold"),
)
main_text_label.pack(
    fill=BOTH,
    expand=True
)

main_text_box = CTkTextbox(
    master=message_text,
    width=560,
    height=350,
    corner_radius=16,
    border_width=2
)
main_text_box.pack(
    fill=BOTH,
    expand=True
)

add_img_button = CTkButton(
    master=message_text, text="Adicionar imagem",
    corner_radius=64,
    border_width=2
)
add_img_button.pack(
    side=BOTTOM,
    pady=25,
    ipady=5,
    padx=8
)

characters_counter_label = CTkLabel(
    master=message_text, 
    text=f"0 Caracteres\n0 Funções   ",
    image=CTkImage(dark_image=whatsapp_icon_png, size=(87, 31), light_image=whatsapp_icon_png),
    font=("Roboto", 12)
)
characters_counter_label.pack(
    padx=15,
    pady=1,
    side=RIGHT
)
main_text_box.bind( '<KeyRelease>',  character_counter)

null_label = CTkLabel(
    master=left_bar,
    text=""
)
null_label.pack(
    side=TOP,
    fill=X,
    pady=50
)

contatos_screen_button = CTkButton(
    master=left_bar, text="Adicionar Contatos", 
    corner_radius=64,
    border_width=2,
    command=contatos_screen,
    image=CTkImage(dark_image=whatsapp_icon_png, size=(12, 12), light_image=whatsapp_icon_png)
)
contatos_screen_button.pack(
    fill=BOTH,
    padx=7,
    pady=8
)

enviar_mensagens_screen_button = CTkButton(
    master=left_bar, text="Enviar mensagens",
    corner_radius=64,
    border_width=2,
    command=teste,
)
enviar_mensagens_screen_button.pack(
    fill=BOTH,
    padx=7,
    pady=8
)

config_tab_button = CTkButton(
    master=left_bar, text="Configurações",
    corner_radius=64,
    border_width=2,
    command=configs_tab
)
config_tab_button.pack(
    side=BOTTOM,
    fill=BOTH,
    padx=7,
    pady=8
)


app.mainloop()