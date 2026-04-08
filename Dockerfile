FROM tobix/pywine:3.12

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/
COPY data/ ./data/
COPY __main__.py .

# Устанавливаем зависимости через Wine-Python
RUN wine python -m pip install --upgrade pip && \
    wine python -m pip install \
        openpyxl \
        pandas \
        python-calamine \
        xlsxwriter \
        pyinstaller

# Переопределяем tmp-директорию на Windows-путь
ENV TEMP=C:\\Temp
ENV TMP=C:\\Temp

RUN wine python -m PyInstaller \
    --onefile \
    --name cnm_scrypt \
    --add-data "data;data" \
    --hidden-import python_calamine \
    --hidden-import openpyxl \
    --hidden-import pandas \
    --hidden-import xlsxwriter \
    --distpath "C:\\dist" \
    __main__.py && \
    cp -r /root/.wine/drive_c/dist ./dist
