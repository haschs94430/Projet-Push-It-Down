from upemtk import *
from time import*
from random import*
import copy

"""
Cette fonction calcule les coordonnées, en pixels, du coin le plus bas 
d'un bloc représenté par le triplet (i, j, k), où i est le numéro de 
ligne et j le numéro de colonne de la case sur laquelle est posé le bloc, 
et k est sa hauteur. Elle reçoit également les dimensions lb et hb d'un 
bloc."""

def coin_bas(i, j, k, lb, hb):

	x = 300 + (j-i) * lb
	y = 300 + (j+i) * lb//2 - (k-1) * hb + lb
	return x, y

"""
Cette fonction affiche le bloc de coordonnées (i, j, k) conformément au 
schéma donné dans le sujet. Elle reçoit également les dimensions lb et hb 
d'un bloc, la taille n du plateau ainsi qu'un paramètre optionnel c 
indiquant la couleur de la face supérieure du bloc. """
def affiche_bloc(i, j, k, lb, hb, c="white"):

	x, y = coin_bas(i, j, k, lb, hb)
	xg, xd, ymb = x - lb, x + lb, y - lb//2
	ybh, ymh, yhh = y - hb, y - lb//2 - hb, y - lb - hb
	face_haut = [(x, ybh), (xd, ymh), (x,  yhh), (xg, ymh)]
	polygone(face_haut, remplissage=c, epaisseur=2)

	if k > 0:
		face_gauche = [(x, y),   (xg, ymb), (xg, ymh), (x,  ybh)]
		face_droite = [(x, y),   (xd, ymb), (xd, ymh), (x,  ybh)]
		polygone(face_gauche, remplissage='grey')
		polygone(face_droite, remplissage='lightgrey')
		
"""
Cette fonction affiche la bille aux coordonnées (i, j, k). Elle reçoit 
également les dimensions lb et hb d'un bloc ainsi que la taille n du 
plateau. """


def affiche_bille(i, j, k, lb, hb, n, tag):

	x, y = coin_bas(i, j, k, lb, hb)
	cercle(x, y - 2*lb//3, lb//3, couleur="red", remplissage="red",tag=tag)
	ligne(x, y - 2*lb//3, x, 20, couleur='red',tag=tag)
	x, y = coin_bas(n-1, j-0.5, 1, lb, hb)
	fleche(x - 20, y + 20, x - 10, y + 10,couleur="red", epaisseur=3,tag=tag)
	x, y = coin_bas(i-0.5, n-1, 1, lb, hb)
	fleche(x + 20, y + 20, x + 10, y + 10,couleur="red", epaisseur=3,tag=tag)
 
#Début de notre code:          
           
def extraire_map (File):
	Map=[]
	fichier=open(File)
	for ligne in fichier:
		liste2=[]
		for charactère in ligne.split():
			chiffre=int(charactère)
			liste2.append(chiffre)
		Map.append(liste2)
	fichier.close()
	return(Map)


def afficher_plateau(Map, x_bille, y_bille,tag):
	efface_tout()
	nb_cube=len(Map)
	Max=0
	for l in Map:
		Max=max(Max,max(l))
	lb=280/nb_cube
	hb=min(1.5*lb,230/(Max+1))
	for i in range(nb_cube):
		for j in range(nb_cube) :
			for hauteur in range(Map[i][j]+1):
				affiche_bloc(i, j, hauteur, lb, hb, c="white")
				affiche_bloc(nb_cube-1, nb_cube-1, Map[nb_cube-1][nb_cube-1], lb, hb, c="green")			
			if i==x_bille and j==y_bille :
				affiche_bille(x_bille, y_bille, Map[x_bille][y_bille]+1, lb, hb, nb_cube,tag=tag)
				
def deplacer_bille(Map,nom_touche,x_bille,y_bille):
	if nom_touche == "Right" and (y_bille>=0) and (y_bille<len(Map)-1):
		if Map[x_bille][y_bille]>= Map[x_bille][y_bille+1]:
			y_bille+=1
		elif y_bille+2 < len(Map) and (Map[x_bille][y_bille+1]) > (Map[x_bille][y_bille+2]):
			if (Map[x_bille][y_bille])+1 == (Map[x_bille][y_bille+1]):
				(Map[x_bille][y_bille+1]) = (Map[x_bille][y_bille+1])-1
				(Map[x_bille][y_bille+2]) = (Map[x_bille][y_bille+2])+1
				y_bille+=1		

	elif nom_touche == "Left" and (y_bille>0) and (y_bille<len(Map)) :
		if Map[x_bille][y_bille] >= Map[x_bille][y_bille-1]:
			y_bille-=1
		elif y_bille-2>=0 and (Map[x_bille][y_bille-1]) > (Map[x_bille][y_bille-2]):
			if (Map[x_bille][y_bille])+1 == (Map[x_bille][y_bille-1]):
				(Map[x_bille][y_bille-1]) = (Map[x_bille][y_bille-1])-1
				(Map[x_bille][y_bille-2]) = (Map[x_bille][y_bille-2])+1
				y_bille-=1			
		
	elif nom_touche == "Up" and (x_bille>0) and (x_bille<len(Map)) :
		if Map[x_bille][y_bille] >= Map[x_bille-1][y_bille]:
			x_bille-=1
		elif  x_bille-2>=0 and (Map[x_bille-1][y_bille]) > (Map[x_bille-2][y_bille]) :
			if (Map[x_bille][y_bille])+1 == (Map[x_bille-1][y_bille]):
				(Map[x_bille-1][y_bille]) = (Map[x_bille-1][y_bille])-1
				(Map[x_bille-2][y_bille]) = (Map[x_bille-2][y_bille])+1
				x_bille-=1

	elif nom_touche == "Down" and (x_bille>=0) and (x_bille<len(Map)-1):
		if Map[x_bille][y_bille] >= Map[x_bille+1][y_bille]:
			x_bille+=1
		elif x_bille+2 < len(Map) and (Map[x_bille+1][y_bille]) > (Map[x_bille+2][y_bille]):
			if (Map[x_bille][y_bille])+1 == (Map[x_bille+1][y_bille]):
				(Map[x_bille+1][y_bille]) = (Map[x_bille+1][y_bille])-1
				(Map[x_bille+2][y_bille]) = (Map[x_bille+2][y_bille])+1
				x_bille+=1
				
	
	return (x_bille,y_bille,Map)

		
def commandes(nom_touche,x_bille, y_bille,Map,historique,tag):		
	if nom_touche == "q":
		quit()
		
	elif nom_touche == "r":
		ferme_fenetre()
		game()
		historique=[]
		
	elif nom_touche == "n":
		if x==6:
			Map=extraire_map("map6.txt")
		else	
			x+=1
			Map=extraire_map("map"+str(x)+".txt")
	elif nom_touche == "p":
		if x==1:
			Map=extraire_map("map1.txt")
		else	
			x-=1
			Map=extraire_map("map"+str(x)+".txt")
			
	elif nom_touche == "a":
		if len(historique)==0:
			ferme_fenetre()
			game()
			historique=[]
	elif nom_touche=="g":
		while Solveur(extraire_map("map6.txt"),x_bille,y_bille,liste_C)!=True:
			generateur()
			Solveur(extraire_map("map6.txt"),x_bille,y_bille,liste_C)

		else:
			efface(tag)
			(Map,x_bille,y_bille)=historique.pop()
			
	else:
		efface(tag)
		(x_bille,y_bille,Map)=deplacer_bille(Map,nom_touche,x_bille,y_bille)
		historique.append((copy.deepcopy(Map),x_bille,y_bille))
	return(x_bille,y_bille,Map)
	

def win(x_bille,y_bille,Map):
	return(x_bille==len(Map)-1 and y_bille==len(Map)-1)
		
def touche_ou_pas():
	"""
	Cette fonction provient du programme 'baby_snake' fait en TP
	et renvoie la touche pressée par le joueur
	"""
	evenement = donne_evenement()
	type_ev = type_evenement(evenement)
	if type_ev == 'Touche':
		return touche(evenement)
	else: 
		return 'pas_touche'

def generateur():
	Map=[]
	x=0
	while x < 5:
		L=[]
		y=0
		while y < 5:
			z=randint(0,3)
			L.append(str(z))
			y+=1
		l=" ".join(L)
		Map.append(l)
		x+=1
	" ".join(Map)
	with open("map6.txt", "r") as fstab:
		fstab_str = ''.join(fstab.readlines()[:-5])

	with open("map6.txt", "w") as fstab:
		for ligne in Map:
			fstab.write(ligne)
			fstab.write("\n")
		
def Solveur(Map,x_bille,y_bille,liste_C):
	c=(x_bille,y_bille,Map)
	if win(x_bille,y_bille,Map):
		return True
	elif c not in liste_C:
		liste_C.append(c)
		for nom_touche in ["Down","Right","Left","Up"]:
			Map2=copy.deepcopy(Map)
			(x_test,y_test,Map2) = deplacer_bille(Map2,nom_touche,x_bille,y_bille)
			print((x_bille,y_bille,Map))		
			if Solveur(Map,x_test,y_test,liste_C):
				return True
		return False
	else:
		return False

def game():
	cree_fenetre(600, 600)
	x=1
	Map=extraire_map("map"+str(x)+".txt")
	tag="player"
	x_bille=0
	y_bille=0
	nb_cube=len(Map)
	Max=0
	historique=[]
	liste_C=[]
	for l in Map:
		Max=max(Max,max(l))
	lb=280/nb_cube
	hb=min(1.5*lb,230/(Max+1))
	afficher_plateau(Map, x_bille, y_bille,tag)
	while True:
		nom_touche=attente_touche()
		(x_bille,y_bille,Map)=commandes(nom_touche,x_bille, y_bille,Map,historique,tag)
		afficher_plateau(Map, x_bille, y_bille,tag)
		if win(x_bille,y_bille,Map):
			texte(125,70,"Vous avez gagné !",couleur="red")
	attente_clic()			

	
game()





