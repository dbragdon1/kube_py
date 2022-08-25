from pathlib import Path

from kubernetes import client, config
from kubernetes.client.rest import ApiException
import base64

config.load_kube_config()




def create_secret(namespace: str, data: dict[str,str], name: str):

    v1 = client.CoreV1Api()
    

    metadata = client.V1ObjectMeta(name = name, namespace = namespace)
    
    body = client.V1Secret()
    body.api_version = "v1"
    #encoded_data = base64.b64encode(text.encode()).decode()
    body.data = data
    #body.data = {'file': encoded_data}

    body.kind = "Secret"
    body.metadata = {"name": name}
    body.type = "Opaque"
    

    try:

        api_response = v1.create_namespaced_secret(namespace = "argo", body = body, pretty = True)

    except ApiException as e:
        print(e)

def create_secret_from_file(namespace: str, name: str, file_path: Path):
    
    with file_path.open('rb') as f:
        data = {file_path.name: base64.b64encode(f.read()).decode()}

        create_secret(namespace = namespace, name = name, data = data)

data = {'section1': base64.b64encode("hello".encode()).decode()}
    
breakpoint()

config_path = Path("./config/credentials.cfg")

#create_secret(namespace = "argo", data = data, name = "my-secret2", text = "hello")

create_secret_from_file(namespace = "argo", name = "login-creds", file_path = config_path)

#alpine = client.V1Container('my_container', 'alpine:latest')
