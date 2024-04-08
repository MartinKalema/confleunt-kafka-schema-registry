#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from uuid import uuid4
from six.moves import input
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer
#from confluent_kafka.schema_registry import *
import pandas as pd
from typing import List

FILE_PATH = "/home/kalema/Projects/data-engineering/confluent-kafka-schema-registry/cardekho_dataset.csv"
columns=['car_name', 'brand', 'model', 'vehicle_age', 'km_driven', 'seller_type',
       'fuel_type', 'transmission_type', 'mileage', 'engine', 'max_power',
       'seats', 'selling_price']

API_KEY = 'E2YGQQM72GSVUFA4'
ENDPOINT_SCHEMA_URL  = 'https://psrc-9jzo5.us-central1.gcp.confluent.cloud'
API_SECRET_KEY = 'emXnHoh11pc7jctD6CBSkgT+K2lMHEm5EGf+WBGMIXpM8FUZJqMHFTqeX4lDYB6T'
BOOTSTRAP_SERVER = 'pkc-12576z.us-west2.gcp.confluent.cloud:9092'
SECURITY_PROTOCOL = 'SASL_SSL'
SSL_MACHENISM = 'PLAIN'
SCHEMA_REGISTRY_API_KEY = 'P5U2TEKAHVBFPHZU'
SCHEMA_REGISTRY_API_SECRET = 'TeIuTyU0PhRU3HWEYLmUmi2boTsZx1NZL4p+RDgczQq28XovwwxYj4Wg/G8/vqE4'