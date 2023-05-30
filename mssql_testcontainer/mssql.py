import time
import signal
import pyodbc
import docker


class SQLServerContainer:
    def __init__(
        self,
        image="mcr.microsoft.com/mssql/server:2019-latest",
        port=1433,
        sa_password="YourPass@1",
        database="temp_db",
        username="SA",
    ):
        self.image = image
        self.port = port
        self.sa_password = sa_password
        self.container = None
        self.database = database
        self.username = username
        signal.signal(signal.SIGINT, self.close)

    def __enter__(self):
        self._create_container()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        if self.container is not None:
            try:
                self._cleanup()
            except:
                pass

    def _create_container(self):
        client = docker.from_env()

        container_config = {
            "image": self.image,
            "ports": {f"{self.port}/tcp": self.port},
            "environment": {"ACCEPT_EULA": "Y", "SA_PASSWORD": self.sa_password},
            "detach": True,
        }

        self.container = client.containers.create(**container_config)
        self.container.start()

        print(
            f"SQL Server container '{self.container.id}' created and started successfully."
        )

    def get_connection_url(self):
        self.wait_until_container_ready()
        connection_string = self.get_connetction_string()
        return f"mssql+pyodbc:///?odbc_connect={connection_string}"

    def get_connetction_string(self, max_retries=10, retry_delay=0.5):
        self.wait_until_container_ready()
        connection_string = self._generate_connection_string()
        retries = 0
        while retries < max_retries:
            try:
                pyodbc.connect(connection_string)
                return connection_string
            except pyodbc.OperationalError:
                retries += 1
                time.sleep(retry_delay)
                print(f"Retrying connection (attempt {retries}/{max_retries})...")

        raise RuntimeError("Unable to connect to the SQL Server container.")

    def _generate_connection_string(self):
        server = f"localhost,{self.port}"
        return f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={self.database};UID={self.username};PWD={self.sa_password}"

    def wait_until_container_ready(self):
        while self.container.status != "running":
            time.sleep(1)
            print("Waiting for Container to get ready.")
            self.container.reload()

    def _cleanup(self):
        if self.container:
            try:
                self.container.stop()
                self.container.remove(force=True)
                print("SQL Server container stopped and removed.")
            except docker.errors.APIError as e:
                print(f"Error occurred while stopping/removing the container: {str(e)}")

    def close(self):
        self._cleanup()

    # def cleanup_handler(self, signum, frame):
