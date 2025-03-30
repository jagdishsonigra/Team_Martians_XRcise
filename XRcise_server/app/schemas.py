from pydantic import BaseModel

class UserResponses(BaseModel):
    responses: dict

    def extract_responses(self):
        return {
            "responses": {
                "pain_location": self.responses.get("pain_location", ""),
                "age_group": self.responses.get("age_group", ""),
                "pain_intensity": self.responses.get("pain_intensity", ""),
                "physical_capacity": self.responses.get("physical_capacity", "")
            }
        }
