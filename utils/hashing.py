import uuid
from schemas.carbon_credits import RegisterCredit #RetireCredit

NAMESPACE = uuid.UUID("87965734-1234-5678-1234-567812345678")

def uuid_generate(data : RegisterCredit)-> str:
    """ generate the same uuid for same same input always. """
    credit_data = f"{data.project_name}:{data.registry}:{data.vintage}:{data.quantity}:{data.serial_number}"

    return str(uuid.uuid5(NAMESPACE, credit_data))