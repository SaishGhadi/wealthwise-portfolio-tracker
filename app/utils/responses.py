def success_response(data=None, message="OK"):
    return {
        "status": "success",
        "data": data,
        "message": message
    }

def error_response(message="Error", status_code=400):
    return {
        "status": "error",
        "message": message,
        "code": status_code
    }
