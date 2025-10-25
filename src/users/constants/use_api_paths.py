# User API Paths Constants

# Base endpoint
BASE_PATH = "/api/v1/users"

# User CRUD operations
CREATE_USER = f"{BASE_PATH}"
GET_ALL_USERS = f"{BASE_PATH}"
GET_USER = f"{BASE_PATH}/{{user_id}}"
UPDATE_USER = f"{BASE_PATH}/{{user_id}}"
DELETE_USER = f"{BASE_PATH}/{{user_id}}"

# HTTP Methods mapping
USER_ENDPOINTS = {
    "create": {"path": CREATE_USER, "method": "POST"},
    "get_all": {"path": GET_ALL_USERS, "method": "GET"},
    "get_one": {"path": GET_USER, "method": "GET"},
    "update": {"path": UPDATE_USER, "method": "PUT"},
    "delete": {"path": DELETE_USER, "method": "DELETE"},
}