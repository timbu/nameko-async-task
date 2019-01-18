from functools import partial

from kombu import Queue
from nameko.messaging import Publisher, consume


def task_routing_key(service_name, task_name):
    return "{}.task.{}".format(service_name, task_name)


class AsyncTaskWrapper:
    def __init__(self, publish_message, service_name):
        self.publish_message = publish_message
        self.service_name = service_name

    def run(self, entrypoint_method, payload):
        self.publish_message(
            payload,
            routing_key=task_routing_key(
                self.service_name, entrypoint_method.__name__
            ),
        )


class AsyncTask(Publisher):
    """
    A DependencyProvider that allows you to execute other marked entrypoints
    (from the same service) asynchronously.

    Implemented as a simple wrapper around the common publish/consume pattern.

    Later we could perhaps genericise and make into a proper entrypoint
        E.g. ::

            from kombu import Exchange
            from nameko_async_task import AsyncTask


            my_service_exchange = Exchange(name="my_service")

            class MyService:

                async_task = AsyncTask(exchange=my_service_exchange)

                @rpc
                def trigger(self):
                    payload = {'x:': 1}
                    self.async_task.run(self.do_work, payload)
                    return 'scheduled'

                @async_task.task()
                def do_work(self, payload):
                    print(payload['x'])
    """

    def __init__(self, exchange):
        self.exchange = exchange
        self.service_name = None
        super().__init__(exchange=exchange)

    def bind(self, container, attr_name):
        self.service_name = container.service_name
        return super().bind(container, attr_name)

    def get_dependency(self, worker_context):
        # TODO - remove when nameko Publisher has extra_headers fixed.
        def publish(msg, **kwargs):
            extra_headers = self.get_message_headers(worker_context)
            self.publisher.publish(msg, extra_headers=extra_headers, **kwargs)

        return AsyncTaskWrapper(publish, self.service_name)

    def task(self, wrapped=None):
        """ Decorator to define a schedulable task method
        """
        if wrapped is None:
            return partial(self.task)

        routing_key = task_routing_key(self.service_name, wrapped.__name__)

        return consume(
            queue=Queue(
                exchange=self.exchange,
                routing_key=routing_key,
                name=routing_key
            ),
        )(wrapped)
