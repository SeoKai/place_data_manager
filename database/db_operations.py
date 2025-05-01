from database.db_connection import get_connection

def save_to_database(data):
    """MySQL에 장소 데이터를 저장"""
    connection = get_connection()
    cursor = connection.cursor()

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
    try:
        # SQL 실행
        cursor.execute(sql, data[:-1])  # 태그 제외 데이터 삽입
        connection.commit()

        # 저장된 location_id 가져오기
        cursor.execute("SELECT location_id FROM tbl_location WHERE place_id = %s", (data[0],))
        location_id = cursor.fetchone()[0]
        print(f"[DEBUG] 저장된 location_id: {location_id}")
        return location_id
    except Exception as e:
        print(f"[ERROR] 장소 저장 실패: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def save_tags(tags):
    """
    태그 데이터를 tbl_tag에 저장하고 고유 tag_id 리스트를 반환
    """
    connection = get_connection()
    cursor = connection.cursor()

    tag_ids = []
    for tag in tags:
        try:
            # 태그가 이미 존재하는지 확인
            cursor.execute("SELECT tag_id FROM tbl_tag WHERE tag_name = %s", (tag,))
            result = cursor.fetchone()
            if result:
                print(f"Tag 이미 존재함 : {tag} (ID: {result[0]})")
                tag_ids.append(result[0])  # 기존 태그 ID 추가
            else:
                # 새로운 태그 삽입
                cursor.execute("INSERT INTO tbl_tag (tag_name) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid
                tag_ids.append(tag_id)  # 삽입된 태그 ID 추가
                print(f"새 tag : {tag} (ID: {tag_id})")
        except Exception as e:
            print(f"예상치 못한 에러: {tag}. Error: {e}")

    connection.commit()
    cursor.close()
    connection.close()
    return tag_ids


def save_location_tags(location_id, tag_ids):
    """
    장소와 태그 간의 관계를 tbl_location_tag에 저장
    """
    connection = get_connection()
    cursor = connection.cursor()

    for tag_id in tag_ids:
        try:
            cursor.execute("""
                INSERT IGNORE INTO tbl_location_tag (location_id, tag_id)
                VALUES (%s, %s)
            """, (location_id, tag_id))
            print(f"Inserted relationship: Location ID {location_id}, Tag ID {tag_id}")
        except Exception as e:
            print(f"Error inserting relationship: Location ID {location_id}, Tag ID {tag_id}. Error: {e}")



    connection.commit()
    cursor.close()
    connection.close()
