from database.db_connection import get_connection
from contextlib import contextmanager

# DB 커서 사용을 위한 컨텍스트 매니저 정의
@contextmanager
def db_cursor():
    # MySQL 연결 생성
    connection = get_connection()
    # 쿼리 실행을 위한 커서 생성
    cursor = connection.cursor()
    try:
        yield cursor  # with 블록 내부에서 cursor 사용
        connection.commit()  # 예외 없으면 커밋
    except:
        connection.rollback()  # 예외 발생 시 롤백
        raise  # 예외 다시 던지기 (상위에서 처리)
    finally:
        cursor.close()  # 커서 닫기
        connection.close()  # 연결 닫기