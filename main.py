import classes as cl
from savefilesystem import *
from graph_view import TreeViewer,TreeWrapper
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

formula=cl.Imp(cl.Not(cl.Variable("a")), cl.Or(cl.Variable("undefined"), cl.Imp(cl.Variable("b"),cl.Bot())))

worlds= cl.World("M:0,0")
#formula = cl.Variable('undefined')
select = formula









def getlistvarrec(current):
	listvar=[]
	
	if isinstance(current, cl.Variable):
		if current.name!='undefined':
			listvar.append(current.name)
	
	elif not isinstance(current, (cl.Top, cl.Bot)) :
		for succ in current.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				if not (var  in listvar):
					listvar.append(var)
	return listvar


def getListVarForm():
	listvar=[]
	
	if isinstance(formula, cl.Variable):
		if formula.name!='undefined':
			listvar.append(formula.name)
	elif not isinstance(formula, (cl.Top,cl.Bot)):
		for succ in formula.succ:
			varsuc=getlistvarrec(succ)
			for var in varsuc:
				if not (var  in listvar):
					listvar.append(var)
	return listvar


def destroyMainWindowSons() :
	for enfant in window.winfo_children():
		if isinstance(enfant, ttk.Frame):
			enfant.destroy()


def createMainFrame() :

	
	window.title("TER 2020-2021 - Logique Intuitionniste - Menu principal")

	window.columnconfigure(0, weight = 1)
	window.rowconfigure(0, weight = 1)
	
	
	# DESTRUCTION DE L'ANCIENNE FENETRE

	destroyMainWindowSons()

	
	# CREATION DU CADRE DE LA FENETRE PRINCIPALE

	mainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))
	mainFrame.grid(column = 0, row = 0, sticky = (N, S, E, W))

	
	# TITRE DE LA FENÊTRE PRINCIPALE

	mainFrameTitle = ttk.Label(mainFrame, text = 'Logique Intuitionniste TER 2020-2021', style='Titre.TLabel')
	mainFrameTitle.grid(column = 0, row = 0, columnspan = 2, sticky =(E, W))


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	mainFrame.columnconfigure(0, weight = 1)
	mainFrame.rowconfigure(0, weight = 1)


def createToolbar() :
	  
  # BARRE DE MENU

  barreMenu = Menu(window)
  window['menu'] = barreMenu

  # MENU FICHIER DE LA BARRE DE MENU

  fichierMenu = Menu(barreMenu, tearoff = 0)
  fichierMenu.add_command(label = 'Créer une nouvelle formule', command = createFormulaFrame)
  fichierMenu.add_command(label = 'Ouvrir un modèle existant', command = None)
  fichierMenu.add_command(label = 'Enregistrer le modèle', command = None) 
  fichierMenu.add_command(label = 'Enregistrer le modèle sous...', command = None) 

  # AJOUT DU MENU FICHIER A LA BARRE DE MENU

  barreMenu.add_cascade(label = 'Fichier', menu = fichierMenu)


def createFormulaFrame() :


	class FormuleWrapper(TreeWrapper):
		def children(self,node):
			if not isinstance(node, (cl.Variable, cl.Top, cl.Bot)) :
				return [succ for succ in node.succ]
			else:
				return None

		def label(self, node):
			if node.name != 'undefined':
				return node.name
			elif node != cl.Node.classVar:
				return ''
			else:
				return None

		def onClick(self,node):
			global select
			select=node
			viewer.drawTree(formula)

		def bg(self, node):
			if node==select:
				return 'yellow2'
			return 'gray77'


	def replacerec(father,selected,elem):
		if not isinstance(father,(cl.Variable, cl.Top, cl.Bot)) :
			if selected in father.succ:
				father.succ=[elem if x==selected else x for x in father.succ]
				return True
			else:
				for succ in father.succ:
					if replacerec(succ,selected,elem):
						return True
				return False

		return False


	def replace(selected,elem):
		global select#temporary
		global formula#temporary
		if formula==selected:
			formula=elem#temporary
			select=elem#temorary
			return True
		else:
			if replacerec(formula,selected,elem):
				select=elem#temporary
				print(formula)
				return True
			else:
				return False
	

	def succDecide(select,newnode):
		if not (isinstance(select,(cl.Top,cl.Bot,cl.Variable)) or isinstance(newnode,(cl.Top,cl.Bot,cl.Variable))):
			index=[ x for x in range(len(select.succ)) if select.succ[x].name!= "undefined"]
            	
			if len(index)!=0:
				popup=Toplevel()
				popup.minsize(300,200)
				popup.maxsize(300,200)
				popup.grab_set()
				def conserver(indexold,indexnew):
					for x in range(len(indexold)):
						newnode.succ[indexnew[x]]=select.succ[indexold[x]]
					popup.grab_release()
					popup.destroy()
					popup.update()

				label = Label(popup,text="{select.name} a déjà "+len(index)+" fils assigné voulez vous en conservé pour nouveau {newnode.name}")
				label.grid(column=0,row=0, sticky=NSEW)
				if isinstance(newnode,cl.Not):
					if len(index)==1:
						conserver=Button(popup,command= conserver([index[0]],[0]))

						conserver.grid(row=2,column=0,sticky=NS)
						
						
					elif len(index)==2:
						conserver1=Button(popup,command= conserver([index[0]],[0]))
						conserver2=Button(popup,command= conserver([index[1]],[0]))

						conserver1.grid(row=2,column=0,sticky=NS)
						conserver2.grid(row=2,column=1,sticky=NS)
				else:
					if len(index)==1:
						conserverL=Button(popup,command= conserver([index[0]],[0]))
						conserverR=Button(popup,command= conserver([index[0]],[1]))

						conserverL.grid(row=2,column=0,sticky=NS)
						conserverR.grid(row=2,column=1,sticky=NS)
		
					
					elif len(index)==2:
						conserver1L=Button(popup,command= conserver([index[0]],[0]))
						conserver1R=Button(popup,command= conserver([index[0]],[1]))
						conserver2L=Button(popup,command= conserver([index[1]],[0]))
						conserver2R=Button(popup,command= conserver([index[1]],[1]))
						conserver=Button(popup,command= conserver(index,[0,1]))
						conserverRev=Button(popup,command= conserver(index,[1,0]))

						conserver1L.grid(row=2,column=0,sticky=NS)
						conserver1R.grid(row=2,column=1,sticky=NS)
						conserver2L.grid(row=2,column=2,sticky=NS)
						conserver2R.grid(row=2,column=3,sticky=NS)
						conserver.grid(row=2,column=4,sticky=NS)
						conserverRev.grid(row=2,column=5,sticky=NS)

						
					
				rien=Button(popup,command= conserver([],[]))
				rien.grid(column=0,row=3,sticky=NS)
						

	def changeEntryTextFromListbox(*args):
		if len(variableListbox.curselection()) > 0 :
			entryText = listVar[int(variableListbox.curselection()[0])]
			entryTextVar.set(entryText)


	def createVar(*args):
		if varnameEntry.get()!='':
			if varnameEntry.get()!= 'undefined':
				var = cl.Variable(varnameEntry.get().lower())
				if replace(select,var):

					viewer.drawTree(formula)

					if var.name in listVar:
						listVar.remove(var.name)
					listVar.insert(0,var.name)
					listVarVar.set(listVar)

					variableListbox.select_clear(0,"end")
					variableListbox.select_set(0)

					varnameEntry.delete(0, len(varnameEntry.get()))

					return messagebox.showinfo('message',f'Variable {var.name} crée')
				else:
					return messagebox.showinfo('ERROR:',f"La node selectionner n'a pas pu être trouvé")
			else:
				return messagebox.showinfo('message',f"undefined n'est pas un nom de variable valide")
		elif  len(variableListbox.curselection())==1:

			var=cl.Variable(listVar[variableListbox.curselection()[0]])
			if replace(select,var):
				viewer.drawTree(formula)

				listVar.remove(var.name)
				listVar.insert(0,var.name)
				listVarVar.set(listVar)

				variableListbox.select_clear(0,"end")
				variableListbox.select_set(0)

				varnameEntry.delete(0, len(varnameEntry.get()))

				return messagebox.showinfo('message',f'Variable {var.name} assignée.')

			else:
				return messagebox.showinfo('ERROR:',f"La node selectionner n'a pas pu être trouvé")
		else:
			return messagebox.showinfo('message',f'Sélectionnez une variable ou entrez en une nouvelle')


	window.title("TER 2020-2021 - Logique Intuitionniste - Éditeur de formule")


	# DESTRUCTION DE l'ANCIENNE FENETRE

	destroyMainWindowSons()


	# VARIABLES DE CONTROLE

	listVar = getListVarForm()
	
	listVarVar = StringVar(value = listVar)

	entryText = ""
	entryTextVar = StringVar(value = entryText)



	# CREATION DU CADRE DE LA PAGE CREER FORMULE

	formulaMainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))


	# CREATION DES ELEMENTS DU CADRE FORMULE

	formulaTitleFrame = ttk.Label(formulaMainFrame, text='Editeur de formule', style='Titre.TLabel')
	graphFrame = ttk.Frame(formulaMainFrame)
	toolBox = ttk.Notebook(formulaMainFrame)
	toolsFrame = ttk.Frame(toolBox)
	variableFrame =ttk.Frame(toolBox)
	varnameEntry = ttk.Entry(variableFrame, textvariable = entryTextVar)
	createVarButton = ttk.Button(variableFrame, text='Ajouter', command = createVar)
	variableListbox = Listbox(variableFrame, selectmode = 'browse', yscrollcommand = True, listvariable = listVarVar)


	# CREATION DES FRAMES DE REMPLISSAGE DES VIDES (si nécessaire)




	# PLACEMENT DU CADRE (FRAME) PRINCIPAL DANS LA FENETRE (window)

	formulaMainFrame.grid(column = 0, row = 0, sticky=(N, S, E, W))


	# PLACEMENT DES ELEMENTS DU CADRE FORMULE DANS LA GRILLE

	formulaTitleFrame.grid(column = 0, row = 0, columnspan = 2, sticky = (N, S, E, W))
	graphFrame.grid(column = 0, row = 1, sticky = (N, S, E, W), pady = 20, padx = (20, 0))

	toolBox.grid(column = 1, row = 1, sticky = (N, S, E, W), pady = 20, padx = 20)
	toolsFrame.pack(fill = 'both', expand = True)
	variableFrame.pack(fill = 'both', expand = True)
	toolBox.add(toolsFrame, text = 'Outils')
	toolBox.add(variableFrame, text = 'Variables')

	varnameEntry.grid(column = 0, row = 0, sticky = (N, S, E, W))
	createVarButton.grid(column = 1, row = 0, sticky = (N, S, E, W))
	variableListbox.grid(column = 0, row = 1, columnspan = 2, sticky = (N, S, E, W))


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	formulaMainFrame.columnconfigure(0, weight = 1)
	formulaMainFrame.rowconfigure(1, weight = 1)

	variableFrame.columnconfigure(0, weight = 1)
	variableFrame.rowconfigure(1, weight = 1)


	# PARTIE FONCTIONNELLE


	

	variableListbox.bind("<<ListboxSelect>>", changeEntryTextFromListbox)
	variableListbox.bind("<Double-1>", createVar)
	window.bind("<Return>", createVar)



	fwrap = FormuleWrapper()	
	viewer = TreeViewer(fwrap, graphFrame, formula)


def createModelFrame() :

	global formula
	global select
	global worlds

	class ModeleWrapper(TreeWrapper):
		def children(self,node):
			if len(self._sons)!=0:
				return self._sons
			else:
				return None

		def label(self, node):
			if node.name != 'undefined':
				return node.name
			else:
				return None

		def onClick(self,node):
			global select
			select=node
			viewer.drawTree(monde)

		def bg(self, node):
			if node==select:
				return 'yellow2'
			return 'gray77'



	# DESTRUCTION DE l'ANCIENNE FENETRE

	destroyMainWindowSons()


	# CREATION DU CADRE DE LA PAGE CREER FORMULE

	worldMainFrame = ttk.Frame(window, padding = (20, 2, 20, 0))


	# CREATION DES ELEMENTS DU CADRE FORMULE

	worldTitleFrame = ttk.Label(worldMainFrame, text='Editeur De Mondes', style='Titre.TLabel')
	graphFrame = ttk.Frame(worldMainFrame)
	toolBox = ttk.Notebook(worldMainFrame)
	toolsFrame = ttk.Frame(toolBox)
	variableFrame = ttk.Frame(toolBox)
	varnameEntry = ttk.Entry(variableFrame)
	createVarButton = ttk.Button(variableFrame, text='Créer', command = createVar)
	variableListbox = Listbox(variableFrame, selectmode = 'single', yscrollcommand = True)


	# CREATION DES FRAMES DE REMPLISSAGE DES VIDES




	# PLACEMENT DU CADRE (FRAME) PRINCIPAL DANS LA FENETRE (window)

	worldMainFrame.grid(column = 0, row = 0, sticky=(N, S, E, W))


	# PLACEMENT DES ELEMENTS DU CADRE FORMULE DANS LA GRILLE

	worldTitleFrame.grid(column = 0, row = 0, columnspan = 2, sticky = (N, S, E, W))
	graphFrame.grid(column = 0, row = 1, sticky = (N, S, E, W), pady = 20, padx = (20, 0))

	toolBox.grid(column = 1, row = 1, sticky = (N, S, E, W), pady = 20, padx = 20)
	toolsFrame.pack(fill = 'both', expand = True)
	variableFrame.pack(fill = 'both', expand = True)
	toolBox.add(toolsFrame, text = 'Outils')
	toolBox.add(variableFrame, text = 'Variables')

	


	# CONFIGURATION DES ELEMENTS DE LA GRILLE (changement de la taille de la fenêtre)

	worldMainFrame.columnconfigure(0, weight = 1)
	worldMainFrame.rowconfigure(1, weight = 1)


	# PARTIE FONCTIONNELLE

	listvar = getlistvar()

	

	fwrap=WorldWrapper()	
	viewer = TreeViewer(fwrap, graphFrame, world)



###############################################
		 # INITIALISATION FENÊTRE #	
###############################################

window = Tk()

window.minsize(720, 360)



createToolbar()

createMainFrame()


###############################################
				 # STYLE #
###############################################

style = ttk.Style()

style.theme_use('clam')

style.configure('AfficheModele.TFrame', background='white', borderwidth=15, relief='sunken')
style.configure('Titre.TLabel', font=('arial 20'), relief='groove', borderwidth=10, anchor='center')



window.mainloop()