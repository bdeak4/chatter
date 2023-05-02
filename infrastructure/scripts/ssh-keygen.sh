#!/bin/sh

env=$1
if [ -z "$env" ]; then
  echo "Usage: $0 <env>"
  exit 1
fi
cd "$(dirname "$0")" || exit 1

ssh_keys="../ssh-keys"

ssh-keygen -t ed25519 -C "$env" -N "" -f "$ssh_keys/$env"
mv "$ssh_keys/$env" "$ssh_keys/$env.enc"
sops -e -i "$ssh_keys/$env.enc"
