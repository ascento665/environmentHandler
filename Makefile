deploy: zip upload


clean:
	rm function.zip

zip:
	(cd package && zip -qr9 ../function.zip .)
	zip -qg function.zip lambda_function.py
	zip -qg function.zip environments.py
	zip -qg function.zip events.py
	zip -qg function.zip hue_wrapper.py
	zip -qg function.zip hue_wrapper_v1.py
	zip -qg function.zip data.cfg
	zip -qg function.zip huepythonrgbconverter/*

upload:
	aws lambda update-function-code --function-name environmentHandler --zip-file fileb://function.zip
