# Делает Families file, принимает на вход папку с последовательностями, папку с маппингом и имя families файла
import sys
import os
from random import shuffle
folder = sys.argv[1]
folder_maps = sys.argv[2]
famfile = sys.argv[3]
fules = os.listdir(folder)
shuffle(fules)
num = 0
with open(famfile, "w") as handle:
    handle.write("[FAMILIES]\n")
    for i in fules:
        name = i.split(".")[0]
        handle.write(("- " + name + "\n"))
        file = "alignment = " + folder + "/" + i
        handle.write(file); handle.write("\n")
        handle.write("mapping = " + (folder_maps+"/"+name + '.txt') + "\n")
        handle.write("subst_model = GTR+G+I\n")
