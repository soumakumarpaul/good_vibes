from dotenv import set_key, load_dotenv
import os

class Environment:

    def __init__(self):
        self.env_file = ".env"
        if not os.path.exists(self.env_file):
            with open(self.env_file, "w") as f:
                f.write("#Environment Variables")

    def set_db(self, folder):
        set_key(self.env_file, "DB_PATH", folder)

    def _reload_env(self):
        load_dotenv(dotenv_path=self.env_file, override=True)

    def get_db(self) ->  str:
        self._reload_env()
        return os.environ.get("DB_PATH", "Select Folder to configure DB")
    
    def get_job_id_counter(self) -> int:
        load_dotenv()
        return int(os.environ.get("JOB_ID", 0))
    
    def set_job_id_counter(self, counter):
        set_key(self.env_file, "JOB_ID", str(counter))

    def get_customer_counter(self) -> int:
        self._reload_env()
        return int(os.environ.get("CUSTOMER_ID", 0))
    
    def set_customer_id_counter(self, counter):
        set_key(self.env_file, "CUSTOMER_ID", str(counter))

    def get_invoice_counter(self) -> int:
        self._reload_env()
        return int(os.environ.get("INVOICE_ID", 0))
    
    def set_invoice_id_counter(self, counter):
        set_key(self.env_file, "INVOICE_ID", str(counter))
        