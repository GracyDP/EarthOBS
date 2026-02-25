## Analisi di dati geospaziali per l'identificazione di cambaimenti di uso e copertura del suolo

Nel seguente ReadMe verrà spiegata la modalità di creazione di una web application per la visualizzazione di dati geografici; tramite GeoPanel e dati geoJson.

Il framework utilizzato è Streamlit, tramtie linguaggio python versione:3.11.5.

La visualizzazione della pagina iniziale è la seguente:
![Visualizzazione homepage](data/img/webapp.png)

L'interfaccia progettata permette tramite sidebar di effettuare la scelta del Layer da visualizzare che può essere 2012, 2018 o il dataset dei cambiamenti 2012-2018.
Sono state svolte delle analisi sui csv associati agli shapefile ed è stato applicato l'algoritmo Douglas-Peaker per ridurre tempi di computazione a fronte di una minore precisione poligonale sui dati(vettoriali). 

Di seguito vengono mostrati due barplot orizzontali:
data/img/cambiamenticlassi.png
data/img/barplotclc.png

Una HeatMap che mostra nell'arco di questi 6 anni di quanto siano cambiate alcune zone tramite un gradient di colore, a colori chiari vengono associati da 0 alla metà dei cambiamenti mentre i colori scuri identificano mutamenti maggiori.

data/img/Heatmap.png


