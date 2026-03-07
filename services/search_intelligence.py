def smart_search(query, products):

    q = query.lower()

    results = []

    for p in products:

        part = p.part_number.lower()

        score = 0

        # exact match
        if q == part:
            score += 100

        # partial match
        if q in part:
            score += 70

        # prefix match
        if part.startswith(q):
            score += 50

        results.append({
            "part_number": p.part_number,
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:20]