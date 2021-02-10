#!/usr/bin/env bash
set -ex

export REGISTRY=vimc
export NETWORK=montagu_default

here=$(dirname $0)

# Run the API and database
docker-compose pull
docker-compose --project-name montagu up -d

# Install orderly-web
pip install git+https://github.com/vimc/orderly-web-deploy@vimc-4558
orderly-web start $here --pull

# Start the APIs
docker exec montagu_api_1 mkdir -p /etc/montagu/api/
docker exec montagu_api_1 touch /etc/montagu/api/go_signal

# Wait for the database
docker exec montagu_db_1 montagu-wait.sh

# migrate the database
migrate_image=${REGISTRY}/montagu-migrate:master
docker pull $migrate_image
docker run --rm --network=montagu_default $migrate_image

# add test user
$here/montagu_cli.sh add "Test User" test.user \
    test.user@example.com password \
    --if-not-exists

$here/montagu_cli.sh addRole test.user user

# Add user to orderlyweb
$here/orderlyweb_cli.sh add-users test.user@example.com
$here/orderlyweb_cli.sh grant test.user@example.com */reports.read */reports.run */reports.review
