docker run --rm  \
--net=host \
--privileged \
--pid=host \
-v /sys:/sys \
-v /var/lib/docker/containers:/var/lib/docker/containers:ro \
-v /tmp/powerapi-sensor-reporting:/reporting \
-v $(pwd):/srv \
-v $(pwd)/config-sensor.json:/config-sensor.json \
ghcr.io/powerapi-ng/hwpc-sensor --config-file /config-sensor.json
