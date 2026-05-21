import os
import random
import string
from typing import List, Optional

from locust import HttpUser, constant, events, task
from locust.clients import HttpSession


def _rand_url() -> str:
    token = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"https://example.com/{token}"


SEEDED = False
SEEDED_CODES: List[str] = []


@events.test_start.add_listener
def _seed_shortlinks(environment, **_) -> None:
    global SEEDED
    if SEEDED:
        return

    count = int(os.getenv("LOCUST_SEED_COUNT", "100"))
    base_url = (
        getattr(environment, "host", None)
        or os.getenv("LOCUST_HOST", "").strip()
        or "http://localhost:8080"
    )

    dummy_user = type(
        "SeedUser",
        (),
        {
            "environment": environment,
            "context": staticmethod(lambda: {}),
        },
    )()
    client = HttpSession(
        base_url=base_url,
        request_event=environment.events.request,
        user=dummy_user,
    )

    codes: List[str] = []
    for _i in range(count):
        resp = client.post("/v1/shortlink", json={"url": _rand_url()})
        if resp.status_code != 201:
            raise RuntimeError(f"seed failed: {resp.status_code} {resp.text}")
        codes.append(resp.json()["data"]["code"])

    SEEDED_CODES[:] = codes
    SEEDED = True


class CountUser(HttpUser):
    host = os.getenv("LOCUST_HOST", "http://localhost:8080")
    wait_time = constant(0.2)

    def on_start(self) -> None:
        self._codes = SEEDED_CODES

    def _pick_code(self) -> Optional[str]:
        if not self._codes:
            return None
        return random.choice(self._codes)

    @task
    def get_clicks_count(self) -> None:
        code = self._pick_code()
        if not code:
            return

        with self.client.get(
            f"/v1/clicks/{code}",
            name="/v1/clicks/{code}",
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"expected 200, got {resp.status_code}: {resp.text}")
                return
            data = resp.json().get("data", {})
            if "count" not in data:
                resp.failure(f"missing count in response: {resp.text}")
