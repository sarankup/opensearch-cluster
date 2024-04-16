export OPENSEARCH_INITIAL_ADMIN_PASSWORD=XXXXXXXXX
docker-compose -f docker-compose.yml up

docker-compose -f docker-compose-node1.yml up
docker-compose -f docker-compose-node2.yml up
docker-compose -f docker-compose-node3.yml up
docker-compose -f docker-compose-dashboard.yml up

./opensearch-perf-top-macos --dashboard ClusterOverview --endpoint localhost:9600