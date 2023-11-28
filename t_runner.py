""""Find all tests and run them"""
import subprocess
import os
import fnmatch
import re

with open('./common.tfvars', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for d in lines:
        if re.match(r'^domain.*', d):
            l = re.split('\"',d)
            domain = l[1]
            print("Found domain: ", domain)

def find_tests(pattern, path):
    """Find tests"""
    print(path)
    tests_found = []
    dirs = []
    dirs.count([0]) #W0612
    for root, dirs, files in os.walk(path):
        if not re.match(r'.*actions-runner.*', root):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    tests_found.append(os.path.join(root, name))
    return tests_found

pytests = find_tests('test*.py', './')

def test_runner():
    """Execute tests"""
    print("Found tests:", pytests)
    working_dir = os.getcwd()
    for t in pytests:
        site_name = os.path.basename(os.path.dirname(t))
        test_dir = os.path.dirname(t)
        found_test = os.path.basename(t)
        os.chdir(test_dir)
        print("Running test at path:")
        subprocess.run(["pwd"], check=True)
        subprocess.run(["py.test", "-rP", "--hosts="+site_name+"."+domain,
 "--ansible-inventory=./inventory.yml", "--connection=ansible", "./"+found_test], check=True)
        os.chdir(working_dir)
test_runner()
