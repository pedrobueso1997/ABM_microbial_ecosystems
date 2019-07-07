#MODELO COMPETICION INHIBICION

##############################################################################
  
#Importamos las funciones que vayamos a utilizar
#Estas son necesarias para definir los valores de determinados atributos y realizar determinados calculos
from random import randint,random
from numpy import zeros 
#Esta es necesaria para copiar elementos
from copy import copy
#Este paquete es necesario para representar los resultados graficamente
import matplotlib.pyplot
import matplotlib.colors
matplotlib.pyplot.switch_backend('agg')
#Este paquete es necesario para generar carpetas y mover los archivos obtenidos a las mismas
import os

##############################################################################

#Definimos los valores de parametros necesarios para caracterizar el modelo
#Vamos a suponer que existen dos especies que compiten por un recurso

#PARAMETROS GENERALES DEL ECOSISTEMA
#Numero de agentes incluidos inicialmente en el modelo
number_agents=200
#Capacidad de carga del modelo (se considera respecto del total de agentes, no respecto de cada especie)
carrying_capacity=number_agents*4
#Numero de filas/columnas en el array espacial (que discretiza el espacio)
rows_columns=100

#PARAMETROS CONSTANTES DE LA ESPECIE 1
#Tasa de reproduccion de la especie 1
species_1_reproduction_rate=0.05
#Tasa de muerte de la especie 1
species_1_death_rate=0.04

#PARAMETROS CONSTANTES DE LA ESPECIE 2
#Tasa de reproduccion de la especie 2
species_2_reproduction_rate=0.05
#Tasa de muerte de la especie 2
species_2_death_rate=0.04

#PARAMETROS VARIABLES
#Porcentaje de individuos incluidos inicialmente en el modelo
percentage=[[0.1,0.9],[0.2,0.8],[0.3,0.7],[0.4,0.6],[0.5,0.5]]
#Velocidad movimiento
movement=[[1,1],[1,2],[2,1]]
#Tasa de secrecion de la sustancia inhibidora
secretion_rate=[[0.1,0.1],[0.1,0.2],[0.2,0.1]]

##############################################################################

#Definimos una clase vacia, sin atributos ni metodos
#Las instancias de esta clase seran denominadas agentes
class agent:
    pass

##############################################################################
     
#Generamos una funcion que permite obtener una lista de agentes y asigna atributos a los mismos
def initialize():
    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, env, inhibitory_1, inhibitory_2, species_1_number, species_2_number, total_number
    agents=[]; species_1_number=[]; species_2_number=[]; total_number=[] 
    #Iteramos sobre el numero de agentes definidos
    for i in range (number_agents):
        #Generamos una instancia de la clase agent
        ag=agent()
        #El primer atributo se refiere al tipo de agente
        #Como existen dos tipos de agente, los podemos representar como 1 (especie 1) y 2 (especie 2)
        ag.type=1 if i<species_1_percentage*number_agents else 2
        #El segundo y tercer atributo se refieren a la ubicacion
        #Planteamos que se encuentran en una posicion aleatoria del cuadrado definido por el numero de filas/columnas
        ag.x=randint(0,rows_columns-1)
        ag.y=randint(0,rows_columns-1) 
        #El cuarto atributo se refiere al tipo de movimiento
        ag.movement=species_1_movement if i<species_1_percentage*number_agents else species_2_movement
        #El quinto atributo se refiere a la tasas de reproduccion
        ag.reproduction_rate=species_1_reproduction_rate if i<species_1_percentage*number_agents else species_2_reproduction_rate
        #El sexto atributo se refiere a la tasa de muerte
        ag.death_rate=species_1_death_rate if i<species_1_percentage*number_agents else species_2_death_rate
        #El septimo atributo se refiere a la tasa de secrecion de la sustancia inhibidora
        ag.secretion_rate=species_1_secretion_rate if i<species_1_percentage*number_agents else species_2_secretion_rate             
        #AÃ±adimos la instancia creada a la lista
        agents.append(ag)  
    #Generamos arrays para las sustancias inhibitorias
    inhibitory_1=zeros([rows_columns,rows_columns])
    inhibitory_2=zeros([rows_columns,rows_columns])
        
##############################################################################

#Generamos una funcion que permite visualizar los resultados
def observe():
    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, inhibitory_1, inhibitory_2  
    #Limpiamos para poder adecuarla a los resultado que se van a obtener en el momento actual
    matplotlib.pyplot.cla()
    #Definimos los ejes, buscando que se mantenga la proporcionalidad entre X e Y, entre 0 y 1   
    matplotlib.pyplot.axis("image")
    matplotlib.pyplot.axis([0,rows_columns-1,0,rows_columns-1]) 
    #Definimos dos listas separadas para la especie 1 y la especie 2
    species_1=[ag for ag in agents if ag.type==1]
    species_2=[ag for ag in agents if ag.type==2]
    #Dibujamos en la grafica la cÃ©luas de la especie 1 (en azul) y de la especie 2 (en rojo)
    #En la funcion plot() el primer argumento indica el componente x, el segundo argumento el componente y, el tercer argumento el tipo de simbolo
    if len(species_1)>0:
        matplotlib.pyplot.plot([ag.x for ag in species_1],[ag.y for ag in species_1],"bo")
    if len(species_2)>0:
        matplotlib.pyplot.plot([ag.x for ag in species_2],[ag.y for ag in species_2],"ro")
    #Dibujamos en la grafica los alimentos y las sustancias inhibitorias
    #En la funcion imshow() el primer argumento indica el array con la informacion de concentracion por localizacion, el segundo argumento indica la escala de color, el tercer y cuarto argumento indican los valores maximos y mi­nimos para ajustar la escala de color
    color0 = matplotlib.colors.colorConverter.to_rgba('white')
    color1 = matplotlib.colors.colorConverter.to_rgba('cyan')
    color2 = matplotlib.colors.colorConverter.to_rgba('orangered')
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap1',[color0,color1],256)
    cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap2',[color0,color2],256)
    matplotlib.pyplot.imshow(inhibitory_1,cmap=cmap1,vmin=0,vmax=10,alpha=1)
    matplotlib.pyplot.imshow(inhibitory_2,cmap=cmap2,vmin=0,vmax=10,alpha=0.6)
      
##############################################################################

#Generamos una funcion que contempla la dinamica de los agentes
def update():
    
    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, inhibitory_1, inhibitory_2
    #Si ya no existen agentes, se sale de la funcion
    if agents==[]:
        return
          
    #SELECCION Y CARACTERIZACION DE UN AGENTE
    #Seleccionamos un agente aleatorio
    ag=agents[randint(0,len(agents)-1)]
    species=ag.type
    movement=ag.movement
    reproduction_rate=ag.reproduction_rate
    death_rate=ag.death_rate
    secretion_rate=ag.secretion_rate
      
    #MOVIMIENTO 
    #En este caso no consideramos que el espacio es abierto como en modelos anteriores sino que existen li­mites
    if movement>0:
        ag.x+=randint(-movement,movement)
        ag.y+=randint(-movement,movement)      
    ag.x=rows_columns-1 if ag.x>rows_columns-1 else 0 if ag.x<0 else ag.x
    ag.y=rows_columns-1 if ag.y>rows_columns-1 else 0 if ag.y<0 else ag.y
    
    #SECRECION DE LAS SUSTANCIAS INHIBIDORAS
    if random()<secretion_rate:
        if species==1:
            inhibitory_1[ag.y,ag.x]+=1
        elif species==2:
            inhibitory_2[ag.y,ag.x]+=1       
    
    #CONSUMO DE LAS SUSTANCIAS INHIBIDORAS
    #Ponemos valor a la variable consume_inhibidor_2
    #Solo la especie 1 puede consumir la sustancia inhibidora 2
    if species==1:
        consume_inhibidor_1=False
        if inhibitory_2[ag.y,ag.x]>0:
            inhibitory_2[ag.y,ag.x]-=1
            consume_inhibidor_2=True
        else:
            consume_inhibidor_2=False
    #Ponemos valor a la variable consume_inhibidor_1
    #Solo la especie 2 puede consumir la sustancia inhibidora 1
    elif species==2:
        consume_inhibidor_2=False
        if inhibitory_1[ag.y,ag.x]>0:
            inhibitory_1[ag.y,ag.x]-=1
            consume_inhibidor_1=True
        else:
            consume_inhibidor_1=False

    #El agente puede haber consumido la sustancia inhibidora o no haberlo hecho
    #Si la ha consumido, puede reproducirse con menor probabilidad (se divide por dos la tasa de reproduccion) y morir
    #Si no la ha consumido, puede reproducirse y morir
    if consume_inhibidor_2==True or consume_inhibidor_1==True:
        if random()<reproduction_rate/2*(1-sum(1 for x in agents)//carrying_capacity):
            newborn=copy(ag) 
            agents.append(newborn)
        if random()<death_rate:
            agents.remove(ag)
            return
    else:
        if random()<reproduction_rate*(1-sum(1 for x in agents)//carrying_capacity):
            newborn=copy(ag) 
            agents.append(newborn)
        if random()<death_rate:
            agents.remove(ag)
            return
        
##############################################################################
            
#Generamos una funcion para controlar el transcurso del tiempo por cada actualizacion
def update_one_unit_time():
    #La lista tenemos que definirla como global pues sino no podremos utilizarla fuera de la funcion, lo que no interesa
    global agents
    #Definimos una variable temporal
    t=0
    #Consideramos que cada actualizacion supone 1/n de una unidad temporal (siendo n el tamaño de la poblacion en el momento de actualizar)
    while t<1.0:
        t+=1.0/len(agents)
        update()

##############################################################################
 
#Generamos una funcion para actualizar el numero de individuos de cada especie 
def update_number():
    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, species_1_number, species_2_number, total_number
    #Definimos dos listas separadas para la especie 1 y la especie 2
    species_1=[ag for ag in agents if ag.type==1]
    species_2=[ag for ag in agents if ag.type==2]
    #Indicamos la poblacion de la especie 1 y de la especie 2
    species_1_number.append(len(species_1))
    species_2_number.append(len(species_2))
    total_number.append(len(species_1)+len(species_2))

###############################################################################

#Generamos una carpeta donde se guardaran los resultados de la simulacion
#Dentro de esta carpeta generamos otras 4, 3 para las imagenes que muestran la distribucion espacial y 1 para los documentos con la evolucion de las poblaciones

os.mkdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion")
os.mkdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Distribucion_espacial_inicial")
os.mkdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Distribucion_espacial_mitad")
os.mkdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Distribucion_espacial_final")
os.mkdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Evolucion_poblaciones")
os.mkdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Coordenadas_espaciales")

#Generamos un vector cuyos elementos son diccionarios con los valores de los parametros variables para cada simulacion

replicas=list(range(1,21))
combinaciones=[]
for p in percentage:
    for m in movement:
        for s in secretion_rate:
            for r in replicas:
                combinaciones.append([p,m,s,r])
            
#Cada elemento del vector incluye todos los parametros de una simulacion; hay un total de 45 elementos (que resultan de la combinatoria de 5*3*3)
#Iteramos sobre el vector
#Asignamos parametros y definimos el nombre del archivo
            
for i in combinaciones:

    species_1_percentage=i[0][0]
    species_2_percentage=i[0][1]
    species_1_movement=i[1][0]
    species_2_movement=i[1][1]
    species_1_secretion_rate=i[2][0]
    species_2_secretion_rate=i[2][1]
    r=i[3]
    
    p=int(species_1_percentage*10)
    if species_1_movement==species_2_movement: m="11"
    elif species_1_movement>species_2_movement: m="21"
    elif species_1_movement<species_2_movement: m="12"
    if species_1_secretion_rate==species_2_secretion_rate: s="11"
    elif species_1_secretion_rate>species_2_secretion_rate: s="21"
    elif species_1_secretion_rate<species_2_secretion_rate: s="12"
    simulacion="p"+str(p)+"m"+str(m)+"s"+str(s)+"r"+str(r)
            
#Simulamos el avance temporal del modelo
#Generamos 3 imagenes de la localizacion espacial de los agentes, incluyendo una al principio, una a la mitad y una al final
#Generamos un documento con las poblaciones de cada especie y total a cada momento de la simulacion
#Generamos una documento con las coordenadas de cada agente al final de la simulacion
#Hay que tener cuidado con los documentos e imagenes no se suporpongan; por ello les asignamos nombres distintos

    initialize()
    observe()
    os.chdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Distribucion_espacial_inicial")
    matplotlib.pyplot.savefig("modelo_competicion_inhibicion_inicio_"+str(simulacion)+".png")
    
    number_steps=1000
    for j in range(number_steps):
        update_number()
        update_one_unit_time()
        if j==(number_steps/2):
            observe()
            os.chdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Distribucion_espacial_mitad")
            matplotlib.pyplot.savefig("modelo_competicion_inhibicion_mitad_"+str(simulacion)+".png")
    
    observe()
    os.chdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Distribucion_espacial_final")
    matplotlib.pyplot.savefig("modelo_competicion_inhibicion_final_"+str(simulacion)+".png")
    
    os.chdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Coordenadas_espaciales")
    document=open("modelo_competicion_inhibicion_coordenadas_espaciales"+str(simulacion)+".txt","w")
    document.write("Especie" + '\t' + "Coordenadas X" + '\t' + "Coordenadas Y" + '\n')
    for ag in agents:
        document.write(str(ag.type) + '\t' + str(ag.x) + '\t' + str(ag.y) + '\n')
    document.close()

    os.chdir("/home/pedro/Simulaciones_modelo_competicion_inhibicion/Evolucion_poblaciones")
    document=open("modelo_competicion_inhibicion_"+str(simulacion)+".txt","w")
    document.write("Momento_temporal" + '\t' + "Especie1" + '\t' + "Especie2" + '\t'+ "Total" + '\n')
    for j in range(len(total_number)):
        document.write(str(j) + '\t' + str(species_1_number[j]) + '\t' + str(species_2_number[j]) + '\t'+ str(total_number[j]) + '\n')
    document.close()

