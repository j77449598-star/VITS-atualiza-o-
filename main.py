import tkinter as tk
import os
import urllib.request
import socket

# ==========================================
# CRIAR PASTAS
# ==========================================

pastas = ["apps", "jogos", "fotos", "gravacoes"]

for pasta in pastas:
    if not os.path.exists(pasta):
        os.mkdir(pasta)

# ==========================================
# SINCRONIZAR COM GITHUB
# ==========================================

def sincronizar():
    try:
        tela = tk.Tk()
        tela.title("VITS")
        tela.geometry("400x150")
        tela.configure(bg="black")
        tk.Label(tela, text="Baixando atualização...", font=("Arial",20), fg="lime", bg="black").pack(pady=40)
        tela.update()
        url = "https://raw.githubusercontent.com/j77449598-star/VITS-atualiza-o-/main/main.py"
        urllib.request.urlretrieve(url, "main.py")
        tela.destroy()
    except:
        pass

sincronizar()

# ==========================================
# CRIAR ARQUIVOS DO SISTEMA
# ==========================================

sistema = {

"apps/vits_store.py": '''
import tkinter as tk
import os

janela = tk.Tk()
janela.title("VITS Store")
janela.geometry("1100x700")
janela.configure(bg="black")

titulo = tk.Label(janela, text="VITS Store", font=("Arial",30), fg="lime", bg="black")
titulo.pack(pady=10)

frame_instalar = tk.Frame(janela, bg="black")
frame_instalar.pack(fill="x", padx=20, pady=5)

tk.Label(frame_instalar, text="Nome:", font=("Arial",13), fg="white", bg="black").grid(row=0, column=0, padx=5)

entry_nome = tk.Entry(frame_instalar, font=("Arial",13), width=20, bg="gray15", fg="white", insertbackground="white")
entry_nome.grid(row=0, column=1, padx=5)

var_tipo = tk.StringVar(value="app")
tk.Radiobutton(frame_instalar, text="App", variable=var_tipo, value="app", bg="black", fg="white", selectcolor="gray20", font=("Arial",12)).grid(row=0, column=2, padx=5)
tk.Radiobutton(frame_instalar, text="Jogo", variable=var_tipo, value="jogo", bg="black", fg="white", selectcolor="gray20", font=("Arial",12)).grid(row=0, column=3, padx=5)

tk.Label(frame_instalar, text="Cole o código:", font=("Arial",13), fg="white", bg="black").grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=5)

texto_codigo = tk.Text(frame_instalar, font=("Consolas",11), bg="gray10", fg="white", insertbackground="white", height=8)
texto_codigo.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

status_label = tk.Label(frame_instalar, text="", font=("Arial",12), fg="lime", bg="black")
status_label.grid(row=3, column=0, columnspan=3, pady=3)

def instalar():
    nome = entry_nome.get().strip().replace(" ","_").lower()
    codigo = texto_codigo.get("1.0", tk.END).strip()
    tipo = var_tipo.get()

    if not nome or not codigo:
        status_label.config(text="Preencha o nome e o código!", fg="red")
        return

    caminho = f"apps/{nome}.py" if tipo == "app" else f"jogos/{nome}.py"

    with open(caminho, "w") as f:
        f.write(codigo)

    nome_display = nome.replace("_"," ").title()
    caminho_studio = f"apps/{nome}_studio.py"

    studio_codigo = f"""
import tkinter as tk
import os

janela = tk.Tk()
janela.title("{nome_display} Studio")
janela.geometry("1200x700")
janela.configure(bg="black")

titulo = tk.Label(janela, text="{nome_display} Studio", font=("Arial",30), fg="lime", bg="black")
titulo.pack(pady=10)

texto = tk.Text(janela, font=("Consolas",13), bg="gray10", fg="white", insertbackground="white")
texto.pack(expand=True, fill="both", padx=20, pady=10)

caminho_arquivo = "{caminho}"

if os.path.exists(caminho_arquivo):
    with open(caminho_arquivo, "r") as f:
        texto.insert("1.0", f.read())

def salvar():
    with open(caminho_arquivo, "w") as f:
        f.write(texto.get("1.0", tk.END))
    status.config(text="Salvo!")

def executar():
    salvar()
    os.system(f"python3 {{caminho_arquivo}}")

status = tk.Label(janela, text="", font=("Arial",12), fg="lime", bg="black")
status.pack()

frame_btn = tk.Frame(janela, bg="black")
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Salvar", width=18, height=2, bg="darkgreen", fg="white", command=salvar).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="Executar", width=18, height=2, bg="darkblue", fg="white", command=executar).grid(row=0, column=1, padx=10)

janela.mainloop()
"""

    with open(caminho_studio, "w") as f:
        f.write(studio_codigo)

    entry_nome.delete(0, tk.END)
    texto_codigo.delete("1.0", tk.END)
    status_label.config(text=f"{nome_display} instalado!", fg="lime")
    carregar()

tk.Button(frame_instalar, text="Instalar", width=15, height=1, bg="darkgreen", fg="white", font=("Arial",13), command=instalar).grid(row=3, column=3, pady=5, padx=5)

tk.Label(janela, text="── Instalados ──", font=("Arial",16), fg="lime", bg="black").pack(pady=5)

canvas = tk.Canvas(janela, bg="black")
scroll = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
frame_canvas = tk.Frame(canvas, bg="black")

frame_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0), window=frame_canvas, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

protegidos = ["vits_store.py", "configuracoes.py"]

def abrir(caminho):
    os.system(f"python3 \'{caminho}\'")

def abrir_cmd(cmd):
    os.system(cmd)

def desinstalar(caminho):
    confirmar = tk.Toplevel()
    confirmar.title("Confirmar")
    confirmar.geometry("400x200")
    confirmar.configure(bg="black")

    nome = os.path.basename(caminho).replace(".py","").replace("_"," ").title()
    tk.Label(confirmar, text=f"Desinstalar {nome}?", font=("Arial",16), fg="white", bg="black").pack(pady=30)

    frame_btn = tk.Frame(confirmar, bg="black")
    frame_btn.pack()

    def confirmar_del():
        os.remove(caminho)
        nome_base = os.path.basename(caminho).replace(".py","")
        studio = f"apps/{nome_base}_studio.py"
        if os.path.exists(studio):
            os.remove(studio)
        confirmar.destroy()
        carregar()

    tk.Button(frame_btn, text="Sim", width=12, height=2, bg="darkred", fg="white", command=confirmar_del).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Cancelar", width=12, height=2, bg="gray20", fg="white", command=confirmar.destroy).grid(row=0, column=1, padx=10)

def carregar():
    for widget in frame_canvas.winfo_children():
        widget.destroy()

    itens = []

    for a in sorted(os.listdir("apps")):
        if a.endswith(".py"):
            nome = a.replace(".py","").replace("_"," ").title()
            itens.append((nome, f"apps/{a}", "gray20", "app"))

    for a in sorted(os.listdir("jogos")):
        if a.endswith(".py"):
            nome = a.replace(".py","").replace("_"," ").title()
            itens.append((nome, f"jogos/{a}", "darkblue", "jogo"))

    jogos_sistema = [
        ("Minecraft", "minecraft", "darkgreen"),
        ("Minecraft Launcher", "minecraft-launcher", "darkgreen")
    ]
    for nome, cmd, cor in jogos_sistema:
        if os.system(f"which {cmd} > /dev/null 2>&1") == 0:
            itens.append((nome, cmd, cor, "sistema"))

    linha = 0
    coluna = 0

    for item in itens:
        nome, caminho, cor, tipo = item[0], item[1], item[2], item[3]

        frame_item = tk.Frame(frame_canvas, bg="black")
        frame_item.grid(row=linha, column=coluna, padx=10, pady=8)

        if tipo == "sistema":
            tk.Button(frame_item, text=nome, width=28, height=2, bg=cor, fg="white", font=("Arial",13), command=lambda c=caminho: abrir_cmd(c)).pack()
        else:
            tk.Button(frame_item, text=nome, width=28, height=2, bg=cor, fg="white", font=("Arial",13), command=lambda c=caminho: abrir(c)).pack()
            arquivo = os.path.basename(caminho)
            if arquivo not in protegidos:
                tk.Button(frame_item, text="Desinstalar", width=28, bg="darkred", fg="white", font=("Arial",10), command=lambda c=caminho: desinstalar(c)).pack()

        coluna += 1
        if coluna > 2:
            coluna = 0
            linha += 1

carregar()
janela.mainloop()
''',

"apps/configuracoes.py": '''
import tkinter as tk

janela = tk.Tk()
janela.title("Configurações")
janela.geometry("600x400")
janela.configure(bg="black")

titulo = tk.Label(janela, text="Configurações", font=("Arial",30), fg="lime", bg="black")
titulo.pack(pady=20)

for opcao in ["Wi-Fi", "Bluetooth", "Áudio", "Tema"]:
    btn = tk.Button(janela, text=opcao, width=25, height=2, bg="gray20", fg="white")
    btn.pack(pady=10)

janela.mainloop()
''',

"apps/vits_studios.py": '''
import tkinter as tk
import os

janela = tk.Tk()
janela.title("VITS Studios")
janela.geometry("1000x650")
janela.configure(bg="black")

titulo = tk.Label(janela, text="VITS Studios", font=("Arial",30), fg="lime", bg="black")
titulo.pack(pady=20)

canvas = tk.Canvas(janela, bg="black")
scroll = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
frame_canvas = tk.Frame(canvas, bg="black")

frame_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0), window=frame_canvas, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

linha = 0
coluna = 0

for a in sorted(os.listdir("apps")):
    if a.endswith("_studio.py"):
        nome = a.replace(".py","").replace("_"," ").title()
        caminho = f"apps/{a}"
        btn = tk.Button(
            frame_canvas,
            text=nome,
            width=30,
            height=2,
            bg="gray20",
            fg="white",
            font=("Arial",13),
            command=lambda c=caminho: os.system(f"python3 \'{c}\'")
        )
        btn.grid(row=linha, column=coluna, padx=10, pady=8)
        coluna += 1
        if coluna > 2:
            coluna = 0
            linha += 1

janela.mainloop()
''',

"apps/vits_king.py": '''
import tkinter as tk
import os
import urllib.request
import json
import base64

GITHUB_TOKEN = "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"
REPO = "j77449598-star/VITS-atualiza-o-"
BRANCH = "main"

janela = tk.Tk()
janela.title("VITS King")
janela.geometry("1200x700")
janela.configure(bg="black")

titulo = tk.Label(janela, text="VITS King", font=("Arial",35), fg="gold", bg="black")
titulo.pack(pady=10)

tk.Label(janela, text="Arquivo (ex: main.py):", font=("Arial",13), fg="white", bg="black").pack()

entry_arquivo = tk.Entry(janela, font=("Arial",13), width=30, bg="gray15", fg="white", insertbackground="white")
entry_arquivo.pack(pady=5)
entry_arquivo.insert(0, "main.py")

tk.Label(janela, text="Código:", font=("Arial",13), fg="white", bg="black").pack()

texto = tk.Text(janela, font=("Consolas",12), bg="gray10", fg="white", insertbackground="white")
texto.pack(expand=True, fill="both", padx=20, pady=10)

status = tk.Label(janela, text="", font=("Arial",12), fg="lime", bg="black")
status.pack()

def carregar_github():
    arquivo = entry_arquivo.get().strip()
    try:
        url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{arquivo}"
        with urllib.request.urlopen(url) as r:
            conteudo = r.read().decode()
        texto.delete("1.0", tk.END)
        texto.insert("1.0", conteudo)
        status.config(text="Carregado do GitHub!", fg="lime")
    except Exception as e:
        status.config(text=f"Erro: {e}", fg="red")

def enviar_github():
    arquivo = entry_arquivo.get().strip()
    conteudo = texto.get("1.0", tk.END)

    try:
        api_url = f"https://api.github.com/repos/{REPO}/contents/{arquivo}"
        req = urllib.request.Request(api_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        with urllib.request.urlopen(req) as r:
            dados = json.loads(r.read().decode())
        sha = dados["sha"]

        corpo = json.dumps({
            "message": "VITS King update",
            "content": base64.b64encode(conteudo.encode()).decode(),
            "sha": sha,
            "branch": BRANCH
        }).encode()

        req2 = urllib.request.Request(api_url, data=corpo, method="PUT",
            headers={"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"})
        urllib.request.urlopen(req2)
        status.config(text="Enviado para todos!", fg="lime")
    except Exception as e:
        status.config(text=f"Erro: {e}", fg="red")

frame_btn = tk.Frame(janela, bg="black")
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Carregar do GitHub", width=22, height=2, bg="gray20", fg="white", command=carregar_github).grid(row=0, column=0, padx=10)
tk.Button(frame_btn, text="Enviar para Todos", width=22, height=2, bg="darkgreen", fg="white", command=enviar_github).grid(row=0, column=1, padx=10)

janela.mainloop()
''',

"apps/minecraft_launcher_vits.py": '''
import tkinter as tk
import os

janela = tk.Tk()
janela.title("Minecraft Launcher VITS")
janela.geometry("700x500")
janela.configure(bg="black")

titulo = tk.Label(janela, text="Minecraft Launcher VITS", font=("Arial",25), fg="lime", bg="black")
titulo.pack(pady=20)

def java():
    os.system("minecraft-launcher")

def pi():
    os.system("minecraft-pi")

def comprar():
    os.system("chromium-browser https://minecraft.net/pt-br")

frame = tk.Frame(janela, bg="black")
frame.pack(pady=20)

tk.Button(frame, text="Minecraft Java Edition", width=30, height=2, bg="darkgreen", fg="white", font=("Arial",14), command=java).pack(pady=10)
tk.Button(frame, text="Minecraft Pi Edition", width=30, height=2, bg="darkblue", fg="white", font=("Arial",14), command=pi).pack(pady=10)
tk.Button(frame, text="Comprar Minecraft", width=30, height=2, bg="gray20", fg="white", font=("Arial",14), command=comprar).pack(pady=10)

janela.mainloop()
'''
}

for caminho, codigo in sistema.items():
    with open(caminho, "w") as f:
        f.write(codigo)

# ==========================================
# JANELA PRINCIPAL
# ==========================================

janela = tk.Tk()
janela.title("VITS")
janela.geometry("1200x750")
janela.configure(bg="black")

titulo = tk.Label(janela, text="VITS", font=("Arial",40), fg="lime", bg="black")
titulo.pack(pady=20)

canvas = tk.Canvas(janela, bg="black")
scroll = tk.Scrollbar(janela, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas, bg="black")

frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)

canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

def abrir(cmd):
    os.system(cmd)

itens = []

for a in sorted(os.listdir("apps")):
    if a.endswith(".py"):
        if a in ["vits_king.py", "vits_studios.py"]:
            if socket.gethostname() == "VITS-King":
                nome = a.replace(".py","").replace("_"," ").title()
                itens.append((nome, f"python3 apps/{a}", "gold"))
        else:
            nome = a.replace(".py","").replace("_"," ").title()
            itens.append((nome, f"python3 apps/{a}", "gray20"))

for a in sorted(os.listdir("jogos")):
    if a.endswith(".py"):
        nome = a.replace(".py","").replace("_"," ").title()
        itens.append((nome, f"python3 jogos/{a}", "darkblue"))

jogos_sistema = [
    ("Minecraft", "minecraft", "darkgreen"),
    ("Minecraft Launcher", "minecraft-launcher", "darkgreen")
]
for nome, cmd, cor in jogos_sistema:
    if os.system(f"which {cmd} > /dev/null 2>&1") == 0:
        itens.append((nome, cmd, cor))

linha = 0
coluna = 0

for nome, cmd, cor in itens:
    btn = tk.Button(
        frame,
        text=nome,
        width=30,
        height=3,
        bg=cor,
        fg="white",
        font=("Arial",14),
        command=lambda c=cmd: abrir(c)
    )
    btn.grid(row=linha, column=coluna, padx=15, pady=15)
    coluna += 1
    if coluna > 1:
        coluna = 0
        linha += 1

janela.mainloop()
