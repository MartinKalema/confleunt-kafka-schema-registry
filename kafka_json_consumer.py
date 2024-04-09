from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
ENDPOINT_SCHEMA_URL  = os.getenv('ENDPOINT_SCHEMA_URL')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
BOOTSTRAP_SERVER = os.getenv('BOOTSTRAP_SERVER')
SECURITY_PROTOCOL = os.getenv('SECURITY_PROTOCOL')
SSL_MACHENISM = os.getenv('SSL_MACHENISM')
SCHEMA_REGISTRY_API_KEY = os.getenv('SCHEMA_REGISTRY_API_KEY')
SCHEMA_REGISTRY_API_SECRET = os.getenv('SCHEMA_REGISTRY_API_SECRET')

def sasl_conf():

    sasl_conf = {'sasl.mechanism': SSL_MACHENISM,
                 # Set to SASL_SSL to enable TLS support.
                #  'security.protocol': 'SASL_PLAINTEXT'}
                'bootstrap.servers':BOOTSTRAP_SERVER,
                'security.protocol': SECURITY_PROTOCOL,
                'sasl.username': API_KEY,
                'sasl.password': API_SECRET_KEY
                }
    return sasl_conf



def schema_config():
    return {'url':ENDPOINT_SCHEMA_URL,
    
    'basic.auth.user.info':f"{SCHEMA_REGISTRY_API_KEY}:{SCHEMA_REGISTRY_API_SECRET}"

    }


class Car:   
    def __init__(self,record:dict):
        for k,v in record.items():
            setattr(self,k,v)
        
        self.record=record
   
    @staticmethod
    def dict_to_car(data:dict,ctx):
        return Car(record=data)

    def __str__(self):
        return f"{self.record}"


def main(topic):

#     schema_str = """
#     {
#   "$id": "http://example.com/myURI.schema.json",
#   "$schema": "http://json-schema.org/draft-07/schema#",
#   "additionalProperties": false,
#   "description": "Sample schema to help you get started.",
#   "properties": {
#     "brand": {
#       "description": "The type(v) type is used.",
#       "type": "string"
#     },
#     "car_name": {
#       "description": "The type(v) type is used.",
#       "type": "string"
#     },
#     "engine": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     },
#     "fuel_type": {
#       "description": "The type(v) type is used.",
#       "type": "string"
#     },
#     "km_driven": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     },
#     "max_power": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     },
#     "mileage": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     },
#     "model": {
#       "description": "The type(v) type is used.",
#       "type": "string"
#     },
#     "seats": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     },
#     "seller_type": {
#       "description": "The type(v) type is used.",
#       "type": "string"
#     },
#     "selling_price": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     },
#     "transmission_type": {
#       "description": "The type(v) type is used.",
#       "type": "string"
#     },
#     "vehicle_age": {
#       "description": "The type(v) type is used.",
#       "type": "number"
#     }
#   },
#   "title": "SampleRecord",
#   "type": "object"
# }
#     """

    # Client Object
    schema_registry_client = SchemaRegistryClient(schema_config()) 

     # latest schema
    schema = schema_registry_client.get_schema(schema_registry_client.get_latest_version(topic + "-value").schema_id)

    # Create deserializer object
    json_deserializer = JSONDeserializer(schema.schema_str,
                                         from_dict=Car.dict_to_car)

    consumer_conf = sasl_conf()
    consumer_conf.update({
                     'group.id': 'group1',
                     'auto.offset.reset': "latest"})

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])


    while True:
        try:
            # SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            car = json_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

            if car is not None:
                print("User record {}: car: {}\n"
                      .format(msg.key(), car))
        except KeyboardInterrupt:
            break

    consumer.close()

main("topic_0")