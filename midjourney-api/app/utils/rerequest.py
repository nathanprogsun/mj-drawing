from pydantic import BaseModel, Field


class PaginationRequest(BaseModel):
    page_number: int = Field(default=1)
    page_size: int = Field(default=20)
    paginate: bool = Field(default=True)

    @property
    def limit(self):
        return self.page_size

    @property
    def offset(self):
        return (self.page_number - 1) * self.page_size
