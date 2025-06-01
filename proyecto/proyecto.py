
from colorama import Fore, Style

def obtener_datos_entrada():
    IDs = input("ID. pacientes (separados por coma): ").split(',')

    # Convertir entrada a enteros
    for i, v in enumerate(IDs):
        IDs[i] = int(IDs[i])

    # Regresa una lista ordenada y sin repeticiones, de los ID
    return list(set(IDs))
    
def desplegar_pantalla_inicio():
    lineac = 50 * chr(0x2015)
    
    print(lineac)
    print("Sistema XYZ".center(50))
    print(lineac)

    # Se leen los datos de la pantalla
    IDs = obtener_datos_entrada()
    
    print(lineac)
    
    return IDs
    
def calcular_nivel_IMC(imc):
    if 18.5 > imc:
        nivel = 'N1'
    elif 18.5 <= imc and imc < 25.0:
        nivel = 'N2'
    elif 25.0 <= imc and imc < 30.0:
        nivel = 'N3'
    elif 30.0 <= imc:
        nivel = 'N4'
    return nivel

def transformar_datos(r, e):
    # Diccionario vacío para almancenar la información
    dicc = {}

    # Recorremos el renglón y extraemos el key y el value
    for k, v in zip(e, r.split(',')):
        dicc[k] = v # Agregamos la info al diccionario

    # Corregimos la entrada 'TA' (para quitarle el cambio de línea)
    dicc['TA'] = v[:-1]

    # Regresamos el diccionario con la información
    return dicc
    
def desplegar_datos(d):
    # Diccionario para los textos
    dicc_e = dict(Pa = "Paciente", 
                  S = "Sexo",
                  E = "Edad",
                  Pe = "Peso",
                  A = "Estatura",
                  IMC = "IMC",
                  Di = "Diabetes",
                  H = "Hipertensión",
                  De = "Depresión",
                  TS = "Trastorno del sueño",
                  TA = "Trastorno de la alimentación"
                 )

    # Recorremos el diccionario con la información
    for k, v in d.items():
        # Checamos el IMC
        v_imc = ''
        if k == 'IMC':
            v_imc = calcular_nivel_IMC(float(v))

        # Checamos si hay alguna alerta de salud
        if v == 'Si' or v_imc == 'N4':            
            print(Fore.RED + Style.BRIGHT + \
                  "{:>30s} : {:^5s}".format(dicc_e[k], str(v)) + \
                  Style.RESET_ALL)
        else:
            print("{:>30s} : {:^5s}".format(dicc_e[k], str(v)))

def abrir_archivo(nombre = "../archivos/personal_data.csv"):
    f = open(nombre)

    # Extraemos encabezado en forma de lista
    e = f.readline().split(',')

    # Eliminamos el '\n' (el último caracter) del último elemento
    e[-1] = e[-1][:-1]

    # Regresamos el descriptor del archivo y el encabezado
    return f, e

def cerrar_archivo(file_descriptor):
    file_descriptor.close()
    
def leer_archivo(IDs):
    lineac = 50 * chr(0x2015)

    # Abrimos el archivo y obtenemos el encabezado
    f, encabezado = abrir_archivo()

    # Construimos una lista vacía para almacenar 
    # la información de los IDs solicitados
    IDs_lista = []

    # Recorremos todo el archivo
    for i, r in enumerate(f, start=1):

        # Checamos si el id está en la lista de los solicitados
        if i in IDs:

            # En caso de que si sea uno de los solicitados
            # vaciamos la información en un diccionario
            dicc = transformar_datos(r, encabezado)
        
            # Presentamos la información en la pantalla
            # con el formato requerido
            desplegar_datos(dicc)

            print(lineac)

    # Cerramos el archivo
    cerrar_archivo(f)

def ejecutar():
    leer_archivo(desplegar_pantalla_inicio())

if __name__ == '__main__':
    ejecutar()