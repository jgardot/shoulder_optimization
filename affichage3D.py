from fonctions import extraction,lecture_IRM
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

d3plot1 = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1\d3plot"
d3plot2 = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1_test\d3plot"
d3plot7 = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide4\d3plot"
simu_path1 = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1"
simu_path2 = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide1_test"
simu_path7 = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Simulation\essai3\Deltoide7"

IRM_path = "E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\points_IRM\points_IRM_recales"
IRM_file1 = "coord_deltIRM1.txt"
IRM_file4 = "coord_deltIRM4.txt"
IRM_file7 = "coord_deltIRM7.txt"

muscle1 = extraction(d3plot1,simu_path1,part_id=102)
x_1, y_1, z_1 = [],[],[]
for i in range(len(muscle1)):
    x_1.append(muscle1[i][0])
    y_1.append(muscle1[i][1])
    z_1.append(muscle1[i][2])
tendon1 = extraction(d3plot1,simu_path1,part_id=120)
xx_1, yy_1, zz_1 = [],[],[]
for i in range(len(tendon1)):
    xx_1.append(tendon1[i][0])
    yy_1.append(tendon1[i][1])
    zz_1.append(tendon1[i][2])

muscle2 = extraction(d3plot2,simu_path2)
x_2, y_2, z_2 = [],[],[]
for i in range(len(muscle2)):
    x_2.append(muscle2[i][0])
    y_2.append(muscle2[i][1])
    z_2.append(muscle2[i][2])
tendon4 = extraction(d3plot2,simu_path2,part_id=120)
xx_4, yy_4, zz_4 = [],[],[]
for i in range(len(tendon4)):
    xx_4.append(tendon4[i][0])
    yy_4.append(tendon4[i][1])
    zz_4.append(tendon4[i][2])

muscle7 = extraction(d3plot7,simu_path7,part_id=102)
x_7, y_7, z_7 = [],[],[]
for i in range(len(muscle7)):
    x_7.append(muscle7[i][0])
    y_7.append(muscle7[i][1])
    z_7.append(muscle7[i][2])
tendon7 = extraction(d3plot7,simu_path7,part_id=120)
xx_7, yy_7, zz_7 = [],[],[]
for i in range(len(tendon7)):
    xx_7.append(tendon7[i][0])
    yy_7.append(tendon7[i][1])
    zz_7.append(tendon7[i][2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_1,y_1,z_1, c='red', label='Points simu cible',marker='x')
#ax.scatter(xx_1,yy_1,zz_1, c='orange', label='Tendon 1')
ax.scatter(x_2,y_2,z_2, c='g', label='Points simu optimisation')
#ax.scatter(xx_4,yy_4,zz_4, c='brown', label='Tendon 4')
#ax.scatter(x_7,y_7,z_7, c='g', label='Muscle 7')
#ax.scatter(xx_7,yy_7,zz_7, c='y', label='Tendon 7')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
for i in range (0,181,40):
    ax.view_init(elev=90, azim=i)
    plt.title('Deltoide position 1')
    fig.savefig('E:\Projet_ModeleCoiffeDeformable\Projet_Optimisation\Resultats\Figures\Deltoide\Delt_DeltTest1_rot%d_elev90.png' %i)