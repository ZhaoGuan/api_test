sonar_host=$1
projectKey=$2
result=$(curl "${sonar_host}"/api/qualitygates/project_status\?projectKey\="${projectKey}" | grep -Eo '"projectStatus":{+"status":"OK"' | grep -c "OK")
if [ "${result}" == 1 ]; then
  echo "${result}"
else
  exit 1
fi
