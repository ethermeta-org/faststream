from typing import Any, Dict, Optional

from faststream._compat import override
from faststream.nats.asyncapi import Publisher
from faststream.nats.shared.router import NatsRouter as BaseRouter


class NatsRouter(BaseRouter):
    _publishers: Dict[str, Publisher]  # type: ignore[assignment]

    @override
    @staticmethod
    def _get_publisher_key(publisher: Publisher) -> str:  # type: ignore[override]
        return publisher.subject

    @override
    @staticmethod
    def _update_publisher_prefix(  # type: ignore[override]
        prefix: str,
        publisher: Publisher,
    ) -> Publisher:
        publisher.subject = prefix + publisher.subject
        return publisher

    @override
    def publisher(  # type: ignore[override]
        self,
        subject: str,
        headers: Optional[Dict[str, str]] = None,
        reply_to: str = "",
        # AsyncAPI information
        title: Optional[str] = None,
        description: Optional[str] = None,
        schema: Optional[Any] = None,
    ) -> Publisher:
        new_publisher = self._update_publisher_prefix(
            self.prefix,
            Publisher(
                subject=subject,
                reply_to=reply_to,
                headers=headers,
                title=title,
                _description=description,
                _schema=schema,
            ),
        )
        publisher_key = self._get_publisher_key(new_publisher)
        publisher = self._publishers[publisher_key] = self._publishers.get(
            publisher_key, new_publisher
        )
        return publisher
