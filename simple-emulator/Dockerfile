FROM ubuntu:20.04

ENV SIM_TTY_1 ""
ENV SIM_TTY_1_ADDRESS ""
ENV SIM_TTY_1_PORT ""

WORKDIR /home/emulator/simple-emulator
COPY . .
RUN chmod +x ./docker/entrypoint.sh

RUN apt-get update \
    && apt-get install -y socat python3-pip
RUN pip3 install .

ENTRYPOINT ["./docker/entrypoint.sh"]

