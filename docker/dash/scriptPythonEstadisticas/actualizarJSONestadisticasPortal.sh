#!/bin/bash




#statsFormatos --> 5293c58e-53ad-4628-9306-b969b6939bb5
#statsDescargasVisitasMesAño --> 36d402c8-84e2-4288-bd84-923d615ca269
#stats --> 476c8820-0338-4d56-b388-0a7a36b4b125
#numeroTotalDatasets --> ebf8db32-be67-417f-bf75-71c328721764
KEY='3d3e039c-e401-4083-80a2-e74bdcaa1f1e'



#for archivo in estadisticas/*json
#do
#	if [[ "$archivo" != "estadisticas/infoIPs.json" ]]
#	then
		
		
#		ar=$(echo $archivo | sed 's/estadisticas//' | tr -d /)
		
		


		#curl -X POST  -H "Content-Type: multipart/form-data"  -H "Authorization: $KEY"  -F "id= 5293c58e-53ad-4628-9306-b969b6939bb5" -F "upload=@$archivo" http://localhost/api/3/action/resource_patch
#	fi
#done




curl -X POST  -H "Content-Type: multipart/form-data"  -H "Authorization: $KEY"  -F "id= 5293c58e-53ad-4628-9306-b969b6939bb5" -F "upload=@/home/usuario/scriptPythonEstadisticas/estadisticas/statsFormatos.json" http://localhost/api/3/action/resource_patch

curl -X POST  -H "Content-Type: multipart/form-data"  -H "Authorization: $KEY"  -F "id= 36d402c8-84e2-4288-bd84-923d615ca269" -F "upload=@/home/usuario/scriptPythonEstadisticas/estadisticas/statsDescargasVisitasMesAño.json" http://localhost/api/3/action/resource_patch

curl -X POST  -H "Content-Type: multipart/form-data"  -H "Authorization: $KEY"  -F "id= 476c8820-0338-4d56-b388-0a7a36b4b125" -F "upload=@/home/usuario/scriptPythonEstadisticas/estadisticas/stats.json" http://localhost/api/3/action/resource_patch



curl -X POST  -H "Content-Type: multipart/form-data"  -H "Authorization: $KEY"  -F "id= ebf8db32-be67-417f-bf75-71c328721764" -F "upload=@/home/usuario/scriptPythonEstadisticas/estadisticas/numeroTotalDatasets.json" http://localhost/api/3/action/resource_patch



