from openapi_server.apis.task_api_base import BaseTaskApi
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate


class TaskApiController(BaseTaskApi):
    """Task API Controller"""

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
        return await self.create_task_impl(task_create)
