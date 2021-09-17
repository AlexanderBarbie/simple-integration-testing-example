# serial-simulator

Simulating a connection to a serial port

# How To

## Build images:

```
dockebuild -t geomar/socattestin -f DockerfileIn .
docker build -t geomar/socattestout .
```

## Start Containers

Start the listener first:

```
docker run -it --rm --name socattestin -p 8080:8080 -v /var/run/docker.sock:/var/run/docker.sock -d geomar/socattestin
```

join container:

```
docker exec -it socattestin bash
```
run 

```
cat < /dev/virtualport0
```

Start the server:

```
docker run -it --rm --name socattestout -v /var/run/docker.sock:/var/run/docker.sock -d geomar/socattestout
```

join container:

```
docker exec -it socattestout bash
```

send message via:

```
echo "hi" > /dev/virtualcom0
```