import time
import google.api_core.exceptions

def run_with_retry(func, *args, **kwargs):
    max_retries = 5
    base_delay = 5
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Check for 429 or ResourceExhausted
            error_str = str(e).lower()
            if "429" in error_str or "resource_exhausted" in error_str or "exhausted" in error_str:
                if attempt == max_retries - 1:
                    raise e
                
                wait_time = base_delay * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise e
