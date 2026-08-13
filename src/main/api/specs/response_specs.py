from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    @staticmethod
    def expect_status(code: HTTPStatus):
        def confirm(response: Response):
            assert response.status_code == code, response.text
        return confirm

    @staticmethod
    def request_ok():
        return ResponseSpecs.expect_status(HTTPStatus.OK)

    @staticmethod
    def request_created():
        return ResponseSpecs.expect_status(HTTPStatus.CREATED)

    @staticmethod
    def request_bad():
        return ResponseSpecs.expect_status(HTTPStatus.BAD_REQUEST)

    @staticmethod
    def request_unauthorized():
        return ResponseSpecs.expect_status(HTTPStatus.UNAUTHORIZED)

    @staticmethod
    def request_forbidden():
        return ResponseSpecs.expect_status(HTTPStatus.FORBIDDEN)

    @staticmethod
    def request_not_found():
        return ResponseSpecs.expect_status(HTTPStatus.NOT_FOUND)
