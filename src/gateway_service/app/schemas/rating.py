from pydantic import BaseModel, constr, conint


class RatingBase(BaseModel):
  username: constr(max_length=80)
  stars: conint(ge=1, le=100)


class RatingUpdate(BaseModel):
  username: constr(max_length=80) | None = None
  stars: conint(ge=1, le=100) | None = None


class RatingCreate(RatingBase):
  pass


class Rating(RatingBase):
  id: int


class UserRatingResponse(BaseModel):
  stars: conint(ge=1, le=100)
