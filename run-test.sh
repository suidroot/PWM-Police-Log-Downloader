#!/bin/bash
#-e LOG_LEVEL="DEBUG" \
docker run --rm \
-e FILE_LOCATION=/output \
-e ENABLE_UPLOAD=True \
-e UPLOAD_DISPATCH_URL=http://host.docker.internal:8000/add/dispatch/ \
-e UPLOAD_ARREST_URL=http://host.docker.internal:8000/add/arrest/ \
-v "./test":/output \
--add-host host.docker.internal:host-gateway \
suidroot/pwmlogdl /bin/bash