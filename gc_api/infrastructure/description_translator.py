from typing import Optional
import yaml

class DescriptionTranslator:
    @staticmethod
    def translate(self, schedule: dict) -> Optional[dict]:
        if "description" not in schedule:
            return None
        try:
            description_str:str = schedule["description"]
            # <br>タグは改行に置換する
            description_str = description_str.replace("<br>", "\n")
            # そのほかのHTMLタグはすべて置換する
            # description = re.sub(r"<[^>]*?>", "", description)
            return yaml.safe_load(description_str)
        except:
            print("yaml parse error" + schedule["description"])
            return None
