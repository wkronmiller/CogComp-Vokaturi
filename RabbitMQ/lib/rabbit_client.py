"""
Client for RabbitMQ
"""
import pika

def _on_channel(_):
    """
    Default channel open handler:
    Print alert when channel is opened
    """
    print "Channel opened"

AUDIO_EXCHANGE = 'raw_audio'
LOGS_EXCHANGE = 'logs'

class RabbitConnection(object):
    """
    Connection handler for RabbitMQ
    """

    def __init__(self, hostname, port):
        """
        Connect to RabbitMQ server with specified hostname and port
        """
        self.connection = pika.adapters.select_connection \
                                       .SelectConnection(parameters=pika \
                                        .ConnectionParameters(hostname, port),
                                                         on_open_callback=self._on_open,
                                                         on_close_callback=self._on_close)
        self.connected = False
        self._channel_callbacks = [_on_channel]

    def _on_channel(self, channel):
        print "Creating exchanges"
        for exchange in [AUDIO_EXCHANGE, LOGS_EXCHANGE]:
            channel.exchange_declare(exchange=exchange, type='fanout')
        print "Launching callbacks"
        for callback in self._channel_callbacks:
            callback(channel)

    def _on_open(self, *_):
        """
        Handler for connection creation
        """
        print "RabbitMQ connection opened"
        self.connected = True
        self.connection.channel(self._on_channel)

    def _on_close(self, *_):
        """
        Handler for connection closure
        """
        print "Rabbit connection closed"
        self.connected = False

    def register_callback(self, callback):
        """
        Add a callback when channel is available
        """
        self._channel_callbacks.append(callback)
        return len(self._channel_callbacks) - 1

    def add_audio_incoming_callback(self, callback):
        """
        Register callback to recieve audio data
        """
        def _start_processing(channel):
            def _handle_audio(*args):
                audio_data = args[3]
                callback(audio_data)

            def _start_consuming(_):
                print "Starting to consume messages"
                channel.basic_consume(_handle_audio, AUDIO_EXCHANGE)

            def _handle_queue_bind(_):
                print "Binding to queue"
                channel.queue_bind(_start_consuming, AUDIO_EXCHANGE, AUDIO_EXCHANGE)

            channel.queue_declare(_handle_queue_bind, AUDIO_EXCHANGE)
            print "Starting to process audio"
            channel.basic_consume(_handle_audio, no_ack=True)
        self._channel_callbacks.append(_start_processing)

    def start(self):
        """
        Start waiting for events
        """
        self.connection.ioloop.start()

    def stop(self):
        """
        Close RabbitMQ connection
        """
        self.connection.close()
