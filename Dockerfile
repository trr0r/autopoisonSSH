FROM tools/ssh_logpoisoning
# Abrimos el puerto y 22
EXPOSE 80, 22

# Ejecutaremos el script para tenerlo todo montado
CMD /bin/bash /.entrypoint