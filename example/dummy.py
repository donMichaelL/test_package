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

    @classmethod
    def desirializer(cls, data: str):
        json_dict = json.loads(data)
        return cls(**json_dict)


app = TheTrial()


@app.intopic("test")
def consumer_no_args():
    print("No Args")


@app.intopic("test")
def consumer_simple(customer: Customer):
    print("Simple: ", customer)
    # customer = Customer(id=1, name="John Doe", email="john@example.com")
    # return customer


@app.intopic("test")
def consumer_full(customer: Customer, **options):
    print("Full: ", customer, options)
    # customer = Customer(id=1, name="John Doe", email="john@example.com")
    # return customer


# @app.outopic("test")
# def producer():
#     customer = Customer(id=1, name="John Doe", email="john@example.com")
#     return customer


if __name__ == "__main__":
    # Running the app
    app.run()
