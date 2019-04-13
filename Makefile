deploy: zip upload


clean:
	rm function.zip

zip:
	(cd package && zip -r9 ../function.zip .)
	zip -g function.zip lambda_function.py
	zip -g function.zip environments.py
	zip -g function.zip events.py
	zip -g function.zip hue_wrapper.py
	zip -g function.zip hue_wrapper_v1.py
	zip -g function.zip data.cfg
	zip -g function.zip huepythonrgbconverter/*

upload:
	aws lambda update-function-code --function-name environmentHandler --zip-file fileb://function.zip
