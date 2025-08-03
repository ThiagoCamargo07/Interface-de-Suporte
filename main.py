import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import subprocess
import socket
import datetime

# Caminho para salvar os logs
LOG_DIR = "relatorios"
os.makedirs(LOG_DIR, exist_ok=True)

def salvar_log(texto):
    data = datetime.datetime.now().strftime("%Y-%m-%d")
    arquivo = os.path.join(LOG_DIR, f"logs_{data}.txt")
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {texto}\n")

def abrir_ultimo_log():
    try:
        data = datetime.datetime.now().strftime("%Y-%m-%d")
        arquivo = os.path.join(LOG_DIR, f"logs_{data}.txt")
        if not os.path.exists(arquivo):
            messagebox.showinfo("Relatório", "Nenhum log encontrado para hoje.")
            return

        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()

        janela_log = tk.Toplevel()
        janela_log.title("Relatório Técnico")
        janela_log.geometry("600x400")
        janela_log.configure(bg="#1e1e2e")

        txt = scrolledtext.ScrolledText(janela_log, wrap=tk.WORD, bg="#2e2e3e", fg="white", font=("Consolas", 10))
        txt.insert(tk.END, conteudo)
        txt.pack(expand=True, fill="both", padx=10, pady=10)
        txt.configure(state="disabled")

    except Exception as e:
        salvar_log(f"Erro ao abrir relatório: {e}")
        messagebox.showerror("Erro", f"Erro ao abrir relatório: {e}")

# Funções do Toolkit

def verificar_ip():
    try:
        nome_maquina = socket.gethostname()
        ip_local = socket.gethostbyname(nome_maquina)
        salvar_log(f"IP Local: {ip_local}")
        messagebox.showinfo("IP Local", f"IP da máquina: {ip_local}")
    except Exception as e:
        salvar_log(f"Erro ao verificar IP: {e}")
        messagebox.showerror("Erro", f"Erro ao verificar IP: {e}")

def testar_ping():
    resposta = os.system("ping www.google.com")
    if resposta == 0:
        salvar_log("Ping bem-sucedido.")
        messagebox.showinfo("Ping", "Conectado à internet!")
    else:
        salvar_log("Falha no ping.")
        messagebox.showwarning("Ping", "Sem conexão com a internet.")

def limpar_temporarios():
    try:
        os.system("del /q /s %temp%\\*")
        salvar_log("Arquivos temporários limpos.")
        messagebox.showinfo("Limpeza", "Arquivos temporários removidos com sucesso.")
    except Exception as e:
        salvar_log(f"Erro na limpeza: {e}")
        messagebox.showerror("Erro", f"Erro ao limpar: {e}")

def otimizar_unidades():
    try:
        subprocess.run(["dfrgui"], shell=True)
        salvar_log("Ferramenta de Otimização de Unidades aberta.")
        messagebox.showinfo("Otimização", "Ferramenta de Otimização de Disco aberta.")
    except Exception as e:
        salvar_log(f"Erro ao abrir Otimizador de Disco: {e}")
        messagebox.showerror("Erro", f"Erro ao abrir o Otimizador: {e}")

def executar_chkdsk():
    try:
        resultado = subprocess.run(["chkdsk"], shell=True, capture_output=True, text=True)
        output = resultado.stdout or "Nenhuma saída capturada."
        salvar_log("CHKDSK executado com sucesso.")
        salvar_log(output)

        # Análise simples da saída para o usuário final
        if "Windows verificou o sistema de arquivos" in output or "Windows has scanned the file system" in output:
            resumo = "Verificação do disco concluída com sucesso."
        elif "não pode continuar" in output.lower():
            resumo = "CHKDSK não pode ser executado no momento."
        else:
            resumo = "CHKDSK executado. Consulte o relatório para mais detalhes."

        messagebox.showinfo("CHKDSK", resumo)
    except Exception as e:
        salvar_log(f"Erro ao executar CHKDSK: {e}")
        messagebox.showerror("Erro", f"Erro ao executar CHKDSK: {e}")

def abrir_update_manager():
    try:
        subprocess.run(["control", "/name", "Microsoft.WindowsUpdate"], shell=True)
        salvar_log("Update Manager aberto.")
    except Exception as e:
        salvar_log(f"Erro ao abrir o Update Manager: {e}")

# Interface Tkinter
root = tk.Tk()
root.title("Toolkit de Suporte Técnico")
root.geometry("500x400")
root.configure(bg="#1e1e2e")

fonte = ("Segoe UI", 10)

# Título
titulo = tk.Label(root, text="Toolkit de Suporte Técnico", bg="#1e1e2e", fg="#00ffff", font=("Segoe UI", 16, "bold"))
titulo.pack(pady=15)

# Frame com botões
frame = tk.Frame(root, bg="#1e1e2e")
frame.pack(pady=10)

botoes = [
    ("Verificar IP", verificar_ip),
    ("Testar Ping", testar_ping),
    ("Limpar Temporários", limpar_temporarios),
    ("Otimizar Disco", otimizar_unidades),
    ("Executar CHKDSK", executar_chkdsk),
    ("Abrir UpdateManager", abrir_update_manager),
    ("Ver Relatório", abrir_ultimo_log),
    ("Sair", root.destroy)
]

for i, (texto, comando) in enumerate(botoes):
    btn = tk.Button(frame, text=texto, command=comando, width=25, height=2, bg="#2e2e3e", fg="#ffffff", font=fonte)
    btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)

# Rodapé
status = tk.Label(root, text="Desenvolvido por Thiago Camargo", bg="#1e1e2e", fg="#aaaaaa", font=("Segoe UI", 8))
status.pack(side="bottom", pady=5)

root.mainloop()
