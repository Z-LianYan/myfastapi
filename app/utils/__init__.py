from fastapi import Request

def get_client_info(request: Request):
    headers = request.headers

    ip = (
        headers.get("X-Forwarded-For")
        or headers.get("X-Real-IP")
        or request.client.host
    )
    user_agent = request.headers.get("user-agent")

    return {
        "ip": ip.split(",")[0].strip(),
        "user_agent": user_agent
    }