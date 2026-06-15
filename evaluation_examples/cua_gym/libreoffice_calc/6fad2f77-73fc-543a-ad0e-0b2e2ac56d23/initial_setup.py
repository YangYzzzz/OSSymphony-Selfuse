"""
Initial Setup: VSCode workspace for Sphinx/reStructuredText documentation project
Task ID: vscode_cm_092
Domain: vscode

Creates a Sphinx documentation project structure at /home/user/projects/docs_project
and opens it in VSCode. Does NOT install extensions, configure settings, or create tasks.
"""

import os
import shlex
import subprocess
import time
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_cm_092'
PROJECT_DIR = f'{WORKDIR}/projects/docs_project'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)

def create_initial():
    # Create project directory structure
    os.makedirs(PROJECT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'source'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'source', '_static'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'source', '_templates'), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_DIR, 'build'), exist_ok=True)

    # Create conf.py - Sphinx configuration
    conf_py = '''\
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = 'DataFlow Analytics Platform'
copyright = '2025, DataFlow Engineering Team'
author = 'Sarah Chen, Marcus Johnson, Elena Rodriguez'
release = '2.4.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
html_title = 'DataFlow Analytics Platform Documentation'

# -- Extension configuration -------------------------------------------------
todo_include_todos = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'conf.py'), 'w') as f:
        f.write(conf_py)

    # Create index.rst
    index_rst = '''\
.. DataFlow Analytics Platform documentation master file

Welcome to DataFlow Analytics Platform
=======================================

DataFlow is an enterprise-grade data analytics platform designed for real-time
stream processing and batch analytics. Built on Apache Kafka and Apache Flink,
it provides seamless integration with cloud-native infrastructure.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   architecture
   api-reference
   deployment
   troubleshooting

Key Features
------------

* **Real-time Stream Processing** - Process millions of events per second with sub-millisecond latency
* **Batch Analytics** - Run complex analytical queries on petabyte-scale datasets
* **Multi-tenant Architecture** - Secure isolation between organizational units
* **Auto-scaling** - Dynamically adjust compute resources based on workload
* **Comprehensive API** - RESTful and gRPC interfaces for all platform operations

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'index.rst'), 'w') as f:
        f.write(index_rst)

    # Create getting-started.rst
    getting_started = '''\
Getting Started
===============

This guide walks you through setting up your first DataFlow analytics pipeline.

Prerequisites
-------------

Before you begin, ensure you have the following installed:

* Python 3.9 or later
* Docker and Docker Compose
* kubectl (for Kubernetes deployments)
* The DataFlow CLI tool (``dfctl``)

Installation
------------

Install the DataFlow SDK using pip:

.. code-block:: bash

   pip install dataflow-analytics
   dfctl init --project my-first-pipeline

Configuration
-------------

Create a configuration file at ``~/.dataflow/config.yaml``:

.. code-block:: yaml

   cluster:
     endpoint: https://dataflow.example.com
     region: us-west-2
   auth:
     method: oauth2
     client_id: your-client-id

Quick Start Example
-------------------

Here is a minimal example of a streaming pipeline:

.. code-block:: python

   from dataflow import Pipeline, KafkaSource, S3Sink

   pipeline = Pipeline("user-events-etl")
   source = KafkaSource(topic="user-events", group="analytics")
   sink = S3Sink(bucket="datalake", prefix="events/")

   pipeline.add_stage(source)
   pipeline.add_stage(sink)
   pipeline.run()

.. todo::

   Add section on authentication token refresh workflow.
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'getting-started.rst'), 'w') as f:
        f.write(getting_started)

    # Create architecture.rst
    architecture = '''\
Architecture Overview
=====================

DataFlow follows a microservices architecture with event-driven communication
between components.

Core Components
---------------

Ingestion Layer
^^^^^^^^^^^^^^^

The ingestion layer handles data intake from multiple sources including:

* Apache Kafka topics
* HTTP webhooks
* Cloud storage (S3, GCS, Azure Blob)
* Database change data capture (CDC)

Each ingestion endpoint supports configurable batching with the ``BatchConfig``
class:

.. code-block:: python

   from dataflow.config import BatchConfig

   config = BatchConfig(
       max_batch_size=1000,
       flush_interval_ms=500,
       compression="snappy"
   )

Processing Engine
^^^^^^^^^^^^^^^^^

The processing engine uses Apache Flink under the hood with a simplified
Python API. It supports both streaming and batch processing modes.

Storage Layer
^^^^^^^^^^^^^

DataFlow uses a tiered storage architecture:

1. **Hot storage** - Apache Kafka for real-time access (retention: 7 days)
2. **Warm storage** - Apache Parquet files on object storage
3. **Cold storage** - Compressed archives for compliance and auditing

Deployment Topology
-------------------

.. list-table:: Service Resource Requirements
   :header-rows: 1
   :widths: 25 15 15 20 25

   * - Service
     - CPU Cores
     - Memory (GB)
     - Storage (GB)
     - Scaling Policy
   * - Ingestion Gateway
     - 4
     - 8
     - 50
     - Horizontal (2-16 replicas)
   * - Stream Processor
     - 8
     - 32
     - 200
     - Horizontal (4-64 replicas)
   * - Query Engine
     - 16
     - 64
     - 500
     - Vertical + Horizontal
   * - Metadata Store
     - 2
     - 4
     - 100
     - Primary-Replica
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'architecture.rst'), 'w') as f:
        f.write(architecture)

    # Create api-reference.rst
    api_reference = '''\
API Reference
=============

This section documents the DataFlow REST API and Python SDK.

Authentication
--------------

All API requests require a valid Bearer token:

.. code-block:: bash

   curl -H "Authorization: Bearer <token>" \\
        https://api.dataflow.example.com/v2/pipelines

Pipeline Management
-------------------

.. http:get:: /v2/pipelines

   List all pipelines in the current workspace.

   **Response:**

   .. code-block:: json

      {
        "pipelines": [
          {
            "id": "pipe-abc123",
            "name": "user-events-etl",
            "status": "running",
            "created_at": "2025-03-15T10:30:00Z"
          }
        ]
      }

.. http:post:: /v2/pipelines

   Create a new pipeline.

   :jsonparam string name: Pipeline name (required)
   :jsonparam object config: Pipeline configuration
   :statuscode 201: Pipeline created successfully
   :statuscode 400: Invalid configuration

Python SDK
----------

.. autoclass:: dataflow.Pipeline
   :members:

.. autofunction:: dataflow.connect
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'api-reference.rst'), 'w') as f:
        f.write(api_reference)

    # Create deployment.rst
    deployment = '''\
Deployment Guide
================

DataFlow supports multiple deployment targets including Kubernetes,
Docker Compose, and bare-metal installations.

Kubernetes Deployment
---------------------

Use Helm to deploy DataFlow to a Kubernetes cluster:

.. code-block:: bash

   helm repo add dataflow https://charts.dataflow.example.com
   helm install dataflow dataflow/dataflow-platform \\
     --namespace analytics \\
     --set global.storageClass=gp3 \\
     --set ingestion.replicas=4

Docker Compose (Development)
-----------------------------

For local development, use the provided Docker Compose configuration:

.. code-block:: bash

   git clone https://github.com/dataflow/platform.git
   cd platform
   docker-compose -f docker-compose.dev.yml up -d

Environment Variables
---------------------

.. list-table::
   :header-rows: 1

   * - Variable
     - Default
     - Description
   * - ``DATAFLOW_CLUSTER_ENDPOINT``
     - ``localhost:9090``
     - Cluster API endpoint
   * - ``DATAFLOW_LOG_LEVEL``
     - ``INFO``
     - Logging verbosity (DEBUG, INFO, WARN, ERROR)
   * - ``DATAFLOW_MAX_WORKERS``
     - ``auto``
     - Number of worker threads (auto = CPU count)
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'deployment.rst'), 'w') as f:
        f.write(deployment)

    # Create troubleshooting.rst
    troubleshooting = '''\
Troubleshooting
===============

Common issues and their resolutions.

Pipeline Failures
-----------------

**Symptom:** Pipeline status shows ``FAILED`` with error code ``E_KAFKA_TIMEOUT``

**Cause:** The Kafka broker is unreachable or the topic does not exist.

**Resolution:**

1. Verify Kafka connectivity:

   .. code-block:: bash

      dfctl diagnose kafka --broker kafka.example.com:9092

2. Check topic existence:

   .. code-block:: bash

      dfctl topics list --cluster production

3. Recreate the topic if necessary:

   .. code-block:: bash

      dfctl topics create user-events --partitions 12 --replication-factor 3

Memory Issues
-------------

**Symptom:** ``OutOfMemoryError`` in stream processor logs

**Resolution:** Increase the JVM heap size in the deployment configuration:

.. code-block:: yaml

   streamProcessor:
     jvmOpts: "-Xmx4g -Xms2g"
     resources:
       limits:
         memory: 6Gi

Performance Tuning
------------------

For high-throughput scenarios, consider the following optimizations:

* Enable compression: ``compression: snappy`` reduces network I/O by 60-70%
* Increase batch size: Larger batches improve throughput at the cost of latency
* Use partition keys: Ensures related events are processed in order
* Enable checkpointing: ``checkpoint_interval_ms: 30000`` for fault tolerance
'''
    with open(os.path.join(PROJECT_DIR, 'source', 'troubleshooting.rst'), 'w') as f:
        f.write(troubleshooting)

    # Create Makefile
    makefile = '''\
# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make mode" may be run without a target.
help:
\t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
\t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
'''
    with open(os.path.join(PROJECT_DIR, 'Makefile'), 'w') as f:
        f.write(makefile)

    # Create make.bat (for completeness)
    make_bat = '''\
@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
\tset SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
\techo.
\techo.The 'sphinx-build' command was not found.
\tgoto end
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:end
popd
'''
    with open(os.path.join(PROJECT_DIR, 'make.bat'), 'w') as f:
        f.write(make_bat)

    # Create .vscode directory (empty - no settings yet, agent needs to configure)
    os.makedirs(os.path.join(PROJECT_DIR, '.vscode'), exist_ok=True)

    print(f'Initial project created: {PROJECT_DIR}')
    print(f'Project structure:')
    for root, dirs, files in os.walk(PROJECT_DIR):
        level = root.replace(PROJECT_DIR, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

    # GUI-ready startup: Open VSCode with the project folder
    launch_gui(f'code "{PROJECT_DIR}"', delay_sec=2.0)
    print('GUI_READY: launched VSCode with DISPLAY=:0')

create_initial()
