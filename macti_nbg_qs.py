#
# Author: Luis Miguel de la Cruz Salas
# Last update: Tue Jan  9 08:00:08 PM UTC 2024
#
import os, sys, shutil
from colorama import Fore, Back, Style
import pandas as pd

def print_macti_info(msg):
    print(Fore.GREEN + '[MACTI | INFO] ' + Style.RESET_ALL, end = '')
    print(Back.WHITE + ' --> ' + msg + Style.RESET_ALL, end='\n')

def init_course_nbgrader(c_name, home, path_c_name_nbg):
    """
    Inicializa el directorio con NBGRADER y modifica la ruta 
    c.CourseDirectory.root dentro del archivo nbgrader_config.py 
    de acuerdo con la ruta del directorio del curso.
    """
    print_macti_info('Inicializando el directorio para NBGRADER ')

    # Primero se crea el directorio nbg
    os.makedirs(path_c_name_nbg, exist_ok=True)
    
    nbgrader_qs = 'nbgrader quickstart ' + path_c_name_nbg
    print('nbgrader quickstart ' + Fore.GREEN + path_c_name_nbg + Style.RESET_ALL)

    # Inicializamos el curso para NBGRADER 
    os.system(nbgrader_qs)

    # Construimos un nuevo nbgrader_config.py 
    lines = []
    lines.append("c = get_config() \n\n")
    lines.append("#"*40 + "\n")
    lines.append("# MACTI: nbgrader_config.py \n")
    lines.append("#"*40 + "\n")
    lines.append('c.CourseDirectory.course_id = "'+ c_name +'" \n')
    lines.append('c.IncludeHeaderFooter.header = "source/header.ipynb" \n')
    lines.append('c.Exchange.root = "/usr/local/share/nbgrader/exchange" \n')
    lines.append('c.CourseDirectory.root = "' + path_c_name_nbg + '" \n')

    # Escribimos el archivo
    print('HELLO ', path_c_name_nbg)
    with open(path_c_name_nbg + "/nbgrader_config.py", "w") as f:
        f.writelines(lines)

    print_macti_info('Copiando el archivo ' + Style.BRIGHT + 'nbgrader_config.py ' + Style.NORMAL + 'a' + Style.BRIGHT + ' {} '.format(home + '.jupyter/  '))
    
    # Copiamos el archivio nbgrader_config.py al $HOME/.jupyter/
    shutil.copy2(path_c_name_nbg + "/nbgrader_config.py", home + '.jupyter/')

    # Eliminar o mantener el ejemplo ps1 creado por NBGRADER.
    eliminar = input('\n El siguiente subdirectorio contiene un ejemplo de uso de NBGRADER: \n' + Style.BRIGHT + ' {}/source/ps1/ '.format(path_c_name_nbg) + Style.RESET_ALL + '\n ¿deseas eliminarlo? Si [S], No [N] ' + Style.RESET_ALL)
    print()
    
    if eliminar in ['S','s']:
        print_macti_info('Eliminando ' + Style.BRIGHT + '{}/source/ps1/'.format(path_c_name_nbg) + Style.NORMAL + ' ...  ')
        shutil.rmtree(path_c_name_nbg +'/source/ps1/')
    else:
        print_macti_info(' El subdirectorio ' + Style.BRIGHT + '{}/source/ps1/'.format(path_c_name_nbg) + Style.NORMAL + ' NO se eliminó  ')
    print()

#-------- DEFINICION DE ALGUNAS RUTAS --------
# Este script se debe ejecutar desde donde está el directorio
# del curso original de donde se van a copiar los notebooks de quizzes

os.system('clear')

line_len = 40
print()
print(Fore.WHITE + Back.GREEN + line_len*'-')
print(Fore.WHITE + Back.GREEN + '   MACTI: Configuración con ' + Style.BRIGHT + 'NBGRADER    ' + Style.RESET_ALL)
print(Fore.WHITE + Back.GREEN +  line_len*'-')
print(Style.RESET_ALL)

# Path del home
home = os.environ['HOME'] + '/'

# Path desde donde se ejecuta el script
path_c_name = os.getcwd()

# Nombre del curso original
c_name = path_c_name.split('/')[-1]

print_macti_info(' Curso: {}'.format(c_name))

# Verificamos que existe el directorio del curso
print_macti_info(' Directorio actual: ' + Style.BRIGHT + '{}  '.format(path_c_name))
    
# Subirectorio dentro del curso para configuración con NBGRADER
c_name_nbg = '/nbg/' + c_name

# Path absoluto al directorio nbg
path_c_name_nbg = path_c_name + c_name_nbg

#-------- INICIALIZACIÓN DEL DIRECTORIO CON NBGRADER --------

if 'nbg' not in os.listdir(path_c_name):
    # El directorio NO existe, se crea usando nbgrader quickstart ...
    continuar = input('\n Se configurará el siguiente directorio con NBGRADER: \n' + Style.BRIGHT + ' {} '.format(path_c_name_nbg) + Style.RESET_ALL + '\n ¿continuar? Si [S], No [N] ' + Style.RESET_ALL)
    
    if continuar in ['S','s']:
        print()
        # Se inicializa el directorio con NBGRADER
        init_course_nbgrader(c_name, home, path_c_name_nbg)
    else:
        sys.exit(Fore.WHITE + Back.RED + '\n Termina el proceso anticipandamente.' + Style.RESET_ALL)

    file_c = 'assignments_creation.csv'
    # Lista de temas para el curso
    topic_list = pd.read_csv(file_c)
    
else:
    file_u = 'assignments_update.csv'
    # El directorio YA existe, solo se copiarán los notebooks de los quizzes
    print(Fore.RED + '\n El directorio ' + 
          Fore.BLACK + Style.BRIGHT + '{}'.format(path_c_name_nbg) + 
          Fore.RED + Style.NORMAL + ' ya se había inicializado previamente.\n' +
          ' Se actualizarán los archivos usando la información de' + 
          Fore.BLACK + Style.BRIGHT + ' {}'.format(file_u) + 
          Style.RESET_ALL + '\n')
    
    # Lista de temas para el curso
    topic_list = pd.read_csv(file_u)

#-------- SE MUESTRAN LOS ARCHIVOS QUE SE VAN A COPIAR --------

print_macti_info('Los siguientes archivos se van a copiar del directorio ' + Style.BRIGHT + '{}'.format(path_c_name))
print_macti_info('al directorio ' + Style.BRIGHT + '{}  '.format(path_c_name_nbg))
print_macti_info('Lista de archivos: ')
print()

for topic in topic_list:
    print(' > ' + Fore.WHITE + Back.GREEN + '  ' + topic + '  ' + Style.RESET_ALL)
    for a in topic_list[topic]:
        print('  -', a)

#-------- SE PREGUNTA SI TODO ESTÁ CORRECTO PARA CONTINUAR --------
seguro = input("\n ¿Continuar? Si [S], No [N] ")
print()

if seguro in ['S', 's']:
    pass
else:
    print()
    sys.exit(Fore.WHITE + Back.RED + ' Termina el proceso anticipandamente.' + Style.RESET_ALL)

#-------- SE COMIENZA LA COPIA DE ARCHIVOS --------

print_macti_info('Copia de' + Style.BRIGHT + ' {} '.format(c_name) + Style.NORMAL + 'a' + Style.BRIGHT + ' {} '.format(c_name_nbg))
print()

# Se recorren los topicos/temas (que son las columnas del DataFrame topic_list)
for topic in topic_list:
    # Se construye el nombre en el directorio source. Se usa la ruta absoluta
    p = path_c_name_nbg + '/source/' + topic
    if os.path.exists(p): 
        print_macti_info('Subdirectorio ' + Style.BRIGHT + '{}'.format(p) + Style.NORMAL + ' YA existe  ')
    else:
        print_macti_info('Subdirectorio ' + Style.BRIGHT + '{}'.format(p) + Style.NORMAL + ' NO existe  ')

        print_macti_info('Creando el directorio :' + Style.BRIGHT + ' {}  '.format(p))
        os.makedirs(p, exist_ok=True)        
    print()
    
    # Por cada topico se determina la lista de notebooks (quizzes) a copiar
    for a in topic_list[topic]:
        if not isinstance(a, float): # Es necesario por si hay nan
            src = path_c_name + '/' + topic + '/' + a
            dst = path_c_name_nbg + '/source/' + topic
            print(' Archivo : {}'.format(a))
            print('  Fuente : {}'.format(path_c_name + '/' + topic + '/') )
            print(' Destino : {}\n'.format(dst))

            # Se copian los archivos
            shutil.copy2(src, dst)

    # Se copian los archivos de respuestas y de retroalimentación
    path_ans_src = path_c_name + '/.ans/' + topic

    # Leemos el path del directorio exchange
    with open('.nbgex', 'r') as f:
        path_nbgex = f.readline()[:-1]
            
    path_ans_dst = path_nbgex + c_name + '/.ans/' + topic
        
    print_macti_info('Copiando respuestas y retroalimentación a:')
    print_macti_info(Style.BRIGHT + '  {}  '.format(path_ans_dst))

    # Realizamos la copia, siempre y cuando exista el archivo fuente
    try:
        shutil.copytree(path_ans_src, path_ans_dst, dirs_exist_ok=True)
    except FileNotFoundError:
        print_macti_info(Fore.RED + 'Archivo fuente' + Fore.RESET + Style.BRIGHT + ' {}'.format(path_ans_src))
        print_macti_info(Fore.RED + '  No existe. No se hizo la copia.' + Style.RESET_ALL)
    else:
        print()

print()
print_macti_info(Style.BRIGHT + '¡Procesamiento exitoso con NBGRADER!' + Style.RESET_ALL)

    