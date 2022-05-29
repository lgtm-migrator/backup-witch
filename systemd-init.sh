SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

ExecStart="python3 ${SCRIPT_DIR}/src/main.py"

read -r -d '' SERVICE << EOM
[Unit]
Description=backup-witch
After=network-online.target
Wants=network-online.target systemd-networkd-wait-online.service

StartLimitIntervalSec=600
StartLimitBurst=5

[Service]
Type=exec
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=${SCRIPT_DIR}

Restart=on-failure
RestartSec=60s

ExecStart=${ExecStart}

[Install]
WantedBy=default.target

EOM

mkdir -p ~/.config/systemd/user/ && printf "%s" "$SERVICE" > "${_}/backup-witch.service"
