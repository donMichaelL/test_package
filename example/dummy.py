# noqa: INP001
import json
from dataclasses import dataclass

from theTrial import TheTrial


@dataclass
class Customer:
    id: int
    name: str
    email: str

    def serializer(self) -> str:
        return json.dumps(self.__dict__)


app = TheTrial()


@app.outopic("test")
def consumer():
    customer = Customer(id=1, name="John Doe", email="john@example.com")
    return customer


if __name__ == "__main__":
    # Running the app
    app.run()
