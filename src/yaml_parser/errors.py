from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationError:
    section: str
    field: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "section": self.section,
            "field": self.field,
            "message": self.message,
        }


def format_error(error: ValidationError) -> str:
    return f"{error.section}.{error.field}: {error.message}"
