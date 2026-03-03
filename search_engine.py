from services.local_service import search_local
from services.nexar_service import search_nexar
from services.cache_layer import get_cache, set_cache
from logging_config import logger

import time


def normalize_part(part: str) -> str:
    return part.strip().lower()


def rank_results(results, query: str):
    """
    Ranking priority:
    - Exact match = 100
    - Startswith = 70
    - Contains = 50
    """

    ranked = []
    query_normalized = normalize_part(query)

    for item in results:
        part = normalize_part(item.get("part_number", ""))

        if part == query_normalized:
            score = 100
        elif part.startswith(query_normalized):
            score = 70
        elif query_normalized in part:
            score = 50
        else:
            score = 10

        ranked.append((score, item))

    ranked.sort(key=lambda x: x[0], reverse=True)

    return [item[1] for item in ranked]


def merge_results(local_results, nexar_results):
    """
    Merge without duplicates
    Local results overwrite Nexar if same part_number
    """

    merged = {}

    for item in nexar_results:
        key = normalize_part(item.get("part_number", ""))
        merged[key] = item

    for item in local_results:
        key = normalize_part(item.get("part_number", ""))
        merged[key] = item

    return list(merged.values())


def build_response(source, results):
    return {
        "source": source,
        "count": len(results),
        "results": results
    }


def search_part(part_number: str, page: int = 1, limit: int = 20):

    start_time = time.time()
    part_number = part_number.strip()

    logger.info(f"Search started | Query: {part_number} | Page: {page}")

    try:
        # 🔹 Cache Key (includes pagination)
        cache_key = f"{part_number}:{page}:{limit}"

        # 🔹 1️⃣ Check Cache
        cached = get_cache(cache_key)
        if cached:
            logger.info("Cache hit")
            return cached

        # 🔹 2️⃣ Search Local
        local_results = search_local(part_number) or []
        local_results = rank_results(local_results, part_number)

        # 🔹 3️⃣ Decide if Nexar needed
        need_external = (
            not local_results or
            any(not item.get("price") for item in local_results)
        )

        nexar_results = []

        if need_external:
            logger.info("Triggering Nexar fallback")
            nexar_results = search_nexar(part_number) or []
            nexar_results = rank_results(nexar_results, part_number)

        # 🔹 4️⃣ Merge logic
        if local_results and nexar_results:
            final_results = merge_results(local_results, nexar_results)
            final_results = rank_results(final_results, part_number)
            response = build_response("Local + Nexar", final_results)

        elif local_results:
            response = build_response("Local Database", local_results)

        elif nexar_results:
            response = build_response("Nexar", nexar_results)

        else:
            response = build_response("Not Found", [])

        # 🔹 Pagination
        total_results = len(response["results"])

        start = (page - 1) * limit
        end = start + limit

        paginated_results = response["results"][start:end]

        paginated_response = {
            "source": response["source"],
            "total_results": total_results,
            "page": page,
            "limit": limit,
            "results": paginated_results
        }

        # 🔹 Save paginated result to cache
        set_cache(cache_key, paginated_response)

        execution_time = round(time.time() - start_time, 4)
        logger.info(
            f"Search completed | Source: {response['source']} | "
            f"Total: {total_results} | Page: {page} | Time: {execution_time}s"
        )

        return paginated_response

    except Exception as e:
        logger.error(f"Search error | Query: {part_number} | Error: {str(e)}")
        return {
            "source": "Error",
            "total_results": 0,
            "page": page,
            "limit": limit,
            "results": []
        }