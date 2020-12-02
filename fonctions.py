''' Définition des fonctions permettant la définition du problème à optimiser.
 Pour l'ensemble des fonctions :
        model_name = nom du fichier de simu .k
        model_path = chemin d'accès au fichier de simu .k
        simu_path = chemin d'accès au dossier de simu
        d3plot_path = chemin d'accès au fichier d3plot correspondant à la simu
 '''

import os
import subprocess
from qd.cae.dyna import *
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import NearestNeighbors

model_name = "MvtScapula.k"
simu_path = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1_test"
simu_path_comp = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1"
model_path = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1_test\MvtScapula.k"
d3plot_path = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1_test\d3plot"
d3plot_path_comp = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1\d3plot"
#IRM_path = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\points_IRM\points_IRM_recales"
#IRM_file = "coord_deltIRM1.txt"

def simulation (model_name,simu_path,ncpu=5, memory=200):
    ''' Lancement d'une simulation LS-DYNA.
    Entrée : ncpu et memory sont les param de calcul
    '''
    #solver_path = "D:\LSDYNA\program\ls-dyna_smp_s_R810_winx64_ifort131"    #laptop asus
    solver_path = "O:\Programs\LSTC\LS-DYNA\program\ls-dyna_smp_s_R810_winx64_ifort131" #serveur
    os.chdir(simu_path)
    subprocess.call([solver_path, "i=%s" % model_name, "ncpu=%d" % ncpu, "memory=%dm" %memory])
    return 0

def parametres_modif (param_mat,model_path,part_id=102):
    '''' Modification des valeurs des paramètres matériaux.
    Entrée :
        param_mat = les nouveaux paramètres à implémenter'''
    Keyword.field_alignment = Keyword.align.right   # mise en page fichier .k
    Keyword.name_alignment = Keyword.align.right
    kf = KeyFile(model_path, read_keywords=True, parse_mesh=False, load_includes=False) # Ouverture du fichier .k
    mat_keyword = kf["*MAT_MOONEY-RIVLIN_RUBBER"]
    for i in range (len(mat_keyword)):  # on parcours tous les mat mooney-rivlin
        kw = mat_keyword[i]
        if kw["mid"]==part_id:
            kw["ro"] = param_mat[0] # on met a jour la valeur des param
            kw["pr"] = param_mat[1]
            #kw["a"] = param_mat[2]
            #kw["b"] = param_mat[3]
    kf.save(model_path)
    return 0

def parametres_lecture (model_path, part_id=102):
    kf = KeyFile(model_path, read_keywords=True, parse_mesh=False, load_includes=False)  # Ouverture du fichier .k
    mat_keyword = kf["*MAT_MOONEY-RIVLIN_RUBBER"]
    for i in range(len(mat_keyword)):  # on parcours tous les mat mooney-rivlin
        kw = mat_keyword[i]
        if kw["mid"] == part_id:
            param_mat = [kw["ro"],kw["pr"]]
            print(kw)
    #return param_mat;
    return 0;

def extraction (d3plot_path, simu_path, part_id=102):
    ''' Récupère les coordonnées en fin de simu des points de la PART spécifié en argument.
    Entrée :
        part_id = identifiant de la part dont on veut les coordoonées. 107 = supra ; 102 = deltoide
    Sortie :
        coords_points_simu = numpy array de taille (nb de points,3)'''
    coords_points_simu = []
    os.chdir(simu_path)
    with open("coords_points_simu.txt", 'w') as fichier_coord:
        d3plot = D3plot(d3plot_path, read_states=["disp"])  # lecture fichier d3plot
        n = d3plot.get_nTimesteps()-1   # nb iterations
        part = d3plot.get_partByID(part_id) # choisi part
        node = part.get_nodes()  # recupere liste noeuds de la part
        for i in range (len(node)):
            tmp = node[i].get_coords()[n,:]
            coords_points_simu.append(tmp)# coord de la derniere iteration
            fichier_coord.write(str(tmp))
            fichier_coord.write("\n")
    return coords_points_simu

def lecture_IRM(IRM_file, IRM_path):
    ''' Enregistre les points de l'enveloppe de la position IRM dans un tableau.
    Entrée :
        IRM_file = nom du fichier texte contenant les coordonnées
        IRM_path = chemin d'accès au dossier contenant IRM_file
    Sortie :
        coords_points_IRM = numpy array de taille (nb de points,3)'''
    tmp = []
    os.chdir(IRM_path)
    with open(IRM_file, 'r') as fichier:    # calcul nb de points
        for line in fichier:
            tmp.append(line)
    coord_points_IRM = np.empty((len(tmp),3))
    with open(IRM_file, 'r') as fichier:
        for i in range(len(tmp)):           # on stocke les valeurs dans un tableau
            line = fichier.readline()
            line = line.split()
            coord_points_IRM[i][0] = float(line[0])
            coord_points_IRM[i][1] = float(line[1])
            coord_points_IRM[i][2] = float(line[2])
    return coord_points_IRM

def affichage3D (coord_points_simu, coords_points_IRM):
    x_simu, y_simu, z_simu = [],[],[]
    for i in range(len(coord_points_simu)):
        x_simu.append(coord_points_simu[i][0])
        y_simu.append(coord_points_simu[i][1])
        z_simu.append(coord_points_simu[i][2])
    x_IRM, y_IRM, z_IRM = [], [], []
    for i in range(len(coords_points_IRM)):
        x_IRM.append(coords_points_IRM[i][0])
        y_IRM.append(coords_points_IRM[i][1])
        z_IRM.append(coords_points_IRM[i][2])
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_simu,y_simu,z_simu, c='red', label='Points simu')
    ax.scatter(x_IRM,y_IRM,z_IRM, c='green', label='Points IRM')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    for i in range (0,181,40):
        ax.view_init(elev=10, azim=i)
        plt.title('supra jobMRI1, azim=%d, elev=10'%i)
        fig.savefig('E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Devel_PyCharm\Figures\Test_rot%d_elev10.png'%i)
    return 0;


def distance (points_simu, points_IRM):
    voisins = NearestNeighbors(5).fit(points_IRM)
    dist = voisins.kneighbors(points_simu)[0]
    return dist;

def eloignement(param_mat):
    parametres_modif(param_mat,model_path)
    simulation(model_name,simu_path)
    points_simu = extraction(d3plot_path, simu_path)
    #points_IRM = lecture_IRM(IRM_file, IRM_path)
    points_test = extraction(d3plot_path_comp,simu_path_comp)
    dist = distance(points_simu, points_test)
    moy_dist = np.mean(dist)
    return moy_dist;
