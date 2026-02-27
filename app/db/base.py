from sqlmodel import SQLModel

from app.models.user import User
from app.models.role import Role
from app.models.video import Video
from app.models.purchase import Purchase
from app.models.subscription import Subscription
from app.models.video_view import VideoView
from app.models.engagement import Engagement

Base = SQLModel


