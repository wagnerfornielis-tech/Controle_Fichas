import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://localhost:5000/api/ficha"  # seu Flask precisa estar rodando

def enviar_fichas():
    try:
        qtd = int(entry_qtd.get())
        if qtd <= 0:
            messagebox.showwarning("Aviso", "Digite um número maior que zero.")
            return

        dados = {"fichas": qtd}
        r = requests.post(API_URL, json=dados)

        if r.status_code == 200:
            resposta = r.json()
            messagebox.showinfo("Sucesso", f"✅ {resposta['fichas']} fichas registradas!")
        else:
            messagebox.showerror("Erro", f"❌ Erro {r.status_code}: {r.text}")

    except ValueError:
        messagebox.showwarning("Aviso", "Digite apenas números.")

# Criar janela
root = tk.Tk()
root.title("Simulador de Fichas")
root.geometry("300x150")

# Label e campo de entrada
label = tk.Label(root, text="Quantidade de fichas:")
label.pack(pady=5)

entry_qtd = tk.Entry(root, justify="center")
entry_qtd.insert(0, "1")  # valor padrão
entry_qtd.pack(pady=5)

# Botão enviar
btn = tk.Button(root, text="Enviar", command=enviar_fichas, bg="#4CAF50", fg="white")
btn.pack(pady=10)

# Rodar interface
root.mainloop()
