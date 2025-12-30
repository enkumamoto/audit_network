# Diagnóstico Avançado de Rede (Python)

Este repositório contém **scripts Python de diagnóstico avançado de rede**, focados em **troubleshooting de conectividade, tráfego e firewall**, com suporte a:

- Linux (bare metal, VM)
- Kubernetes
- OpenShift
- Ambientes corporativos e produtivos

Os scripts coletam informações técnicas completas e geram relatórios em **TXT, JSON e HTML**, ideais para:
- Análise de incidentes
- RCA (Root Cause Analysis)
- Chamados de suporte
- Auditoria
- Automação e pipelines

---

## 📦 Scripts Disponíveis

### 1️⃣ `network-diagnostic.py`
**Diagnóstico de rede para hosts Linux**

Indicado para:
- Servidores Linux
- Máquinas virtuais
- Hosts Docker
- Ambientes fora de Kubernetes

**Gera:**
- Relatório em texto (`.txt`)

---

### 2️⃣ `diagnostico_rede_k8s.py`
**Diagnóstico de rede para Kubernetes / OpenShift (host)**

Indicado para:
- Nós Worker
- Control Plane
- OpenShift 4.x
- Execução via `oc debug node`

**Gera:**
- Relatório em texto (`.txt`)
- Relatório estruturado (`.json`)
- Relatório visual (`.html`)

---

## 🧠 O que os scripts analisam

✔ Interface de rede e IP  
✔ Gateway e rotas  
✔ DNS  
✔ Conectividade externa  
✔ Latência e perda de pacotes  
✔ Conexões ativas e portas  
✔ Consumo de rede por processo  
✔ Captura de pacotes (tcpdump)  
✔ Firewall (iptables / nftables)  
✔ Kubernetes / OpenShift (quando aplicável)  
✔ CNI (Calico, OVN, Flannel, Cilium, etc.)  
✔ Possíveis causas de indisponibilidade  

---

## 🔐 Elevação automática de privilégios

Ambos os scripts realizam **elevação automática para root** usando `sudo`, necessária para comandos como:

- `iptables`
- `nft`
- `tcpdump`
- `iftop`
- `nethogs`
- acesso `netlink`

> ⚠️ Não é necessário executar manualmente com `sudo`.

---

## ▶️ Como executar

### Pré-requisitos
Pacotes recomendados:

```bash
sudo apt install -y \
  iproute2 iputils-ping dnsutils \
  tcpdump iftop nethogs vnstat \
  mtr lsof jq
````

Python:

```bash
python3 --version
```

---

### Execução – Host Linux

```bash
chmod +x network-diagnostic.py
./network-diagnostic.py
```

---

### Execução – Kubernetes / OpenShift (host)

```bash
chmod +x diagnostico_rede_k8s.py
./diagnostico_rede_k8s.py
```

Ou via OpenShift:

```bash
oc debug node/<nome-do-no>
chroot /host
./diagnostico_rede_k8s.py
```

---

## 📄 Relatórios Gerados

### TXT

* Relatório completo em texto
* Ideal para anexar em tickets

### JSON

* Estruturado
* Ideal para:

  * ELK / Splunk / Loki
  * CI/CD
  * Automação

### HTML

* Visual
* Leitura fácil para times N1/NOC
* Pode ser aberto diretamente no navegador

---

## 📁 Exemplo de arquivos gerados

```text
diagnostico_rede_20250101_153000.txt
diagnostico_rede_20250101_153000.json
diagnostico_rede_20250101_153000.html
```

---

## ⚠️ Observações importantes

### Execução em Pods

❌ **Não funciona em pods comuns**

Para Kubernetes/OpenShift:

* Execute no **host**
* Use `oc debug node`
* Ou implemente como **DaemonSet privileged**

---

## 🧩 Possíveis causas detectadas automaticamente

* Interface DOWN
* Gateway padrão ausente
* DNS inoperante
* Bloqueio de firewall
* Perda de conectividade externa
* Problemas de CNI
* Consumo excessivo de banda

---

## 🔧 Extensões possíveis

* Execução como **DaemonSet privileged**
* Exportação automática para S3
* Integração com ELK / Prometheus
* Captura de PCAP automática
* Modo **pré-upgrade / pós-upgrade**
* Versão simplificada para N1/NOC

---

## 👨‍💻 Público-alvo

* SRE
* DevOps
* Cloud Engineers
* Administradores de sistemas
* Times de suporte N2/N3

---

## 📜 Licença

Uso interno / corporativo.
Adapte conforme as políticas da sua organização.

---

## ✅ Conclusão

Estes scripts fornecem **visibilidade profunda da rede**, reduzem tempo de diagnóstico e ajudam a identificar rapidamente **causas reais de falhas de conectividade** em ambientes Linux e Kubernetes.

````

---

## ⬇️ Como “baixar” o README

1. Copie todo o conteúdo acima  
2. Salve como:
   ```bash
   README.md
````

3. Commit no repositório:

   ```bash
   git add README.md
   git commit -m "Add detailed README for network diagnostics scripts"
   ```

---
