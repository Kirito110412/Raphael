import time

def with_retry(func, max_retries=3, backoff=2):
    def wrapper(*args, **kwargs):
        for i in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if i == max_retries - 1:
                    raise e
                time.sleep(backoff ** i)
    return wrapper
