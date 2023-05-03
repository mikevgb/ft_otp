#!/bin/bash

docker stop ft_otp_oath
docker rm ft_otp_oath
docker build -t ft_otp_oath .
docker run --name ft_otp_oath -d ft_otp_oath sleep infinity
docker exec -it ft_otp_oath /bin/bash

