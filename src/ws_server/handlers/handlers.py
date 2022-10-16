from exceptions.server_exceptions import WrongRequestData
from ws_server.business_logic.add_new_url import AddNewURL
from ws_server.business_logic.get_all_url_statuses import GetAllURLStatuses
from ws_server.core.structs import Request, Response
from ws_server.handlers.base import BaseHandler


class HTTPClientStatusHandler(BaseHandler):
    """
    Handles the situation when status of the HTTP-client must be
    retrieved.
    """

    command = GetAllURLStatuses()

    async def handle(self, request: Request):
        """Returns all URLs and their statuses."""
        return Response(self.command.execute())


class AddNewUrlHandler(BaseHandler):
    """
    Handles the situation when new url is added to a download queue.
    """

    command = AddNewURL()

    async def handle(self, request: Request):
        """Adds a URL to the download queue if it is possible."""
        try:
            is_added = await self.command.execute(request.data.get('url'))
        except WrongRequestData as e:
            return self.construct_response(e.detail)
        return self.construct_response(
            "URL has been added." if is_added
            else "URL can't be added. It is processing or is already processed."
        )

    @staticmethod
    def construct_response(message: str) -> Response:
        """Constructs a response with a given message."""
        return Response({'message': message})
