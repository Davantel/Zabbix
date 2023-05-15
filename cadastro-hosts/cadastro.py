import csv
from tkinter import *
from tkinter import filedialog, messagebox
from zabbix_api import ZabbixAPI, ZabbixAPIException
import customtkinter as tkc
from PIL import Image
import time

api_conectada = False

# Função para conectar à API do Zabbix
def connect_zabbix():
    global zapi, api_conectada

    hostname = host_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    try:
        zapi = ZabbixAPI(hostname)
        zapi.validate_certs = False
        zapi.login(username, password)
        api_conectada = True
        status_label.configure(text="Conectado na API", text_color='#04c46c')

        select_csv_button.configure(state="normal")
        csv_path_entry.configure(state="normal")

    except ZabbixAPIException as e:
        messagebox.showerror("Erro", str(e))
        status_label.configure(text="Não Conectado na API", text_color='red')

    status_label.update()


# Função para selecionar o arquivo CSV
def select_csv_file():
    global csv_file_path

    csv_file_path = filedialog.askopenfilename(filetypes=[('Arquivos CSV', '*.csv')])
    csv_path_entry.delete(0, END)
    csv_path_entry.insert(0, csv_file_path)
    cadastrar_button.configure(state="normal")

# Função para cadastrar os hosts
def cadastrar_hosts():
    global csv_file_path

    if not csv_file_path:
        messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado.")
        return

    with open(csv_file_path, 'r') as csvfile:
        arquivo = csv.reader(csvfile, delimiter=';')
        next(arquivo)

        for (i, a, b, c, d, e) in arquivo:

            host_label.configure(text=f"Cadastrando equipamento - {i}")
            host_label.update()

            existing_hosts = zapi.host.get({"filter": {"host": i}})
            if existing_hosts:
                host_label.configure(text=f"O host {i} já existe")
                host_label.update()
                time.sleep(2)
                
                continue

            interfaces = []
            if b.lower() == "agent":
                interfaces.append({
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": a,
                    "dns": "",
                    "port": "10050"
                })
            elif b.lower() == "snmp":
                interfaces.append({
                    "type": 2,
                    "main": 1,
                    "useip": 1,
                    "ip": a,
                    "dns": "",
                    "port": "161",
                    "details": {
                        "version": "2",
                        "bulk": "1",
                        "community": "{$SNMP_COMMUNITY}"
                    }
                })

            groups = []
            for group_name in c.split(','):
                group_id = zapi.hostgroup.get({"filter": {"name": group_name}})[0]['groupid']
                groups.append({"groupid": group_id})

            templates = []
            for template_name in d.split(','):
                template_id = zapi.template.get({"filter": {"name": template_name}})[0]['templateid']
                templates.append({"templateid": template_id})

            if e.lower() == "proxy":
                proxy_id = zapi.proxy.get({"filter": {"host": "proxy1"}})[0]['proxyid']

            zapi.host.create({
                "host": i,
                "interfaces": interfaces,
                "groups": groups,
                "templates": templates,
                "proxy_hostid": proxy_id if e.lower() == "proxy" else "0"
            })

        progress_label.configure(text=f"Todos os hosts foram cadastrados")
        

tkc.set_appearance_mode("System")
tkc.set_default_color_theme("blue")
app = tkc.CTk()
app.geometry('400x660')
app.title('Cadastro de Hosts no Zabbix')

#logo
imagem = tkc.CTkImage(dark_image=Image.open('icon.png'), size=(45, 45))
logo = tkc.CTkLabel(app, text="", height=10, image=imagem)
logo.place(x=50,y=12)

#texto intro
intro = tkc.CTkLabel(app, text="Cadastro de hosts", font=('Ivy', 28, 'bold'), height=10)
intro.place(x=110,y=18)

linha = tkc.CTkLabel(app, text="", width=450, height=1, font=('Ivy', 1), fg_color=('#d81424'))
linha.place(x=0,y=70)

# Frame conexão
frame = tkc.CTkFrame(app, width=380, height=250, border_width=1, border_color='#d81424')
frame.place(x=10, y=100)

# Credenciais de conexão
tkc.CTkLabel(frame, text="Conexão", font=('Ivy', 15, 'bold'), height=10).place(x=170, y=10)
tkc.CTkLabel(frame, text="Servidor", font=('Ivy', 12, 'bold')).place(x=70, y=40)
tkc.CTkLabel(frame, text="Usuário", font=('Ivy', 12, 'bold')).place(x=70, y=80)
tkc.CTkLabel(frame, text="Senha", font=('Ivy', 12, 'bold')).place(x=70, y=120)

host_entry = tkc.CTkEntry(frame, font=('Ivy', 12, 'bold'), corner_radius=13)
user_entry = tkc.CTkEntry(frame, font=('Ivy', 12, 'bold'), corner_radius=13)
password_entry = tkc.CTkEntry(frame, show="*", corner_radius=13)

host_entry.place(x=130, y=40)
user_entry.place(x=130, y=80)
password_entry.place(x=130, y=120)

# Botão de conexão
connect_button = tkc.CTkButton(frame, text="Conectar", command=connect_zabbix, font=('Ivy', 15, 'bold'), corner_radius=13, fg_color='#d81424', hover_color='#ec1c2c')
connect_button.place(x=130, y=170)

status_label = tkc.CTkLabel(frame, text="", font=('Ivy', 15, 'bold'), width=330, height=30, fg_color=('black', '#323232'), corner_radius=8)
status_label.place(x=25, y=210)

# frame cadastro
frame2 = tkc.CTkFrame(app, width=380, height=260, border_width=1, border_color='#d81424')
frame2.place(x=10, y=355)

# Selecionar arquivo CSV
tkc.CTkLabel(frame2, text="Cadastro", font=('Ivy', 15, 'bold'), height=10).place(x=170, y=10)

select_csv_button = tkc.CTkButton(frame2, text="Selecionar arquivo CSV", command=select_csv_file, font=('Ivy', 15, 'bold'), corner_radius=13, fg_color='#d81424', state="disabled", hover_color='#ec1c2c')
select_csv_button.place(x=105, y=50)

csv_path_entry = tkc.CTkEntry(frame2, corner_radius=13, font=('Ivy', 12, 'bold'), width=197, state="disabled")
csv_path_entry.place(x=105, y=90)

# Botão de cadastro
cadastrar_button = tkc.CTkButton(frame2, text="Cadastrar Hosts", command=cadastrar_hosts, font=('Ivy', 15, 'bold'), corner_radius=13, fg_color='#d81424', state="disabled", hover_color='#ec1c2c')
cadastrar_button.place(x=130, y=140)

# Progresso do cadastro
host_label = tkc.CTkLabel(frame2, text="", font=('Ivy', 15, 'bold'), width=330, height=30, fg_color=('black', '#323232'), corner_radius=8)
host_label.place(x=25, y=180)

progress_label = tkc.CTkLabel(frame2, text="", text_color='#04c46c', font=('Ivy', 15, 'bold'), width=330, height=30, fg_color=('black', '#323232'), corner_radius=8)
progress_label.place(x=25, y=220)

copy = tkc.CTkLabel(app, text="© 2023 by Caio Davantel. All rights reserved.", font=('Ivy', 9, 'bold'), width=400, height=30, fg_color=('black', '#323232'))
copy.place(x=0, y=630)

app.mainloop()

