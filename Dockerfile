FROM apache/airflow:3.0.3-python3.10

USER root

# Install system packages including bash
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash curl wget procps gcc g++ python3-dev \
        unixodbc-dev libsasl2-dev libpq-dev python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Java (OpenJDK 11)
RUN wget -qO openjdk11.tar.gz https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_linux-x64_bin.tar.gz && \
    tar -xzf openjdk11.tar.gz -C /opt && \
    mv /opt/jdk-11* /opt/java11 && \
    rm openjdk11.tar.gz

# Install Spark 3.5.0 with Hadoop 3
RUN curl -L -o spark.tgz https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz && \
    tar -xzf spark.tgz && \
    mv spark-3.5.0-bin-hadoop3 /opt/spark && \
    rm spark.tgz

# Set environment variables
ENV JAVA_HOME=/opt/java11
ENV SPARK_HOME=/opt/spark
ENV PATH="$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH"
ENV SPARK_LOCAL_IP=127.0.0.1

# Set Spark and Python paths
ENV PYSPARK_PYTHON=/home/airflow/.local/bin/python3 \
    PYSPARK_DRIVER_PYTHON=/home/airflow/.local/bin/python3 
    
# Persist environment variables across sessions
RUN echo "JAVA_HOME=/opt/java11" >> /etc/environment && \
    echo "export JAVA_HOME=/opt/java11" >> /etc/profile && \
    echo "export SPARK_HOME=/opt/spark" >> /etc/profile && \
    echo 'export PATH="$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH"' >> /etc/profile

# Create log/output dirs with proper permissions
RUN mkdir -p /opt/logs /opt/output && \
    touch /opt/logs/streamline.log && \
    chown -R airflow: /opt/logs /opt/output && \
    chmod -R 775 /opt/logs /opt/output

USER airflow

# Install Python dependencies
RUN pip install --no-cache-dir pyarrow pyspark flask findspark twilio
RUN echo "import findspark; findspark.init('/opt/spark')" > /home/airflow/.local/lib/python3.10/site-packages/findspark_auto.pth

