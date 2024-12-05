from typing import Dict

def load_services() -> Dict[str, str]:
    services = {
        "compute": "Cloud computing service for running virtual machines",
        "storage": "Object storage service for data persistence",
        "database": "Managed database service for various DB engines",
        "network": "Virtual networking and connectivity service",
        "serverless": "Function-as-a-service platform for event-driven compute",
    }
    return dict(sorted(services.items()))


def get_service_description(service_name: str) -> str:
    services_map = load_services()
    # Fetch the description directly
    return services_map.get(service_name, "Service not found")


# Example usage
service_description = get_service_description("network")
print(service_description)

