# https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/packaging-layers.html
generate_layer:
	mkdir python
	pip install -r requirements.txt -t python/python/lib/python3.11/site-packages/
	cd python && zip -r ../dependencies.zip .
	rm -rf python

deploy:
	cd cdk && cdk deploy --profile private --require-approval never

bootstrap:
	cd cdk && cdk bootstrap --profile private

run:
	cd gc_api && open http://localhost:10111/docs && uvicorn main:gc_api --reload --port 10111
