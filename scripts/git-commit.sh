#!/bin/bash

# Verifica si el mensaje del commit fue proporcionado
if [ -z "$1" ]; then
  echo "Por favor, proporciona un mensaje para el commit."
  exit 1
fi

# Comandos de git
git add .
git reset .gitignore
git commit -m "$1"
git push -u origin main