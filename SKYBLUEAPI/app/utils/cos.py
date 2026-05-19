import os

from dotenv import load_dotenv


load_dotenv()

# 获取 COS URL
# @param path: 路径
# @return: COS URL

def get_cos_url(path: str | None) -> str | None:
    if not path:
        return path

    cos_url = os.getenv("COS_URL", "")
    if not cos_url:
        return path

    return f"{cos_url.rstrip('/')}/{path.lstrip('/')}"
