FROM nginx:stable

RUN apt update && apt upgrade oathtool -y

COPY key.hex ./