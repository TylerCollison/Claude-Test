import redis
import json
import threading

class RedisConnector:
    """Redis Pub/Sub implementation for agent communication"""

    def __init__(self, config):
        self.redis_url = config.get("REDIS_URL", "redis://localhost:6379")
        self.client = redis.Redis.from_url(self.redis_url)
        self.pubsub = self.client.pubsub()
        self.callbacks = {}
        self.listening = False
        self.thread = None

    def publish(self, topic, message):
        """Publish message to Redis channel"""
        payload = json.dumps(message)
        return self.client.publish(topic, payload)

    def subscribe(self, topic, callback):
        """Subscribe to Redis channel with callback"""
        self.callbacks[topic] = callback
        self.pubsub.subscribe(topic)

    def start_listening(self):
        """Start message listener in background thread"""
        if not self.listening:
            self.listening = True
            self.thread = threading.Thread(target=self._listen)
            self.thread.daemon = True
            self.thread.start()

    def _listen(self):
        """Internal message listener"""
        for message in self.pubsub.listen():
            if message["type"] == "message":
                topic = message["channel"].decode()
                data = json.loads(message["data"])
                if topic in self.callbacks:
                    self.callbacks[topic](data)