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
