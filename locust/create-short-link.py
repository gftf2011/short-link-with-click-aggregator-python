import os
import random
import string

from locust import HttpUser, constant, task


def _rand_url() -> str:
    token = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"https://example.com/{token}"


class CreateShortLinkUser(HttpUser):

    # Defaults to http://localhost:8080 when running `locust` without -H.
    host = os.getenv("LOCUST_HOST", "http://localhost:8080")
    wait_time = constant(1.0)

    @task
    def create_shortlink(self) -> None:
        payload: dict[str, str] = {"url": _rand_url()}

        with self.client.post(
            "/v1/shortlink",
            json=payload,
            name="POST /v1/shortlink",
            catch_response=True,
        ) as resp:
            if resp.status_code != 201:
                resp.failure(f"expected 201, got {resp.status_code}: {resp.text}")
                return
