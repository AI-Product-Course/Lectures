from locust import HttpUser, task, between


class BookAPITester(HttpUser):
    wait_time = between(0.5, 3.0)

    def on_start(self):
        pass

    def on_stop(self):
        pass

    @task(1)
    def get_books(self):
        self.client.get("/")
