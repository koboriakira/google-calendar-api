dev:
	docker compose up -d
	open http://localhost:10112/docs

cdk-test:
	cd cdk && npm run test
