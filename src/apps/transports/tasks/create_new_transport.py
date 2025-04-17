import logging

from celery import shared_task

from apps.transports.serializers import TransportSerializer

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=10, name="create_new_transport")
def create_new_transport(self, data, user_id):
    """
    Task to create a new transport.
    """
    try:
        serializer = TransportSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=user_id)
            logger.info("Transport created successfully by user_id: %s", user_id)
            return serializer.data
    except Exception as e:
        logger.error("Error creating transport: %s", str(e))
        raise self.retry(exc=e)




