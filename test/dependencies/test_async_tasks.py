import pytest
from kombu import Exchange
from nameko.rpc import rpc
from mock import patch
from nameko.standalone.rpc import ServiceRpcProxy
from nameko.testing.services import entrypoint_waiter

from nameko_async_task.dependencies.async_tasks import AsyncTask


exchange_task_test = Exchange(name="task_test")


class TaskTestService:
    name = "task_test"

    async_task = AsyncTask(exchange=exchange_task_test)

    @rpc
    def foo(self, bar):
        self.async_task.run(self.do_foo, bar)
        return "ok, I will do it"

    @async_task.task()
    def do_foo(self, bar):
        return bar * 2



class TestAsyncTask:

    @pytest.fixture
    def container(self, container_factory):
        container = container_factory(TaskTestService)
        container.start()
        return container

    def test_task_decorator(self, rabbit_config, container):
        with entrypoint_waiter(container, "do_foo") as result:
            with ServiceRpcProxy("task_test", rabbit_config) as service_proxy:
                assert service_proxy.foo(1) == "ok, I will do it"

            assert result.get() == 2


class TestAsyncTaskDependency:

    @pytest.fixture
    def patch_consume(self):
        with patch("nameko_async_task.dependencies.async_tasks.consume") as consume:
            yield consume

    def test_passes_consume_args_to_consume(self, patch_consume):
        def wrapped():
            pass

        async_task = AsyncTask(exchange_task_test)

        async_task.task(wrapped=wrapped, prefetch_count=2)

        assert len(patch_consume.call_args_list) == 1
        assert patch_consume.call_args_list[0][1]["prefetch_count"] == 2
