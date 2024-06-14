import pdb
import json
from ..core.domain import Request
from confluent_kafka import Producer, KafkaException, SerializingProducer
from confluent_kafka.avro import AvroProducer, CachedSchemaRegistryClient

UTF_8 = 'UTF-8'
ENCODING = UTF_8

class KafkaProducer():
    
    def __init__(self, item: Request):
        super().__init__()
        self.item = item
        kafkaBrokers = ','.join([i for i in item.brokers])
        producer_config = {
            "bootstrap.servers": kafkaBrokers,
            "schema.registry.url": item.schema_registry
        }
        if item.certificate != None:
            producer_config['security.protocol'] = 'SSL'
            producer_config['ssl.ca.location'] = item.certificate.ca_location
            producer_config['ssl.certificate.location'] = item.certificate.cert_location
            producer_config['ssl.key.location'] = item.certificate.key_location
        
        client = CachedSchemaRegistryClient({'url': item.schema_registry})
        
        default_key_schema = ''
        default_value_schema = ''
        
        if item.has_key_schema:
            key_schema_id, key_schema, key_version = client.get_latest_schema(item.topic + '-key')
            default_key_schema = key_schema
            self.key_schema = key_schema
            self.key_schema_id = key_schema_id
        if item.has_value_schema:
            value_schema_id, value_schema, value_version = client.get_latest_schema(item.topic + '-value')
            default_value_schema = value_schema
            self.value_schema = value_schema
            self.value_schema_id = value_schema_id

        self.avro_producer = AvroProducer(
            producer_config,
            default_value_schema=default_key_schema,
            default_key_schema=default_value_schema
        )
        producer_config['value.serializer'] = self.value_serializer
        producer_config['key.serializer'] = self.key_serializer
        props = producer_config.copy()
        del props['schema.registry.url']
        self.producer = SerializingProducer(props)

    def value_serializer(self, value, ctx):
        if self.item.has_value_schema:
            return self.avro_producer._serializer.encode_record_with_schema(ctx.topic, self.value_schema, value)
        return value.encode(ENCODING)
    
    def key_serializer(self, key, ctx):
        if self.item.has_key_schema:
            return self.avro_producer._serializer.encode_record_with_schema(ctx.topic, self.key_schema, key, is_key=True)
        return key.encode(ENCODING)
    
    def produce(self, value, key):
        if self.item.has_key_schema:
            key = json.loads(json.dumps(key))
        if self.item.has_value_schema:
            value = json.loads(json.dumps(value))
        self.producer.produce(topic=self.item.topic, value=value, key=key)
        
    def flush(self):
        self.producer.flush()

def produce(item: Request) -> bool:
    try:
        producer = KafkaProducer(item)
        for record in item.records:
            producer.produce(value=json.loads(json.dumps(record.value)), key=record.key)
        producer.flush()

    except KafkaException as e:
        print('Kafka failure ', e)
        return False
    return True
