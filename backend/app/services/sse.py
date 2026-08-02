import json


class SSE:

    @staticmethod
    def event(
        event: str,
        data,
    ) -> str:

        if not isinstance(data, str):
            data = json.dumps(
                data,
                ensure_ascii=False,
            )

        return (
            f"event: {event}\n"
            f"data: {data}\n\n"
        )