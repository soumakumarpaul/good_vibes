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
        