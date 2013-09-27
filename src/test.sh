# Server window
cd /home/leal/git/reductionServer/src
./reductionServer.py

# Client window

cd /home/leal/Documents/Mantid/IN5/2013-02-08
curl -s -X POST --data-binary @102296.nxs http://localhost:8080/file/102296 | python -mjson.tool
curl -s -X POST --data-binary @102297.nxs http://localhost:8080/file/102297 | python -mjson.tool

curl -s -X POST -d '{"function":"theta_vs_counts","input_params":{"numors":[102296]}}'  http://localhost:8080/query | python -mjson.tool

curl -s http://localhost:8080/results/ | python -mjson.tool

