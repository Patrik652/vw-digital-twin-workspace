ENV ?= dev

init:
	terraform -chdir=environments/$(ENV) init -backend-config=backend.hcl

plan:
	terraform -chdir=environments/$(ENV) plan

apply:
	terraform -chdir=environments/$(ENV) apply

destroy:
	terraform -chdir=environments/$(ENV) destroy
