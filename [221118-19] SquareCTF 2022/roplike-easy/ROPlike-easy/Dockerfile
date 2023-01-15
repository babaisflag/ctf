FROM ubuntu:22.04
MAINTAINER kfox

RUN apt-get update && apt-get install -y socat

RUN useradd -ms /bin/sh pwnable_user
WORKDIR /home/pwnable_user

ARG BINARY_NAME=roplike
ENV BINARY_NAME=$BINARY_NAME

COPY ./$BINARY_NAME ./
COPY ./flag.txt ./
COPY ./gadgets ./gadgets


RUN chown -R root:pwnable_user /home/pwnable_user && \
     chmod 750 /home/pwnable_user && \
     chmod 550 /home/pwnable_user/$BINARY_NAME && \
     chmod -R 550 /home/pwnable_user/gadgets && \
     chown root:pwnable_user /home/pwnable_user/flag.txt && \
     chmod 440 /home/pwnable_user/flag.txt

EXPOSE 8000


CMD ["sh", "-c", "socat -T720 TCP-LISTEN:8000,reuseaddr,fork,su=pwnable_user EXEC:/home/pwnable_user/${BINARY_NAME},pty,ctty,rawer"]
