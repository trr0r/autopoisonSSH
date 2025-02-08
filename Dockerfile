FROM trr0r/ssh_logpoisoning:latest

# Estarán abiertos los puertos 80 y 22
EXPOSE 80 22

# Ejecutamos el script entrypoint para levantar los servicios necesarios
ENTRYPOINT ["/bin/bash", "/.entrypoint"]