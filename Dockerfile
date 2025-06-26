# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/default-java

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    wget \
    curl \
    unzip \
    default-jre \
    default-jdk \
    build-essential \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install samtools with proper dependencies
RUN wget https://github.com/samtools/samtools/releases/download/1.17/samtools-1.17.tar.bz2 \
    && tar -xjf samtools-1.17.tar.bz2 \
    && cd samtools-1.17 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd .. \
    && rm -rf samtools-1.17*

# Install htslib separately with all plugins
RUN wget https://github.com/samtools/htslib/releases/download/1.17/htslib-1.17.tar.bz2 \
    && tar -xjf htslib-1.17.tar.bz2 \
    && cd htslib-1.17 \
    && ./configure --prefix=/usr/local --enable-plugins --enable-libcurl \
    && make \
    && make install \
    && cd .. \
    && rm -rf htslib-1.17*

# Set up plugin path for htslib
ENV HTSLIB_PLUGIN_PATH=/usr/local/lib/htslib

# Install QualiMap v2.3 (with error handling)
RUN wget https://bitbucket.org/kokonech/qualimap/downloads/qualimap_v2.3.zip && \
    unzip qualimap_v2.3.zip && \
    mv qualimap_v2.3 /opt/qualimap && \
    chmod +x /opt/qualimap/qualimap && \
    ln -s /opt/qualimap/qualimap /usr/local/bin/qualimap && \
    rm qualimap_v2.3.zip || \
    (echo "QualiMap installation failed, trying alternative source..." && \
     wget https://github.com/bioconda/bioconda-recipes/raw/master/recipes/qualimap/qualimap_v2.2.1.zip -O qualimap.zip && \
     unzip qualimap.zip && \
     mv qualimap_v2.2.1 /opt/qualimap && \
     chmod +x /opt/qualimap/qualimap && \
     ln -s /opt/qualimap/qualimap /usr/local/bin/qualimap && \
     rm qualimap.zip)

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.fileWatcherType=none", \
    "--browser.gatherUsageStats=false"]
