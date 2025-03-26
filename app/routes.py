from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app.redis_helper import cache_client_data, get_cached_client

client_bp = Blueprint("clients", __name__)

# Create Client
@client_bp.route("/clients", methods=["POST"])
def create_client():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO my_client (name, slug, is_project, self_capture, client_prefix, client_logo, address, phone_number, city, created_at, updated_at, deleted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NULL, NULL)
                RETURNING id;
            """, (data["name"], data["slug"], data["is_project"], data["self_capture"],
                  data["client_prefix"], data["client_logo"], data["address"],
                  data["phone_number"], data["city"]))
            conn.commit()
            client_id = cur.fetchone()[0]

        # Cache in Redis
        data["id"] = client_id
        cache_client_data(data["slug"], data)

        return jsonify({"message": "Client added successfully", "id": client_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# Get Client by Slug (with Redis Cache)
@client_bp.route("/clients/<slug>", methods=["GET"])
def get_client(slug):
    # Try Redis first
    cached_data = get_cached_client(slug)
    if cached_data:
        return jsonify(cached_data)

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM my_client WHERE slug = %s;", (slug,))
            row = cur.fetchone()

        if not row:
            return jsonify({"message": "Client not found"}), 404

        client_data = {
            "id": row[0], "name": row[1], "slug": row[2], "is_project": row[3],
            "self_capture": row[4], "client_prefix": row[5], "client_logo": row[6],
            "address": row[7], "phone_number": row[8], "city": row[9],
            "created_at": row[10], "updated_at": row[11], "deleted_at": row[12],
        }

        # Store in Redis
        cache_client_data(slug, client_data)
        return jsonify(client_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()