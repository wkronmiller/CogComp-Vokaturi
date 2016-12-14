"""
Client for RabbitMQ
"""
import sys
import random
import string
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

    def __make_client(self):
        sys.stderr.write("Creating client\n")
        self.connection = pika.adapters.select_connection \
                                       .SelectConnection(parameters=pika \
                                        .ConnectionParameters(self._hostname, self._port),
                                                         on_open_callback=self._on_open,
                                                         on_close_callback=self._on_close)
        sys.stderr.write("Created client\n")
    def __init__(self, hostname, port):
        """
        Connect to RabbitMQ server with specified hostname and port
        """
        self._hostname = hostname
        self._port = port
        self.__make_client()
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
        sys.stderr.write("RabbitMQ connection opened\n")
        self.connected = True
        self.connection.channel(self._on_channel)

    def _on_close(self, *_):
        """
        Handler for connection closure
        """
        sys.stderr.write("Rabbit connection closed\n")
        self.connection.ioloop.stop()
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
        queue_name = ''.join([random.choice(string.ascii_letters) for _ in range(10)])
        def _start_processing(channel):
            def _handle_audio(*args):
                audio_data = args[3]
                callback(audio_data)

            def _start_consuming(_):
                sys.stderr.write("Starting to consume messages\n")
                channel.basic_consume(_handle_audio, queue=queue_name)

            def _handle_queue_bind(_):
                print "Binding to queue"
                channel.queue_bind(callback=_start_consuming,
                                   queue=queue_name,
                                   exchange=AUDIO_EXCHANGE)

            channel.queue_declare(callback=_handle_queue_bind,
                                  queue=queue_name,
                                  exclusive=True,
                                  auto_delete=True)
            print "Starting to process audio in queue %s" % queue_name
            #channel.basic_consume(_handle_audio, queue_name, no_ack=True)
        self._channel_callbacks.append(_start_processing)

    def start(self):
        """
        Start waiting for events
        """
        print "Starting client"
        self.connection.ioloop.start()

    def stop(self):
        """
        Close RabbitMQ connection
        """
        self.connected = False
        self.connection.close()
