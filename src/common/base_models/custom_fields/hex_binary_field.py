from tortoise import fields
import uuid
import binascii


class HexBinaryField(fields.BinaryField):
    """
    바이트 배열을 16진수로 변환하여 처리하는 커스텀 필드
    """

    def to_db_value(self, value, instance):
        """
        데이터베이스로 저장될 때 바이트 배열로 변환
        """
        if isinstance(value, uuid.UUID):
            return value.bytes  # UUID 객체를 바이트 배열로 변환
        elif isinstance(value, str):
            return uuid.UUID(value).bytes  # 문자열을 UUID로 변환하여 바이트 배열로 변환
        elif isinstance(value, bytes):
            return value  # 이미 바이트 배열이면 그대로 반환
        raise ValueError(f"Unsupported value type: {type(value)}")

    def to_python_value(self, value):
        """
        데이터베이스에서 읽어올 때 바이트 배열을 16진수로 변환하여 반환
        """
        if isinstance(value, bytes):
            return binascii.hexlify(value).decode(
                "utf-8"
            )  # 바이트 배열을 16진수로 변환하여 반환
        return value

    def get_db_value(self, value, instance):
        """
        쿼리에서 바이트 배열을 16진수로 변환하여 사용
        """
        if isinstance(value, bytes):
            return f"0x{binascii.hexlify(value).decode('utf-8')}"  # 바이트 배열을 16진수로 변환하여 쿼리에 사용
        return value
