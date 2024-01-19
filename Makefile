run:
	cd gc_api && open http://localhost:10111/docs && uvicorn main:gc_api --reload --port 10111

cdk-test:
	cd cdk && npm run test
