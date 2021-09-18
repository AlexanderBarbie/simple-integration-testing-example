FROM ubuntu:20.04

ENV EMU_SIM_TTY_1 ""
ENV EMU_SIM_TTY_1_PORT ""

WORKDIR /home/driver/simple-driver
COPY . .
RUN chmod +x ./docker/entrypoint.sh

RUN apt-get update \
    && apt-get install -y socat python3-pip
RUN pip3 install .

ENTRYPOINT ["./docker/entrypoint.sh"]

