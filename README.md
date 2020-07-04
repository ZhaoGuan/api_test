# api_test
pytest -s -q --alluredir ./report/test

allure generate --clean  ./report/test

接口测试框架