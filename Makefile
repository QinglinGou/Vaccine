
county:
	python -B src/data_process/project_county.py
	
pic:
	python -B src/visualization/pic.py
	
pop:
	python -B src/visualization/pic_popdensity.py
	
deaths:      
	python -B src/visualization/pic_death.py
	
confirmed:
	python -B src/visualization/pic_confirm.py
	
vac:
	python -B src/visualization/pic_vac.py
	
rate:
	python -B src/visualization/pic_rate.py
		
scatter:
	python -B src/visualization/scatter.py

barchart:

	python -B src/visualization/barchart.py
	
lstmus:
	python -B src/lstm/lstm_us.py
	
lstmcounty:
	python -B src/lstm/lstm_county.py
	
	

