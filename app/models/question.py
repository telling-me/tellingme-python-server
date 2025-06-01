from tortoise import fields
from tortoise.models import Model


class Question(Model):
    date = fields.DateField(pk=True)  # 기본 키로 설정된 날짜 필드
    phrase = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    spare_phrase = fields.CharField(max_length=255)
    spare_title = fields.CharField(max_length=255)

    class Meta:
        table = "question"  # 데이터베이스에서 매핑할 테이블 이름
