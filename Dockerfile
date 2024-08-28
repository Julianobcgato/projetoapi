# Use uma imagem base adequada
FROM python:3.12-slim

# Instale dependências necessárias
RUN apt-get update && apt-get install -y \
    wget \
    && wget https://github.com/aquasecurity/trivy/releases/download/v0.35.0/trivy_0.35.0_Linux-64bit.deb \
    && dpkg -i trivy_0.35.0_Linux-64bit.deb \
    && rm trivy_0.35.0_Linux-64bit.deb

# Defina o diretório de trabalho
WORKDIR /app

# Copie o código da aplicação para o contêiner
COPY . /app

# Instale as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta que sua aplicação utiliza
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]





