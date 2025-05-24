from openapi_server.apis.task_api_base import BaseTaskApi
from openapi_server.business.usecase.create_task_usecase import create_task_usecase
from openapi_server.logger import log_function
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate


class TaskApiController(BaseTaskApi):
    """Task API Controller."""

    @log_function("INFO")
    async def create_task(
        self,
        task_create: TaskCreate,
    ) -> Task:
        """Create a new task Endpoint.

        Args:
            task_create (TaskCreate): TaskCreate object containing the task details

        Returns:
            Task: Created Task object

        """
        return await create_task_usecase(task_create)

