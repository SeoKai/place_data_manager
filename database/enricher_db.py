from database.db_connection import get_connection

def get_places_without_description(region_id=None):
    """DB에서 상세 설명이 없는 장소 데이터를 가져오기 (지역 ID 필터)"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if region_id:
        query = """
        SELECT place_id, location_name FROM tbl_location
        WHERE (description IS NULL OR description = '')
        AND region_id = %s
        """
        cursor.execute(query, (region_id,))
    else:
        query = """
        SELECT place_id, location_name FROM tbl_location
        WHERE description IS NULL OR description = ''
        """
        cursor.execute(query)

    places = cursor.fetchall()
    cursor.close()
    connection.close()
    return places

def update_place_description(place_id, description):
    """DB에 장소의 상세설명 업데이트"""
    connection = get_connection()
    cursor = connection.cursor()

    query = "UPDATE tbl_location SET description = %s WHERE place_id = %s"
    cursor.execute(query, (description, place_id))
    connection.commit()

    cursor.close()
    connection.close()
