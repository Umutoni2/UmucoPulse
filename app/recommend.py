def _tokens(text):
    raw = (text or "").replace("·", ",").replace("|", ";").replace("/", ",")
    parts = []
    for chunk in raw.replace(";", ",").split(","):
        piece = chunk.strip().lower()
        if piece:
            parts.append(piece)
    return set(parts)


def _kind_label(profile, t):
    kind = profile.profile_kind or "individual"
    if kind == "troupe":
        return t.get("kind_troupe_one", "Cultural troupe")
    if kind == "community_group":
        return t.get("kind_community", "Community group")
    if kind == "organisation":
        return t.get("kind_organisation", "Organisation")
    return t.get("kind_person", "Individual")


def similar_profiles(source, candidates, t, area_name_fn, you_both=True, exclude_user_id=None, limit=5):
    if not source:
        return []
    src_practices = {x.lower() for x in source.practices_list()}
    src_langs = _tokens(source.languages)
    ranked = []
    for profile in candidates:
        if profile.id == source.id:
            continue
        if exclude_user_id and profile.user_id == exclude_user_id:
            continue
        score = 0
        reasons = []
        area_label = area_name_fn(source.area) if source.area else ""
        if source.area and profile.area == source.area:
            score += 4
            if you_both:
                reasons.append(t["same_art_area"].format(area=area_label))
            else:
                reasons.append(t["same_art_area_also"].format(area=area_label))
        shared_practice = src_practices & {x.lower() for x in profile.practices_list()}
        if shared_practice:
            sample = sorted(shared_practice)[0]
            score += 2 * min(len(shared_practice), 3)
            reasons.append(t["same_art_practice"].format(practice=sample))
        loc_match = False
        if source.location_key and source.location_key not in ("", "unlisted") and profile.location_key == source.location_key:
            loc_match = True
        elif source.location and profile.location and source.location.strip().lower() == profile.location.strip().lower():
            loc_match = True
        if loc_match:
            score += 2
            place = profile.location or source.location or source.location_key
            reasons.append(t["same_art_place"].format(place=place))
        shared_lang = src_langs & _tokens(profile.languages)
        if shared_lang:
            score += 1
            reasons.append(t["same_art_lang"].format(lang=sorted(shared_lang)[0]))
        if score <= 0:
            continue
        ranked.append(
            {
                "profile": profile,
                "score": score,
                "reason": reasons[0] if reasons else t["same_art_generic"],
                "kind_label": _kind_label(profile, t),
            }
        )
    ranked.sort(key=lambda row: (-row["score"], row["profile"].display_name.lower()))
    return ranked[:limit]
