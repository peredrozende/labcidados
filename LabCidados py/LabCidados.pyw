#!/usr/bin/env python3.7
### LabCidados.py ###

# importa módulos
import sys
import os
import csv
from dbfread import DBF
from string import Template
from io import StringIO
from zipfile import ZipFile, ZIP_DEFLATED
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory

try:
	from PyQt5 import QtCore, QtGui, QtWidgets, uic
except ModuleNotFoundError:
	os.system('python -m pip install PyQt5 --quiet')

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# cria variáveis do programa
parent = os.path.dirname(os.path.realpath(__file__))
lic = [x.replace('.txt','') for x in os.listdir('licencas') if not x.startswith('_')]
qtCreatorFile = 'LabCidados.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# classe de interface
class LabCidados(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.avisosucesso.hide()
		self.listaalvos = []

		renome = QtCore.QRegExp('[^/:?|<>*"]{1,}')
		validanome = QtGui.QRegExpValidator(renome)
		self.titulo.setValidator(validanome)

		self.empacotar.clicked.connect(self.executar)
		self.browseAlvos.clicked.connect(self.achar_dados)
		self.limparAlvos.clicked.connect(self.limpar_dados)
		self.browseDestino.clicked.connect(self.achar_destino)
		self.titulo.editingFinished.connect(self.checar)
		self.equipe.editingFinished.connect(self.checar)
		self.financiadores.editingFinished.connect(self.checar)
		self.adicionarVariavel.clicked.connect(self.nova_variavel)
		self.excluirVariavel.clicked.connect(self.excluir_variavel)
		
		# lida com a escolha da licença
		self.licenca.addItems(lic)
		self.resumir_licenca()
		self.licenca.currentTextChanged.connect(self.resumir_licenca)

	def nome_vars(self,arquivo):
		nvars = ['']
		if arquivo.endswith('.csv') or arquivo.endswith('.txt'):
			try:
				with open(arquivo,'r') as alvo:
					head = alvo.readline()
					head = head.replace('\n','')
				seps = [';','	','|',',']
				for s in seps:
					nvars = head.split(s)
					if len(nvars) > 1:
						break
			except:
				pass
		elif arquivo.endswith('.dbf'):
			try:
				t = DBF(arquivo)
				nvars = t.field_names
			except:
				pass
		return nvars

	def resumir_licenca(self):
		self.resumoLicenca.clear()
		rlic = parent+'\licencas\_{}.txt'.format(self.licenca.currentText())
		try:
			with open (rlic,'r',encoding='utf-8') as html:
				trlic = html.read()
			self.resumoLicenca.insertHtml(trlic)
		except:
			pass

	def achar_dados(self):
		Tk().withdraw()
		a = askopenfilenames(title='Escolha os arquivos a empacotar')
		if a:
			b = [x for x in a if os.path.basename(x) not in self.listaalvos]
			self.alvos.addItems(b)
			bn = [os.path.basename(x) for x in b]
			for x in bn:
				self.listaalvos.append(x)
			for r in range(self.variaveis.rowCount()):
				self.variaveis.cellWidget(r,0).addItems(bn)
			self.checar()
			
			# autopreenche linhas na tabela
			c = 0
			for fonte in b:
				nomevars = self.nome_vars(fonte)
				for n in nomevars:
					self.nova_variavel()
					combo =self.variaveis.cellWidget(self.variaveis.rowCount()-1,0)
					index = combo.findText(bn[c], QtCore.Qt.MatchFixedString)
					combo.setCurrentIndex(index)
					v = QtWidgets.QTableWidgetItem()
					v.setText(n)
					self.variaveis.setItem(self.variaveis.rowCount()-1,1,v)
					d = QtWidgets.QTableWidgetItem()
					d.setText('')
					self.variaveis.setItem(self.variaveis.rowCount()-1,2,d)
				c+=1

	def limpar_dados(self):
		self.alvos.clear()
		self.listaalvos = []
		self.variaveis.setRowCount(0)
		self.checar()

	def achar_destino(self):
		Tk().withdraw()
		d = askdirectory()
		if d:
			self.destino.clear()
			self.destino.insert(d)
			self.listadestino = os.listdir(d)
			self.checar()

	def nova_variavel(self):
		n = self.variaveis.rowCount()
		self.variaveis.insertRow(n)
		combo = QtWidgets.QComboBox()
		if self.listaalvos:
			combo.addItems(self.listaalvos)
		self.variaveis.setCellWidget(n,0,combo)

	def excluir_variavel(self):
		n = self.variaveis.currentRow()
		self.variaveis.removeRow(n)

	def checar(self):
		try:
			assert os.path.isdir(self.destino.text())
			assert self.alvos.count() > 0
			assert len(self.titulo.text())>0
			assert len(self.equipe.text())>0
			assert len(self.financiadores.text())>0
			self.empacotar.setEnabled(True)
		except AssertionError:
			self.empacotar.setEnabled(False)
			self.avisosucesso.hide()
			pass

	def documentar(self):
		arqtt = parent + r'\recursos\template_doc.txt'
		with open(arqtt,'r',encoding='utf-8') as arq:
			modelo = Template(arq.read())	
		_nome = self.titulo.text().upper()
		Lequipe = self.equipe.text().split(';')
		Lequipe = [x.strip().title() for x in Lequipe]
		_equipe = ', '.join(Lequipe)
		Lfin = self.financiadores.text().split(';')
		Lfin = [x.strip() for x in Lfin]
		_financiadores = ', '.join(Lfin)
		_licenca = self.licenca.currentText()
		Ldata = str(self.data.date().toPyDate())
		Ldata = Ldata.split('-')
		_data = '/'.join(Ldata[::-1])

		if len(self.periodicidade.text()) > 0:
			_periodicidade = self.periodicidade.text().lower()
		else:
			_periodicidade = 'não prevista'

		_alvos = '\n'.join(self.listaalvos)
		_conteudo = self.conteudo.toPlainText()
		_metodologia = self.metodologia.toPlainText()
		_finalidade = self.contexto.toPlainText()
		Lterceiros = self.terceiros.toPlainText().split(';')
		Lterceiros = ['- '+x.strip() for x in Lterceiros if x]
		_terceiros = '\n'.join(Lterceiros)

		dfill = {'nome':_nome,
		'equipe':_equipe,
		'financiadores':_financiadores,
		'licenca':_licenca,
		'data':_data,
		'periodicidade':_periodicidade,
		'alvos':_alvos,
		'conteudo':_conteudo,
		'metodologia':_metodologia,
		'finalidade':_finalidade,
		'terceiros':_terceiros
		}

		doc = modelo.substitute(dfill)
		return doc

	def listar_variaveis(self):
		self.docvar = []
		for r in range(self.variaveis.rowCount()):
			dic = {}
			dic['Arquivo'] = self.variaveis.cellWidget(r,0).currentText()
			dic['Variável'] = self.variaveis.item(r,1).text()
			dic['Descrição'] = self.variaveis.item(r,2).text()
			self.docvar.append(dic)

	def executar(self):
		# configura o pacote
		nome = self.titulo.text()
		iguais = [x for x in self.listadestino if x.startswith(nome) and x.endswith('.zip')]

		if iguais:
			sufixo = '_' + str(len(iguais))
		else:
			sufixo = ''

		zf = self.destino.text() +'/{0}{1}.zip'.format(self.titulo.text(),sufixo)
		saida = ZipFile(zf,'w',ZIP_DEFLATED)

		for i in range(self.alvos.count()):
			alvo = self.alvos.item(i).text()
			copia = '{0}\\{1}'.format(self.titulo.text(),os.path.basename(alvo))
			saida.write(alvo,copia)

		# empacota a licença
		licf = parent + '\licencas\{}.txt'.format(self.licenca.currentText())
		saida.write(licf,'LICENÇA.txt')
		
		# empacota as informações das variáveis
		self.listar_variaveis()
		if self.docvar:
			string_saida = StringIO()
			keys = list(self.docvar[0].keys())
			writer = csv.DictWriter(string_saida,delimiter=';',fieldnames=keys)
			writer.writeheader()
			for i in self.docvar:
				writer.writerow(i)
			saida.writestr('VARIÁVEIS.csv',string_saida.getvalue())
			string_saida.close()

		# empacota a documentação
		doc = self.documentar()
		saida.writestr('DOCUMENTAÇÃO.md',doc)

		# fecha o arquivo zip
		saida.close()

		# reseta a interface
		self.empacotar.setEnabled(False)
		self.avisosucesso.show()
		self.alvos.clear()
		self.destino.clear()
		self.titulo.clear()
		self.equipe.clear()
		self.financiadores.clear()
		self.periodicidade.clear()
		self.conteudo.clear()
		self.metodologia.clear()
		self.contexto.clear()
		self.terceiros.clear()
		self.variaveis.setRowCount(0)
		self.docvar = []

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = LabCidados()
	window.show()
	sys.exit(app.exec_())
