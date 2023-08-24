from enum import Enum, IntEnum


class Status(Enum):
    OK = "ok"
    ACCOUNT_ALREADY_EXISTS = "account already exists"
    ACCOUNT_REGISTER_ERROR = "account registration error"
    ACCOUNT_DOES_NOT_EXIST = "account does not exist"
    USER_ALREADY_LOGGED_IN = "user already logged in"
    USER_NOT_LOGGED_IN = "user not logged in"
    USER_SETUP_ERROR = "user setup error"
    USER_NOT_FOUND = "User not found"
    APPLICATION_CREATE_ERROR = "application creation error"
    APPLICATION_DOES_NOT_EXIST = "application does not exist"
    APPLICATION_UPDATE_ERROR = "application update failed"
    APPLICATION_INTERACTION_ERROR = "application interaction failed"
    APPLICATION_DELETE_ERROR = "application deletion failed"
    ERROR_CREATING_COMPANY = "Error occurred creating company"
    COMPANY_DOES_NOT_EXIST = "Company does not exist"
    ERROR_DELETING_COMPANY = "Error occurred while deleting company"
    UNSUPPORTED_IMAGE_FORMAT = "Unsupported image format"


class HttpResponseCode(IntEnum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500


STATUS_HTTP_MAPPING = {
    Status.OK: HttpResponseCode.SUCCESS,
    Status.ACCOUNT_ALREADY_EXISTS: HttpResponseCode.BAD_REQUEST,
    Status.ACCOUNT_REGISTER_ERROR: HttpResponseCode.SERVER_ERROR,
    Status.USER_ALREADY_LOGGED_IN: HttpResponseCode.BAD_REQUEST,
    Status.ACCOUNT_DOES_NOT_EXIST: HttpResponseCode.BAD_REQUEST,
    Status.USER_NOT_LOGGED_IN: HttpResponseCode.BAD_REQUEST,
    Status.APPLICATION_CREATE_ERROR: HttpResponseCode.SERVER_ERROR,
    Status.APPLICATION_DOES_NOT_EXIST: HttpResponseCode.BAD_REQUEST,
    Status.APPLICATION_UPDATE_ERROR: HttpResponseCode.SERVER_ERROR,
    Status.ERROR_CREATING_COMPANY: HttpResponseCode.SERVER_ERROR,
    Status.COMPANY_DOES_NOT_EXIST: HttpResponseCode.NOT_FOUND,
    Status.ERROR_DELETING_COMPANY: HttpResponseCode.SERVER_ERROR,
    Status.USER_NOT_FOUND: HttpResponseCode.NOT_FOUND,
    Status.UNSUPPORTED_IMAGE_FORMAT: HttpResponseCode.BAD_REQUEST,
}
