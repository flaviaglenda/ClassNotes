# Flávia Glenda G Carvalho
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

dados = pd.DataFrame(columns=["Nome", "Idade", "Curso", "Nota Final", "Status"])

def adicionar_aluno():
    global dados
    nome = entry_nome.get()
    idade = entry_idade.get()
    curso = entry_curso.get()
    nota = entry_nota.get()

    if nome == "" or idade == "" or curso == "" or nota == "":
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    try:
        idade = int(idade)
        nota = float(nota)
    except:
        messagebox.showerror("Erro", "Idade e Nota precisam ser números!")
        return

    status = "Aprovado" if nota >= 5 else "Reprovado"

    novo = {"Nome": nome, "Idade": idade, "Curso": curso, "Nota Final": nota, "Status": status}
    dados = pd.concat([dados, pd.DataFrame([novo])], ignore_index=True)
    atualizar_tabela()
    limpar_campos()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_curso.delete(0, tk.END)
    entry_nota.delete(0, tk.END)

def atualizar_tabela(df=None):
    for i in tree.get_children():
        tree.delete(i)
    if df is None:
        df = dados
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

def filtrar():
    try:
        media = float(entry_media.get())
        filtrado = dados[dados["Nota Final"] > media]
        if filtrado.empty:
            messagebox.showinfo("Aviso", "Nenhum aluno com nota acima dessa média.")
        else:
            messagebox.showinfo("Sucesso", f"Foram encontrados {len(filtrado)} alunos com nota acima de {media}.")
        atualizar_tabela(filtrado)
    except:
        messagebox.showerror("Erro", "Digite uma média válida!")

def salvar_csv():
    if dados.empty:
        messagebox.showwarning("Aviso", "Não há dados para salvar!")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if caminho:
        dados.to_csv(caminho, index=False)
        messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso!")

def carregar_csv():
    global dados
    caminho = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
    if caminho:
        dados = pd.read_csv(caminho)
        atualizar_tabela()

def exportar_filtrado():
    try:
        media = float(entry_media.get())
        filtrado = dados[dados["Nota Final"] > media]
        if filtrado.empty:
            messagebox.showinfo("Aviso", "Nenhum aluno com nota acima dessa média.")
            return
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if caminho:
            filtrado.to_csv(caminho, index=False)
            messagebox.showinfo("Sucesso", "Relatório exportado com sucesso!")
    except:
        messagebox.showerror("Erro", "Digite uma média válida!")

janela = tk.Tk()
janela.title("📚 Sistema de Cadastro de Alunos")
janela.geometry("650x550")
janela.configure(bg="#f7f7f7")

tk.Label(janela, text="Nome:", bg="#f7f7f7").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nome = tk.Entry(janela, width=30)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(janela, text="Idade:", bg="#f7f7f7").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_idade = tk.Entry(janela, width=30)
entry_idade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(janela, text="Curso:", bg="#f7f7f7").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_curso = tk.Entry(janela, width=30)
entry_curso.grid(row=2, column=1, padx=5, pady=5)

tk.Label(janela, text="Nota Final:", bg="#f7f7f7").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_nota = tk.Entry(janela, width=30)
entry_nota.grid(row=3, column=1, padx=5, pady=5)

tk.Button(janela, text="Cadastrar", command=adicionar_aluno, bg="#4CAF50", fg="white", width=15).grid(row=4, column=1, pady=10)

colunas = ("Nome", "Idade", "Curso", "Nota Final", "Status")
tree = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
for col in colunas:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

#filtrar
tk.Label(janela, text="Filtrar alunos com nota acima de:", bg="#f7f7f7").grid(row=6, column=0, padx=5, pady=5, sticky="e")
entry_media = tk.Entry(janela, width=10)
entry_media.grid(row=6, column=1, sticky="w")
tk.Button(janela, text="Filtrar", command=filtrar, bg="#2196F3", fg="white", width=10).grid(row=6, column=1, sticky="e")

tk.Button(janela, text="Salvar CSV", command=salvar_csv, bg="#FF9800", fg="white", width=15).grid(row=7, column=0, pady=5)
tk.Button(janela, text="Carregar CSV", command=carregar_csv, bg="#9C27B0", fg="white", width=15).grid(row=7, column=1, pady=5)
tk.Button(janela, text="Exportar Relatório Filtrado", command=exportar_filtrado, bg="#E91E63", fg="white", width=25).grid(row=8, column=0, columnspan=2, pady=10)

janela.mainloop()
