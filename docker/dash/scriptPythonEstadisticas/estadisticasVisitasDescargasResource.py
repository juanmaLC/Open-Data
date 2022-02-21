import pandas as pd
import re
import numpy as np
import requests
import ckanapi
import json
import os
from datetime import datetime




#Dataframe con nombre, id, nombreDataset de los recursos del portal
def getDatasets(APIKEY, IP):


	ckan =ckanapi.RemoteCKAN(IP, apikey=APIKEY)
	datasets=ckan.action.package_list()



	idnombre=pd.DataFrame(columns=['dataset','id','nombre'])
	for dataset in datasets:

		#print (dataset)
		resources=ckan.action.package_show(id=dataset)
		for resource in resources['resources']:
				#print (resource['name'])
				idnombre=idnombre.append({'dataset':dataset, 'id':resource['id'],'nombre':resource['name']},ignore_index=True)


	return idnombre


def getLogNginx():
	log=pd.read_table('/var/log/nginx/access.log', names=['info'])
	exIP = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
	exFecha = re.compile(r'(\d{1,2}\/\[a-z]\/\d{4})')
	logFiltrado=pd.DataFrame(columns=['IP', 'Fecha','Accion'])
	#lista=[]
	for line in log['info']:


		l=line.split(sep=' ')

    	#Descargas desde boton
    	#200 5334 -> vista a resource 200 1186 -> vista a datastore
		#Descargas desde boton
    #200 5334 -> vista a resource 200 1186 -> vista a datastore
		if ('GET /' in line and ('/download/' in line or '/dump/' in line)):
		    #lista.append(exIP.match(line).group())
		    ip=exIP.match(line).group()

		    #Eliminar primer [
		    fecha=l[3][1:]
		    pos=fecha.find(':')
		    fecha=fecha[:pos]

		    #Accion
		    accion=l[5][1:] +' ' +l[6]
		    logFiltrado=logFiltrado.append({'IP': ip, 'Fecha': fecha, 'Accion':accion}, ignore_index=True)

		#elif ('GET /dataset/' in line and '/resource' in line and '/view' not in line and '/dataset/ HTTP' not in line and '/resource/new' not in line and 'http://opendata-test.ugr.es/dataset' not in line):
		elif ('GET /dataset/' in line and '/resource' in line and '/view' not in line and '/dataset/ HTTP' not in line and '/resource/new' not in line ):
		    ip=exIP.match(line).group()
		    #Eliminar primer [
		    fecha=l[3][1:]
		    pos=fecha.find(':')
		    fecha=fecha[:pos]

		    #accion
		    accion=l[5][1:] +' ' +l[6]
		    cadena= accion.split(sep='/')
		    ##MEJORAR LA BUSQUEDA DE VISTAS -----> log de recargar vista de resource

		    if ((len(cadena)) > 3):
		        if (cadena[3] == 'resource'):
		            logFiltrado=logFiltrado.append({'IP': ip, 'Fecha': fecha, 'Accion':accion}, ignore_index=True)

	return logFiltrado



def getDescargasVisitasResource():

	existe = os.path.exists('estadisticas/stats.json')

	if (existe):
		print ("Cargando archivo stats.json")
		descargas = pd.read_json('estadisticas/stats.json')
		resourcesD=descargas['resource'].tolist()

	else:
		print ("Creando archivo stats.json")
		descargas= pd.DataFrame(columns=['dataset','resource','nombre','descargas','visitas'])
		resourcesD=descargas['resource'].tolist()

	dump=0
	click=0

	for acc in logFiltrado['Accion']:
		cadena= acc.split(sep='/')


		if ('/dump/' in acc):
		    dump=dump+1
		    c=cadena[3]
		    #Eliminamos el ?format=....
		    pos=c.find('?')
		    c=c[:pos]

		    #Aumento contador
		    if (c in resourcesD):
		        index=np.where(descargas['resource'] == c)[0][0]
		        descargas.at[index,'descargas']=descargas.at[index,'descargas'] + 1

		    #Añado uno nuevo
		    elif (c in idnombre['id'].tolist()):

		        index=np.where(idnombre['id'] == c)[0][0]
		        nombre=idnombre.at[index,'nombre']
		        dataset=idnombre.at[index,'dataset']
		        print (nombre)
		        descargas=descargas.append({'dataset':dataset,'resource':c,'descargas':1,'nombre':nombre,'visitas':0}, ignore_index=True)
		        resourcesD=descargas['resource'].tolist()



		elif ('/download/' in acc):
		    click=click+1
		    c=cadena[4]
		    if (c in resourcesD):
		        index=np.where(descargas['resource'] == c)[0][0]
		        descargas.at[index,'descargas']=descargas.at[index,'descargas'] + 1
		    elif (c in idnombre['id'].tolist()):

		        index=np.where(idnombre['id'] == c)[0][0]
		        nombre=idnombre.at[index,'nombre']
		        dataset=idnombre.at[index,'dataset']

		        descargas=descargas.append({'dataset':dataset,'resource':c,'descargas':1,'visitas':0,'nombre':nombre}, ignore_index=True)
		        resourcesD=descargas['resource'].tolist()

		elif ('GET /dataset/' in acc and '/resource' in acc and '/view' not in acc and '/dataset/ HTTP' not in acc):
		    c=cadena[4].split(sep=' ')[0]

		    if (c in resourcesD):
		        index=np.where(descargas['resource'] == c)[0][0]
		        descargas.at[index,'visitas']=descargas.at[index,'visitas'] + 1
		    elif (c in idnombre['id'].tolist()):


		        index=np.where(idnombre['id'] == c)[0][0]


		        nombre=idnombre.at[index,'nombre']
		        dataset=idnombre.at[index,'dataset']

		        descargas=descargas.append({'dataset':dataset,'resource':c,'descargas':0,'nombre':nombre,'visitas':1}, ignore_index=True)
		        resourcesD=descargas['resource'].tolist()

	print ('Desdse dump --> ' + str(dump))
	print ('Desde click --> ' + str(click))


	statsjson = descargas.to_json(index=True)
	statsjson = json.loads(statsjson)
	with open('estadisticas/stats.json','w' ) as json_file:
		json.dump(statsjson,json_file)




def getDescargasVisitasMes():

	existe = os.path.exists('estadisticas/statsDescargasVisitasMesAño.json')

	if (existe):
		print ("Cargando archivo statsDescargasVisitasMesAño.json")
		descargasVisitasMes = pd.read_json('estadisticas/statsDescargasVisitasMesAño.json')


	else:
		print ("Creando archivo statsDescargasVisitasMesAño.json")
		descargasVisitasMes=pd.DataFrame(columns=['mes/año','descargas','visitas'])


	descargas=0
	visitas=0

	fechasGuardadas=descargasVisitasMes['mes/año'].tolist()

	for acc in logFiltrado['Accion']:

		#Descarga
		if ('/dump/' in acc or '/download/' in acc):
		    descargas=descargas+1



		#visita
		elif ('GET /dataset/' in acc and '/resource' in acc and '/view' not in acc and '/dataset/ HTTP' not in acc):
		    visitas=visitas+1


	if (logFiltrado.empty == False ):
		fecha=logFiltrado['Fecha'][0].split(sep='/')[1] +'/'+logFiltrado['Fecha'][0].split(sep='/')[2]
		#mes=logFiltrado['Fecha'][0].split(sep='/')[1]
		#año=logFiltrado['Fecha'][0].split(sep='/')[2]
		#fecha=mes+'/'+año



		if (fecha in fechasGuardadas):
			index=np.where(descargasVisitasMes['mes/año'] == fecha)[0][0]
			descargasVisitasMes.at[index,'descargas']=descargasVisitasMes.at[index,'descargas'] + descargas
			descargasVisitasMes.at[index,'visitas']=descargasVisitasMes.at[index,'visitas'] + visitas
		else:
			descargasVisitasMes=descargasVisitasMes.append({'mes/año':fecha,'descargas':descargas,'visitas':visitas}, ignore_index=True)




	statsjson = descargasVisitasMes.to_json(index=True)
	statsjson = json.loads(statsjson)
	with open('estadisticas/statsDescargasVisitasMesAño.json','w' ) as json_file:
		json.dump(statsjson,json_file)



def getTamDatasetsTamResources(APIKEY,IP):


	fechaActual=datetime.today().strftime('%Y-%m-%d')


	existe = os.path.exists('estadisticas/numeroTotalDatasets.json')

	if (existe):

		numeroDR= pd.read_json('estadisticas/numeroTotalDatasets.json')
		print ("Cargando archivo numeroTotalDatasets.json")
	else:
		numeroDR=pd.DataFrame(columns=['fecha','nº conjuntos'])
		print ("Creando archivo numeroTotalDatasets.json")



	ckan =ckanapi.RemoteCKAN(IP, apikey=APIKEY)
	datasets=ckan.action.package_list()


	datasets=ckan.action.package_list()
	tamDatasets=len(datasets)-1 #portal eu
	tamResources=0

	for dataset in datasets:
		resources=ckan.action.package_show(id=dataset)
		tamResources=len(resources['resources']) + tamResources


	print (tamDatasets)
	print (tamResources)



	if (fechaActual not in numeroDR['fecha'].tolist() ):

		numeroDR=numeroDR.append({'fecha':fechaActual,'nº conjuntos':tamDatasets,'nº recursos':tamResources}, ignore_index=True)

		statsjson=numeroDR.to_json(index=True)
		statsjson=json.loads(statsjson)
		with open('estadisticas/numeroTotalDatasets.json','w') as json_file:
		    json.dump(statsjson,json_file)





def getinfoIPs():

	existe = os.path.exists('estadisticas/infoIPs.json')

	if (existe):
		print ("Cargando archivo infoIPs.json")
		registroIPs = pd.read_json('estadisticas/infoIPs.json')


	else:
		print ("Creando archivo infoIPs.json")
		registroIPs= pd.DataFrame(columns=['ip','lat','long','city','state'])




	listaIPRegistradas=registroIPs['ip'].tolist()
	#listaIPRegistradas.append('172.25.22.67')
	for i in logFiltrado['IP']:

		ip=(i.split(sep=' ')[0])



		if ip not in listaIPRegistradas :
		    urlConsulta= 'https://geolocation-db.com/jsonp/' + ip
		    response = requests.get(urlConsulta)
		    datos=response.content.decode()
		    datos=datos.split("(")[1].strip(")")
		    datos=json.loads(datos)
		    listaIPRegistradas.append(ip)
		    if (datos['latitude'] != 'Not found' and datos['longitude'] != 'Not found'):
		        registroIPs=registroIPs.append({'ip':ip,'lat':datos['latitude'],'long':datos['longitude'],'city':datos['city'],'state':datos['state'],}, ignore_index=True)



	statsIP=registroIPs.to_json(index=True)
	statsIP=json.loads(statsIP)
	with open('estadisticas/infoIPs.json','w') as json_file:
		json.dump(statsIP,json_file)


def getFormatos(APIKEY,IP):

	

        print ("Creando archivo statsFormatos.json")
        formatosD=pd.DataFrame(columns=['formato','contador'])


        ckan =ckanapi.RemoteCKAN(IP, apikey=APIKEY)
        datasets=ckan.action.package_list()

        for dataset in datasets:
	        datos=ckan.action.package_show(id=dataset)
	        for dato in datos['resources']:
		        formato=dato['format']
		        if (formato in formatosD['formato'].tolist()):
			        index=np.where(formatosD['formato'] == formato)[0][0]
			        formatosD.at[index,'contador']=formatosD.at[index,'contador'] + 1
		        else:
			        formatosD=formatosD.append({'formato':formato, 'contador': 1 }, ignore_index=True)




        formatosD=formatosD.sort_values('contador', ascending=False)
        statsFormatos = formatosD.to_json(index=True)
        statsFormatos = json.loads(statsFormatos)
        with open('estadisticas/statsFormatos.json','w' ) as json_file:
                json.dump(statsFormatos,json_file)


#APIKEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJONlNtbXRqQnc2cFdxbkpQdHFhVV9mS1Z2U212WHZzbjBXWUlJdUVWbFJ5YlVlNjg3NjJDT2NJcHloVW5sc2RMcjY4eWFSbEdyTVVMQlJ5aCIsImlhdCI6MTYzNDgwNTkwOX0.cFGQpmTZoscO0F_Z6R5tisBBiHI0PKntIaGHboqjo8c'


# opendata-test.ugr.es --->
APIKEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJXR3BpREJ4YjdqcV9PSTZnZ1p0ZlhJa3JmeWJra0hlcEhZQjlQZzA0dGhhSjRqazY4RTM4ODVybEppTDBXTzVJZzdBVk5NSk9mc09rT1dFUCIsImlhdCI6MTYzNTUwNTkwNn0.BCaUAoUYdYPuzQkJH-7BS3I6xbO9svu6NZLjA97sPcw'

idnombre = getDatasets(APIKEY,'http://opendata-test.ugr.es')
logFiltrado = getLogNginx()




getDescargasVisitasResource()
getDescargasVisitasMes()
getTamDatasetsTamResources(APIKEY,'http://opendata-test.ugr.es')
getinfoIPs()
getFormatos(APIKEY,'http://opendata-test.ugr.es')
