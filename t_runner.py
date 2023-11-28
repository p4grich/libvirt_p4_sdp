#!/usr/bin/env python
import subprocess
import os, fnmatch
import re

f = open("./common.tfvars", "r")
lines = f.readlines()
for d in lines:
    if re.match(r'^domain.*', d):
        l = re.split('\"',d)
        domain = l[1]
        print("Found domain: ", domain) 

def find_tests(pattern, path):
    tests_found = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                tests_found.append(os.path.join(root, name))
    return tests_found

pytests = find_tests('test*.py', './')

def test_runner():
    print("Found tests:", pytests)
    working_dir = os.getcwd()
    for t in pytests:
        site_name = os.path.basename(os.path.dirname(t))
        dir = os.path.dirname(t)
        found_test = os.path.basename(t)
        os.chdir(dir)
        print("Running test at path:")
        subprocess.run(["pwd"])
        subprocess.run(["py.test", "-rP", "--hosts="+site_name+"."+domain, "--ansible-inventory=./inventory.yml", "--connection=ansible", "./"+found_test])
        os.chdir(working_dir)
test_runner()
