install:
	@pip install -r requirements.txt
	@brew install terraform
	@brew install terragrunt
	@echo "Read: https://libvirt.org/nss.html for local nss support/setup"
	@echo "Installing apt install -y libnss-libvirt or yum install -y libvirt-nss"
	@echo ""
	@if which apt; then sudo apt install -y libnss-libvirt; else sudo yum install -y libvirt-nss; fi

test_runner:
	@python t_runner.py
deploy_commit:
	@ cd dev/commit; terragrunt init
	@ cd dev/commit; terragrunt plan
	@ cd dev/commit; terragrunt apply
	@ cd dev/commit; terragrunt apply
	@ cd dev/commit; py.test -rP --hosts=commit.fstat.io --ansible-inventory=./inventory.yml --connection=ansible ./test.py
test_commit:
	@ cd dev/commit; py.test -rP --hosts=commit.fstat.io --ansible-inventory=./inventory.yml --connection=ansible ./test.py
clean_commit:
	@ cd dev/commit; terragrunt destroy
	@ cd dev/commit; rm -rf tf.log

deploy_nfs:
	@ cd dev/nfs; terragrunt init
	@ cd dev/nfs; terragrunt plan
	@ cd dev/nfs; terragrunt apply
	@ cd dev/nfs; terragrunt apply
	@ cd dev/nfs; py.test -rP --hosts=nfs.fstat.io --ansible-inventory=./inventory.yml --connection=ansible ./test.py
test_nfs:
	@ cd dev/nfs; py.test -rP --hosts=nfs.fstat.io --ansible-inventory=./inventory.yml --connection=ansible ./test.py
clean_nfs:
	@ cd dev/nfs; terragrunt destroy -var hostname=nfs
	@ cd dev/nfs; rm -rf tf.log
