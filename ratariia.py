from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import os
from PIL import Image,ImageTk
from bs4 import BeautifulSoup
import requests



class Tela:
	def __init__(self,root):
		self.root = root
		self.root.title("Rataria 2.0")
		self.root.geometry("1300x600")
		self.root.resizable(width=0, height=0)
		
	
		#self.root.configure(bg="black")
		self.bg=ImageTk.PhotoImage(file="imagens/bk7.jpg")
		bg=Label(self.root,image=self.bg).place(x=0, y=0, width=1300, height=600)
		
		self.left=ImageTk.PhotoImage(file="imagens/pd.png")
		left=Label(self.root,image=self.left).place(x=40, y=80, height=400, width=398)

		self.top=ImageTk.PhotoImage(file="imagens/bk6.jpg")
		top=Label(self.root,image=self.top).place(x=420, y=20)

		#Valor de entrada o INPUT DE ENTRADA DA PESQUISA .
		self.entrada_str= StringVar()
		entrada=Entry(self.root,textvariable=self.entrada_str, bg="#39dfff",font=("times new roman",15)).place(x=340, y=520,width=550)

		#Butão de pesquisa 	
		self.botao= Button(self.root,text="Go!",bg="#39dfff",fg="white",font=("bungee",20,'bold'),command=self.mostra)
		self.botao.place(x=260, y=519,relwidth=.060 ,relheight=.050)
		#Height and width === 
		#altura e largura

		# Onde recebe o conteudo
	
		self.t1= scrolledtext.ScrolledText(self.root, fg="#fff",relief=FLAT,bg="#444444",font=("ariel",9,'bold'))
		self.t1.place(x=450,y=80, width=830, height=400)

	#===============================INFORMAÇÔES SOBRE O PERFIL DO AUTOR DO ASSUNTO =========================================#
		self.var_autor = StringVar()
		self.autor = Label(self.root,text="weather", textvariable=self.var_autor,bg="#7D9EC0",fg="yellow",anchor=W,font=("bungee",13,"bold"))
		self.autor.place(x=40, y=150, width=400 ,relheight=.050)

		self.var_previa = StringVar()
		self.previa = Label(self.root,text="weather",textvariable=self.var_previa,bg="#7D9EC0",fg="yellow",anchor=W,font=("bungee",13,"normal"))
		self.previa.place(x=40, y=190, width=400 ,relheight=.050)


		self.var_tema = StringVar()
		self.tema = Label(self.root,text="weather",textvariable=self.var_tema,bg="#7D9EC0",fg="yellow",anchor=W,font=("bungee",9,"normal"))
		self.tema.place(x=40, y=230, width=400 ,relheight=.050)


		self.btn = Button(self.root,text="Visitar o perfil",bg="#7D9EC0",fg="yellow",font=("bungee",9,"normal"),command=self.perfil)
		self.btn.place(x=40, y=25, width= 140 , height=50)
	#=====================================PAGINAÇÃO==========================================#
		self.paginas = []
		for i in range(1, 100):
			self.paginas.append(i)

		self.pg = Label(self.root,text="Selecione Paginas de Pré-visualização", bg="#7D9EC0",fg="yellow",font=("bungee",9,"normal"))
		self.pg.place(x=850, y=0)

		self.pgg= ttk.Combobox(self.root,values=self.paginas)
		self.pgg.set("Selecione")
		self.pgg.place(x=900, y=40, width=80)

		self.btn = Button(self.root,text="IR",command=self.pag)
		self.btn.place(x=1000, y=40)

	#=====================================================================================#
	def pag(self):
		try:
			pag_dados = self.entrada_str.get()
			nu = self.pgg.get()
			if (pag_dados.count("/") == 5):
				new = pag_dados
				forma = new+"/"+nu
			elif (pag_dados.count("/") == 6):
				new = pag_dados[:-2]
				forma = new+"/"+nu
			new_page = requests.get(forma)
			new_soup = BeautifulSoup(new_page.content,'html.parser')
			new_sumary = new_soup.find_all('div',class_="preview-text fancy-scroll pd-paragraph-sm")[0]
			#============================================================#
			new_nome = new_soup.find_all('span',class_="jsx-2727782007")[0]
			new_paginas = new_soup.find_all('h2',class_="pd-heading-md")[0]
			new_cabeca = new_soup.find_all('h1',class_="jsx-2014966987 pd-heading-lg file-name test-file-name")[0]
			self.t1.delete(0.0, END)
			self.t1.insert(0.0, new_sumary.text)
			self.var_autor.set("Autor(a): " + new_nome.text)
			self.var_previa.set(new_paginas.text)
			self.var_tema.set("Tema:"+ new_cabeca.text)
		except:
			self.t1.delete(0.0, END)
			self.t1.insert(0.0, "Você colocou o link errado ou o rataria não consegue pega a informação dessa pagina!!")
		

	def mostra(self):
		try:
			dados = self.entrada_str.get()
			page = requests.get(dados)
			soup = BeautifulSoup(page.content, 'html.parser')
			#Menu informativo 
			sumary = soup.find_all('div',class_="preview-text fancy-scroll pd-paragraph-sm")[0]
			nome = soup.find_all('span',class_="jsx-2727782007")[0]
			paginas = soup.find_all('h2',class_="pd-heading-md")[0]
			cabeca = soup.find_all('h1',class_="jsx-2014966987 pd-heading-lg file-name test-file-name")[0]
			self.t1.delete(0.0, END)
			self.t1.insert(0.0, sumary.text)
			self.var_autor.set("Autor(a): " + nome.text)
			self.var_previa.set(paginas.text)
			self.var_tema.set("Tema:"+ cabeca.text)
		except:
			self.t1.delete(0.0, END)
			self.t1.insert(0.0, "Você colocou o link errado ou o rataria não consegue pega a informação dessa pagina!")

	def perfil(self):
		try:
			from selenium import webdriver
			perfil_nome = self.entrada_str.get()
			driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
			driver.get(perfil_nome)
			element = driver.find_element_by_class_name("jsx-2727782007")
			element.click()
		except:
			self.t1.delete(0.0, END)
			self.t1.insert(0.0, "Você colocou o link errado ou o rataria não consegue pega a informação dessa pagina!!!")


		
		
		
		


		
root =Tk()
obj = Tela(root)
root.mainloop()