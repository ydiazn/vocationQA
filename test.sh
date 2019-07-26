cd vocationQA
coverage run manage.py test --keepdb
coverage report -m --skip-covered
coverage html --skip-covered -d ../htmlcov
cd ..