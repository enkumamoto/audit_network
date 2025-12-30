#!/usr/bin/env python3
import os
import sys
import subprocess
from datetime import datetime
import shutil

# ==========================================================
# ELEVAÇÃO AUTOMÁTICA PARA ROOT
# ==========================================================
if os.geteuid() != 0:
    print("⚠️  Permissões insuficientes detectadas.")
    print("➡️  Reexecutando o script com sudo para evitar erros de permissão...")
    os.execvp("sudo", ["sudo", "-E", sys.executable] + sys.argv)

# ==========================================================
# VARIÁVEIS
# ==========================================================
DATA = datetime.now().strftime("%Y%m%d_%H%M%S")
RELATORIO = f"relatorio_rede_{DATA}.txt"
ALVO = "8.8.8.8"
TESTE_DNS = "google.com"

# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================
def run(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"Erro ao executar comando: {e}\n"

def comando_existe(cmd):
    return shutil.which(cmd) is not None

def interface_padrao():
    cmd = "ip route | awk '/default/ {print $5}' | head -n1"
    return run(cmd).strip() or "desconhecida"

INTERFACE = interface_padrao()

# ==========================================================
# REDIRECIONA SAÍDA PARA ARQUIVO
# ==========================================================
with open(RELATORIO, "w") as f:
    sys.stdout = f
    sys.stderr = f

    print("==================================================")
    print(" RELATÓRIO DE DIAGNÓSTICO DE REDE")
    print(f" Gerado em: {datetime.now()}")
    print(f" Interface analisada: {INTERFACE}")
    print("==================================================\n")

    # --------------------------------------------------
    print("[1] INFORMAÇÕES DO SISTEMA E INTERFACE")
    print(run("uname -a"))
    print(run(f"ip addr show {INTERFACE}"))
    print(run("ip route"))

    # --------------------------------------------------
    print("[2] STATUS DO LINK")
    print(run(f"ip link show {INTERFACE}"))

    # --------------------------------------------------
    print("[3] CONFIGURAÇÃO DE DNS")
    print(run("cat /etc/resolv.conf"))

    print("[3.1] TESTE DE RESOLUÇÃO DNS")
    print(run(f"getent hosts {TESTE_DNS}") or "❌ Falha na resolução de DNS")

    # --------------------------------------------------
    print("[4] TESTE BÁSICO DE CONECTIVIDADE (PING)")
    print(run(f"ping -c 4 {ALVO}") or "❌ Falha no teste de ping")

    # --------------------------------------------------
    print("[5] ANÁLISE DE ROTA E LATÊNCIA (MTR)")
    if comando_existe("mtr"):
        print(run(f"mtr -r -c 10 {ALVO}"))
    else:
        print("mtr não disponível")

    # --------------------------------------------------
    print("[6] CONEXÕES ATIVAS")
    print(run("ss -tunap"))

    # --------------------------------------------------
    print("[7] PORTAS EM ESCUTA")
    print(run("ss -tulnp"))

    # --------------------------------------------------
    print("[8] PROCESSOS UTILIZANDO A REDE (LSOF)")
    print(run("lsof -i -n -P | head -n 20"))

    # --------------------------------------------------
    print("[9] USO DE BANDA POR PROCESSO (NETHOGS - SNAPSHOT)")
    if comando_existe("nethogs"):
        print(run(f"timeout 10 nethogs -t {INTERFACE}"))
    else:
        print("nethogs não disponível")

    # --------------------------------------------------
    print("[10] VISÃO GERAL DO TRÁFEGO (IFTOP - SNAPSHOT)")
    if comando_existe("iftop"):
        print(run(f"timeout 10 iftop -t -i {INTERFACE}"))
    else:
        print("iftop não disponível")

    # --------------------------------------------------
    print("[11] ESTATÍSTICAS DE TRÁFEGO DA INTERFACE (VNSTAT)")
    if comando_existe("vnstat"):
        print(run(f"vnstat -i {INTERFACE}"))
    else:
        print("vnstat não disponível")

    # --------------------------------------------------
    print("[12] AMOSTRA DE CAPTURA DE PACOTES (TCPDUMP)")
    if comando_existe("tcpdump"):
        print(run(f"timeout 10 tcpdump -i {INTERFACE} -nn -c 50"))
    else:
        print("tcpdump não disponível")

    # --------------------------------------------------
    print("[13] FIREWALL")
    if comando_existe("iptables"):
        print("→ iptables:")
        print(run("iptables -L -n | head -n 20"))
    else:
        print("iptables não disponível")

    if comando_existe("nft"):
        print("→ nftables:")
        print(run("nft list ruleset | head -n 20"))
    else:
        print("nftables não disponível")

    # --------------------------------------------------
    print("[14] POSSÍVEIS CAUSAS DE CONEXÃO INDISPONÍVEL")
    if "DOWN" in run(f"ip link show {INTERFACE}"):
        print("❌ Interface está DOWN")
    else:
        print("✔ Interface está UP")

    if "default" not in run("ip route"):
        print("❌ Gateway padrão não configurado")

    if not run(f"getent hosts {TESTE_DNS}"):
        print("❌ DNS não está resolvendo nomes")

    if "0 received" in run(f"ping -c1 {ALVO}"):
        print("❌ Sem conectividade externa")

    print("\n==================================================")
    print(" FIM DO RELATÓRIO")
    print(f" Relatório salvo em: {RELATORIO}")
    print("==================================================")

# Restaura stdout
sys.stdout = sys.__stdout__
print(f"✔ Diagnóstico concluído. Relatório gerado em: {RELATORIO}")
