from rest_framework.throttling import UserRateThrottle

class LikeThrottle(UserRateThrottle):
    rate = '1/second'