#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="tobix/pywine:3.12"

if ! sudo docker image inspect "$IMAGE" &>/dev/null; then
  echo "=== Скачивание образа $IMAGE ==="
  sudo docker pull "$IMAGE"
fi

echo "=== Запуск сборки .exe через Docker ($IMAGE) ==="
echo "Проект: $PROJECT_DIR"

sudo docker run --rm \
  -v "$PROJECT_DIR:/src" \
  -w /src \
  "$IMAGE" \
  bash -c "
    set -e

    PYTHON='wine /opt/wineprefix/drive_c/Python/python.exe'

    echo '--- Проверка Python ---'
    xvfb-run \$PYTHON --version

    echo '--- Установка зависимостей ---'
    xvfb-run \$PYTHON -m pip install --upgrade pip --quiet
    xvfb-run \$PYTHON -m pip install --quiet \
      openpyxl \
      pandas \
      python-calamine \
      xlsxwriter \
      pyinstaller

    echo '--- Запуск PyInstaller ---'
    xvfb-run \$PYTHON -m PyInstaller \
      --onefile \
      --console \
      --name cnm_scrypt \
      --add-data 'data;data' \
      --hidden-import openpyxl \
      --hidden-import openpyxl.cell._writer \
      --hidden-import pandas \
      --hidden-import python_calamine \
      --hidden-import xlsxwriter \
      --hidden-import xlsxwriter.workbook \
      --hidden-import xlsxwriter.worksheet \
      --hidden-import xlsxwriter.format \
      --hidden-import zoneinfo \
      --clean \
      --noconfirm \
      __main__.py
  "

echo ""
echo "=== Готово ==="
echo "Файл: $PROJECT_DIR/dist/cnm_scrypt.exe"
