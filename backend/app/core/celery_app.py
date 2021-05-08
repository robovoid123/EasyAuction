from celery import Celery

celery_app = Celery(
    "worker",
    backend=None,
    broker=None,
)

celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}
