# MySQL 연결 함수와 contextmanager 가져오기
from database.db_connection import get_connection
from database.cursor_manager import db_cursor

# 장소 데이터를 DB에 저장하는 함수
def save_to_database(data):
    with db_cursor() as cursor:
        # 장소 정보를 INSERT 또는 UPDATE (중복 place_id 처리)
        sql = """
        INSERT INTO tbl_location (
            place_id, location_name, description, latitude, longitude,
            google_rating, user_ratings_total, place_img_url,
            formatted_address, opening_hours, website, phone_number, region_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            location_name=VALUES(location_name),
            description=VALUES(description),
            latitude=VALUES(latitude),
            longitude=VALUES(longitude),
            google_rating=VALUES(google_rating),
            user_ratings_total=VALUES(user_ratings_total),
            place_img_url=VALUES(place_img_url),
            formatted_address=VALUES(formatted_address),
            opening_hours=VALUES(opening_hours),
            website=VALUES(website),
            phone_number=VALUES(phone_number),
            region_id=VALUES(region_id);
        """
        cursor.execute(sql, data[:-1])  # 태그를 제외한 13개 필드 삽입
        # 저장된 location_id를 다시 조회
        cursor.execute("SELECT location_id FROM tbl_location WHERE place_id = %s", (data[0],))
        location_id = cursor.fetchone()[0]
        print(f"[DEBUG] 저장된 location_id: {location_id}")
        return location_id

# 태그 데이터를 tbl_tag에 저장하고 ID 리스트 반환
def save_tags(tags):
    tag_ids = []
    with db_cursor() as cursor:
        for tag in tags:
            try:
                # 이미 있는 태그인지 확인
                cursor.execute("SELECT tag_id FROM tbl_tag WHERE tag_name = %s", (tag,))
                result = cursor.fetchone()
                if result:
                    # 이미 있는 경우 기존 ID 사용
                    print(f"Tag 이미 존재함 : {tag} (ID: {result[0]})")
                    tag_ids.append(result[0])
                else:
                    # 새 태그 삽입
                    cursor.execute("INSERT INTO tbl_tag (tag_name) VALUES (%s)", (tag,))
                    tag_id = cursor.lastrowid
                    tag_ids.append(tag_id)
                    print(f"새 tag : {tag} (ID: {tag_id})")
            except Exception as e:
                print(f"예상치 못한 에러: {tag}. Error: {e}")
    return tag_ids

# 장소와 태그 간의 연결 관계를 저장
def save_location_tags(location_id, tag_ids):
    with db_cursor() as cursor:
        for tag_id in tag_ids:
            try:
                # 관계 테이블에 중복 없이 삽입
                cursor.execute("""
                    INSERT IGNORE INTO tbl_location_tag (location_id, tag_id)
                    VALUES (%s, %s)
                """, (location_id, tag_id))
                print(f"장소-태그 연결 완료: Location ID {location_id}, Tag ID {tag_id}")
            except Exception as e:
                print(f"장소-태그 연결 오류: Location ID {location_id}, Tag ID {tag_id}. Error: {e}")
