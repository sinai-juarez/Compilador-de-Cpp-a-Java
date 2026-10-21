#!/bin/sh
# Doble clic en macOS: abre la interfaz del compilador.
cd "$(dirname "$0")" || exit 1
exec sh iniciar.sh
