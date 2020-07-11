sonar_host=$1
projectKey=$2
sleep 10
response=$(curl "${sonar_host}"/api/qualitygates/project_status\?projectKey\="${projectKey}")
echo "${response}"
result=$(echo "${response}" | grep -Eo '"projectStatus":{"status":"OK"' | grep -c "OK")
if [ "${result}" == 1 ]; then
  echo "${result}"
else
  exit 1
fi
