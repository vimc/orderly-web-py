#!/usr/bin/env bash
set -ex

here=$(dirname $0)
$here/clear-docker.sh
source $here/run-dependencies.sh

# From now on, if the user presses Ctrl+C we should teardown gracefully
trap on_interrupt INT
function on_interrupt() {
    docker-compose --project-name montagu down --volumes
    docker-compose --project-name montagu rm
}

# Wait for Ctrl+C
echo "Ready to use. Press Ctrl+C to teardown."
sleep infinity 