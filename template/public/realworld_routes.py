from flask import Blueprint, request, jsonify
from ..cache import cache
import time
import json

real_bp = Blueprint('real', __name__)

# --- 1. Simulated User Info Caching ---
@real_bp.route('/user/<int:user_id>')
def get_user_info(user_id):
    key = f"user:{user_id}"
    cached = cache.cache.get(key)
    if cached:
        return jsonify(json.loads(cached))

    # Simulated DB call
    user = {
        "id": user_id,
        "name": f"User {user_id}",
        "role": "admin" if user_id % 2 == 0 else "viewer"
    }

    cache.cache.set(key, json.dumps(user), ex=60)  # 1 min cache
    return jsonify(user)

# --- 2. Fake Expensive DB Query ---
@real_bp.route('/expensive-query')
@cache.cached(timeout=20)
def expensive_query():
    time.sleep(3)  # Simulate slow query
    return jsonify({"data": "Heavy data result", "fetched_at": time.time()})

# --- 3. Simple Rate Limiting ---
@real_bp.route('/limited')
def rate_limited():
    ip = request.remote_addr
    key = f"rate:{ip}"
    count = cache.cache.get(key)

    if count is None:
        cache.cache.set(key, '1', ex=60)
        count = 1
    else:
        count = int(count) + 1
        cache.cache.set(key, str(count), ex=60)

    if count > 5:
        return jsonify({"error": "Too many requests. Slow down!"}), 429

    return jsonify({"message": f"Request {count} allowed!"})
