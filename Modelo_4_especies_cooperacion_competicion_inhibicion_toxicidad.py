#MODELO COOPERACION (2 ESPECIES) + COMPETICION INHIBICION (1 ESPECIE) + COMPETICION TOXICIDAD (1 ESPECIE)

##############################################################################
  
#Importamos las funciones que vayamos a utilizar
#Estas son necesarias para definir los valores de determinados atributos y realizar determinados calculos
from random import randint,random,shuffle
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
#Numero de agentes incluidos inicialmente en el modelo por especie
number_agents=50
#Numero de especies
number_species=4
#Capacidad de carga del modelo (se considera respecto del total de agentes, no respecto de cada especie)
carrying_capacity=number_agents*number_species*3
#Numero de filas/columnas en el array espacial (que discretiza el espacio)
rows_columns=100

#PARAMETROS CONSTANTES
#Tasa de reproduccion
reproduction_rate=0.05
#Tasa de muerte
death_rate=0.04
#Tasa de secrecion
secretion_rate=0.1
#Velocidad de movimiento 
movement=1

#PARAMETROS VARIABLES
#Radio de deteccion: distancia por debajo de la cual se consideran vecinos a los agentes a la hora de secretar
detection_ratios=[5,10]
#Radio de competicion: distancia por debajo de la cual se consideran vecinos a los agentes a la hora de competir por alimento
competition_ratio=5
#max_number: numero de vecinos (considerados con el radio de competicion) para el cual la tasa de reproduccion es 0
max_numbers=[30,60,120]
#[carrying_capacity/20,carrying_capacity/10,carrying_capacity/5]

##############################################################################

#Definimos una clase vacia, sin atributos ni metodos
#Las instancias de esta clase seran denominadas agentes
class agent:
    pass

##############################################################################
     
#Generamos una funcion que permite obtener una lista de agentes y asigna atributos a los mismos
def initialize():
    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, metabolite_1, metabolite_2, metabolite_3, metabolite_4
    global species_1_number, species_2_number, species_3_number, species_4_number, total_number
    agents=[]; species_1_number=[]; species_2_number=[]; species_3_number=[]; species_4_number=[]; total_number=[] 
    #Iteramos sobre el numero de agentes definidos
    for i in range (number_agents*number_species):
        #Generamos una instancia de la clase agent
        ag=agent()
        #El primer atributo se refiere al tipo de agente
        if i<number_agents:
            ag.type=1
        elif number_agents<=i<number_agents*2:
            ag.type=2
        elif number_agents*2<=i<number_agents*3:
            ag.type=3
        else:
            ag.type=4
        #El segundo y tercer atributo se refieren a la ubicacion
        #Planteamos que se encuentran en una posicion aleatoria del cuadrado definido por el numero de filas/columnas
        ag.x=randint(0,rows_columns-1)
        ag.y=randint(0,rows_columns-1) 
        #El cuarto atributo se refiere a la tasas de reproduccion
        ag.reproduction_rate=reproduction_rate
        #El quinto atributo se refiere a la tasa de muerte
        ag.death_rate=death_rate
        #El sexto atributo se refiere a la tasa de secrecion
        ag.secretion_rate=secretion_rate
        #El septimo atributo se refiere a la tasa de movimiento
        ag.movement=movement             
        #Añadimos la instancia creada a la lista
        agents.append(ag)  
    #Generamos arrays para los metabolitos
    metabolite_1=zeros([rows_columns,rows_columns])
    metabolite_2=zeros([rows_columns,rows_columns])
    metabolite_3=zeros([rows_columns,rows_columns])
    metabolite_4=zeros([rows_columns,rows_columns])
        
##############################################################################

#Generamos una funcion que permite visualizar los resultados
def observe():
    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, metabolite_1, metabolite_2, metabolite_3, metabolite_4
    global species_1_number, species_2_number, species_3_number, species_4_number, total_number  
    #Limpiamos la grafica para poder adecuarla a los resultado que se van a obtener en el momento actual
    matplotlib.pyplot.cla()
    #Definimos los ejes, buscando que se mantenga la proporcionalidad entre X e Y, entre 0 y 1   
    matplotlib.pyplot.axis("image")
    matplotlib.pyplot.axis([0,rows_columns-1,0,rows_columns-1]) 
    #Definimos listas separadas para cada especie
    species_1=[ag for ag in agents if ag.type==1]
    species_2=[ag for ag in agents if ag.type==2]
    species_3=[ag for ag in agents if ag.type==3]
    species_4=[ag for ag in agents if ag.type==4]
    #Dibujamos en la grafica la celulas
    if len(species_1)>0:
        matplotlib.pyplot.scatter([ag.x for ag in species_1],[ag.y for ag in species_1], marker="o",color="#2196F3")
    if len(species_2)>0:
        matplotlib.pyplot.scatter([ag.x for ag in species_2],[ag.y for ag in species_2], marker="o",color="#3F51B5")
    if len(species_3)>0:
        matplotlib.pyplot.scatter([ag.x for ag in species_3],[ag.y for ag in species_3], marker="o",color="#E53935")
    if len(species_4)>0:
        matplotlib.pyplot.scatter([ag.x for ag in species_4],[ag.y for ag in species_4], marker="o",color="#FF7043")
    #Dibujamos en la grafica los metabolitos
    color0 = matplotlib.colors.colorConverter.to_rgba('white')
    color1 = matplotlib.colors.colorConverter.to_rgba('#2196F3')
    color2 = matplotlib.colors.colorConverter.to_rgba('#3F51B5')
    color3 = matplotlib.colors.colorConverter.to_rgba('#E53935')
    color4 = matplotlib.colors.colorConverter.to_rgba('#FF7043')                                                      
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap1',[color0,color1],256)
    cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap2',[color0,color2],256)
    cmap3 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap3',[color0,color3],256)
    cmap4 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap4',[color0,color4],256)
    matplotlib.pyplot.imshow(metabolite_1,cmap=cmap1,vmin=0,vmax=5,alpha=1)
    matplotlib.pyplot.imshow(metabolite_2,cmap=cmap2,vmin=0,vmax=5,alpha=0.75)
    matplotlib.pyplot.imshow(metabolite_3,cmap=cmap3,vmin=0,vmax=5,alpha=0.5)
    matplotlib.pyplot.imshow(metabolite_4,cmap=cmap4,vmin=0,vmax=5,alpha=0.25)

      
##############################################################################

#Generamos una funcion que contempla la dinamica de los agentes
def update():

    #Las listas tenemos que definirlas como globales pues sino no podremos utilizarlas fuera de la funcion, lo que no interesa
    global agents, metabolite_1, metabolite_2, metabolite_3, metabolite_4
    
    #Si ya no existen agentes, se sale de la funcion
    if agents==[]:
        return
          
    #SELECCION Y CARACTERIZACION DE UN AGENTE
    #Seleccionamos un agente aleatorio
    ag=agents[randint(0,len(agents)-1)]
    species=ag.type
    reproduction_rate=ag.reproduction_rate
    death_rate=ag.death_rate
    secretion_rate=ag.secretion_rate
    movement=ag.movement
 
    #MOVIMIENTO 
    #En este caso no consideramos que el espacio es abierto como en modelos anteriores sino que existen limites
    if movement>0:
        ag.x+=randint(-movement,movement)
        ag.y+=randint(-movement,movement)      
    ag.x=rows_columns-1 if ag.x>rows_columns-1 else 0 if ag.x<0 else ag.x
    ag.y=rows_columns-1 if ag.y>rows_columns-1 else 0 if ag.y<0 else ag.y
    
    #SECRECION DE LOS METABOLITOS
    #En este codigo vamos a introducir la idea de secrecion por estimulo; solo se secretan metabolitos cuando la bacteria sensa que esta rodeada de bacterias de la otra especie
    #Definimos un entorno (distancia menor al ratio) tal que, si en ese entorno hay celulas de la otra especie (vecinos), se activa la probabilidad de secretar
    neighbors=[]
    for nb in agents:
        if (ag.x-nb.x)**2+(ag.y-nb.y)**2 < detection_ratio**2:
            neighbors.append(nb)
    if species==1:
        detection_neighbors=sum(1 for nb in neighbors if nb.type==2)
    elif species==2:
        detection_neighbors=sum(1 for nb in neighbors if nb.type==1)
    else:
        detection_neighbors=sum(1 for nb in neighbors if nb.type!=ag.type)
    if detection_neighbors>0:
        if random()<secretion_rate:
            if species==1:
                metabolite_1[ag.y,ag.x]+=1
            elif species==2:
                metabolite_2[ag.y,ag.x]+=1 
            elif species==3:
                metabolite_3[ag.y,ag.x]+=1  
            elif species==4:
                metabolite_4[ag.y,ag.x]+=1                 
    
    #CONSUMO DE METABOLITOS Y ALIMENTO
    #Como los arrays espaciales son independientes, en una misma posicion podriamos tener metabolitos que provienen de especies distintas
    #A nosotros nos interesa que, a cada iteracion, un agente solo consuma un metabolito, de manera que cuando ya ha consumido uno se deja de comprobar si existen de otro tipo
    #Para no establecer un orden de predominancia, hacemos que el orden sea aleatorio
    #La especie 1 puede consumir el bien comun 2, el inhibidor 3 y la toxina 4
    #La especie 2 puede consumir el bien comun 1, el inhibidor 3 y el toxina 4
    #La especie 3 puede consumir la toxina 4
    #La especie 4 puede consumir el inhibidor 3
    consume_bien_comun=False
    consume_inhibidor=False
    consume_toxina=False
    if species==1:
        orden=[2,3,4]
        shuffle(orden)
        if globals()["metabolite_"+str(orden[0])][ag.y,ag.x]>0:
            globals()["metabolite_"+str(orden[0])][ag.y,ag.x]-=1
            if orden[0]==2:
                consume_bien_comun=True
            elif orden[0]==3:
                consume_inhibidor=True
            elif orden[0]==4:
                consume_toxina=True
        elif globals()["metabolite_"+str(orden[1])][ag.y,ag.x]>0:
            globals()["metabolite_"+str(orden[1])][ag.y,ag.x]-=1
            if orden[1]==2:
                consume_bien_comun=True
            elif orden[1]==3:
                consume_inhibidor=True
            elif orden[1]==4:
                consume_toxina=True
        elif globals()["metabolite_"+str(orden[2])][ag.y,ag.x]>0:
            globals()["metabolite_"+str(orden[2])][ag.y,ag.x]-=1
            if orden[2]==2:
                consume_bien_comun=True
            elif orden[2]==3:
                consume_inhibidor=True
            elif orden[2]==4:
                consume_toxina=True
    elif species==2:
        orden=[1,3,4]
        shuffle(orden)
        if globals()["metabolite_"+str(orden[0])][ag.y,ag.x]>0:
            globals()["metabolite_"+str(orden[0])][ag.y,ag.x]-=1
            if orden[0]==1:
                consume_bien_comun=True
            elif orden[0]==3:
                consume_inhibidor=True
            elif orden[0]==4:
                consume_toxina=True
        elif globals()["metabolite_"+str(orden[1])][ag.y,ag.x]>0:
            globals()["metabolite_"+str(orden[1])][ag.y,ag.x]-=1
            if orden[1]==1:
                consume_bien_comun=True
            elif orden[1]==3:
                consume_inhibidor=True
            elif orden[1]==4:
                consume_toxina=True
        elif globals()["metabolite_"+str(orden[2])][ag.y,ag.x]>0:
            globals()["metabolite_"+str(orden[2])][ag.y,ag.x]-=1
            if orden[2]==1:
                consume_bien_comun=True
            elif orden[2]==3:
                consume_inhibidor=True
            elif orden[2]==4:
                consume_toxina=True
    elif species==3:
        if metabolite_4[ag.y,ag.x]>0:
            metabolite_4[ag.y,ag.x]-=1
            consume_toxina=True         
    elif species==4:
        if metabolite_3[ag.y,ag.x]>0:
            metabolite_3[ag.y,ag.x]-=1
            consume_inhibidor=True
            
    #Consideramos una competicion local por el alimento, luego la tasa de reproduccion disminuye linealmente cuanto mayor sea el numero de vecinos alrededor
    #Definimos un entorno (distancia menor al ratio de competicion) tal que, cuanto mayor sea el numero de celulas en este entorno, menor es la tasa de reproduccion
    if competition_ratio<detection_ratio:
        competition_neighbors=sum(1 for nb in neighbors if (ag.x-nb.x)**2+(ag.y-nb.y)**2 < competition_ratio**2)
    else:
        competition_neighbors=sum(1 for nb in neighbors)
    
    #El agente puede haber consumido un bien comun, haber consumido un inhibidor, haber consumido una toxina o no haber consumido nada
    #Si ha consumido el bien comun, puede reproducirse con mayor probabilidad (se duplica la tasa de reproduccion) y morir
    #Si ha consumido el inhibidor, puede reproducirse con menor probabilidad (se divide por dos la tasa de reproduccion) y morir
    #Si ha consumido la toxina, puede reproducirse y morir con mayor probabilidad (se duplica la tasa de muerte)
    #Si no ha consumido nada, puede reproducirse y morir
    if consume_bien_comun==True:
        if random()<(reproduction_rate-((reproduction_rate)*(competition_neighbors/max_number)))*2*(1-sum(1 for x in agents)//carrying_capacity):
            newborn=copy(ag) 
            agents.append(newborn)
        if random()<death_rate:
            agents.remove(ag)
            return
    elif consume_inhibidor==True:
        if random()<(reproduction_rate-((reproduction_rate)*(competition_neighbors/max_number)))/2*(1-sum(1 for x in agents)//carrying_capacity):
            newborn=copy(ag) 
            agents.append(newborn)
        if random()<death_rate:
            agents.remove(ag)
            return
    elif consume_toxina==True:
        if random()<(reproduction_rate-((reproduction_rate)*(competition_neighbors/max_number)))*(1-sum(1 for x in agents)//carrying_capacity):
            newborn=copy(ag) 
            agents.append(newborn)
        if random()<death_rate*2:
            agents.remove(ag)
            return
    else:
        if random()<(reproduction_rate-((reproduction_rate)*(competition_neighbors/max_number)))*(1-sum(1 for x in agents)//carrying_capacity):
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
    global agents, species_1_number, species_2_number, species_3_number, species_4_number, total_number
    #Definimos dos listas separadas para las especies
    species_1=[ag for ag in agents if ag.type==1]
    species_2=[ag for ag in agents if ag.type==2]
    species_3=[ag for ag in agents if ag.type==3]
    species_4=[ag for ag in agents if ag.type==4]
    #Indicamos la poblacion de las especies
    species_1_number.append(len(species_1))
    species_2_number.append(len(species_2))
    species_3_number.append(len(species_3))
    species_4_number.append(len(species_4))
    total_number.append(len(species_1)+len(species_2)+len(species_3)+len(species_4))

###############################################################################

#Generamos una carpeta donde se guardaran los resultados de la simulacion
#Dentro de esta carpeta generamos otras 4, 3 para las imagenes que muestran la distribucion espacial y 1 para los documentos con la evolucion de las poblaciones

os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_0")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_500")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_1000")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_1500")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_2000")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Evolucion_poblaciones")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Coordenadas_espaciales_1000")
os.mkdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Coordenadas_espaciales_2000")

#Generamos un vector cuyos elementos son diccionarios con los valores de los parametros variables para cada simulacion

replicas=list(range(21,51))
combinaciones=[]
for mn in max_numbers:
    for dr in detection_ratios:
        for r in replicas:
            combinaciones.append([mn,dr,r])
            
#Cada elemento del vector incluye todos los parametros de una simulacion; hay un total de 6 elementos (que resultan de la combinatoria de 3*2)
#Iteramos sobre el vector
#Asignamos parametros y definimos el nombre del archivo
            
for i in combinaciones:

    max_number=i[0]
    detection_ratio=i[1]
    r=i[2]
    simulacion="mn"+str(max_number)+"dr"+str(detection_ratio)+"r"+str(r)
            
#Simulamos el avance temporal del modelo
#Generamos 5 imagenes de la localizacion espacial de los agentes
#Generamos un documento con las poblaciones de cada especie y total a cada momento de la simulacion
#Generamos 2 documento con las coordenadas de cada agente a la mitad y al final de la simulacion
#Hay que tener cuidado con los documentos e imagenes no se suporpongan; por ello les asignamos nombres distintos

    initialize()
    observe()
    os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_0")
    matplotlib.pyplot.savefig("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_0_"+str(simulacion)+".png")
    
    number_steps=2000
    for j in range(number_steps):
        update_number()
        update_one_unit_time()
        
        if j==(number_steps*0.25):
            observe()
            os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_500")
            matplotlib.pyplot.savefig("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_500_"+str(simulacion)+".png")
            
        if j==(number_steps*0.5):
            
            observe()
            os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_1000")
            matplotlib.pyplot.savefig("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_1000_"+str(simulacion)+".png")
            
            os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Coordenadas_espaciales_1000")
            document=open("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_coordenadas_espaciales_1000_"+str(simulacion)+".txt","w")
            document.write("Especie" + '\t' + "Coordenadas X" + '\t' + "Coordenadas Y" + '\n')
            for ag in agents:
                document.write(str(ag.type) + '\t' + str(ag.x) + '\t' + str(ag.y) + '\n')
            document.close()
                
        if j==(number_steps*0.75):
            observe()
            os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_1500")
            matplotlib.pyplot.savefig("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_1500_"+str(simulacion)+".png")
    
    observe()
    os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Distribucion_espacial_2000")
    matplotlib.pyplot.savefig("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_2000_"+str(simulacion)+".png")
    
    os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Coordenadas_espaciales_2000")
    document=open("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_coordenadas_espaciales_2000_"+str(simulacion)+".txt","w")
    document.write("Especie" + '\t' + "Coordenadas X" + '\t' + "Coordenadas Y" + '\n')
    for ag in agents:
        document.write(str(ag.type) + '\t' + str(ag.x) + '\t' + str(ag.y) + '\n')
    document.close()

    os.chdir("/home/pedro/Simulaciones_modelo_mixto_cooperacion_competicion_inhibicion_toxicidad/Evolucion_poblaciones")
    document=open("modelo_mixto_cooperacion_competicion_inhibicion_toxicidad_"+str(simulacion)+".txt","w")
    document.write("Momento_temporal" + '\t' + "Especie1" + '\t' + "Especie2" + '\t'+ "Especie3" + '\t' + "Especie4" + '\t' + "Total" + '\n')
    for j in range(len(total_number)):
        document.write(str(j) + '\t' + str(species_1_number[j]) + '\t' + str(species_2_number[j]) + '\t' + str(species_3_number[j]) + '\t' + str(species_4_number[j]) + '\t' + str(total_number[j]) + '\n')
    document.close()

