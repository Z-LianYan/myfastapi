import uvicorn
import os

if __name__ == "__main__":
    os.environ.setdefault("ENV", "dev")  # 如果没设置，默认 dev
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )