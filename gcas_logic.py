import re


# 재료 이름과 상품명 인식 규칙
ITEM_RULES = {
    "bread": {
        "name": "빵",
        "keywords": ["bread", "식빵", "빵"],
        "exclude": ["breadcrumbs", "bread crumbs", "breaded"],
    },
    "bagel": {
        "name": "베이글",
        "keywords": ["bagel", "bagels", "베이글"],
        "exclude": [],
    },
    "tortilla": {
        "name": "또띠아",
        "keywords": ["tortilla", "tortillas", "또띠아"],
        "exclude": ["chips", "칩"],
    },
    "ham": {
        "name": "햄",
        "keywords": ["ham", "햄"],
        "exclude": [],
    },
    "egg": {
        "name": "달걀",
        "keywords": ["egg", "eggs", "달걀", "계란"],
        "exclude": ["egg noodles", "egg rolls"],
    },
    "tuna": {
        "name": "참치",
        "keywords": ["tuna", "참치"],
        "exclude": [],
    },
    "tofu": {
        "name": "두부",
        "keywords": ["tofu", "두부"],
        "exclude": [],
    },
    "cheese": {
        "name": "치즈",
        "keywords": ["cheese", "cheddar", "mozzarella", "치즈"],
        "exclude": ["cheesecake", "cheese cake"],
    },
    "lettuce": {
        "name": "잎채소",
        "keywords": ["lettuce", "romaine", "양상추", "로메인"],
        "exclude": [],
    },
    "tomato": {
        "name": "토마토",
        "keywords": ["tomato", "tomatoes", "토마토", "방울토마토"],
        "exclude": ["sauce", "paste", "soup", "juice", "소스"],
    },
}


GOAL_RULES = {
    "sandwich": {
        "name": "샌드위치",
        "required": {
            "베이스": ["bread", "bagel", "tortilla"],
            "메인 재료": ["ham", "egg", "tuna", "tofu", "cheese"],
        },
        "optional": {
            "채소": ["lettuce", "tomato"],
        },
    },
}


def normalize_text(value):
    text = str(value).lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def contains_keyword(text, keyword):
    keyword = normalize_text(keyword)
    pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"
    return re.search(pattern, text) is not None


def matches_item(product_name, item_id):
    text = normalize_text(product_name)
    rule = ITEM_RULES[item_id]

    if any(
        contains_keyword(text, word)
        for word in rule["exclude"]
    ):
        return False

    return any(
        contains_keyword(text, word)
        for word in rule["keywords"]
    )


def analyze_cart(cart, goal_id):
    if goal_id not in GOAL_RULES:
        raise ValueError(f"아직 지원하지 않는 메뉴입니다: {goal_id}")

    config = GOAL_RULES[goal_id]
    clean_cart = [
        name.strip()
        for name in cart
        if isinstance(name, str) and name.strip()
    ]

    details = []

    for group_type in ["required", "optional"]:
        for group_name, options in config[group_type].items():
            matched_products = [
                name
                for name in clean_cart
                if any(
                    matches_item(name, item_id)
                    for item_id in options
                )
            ]

            details.append({
                "name": group_name,
                "required": group_type == "required",
                "fulfilled": bool(matched_products),
                "products": matched_products,
                "alternatives": [
                    ITEM_RULES[item_id]["name"]
                    for item_id in options
                ],
            })

    required_details = [
        detail for detail in details
        if detail["required"]
    ]

    fulfilled_count = sum(
        detail["fulfilled"]
        for detail in required_details
    )

    return {
        "goal_name": config["name"],
        "completion_rate": fulfilled_count / len(required_details),
        "missing_groups": [
            detail["name"]
            for detail in required_details
            if not detail["fulfilled"]
        ],
        "details": details,
    }

# ─────────────────────────────────────
# 추가 재료 인식 규칙
# ─────────────────────────────────────
ITEM_RULES.update({
    "spinach": {
        "name": "시금치",
        "keywords": ["spinach", "시금치"],
        "exclude": ["dip", "pizza"],
    },
    "kale": {
        "name": "케일",
        "keywords": ["kale", "케일"],
        "exclude": ["chips"],
    },
    "arugula": {
        "name": "루콜라",
        "keywords": ["arugula", "루콜라"],
        "exclude": [],
    },
    "cucumber": {
        "name": "오이",
        "keywords": ["cucumber", "cucumbers", "오이"],
        "exclude": ["pickle", "pickles"],
    },
    "carrot": {
        "name": "당근",
        "keywords": ["carrot", "carrots", "당근"],
        "exclude": ["cake", "juice"],
    },
    "avocado": {
        "name": "아보카도",
        "keywords": ["avocado", "avocados", "아보카도"],
        "exclude": ["oil"],
    },
    "dressing": {
        "name": "드레싱",
        "keywords": [
            "salad dressing", "ranch dressing",
            "caesar dressing", "vinaigrette", "드레싱",
        ],
        "exclude": [],
    },
    "pasta": {
        "name": "파스타 면",
        "keywords": [
            "pasta", "spaghetti", "penne",
            "rigatoni", "fusilli", "스파게티", "파스타",
        ],
        "exclude": ["sauce", "salad", "소스"],
    },
    "tomato_sauce": {
        "name": "토마토 소스",
        "keywords": [
            "tomato sauce", "pasta sauce",
            "marinara", "토마토 소스",
        ],
        "exclude": [],
    },
    "pesto": {
        "name": "페스토",
        "keywords": ["pesto", "페스토"],
        "exclude": [],
    },
    "cream": {
        "name": "크림",
        "keywords": [
            "heavy cream", "heavy whipping cream",
            "cooking cream", "cream sauce",
            "alfredo", "생크림", "크림 소스",
        ],
        "exclude": ["ice cream", "아이스크림"],
    },
    "parmesan": {
        "name": "파르메산 치즈",
        "keywords": ["parmesan", "parmigiano", "파르메산", "파마산"],
        "exclude": [],
    },
    "milk": {
        "name": "우유",
        "keywords": ["milk", "우유"],
        "exclude": ["milk chocolate", "soap"],
    },
    "cereal": {
        "name": "시리얼",
        "keywords": ["cereal", "granola", "시리얼", "그래놀라"],
        "exclude": ["bar"],
    },
    "oatmeal": {
        "name": "오트밀",
        "keywords": ["oatmeal", "rolled oats", "steel cut oats", "오트밀"],
        "exclude": ["cookie", "cookies", "bar"],
    },
    "yogurt": {
        "name": "요거트",
        "keywords": ["yogurt", "yoghurt", "요거트"],
        "exclude": ["frozen", "ice cream"],
    },
    "soy_milk": {
        "name": "두유",
        "keywords": ["soy milk", "soymilk", "두유"],
        "exclude": [],
    },
    "banana": {
        "name": "바나나",
        "keywords": ["banana", "bananas", "바나나"],
        "exclude": ["chips", "bread", "muffin"],
    },
    "apple": {
        "name": "사과",
        "keywords": ["apple", "apples", "사과"],
        "exclude": ["juice", "sauce", "pie"],
    },
    "strawberry": {
        "name": "딸기",
        "keywords": ["strawberry", "strawberries", "딸기"],
        "exclude": ["jam", "jelly"],
    },
    "chips": {
        "name": "칩 과자",
        "keywords": ["chips", "crisps", "감자칩"],
        "exclude": ["chocolate"],
    },
    "chocolate": {
        "name": "초콜릿",
        "keywords": ["chocolate", "초콜릿"],
        "exclude": ["chocolate milk", "cereal", "초코 우유"],
    },
    "popcorn": {
        "name": "팝콘",
        "keywords": ["popcorn", "팝콘"],
        "exclude": ["kernel", "kernels"],
    },
    "nuts": {
        "name": "견과류",
        "keywords": [
            "almonds", "cashews", "walnuts",
            "peanuts", "mixed nuts", "아몬드", "견과류",
        ],
        "exclude": ["milk", "butter", "flour"],
    },
    "cookies": {
        "name": "쿠키",
        "keywords": ["cookie", "cookies", "쿠키"],
        "exclude": ["dough"],
    },
    "soda": {
        "name": "탄산음료",
        "keywords": ["soda", "cola", "콜라", "탄산음료"],
        "exclude": ["baking soda"],
    },
    "tea": {
        "name": "차",
        "keywords": ["tea", "홍차", "녹차"],
        "exclude": [],
    },
    "coffee": {
        "name": "커피",
        "keywords": ["coffee", "커피"],
        "exclude": [],
    },
})


# ─────────────────────────────────────
# 샌드위치 외 메뉴 기준
# ─────────────────────────────────────
GOAL_RULES.update({
    "salad": {
        "name": "샐러드",
        "required": {
            "잎채소": ["lettuce", "spinach", "kale", "arugula"],
            "곁들임 채소": ["tomato", "cucumber", "carrot", "avocado"],
        },
        "optional": {
            "드레싱": ["dressing"],
        },
    },
    "pasta": {
        "name": "파스타",
        "required": {
            "파스타 면": ["pasta"],
            "소스 베이스": ["tomato_sauce", "pesto", "cream"],
        },
        "optional": {
            "토핑": ["parmesan"],
        },
    },
    "breakfast": {
        "name": "아침 식사",
        "required": {
            "주식": ["bread", "bagel", "cereal", "oatmeal"],
            "곁들임": ["milk", "egg", "yogurt", "soy_milk"],
        },
        "optional": {
            "과일": ["banana", "apple", "strawberry"],
        },
    },
    "snack": {
        "name": "간식",
        "required": {
            "간식": ["chips", "chocolate", "popcorn", "nuts", "cookies"],
        },
        "optional": {
            "음료": ["soda", "tea", "coffee"],
        },
    },
})

# ─────────────────────────────────────
# 새 상품에 필요한 재료 인식 규칙
# ─────────────────────────────────────
ITEM_RULES.update({
    "rice": {
        "name": "쌀",
        "keywords": ["white rice", "brown rice", "쌀"],
        "exclude": ["rice cake", "rice noodles"],
    },
    "chicken": {
        "name": "닭고기",
        "keywords": ["chicken breast", "닭가슴살", "닭고기"],
        "exclude": [],
    },
    "pork": {
        "name": "돼지고기",
        "keywords": ["pork", "돼지고기"],
        "exclude": [],
    },
    "onion": {
        "name": "양파",
        "keywords": ["yellow onions", "onion", "양파"],
        "exclude": ["green onions", "onion powder"],
    },
    "potato": {
        "name": "감자",
        "keywords": ["potato", "potatoes", "감자"],
        "exclude": ["chips", "감자칩"],
    },
    "mushroom": {
        "name": "버섯",
        "keywords": ["mushroom", "mushrooms", "버섯"],
        "exclude": [],
    },
    "green_onion": {
        "name": "대파",
        "keywords": ["green onions", "green onion", "대파"],
        "exclude": [],
    },
    "zucchini": {
        "name": "애호박",
        "keywords": ["zucchini", "애호박"],
        "exclude": [],
    },
    "curry": {
        "name": "카레 소스",
        "keywords": ["curry sauce", "카레 소스"],
        "exclude": [],
    },
    "doenjang": {
        "name": "된장",
        "keywords": ["soybean paste", "된장"],
        "exclude": [],
    },
    "kimchi": {
        "name": "김치",
        "keywords": ["kimchi", "김치", "배추김치"],
        "exclude": [],
    },
    "soy_sauce": {
        "name": "간장",
        "keywords": ["soy sauce", "간장"],
        "exclude": [],
    },
})


# ─────────────────────────────────────
# 메뉴 7개 추가
#
# 필수 구성은 이 서비스에서 정한 기본 준비 기준입니다.
# 물과 소금 및 조리용 기름 같은 기본 양념은 별도입니다.
# ─────────────────────────────────────
GOAL_RULES.update({
    "fried_rice": {
        "name": "볶음밥",
        "required": {
            "밥 재료": ["rice"],
            "메인 재료": ["egg", "ham", "tuna", "tofu", "chicken"],
            "채소": ["carrot", "onion", "green_onion", "kimchi"],
        },
        "optional": {
            "간 맞추기": ["soy_sauce"],
        },
    },

    "curry_rice": {
        "name": "카레라이스",
        "required": {
            "밥 재료": ["rice"],
            "카레": ["curry"],
            "채소": ["onion", "carrot", "potato", "mushroom"],
        },
        "optional": {
            "메인 재료": ["chicken", "pork", "tofu"],
        },
    },

    "kimchi_stew": {
        "name": "김치찌개",
        "required": {
            "김치": ["kimchi"],
            "메인 재료": ["pork", "tuna", "tofu"],
        },
        "optional": {
            "곁들임 채소": ["onion", "green_onion"],
            "밥 재료": ["rice"],
        },
    },

    "doenjang_stew": {
        "name": "된장찌개",
        "required": {
            "된장": ["doenjang"],
            "채소": ["zucchini", "potato", "onion", "mushroom"],
            "두부": ["tofu"],
        },
        "optional": {
            "대파": ["green_onion"],
            "밥 재료": ["rice"],
        },
    },

    "toast": {
        "name": "토스트",
        "required": {
            "빵": ["bread", "bagel"],
            "곁들임 재료": ["egg", "cheese", "ham"],
        },
        "optional": {
            "채소": ["lettuce", "tomato"],
        },
    },

    "chicken_salad": {
        "name": "닭가슴살 샐러드",
        "required": {
            "잎채소": ["lettuce", "spinach", "kale", "arugula"],
            "닭가슴살": ["chicken"],
        },
        "optional": {
            "곁들임 채소": ["tomato", "cucumber", "carrot"],
            "드레싱": ["dressing"],
        },
    },

    "oatmeal_bowl": {
        "name": "오트밀 볼",
        "required": {
            "오트밀": ["oatmeal"],
            "곁들임": ["milk", "yogurt", "soy_milk"],
        },
        "optional": {
            "과일": ["banana", "apple", "strawberry"],
            "견과류": ["nuts"],
        },
    },
})


# 웹에서 사용할 메뉴 목록
MENU_OPTIONS = {
    "선택해주세요": None,
    **{
        config["name"]: goal_id
        for goal_id, config in GOAL_RULES.items()
    },
}

def decide_intervention(goal_id, missing_rate):
    """누락률에 따라 안내 수준을 결정합니다."""
    if (
        goal_id not in GOAL_RULES
        or missing_rate is None
    ):
        return {
            "type": "no_goal",
            "message": "메뉴를 선택하면 필요한 재료를 확인할 수 있습니다.",
        }

    # 판단에는 반올림하지 않은 값을 사용
    if missing_rate >= 2 / 3:
        return {
            "type": "warning",
            "message": "필수 구성이 많이 비어 있습니다. 필요한 재료를 확인해주세요.",
        }

    if missing_rate > 0:
        return {
            "type": "soft_suggest",
            "message": "부족한 구성을 채울 재료를 추천합니다.",
        }

    return {
        "type": "no_intervention",
        "message": "기본 구성이 갖춰졌습니다.",
    }

def decide_intervention(goal_id, missing_rate):
    if goal_id not in GOAL_RULES or missing_rate is None:
        return {
            "type": "no_goal",
            "message": "메뉴를 선택해주세요.",
        }

    if missing_rate >= 2 / 3:
        return {
            "type": "warning",
            "message": "필수 구성이 많이 비어 있습니다. 필요한 재료를 확인해주세요.",
        }

    if missing_rate > 0:
        return {
            "type": "soft_suggest",
            "message": "부족한 구성을 채울 재료를 추천합니다.",
        }

    return {
        "type": "no_intervention",
        "message": "기본 구성이 갖춰졌습니다.",
    }

# 실제 주문 검토에서 발견한 오탐 보완
EXTRA_EXCLUSIONS = {
    "strawberry": [
        "licorice",
        "candy",
        "gummies",
        "gummy",
        "smoothie",
        "yogurt",
        "yoghurt",
    ],
    "rice": [
        "rice cakes",
        "rice crackers",
        "rice crisps",
        "rice cereal",
        "rice flour",
        "rice milk",
        "rice pudding",
    ],
    "carrot": [
        "baby food",
        "puree",
        "purees",
        "smoothie",
    ],
}

for item_id, excluded_words in EXTRA_EXCLUSIONS.items():
    rule = ITEM_RULES[item_id]

    # 重複せず追加
    rule["exclude"] = list(dict.fromkeys(
        rule["exclude"] + excluded_words
    ))

# 자동 추론에서 반드시 확인할 핵심 재료
# 나열된 재료 중 하나 이상이 있어야 해당 목표를 후보로 인정
GOAL_ANCHORS = {
    "curry_rice": ["curry"],
    "doenjang_stew": ["doenjang"],
    "kimchi_stew": ["kimchi"],
    "chicken_salad": ["chicken"],
    "oatmeal_bowl": ["oatmeal"],
    "pasta": ["pasta"],
}


def has_goal_anchor(cart, goal_id):
    options = GOAL_ANCHORS.get(goal_id)

    # 핵심 재료 조건이 없는 목표는 기존 기준 사용
    if options is None:
        return True

    return any(
        matches_item(product_name, item_id)
        for product_name in cart
        for item_id in options
    )

# 추가 오탐 제외 규칙
REVIEW_EXCLUSIONS = {
    "rice": ["rice snaps"],
    "onion": ["rice snaps"],
    "spinach": [
        "baby food",
        "pureed",
        "puree",
        "littles",
    ],
}

for item_id, words in REVIEW_EXCLUSIONS.items():
    ITEM_RULES[item_id]["exclude"] = list(dict.fromkeys(
        ITEM_RULES[item_id]["exclude"] + words
    ))

def infer_goal_from_sequence(cart_sequence, initial_n=None):
    """
    상품 추가 순서대로 입력된 목록에서 목표를 추론합니다.
    점수는 규칙 비교용이며 예측 확률이 아닙니다.
    """
    cart = [
        name.strip()
        for name in cart_sequence
        if isinstance(name, str) and name.strip()
    ]

    if initial_n is not None:
        if initial_n < 1:
            raise ValueError("initial_n은 1 이상이어야 합니다.")

        cart = cart[:initial_n]

    ranking = []

    for goal_id, config in GOAL_RULES.items():
        result = analyze_cart(cart, goal_id)

        required = [
            detail
            for detail in result["details"]
            if detail["required"]
        ]

        optional = [
            detail
            for detail in result["details"]
            if not detail["required"]
        ]

        required_hits = sum(
            detail["fulfilled"]
            for detail in required
        )

        optional_hits = sum(
            detail["fulfilled"]
            for detail in optional
        )

        score = required_hits * 2 + optional_hits
        max_score = len(required) * 2 + len(optional)
        normalized_score = score / max_score

        minimum_hits = min(2, len(required))
        anchor_matched = has_goal_anchor(cart, goal_id)

        eligible = (
            required_hits >= minimum_hits
            and anchor_matched
        )

        ranking.append({
            "goal_id": goal_id,
            "goal_name": config["name"],
            "required_hits": required_hits,
            "optional_hits": optional_hits,
            "score": score,
            "normalized_score": normalized_score,
            "eligible": eligible,
            "anchor_matched": anchor_matched,
        })

    ranking.sort(
        key=lambda item: (
            item["normalized_score"],
            item["required_hits"],
        ),
        reverse=True,
    )

    candidates = [
        item
        for item in ranking
        if item["eligible"]
    ]

    if not candidates:
        goal_id = "unknown"
        reason = "메뉴를 판단할 재료가 부족합니다."

    elif len(candidates) == 1:
        goal_id = candidates[0]["goal_id"]
        reason = "후보 기준을 충족한 메뉴가 하나입니다."

    else:
        score_gap = (
            candidates[0]["normalized_score"]
            - candidates[1]["normalized_score"]
        )

        if score_gap < 0.10:
            goal_id = "unknown"
            reason = (
                "여러 메뉴의 점수가 비슷합니다. "
                "준비할 메뉴를 선택해주세요."
            )
        else:
            goal_id = candidates[0]["goal_id"]
            reason = "후보 중 비교 점수가 가장 높은 메뉴입니다."

    return {
        "goal_id": goal_id,
        "reason": reason,
        "input_items": cart,
        "ranking": ranking,
        "candidate_ids": [
            item["goal_id"]
            for item in candidates
        ],
    }