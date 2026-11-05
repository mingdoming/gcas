# gcas_products.py
# 상품명과 용량 및 가격과 열량은 시연용 예시입니다.
# 실제 판매용으로 사용할 때는 제품 정보로 교체해야 합니다.

CATEGORY_COLORS = {
    "채소": "#DBE6D5",
    "과일": "#EFE2D6",
    "베이커리": "#EEE3D2",
    "유제품·달걀": "#EDEADF",
    "육류·생선": "#EADDD7",
    "쌀·면": "#EAE2CE",
    "두부·콩": "#E5E7DC",
    "소스·양념": "#E2E5D7",
    "간식": "#EFE5D8",
    "음료": "#DFE8E5",
}

# 각 행의 순서:
# ID / 한글명 / 분석용 이름 / 카테고리 / 설명
# 판매 단위 / 가격 / 포장 전체 kcal
# 메뉴 사용량 / 해당 사용량 kcal

PRODUCT_ROWS = [
    (
        "bread", "통밀 식빵", "Whole Wheat Bread",
        "베이커리", "샌드위치와 토스트용",
        "400g · 20장", 3900, 1000,
        "2장 · 40g", 100,
    ),
    (
        "bagel", "플레인 베이글", "Plain Bagels",
        "베이커리", "달걀이나 치즈를 곁들이기 좋은 빵",
        "4개", 4800, 1000,
        "1개", 250,
    ),
    (
        "tortilla", "밀 또띠아", "Flour Tortillas",
        "베이커리", "채소와 메인 재료를 넣어 만드는 랩",
        "6장", 4200, 900,
        "1장", 150,
    ),
    (
        "egg", "신선한 달걀", "Large Brown Eggs",
        "유제품·달걀", "아침 식사와 볶음밥용",
        "10구", 4900, 700,
        "1개", 70,
    ),
    (
        "cheese", "체더 치즈", "Cheddar Cheese",
        "유제품·달걀", "샌드위치와 토스트에 한 장씩",
        "200g · 10매", 4200, 800,
        "1장 · 20g", 80,
    ),
    (
        "milk", "우유", "Whole Milk",
        "유제품·달걀", "시리얼과 함께 준비하는 우유",
        "1L", 2900, 650,
        "200mL", 130,
    ),
    (
        "yogurt", "플레인 요거트", "Plain Yogurt",
        "유제품·달걀", "과일이나 오트밀에 곁들이는 요거트",
        "400g", 3900, 280,
        "100g", 70,
    ),
    (
        "cream", "쿠킹크림", "Cooking Cream",
        "유제품·달걀", "크림 파스타와 수프용",
        "200mL", 3500, 600,
        "50mL", 150,
    ),
    (
        "parmesan", "파르메산 치즈", "Parmesan Cheese",
        "유제품·달걀", "파스타 위에 곁들이는 치즈",
        "100g", 5900, 420,
        "10g", 42,
    ),
    (
        "lettuce", "로메인", "Romaine Lettuce",
        "채소", "샐러드와 샌드위치용",
        "200g", 2500, 34,
        "20g", 3.4,
    ),
    (
        "tomato", "방울토마토", "Cherry Tomatoes",
        "채소", "샐러드에 곁들이기 좋은 채소",
        "500g", 5900, 90,
        "50g", 9,
    ),
    (
        "cucumber", "오이", "Fresh Cucumber",
        "채소", "샐러드와 샌드위치용",
        "300g", 2200, 45,
        "50g", 7.5,
    ),
    (
        "carrot", "당근", "Fresh Carrots",
        "채소", "볶음밥과 카레에 사용하는 채소",
        "500g", 2800, 200,
        "50g", 20,
    ),
    (
        "onion", "양파", "Yellow Onions",
        "채소", "볶음 요리와 국물 요리용",
        "1kg", 3500, 400,
        "50g", 20,
    ),
    (
        "potato", "감자", "Fresh Potatoes",
        "채소", "카레와 된장찌개용",
        "1kg", 4500, 770,
        "100g", 77,
    ),
    (
        "spinach", "시금치", "Baby Spinach",
        "채소", "샐러드와 달걀 요리용",
        "200g", 2900, 46,
        "50g", 11.5,
    ),
    (
        "mushroom", "양송이버섯", "Button Mushrooms",
        "채소", "파스타와 카레에 곁들이는 버섯",
        "200g", 3200, 44,
        "50g", 11,
    ),
    (
        "green_onion", "대파", "Green Onions",
        "채소", "볶음밥과 찌개용",
        "300g", 2500, 90,
        "20g", 6,
    ),
    (
        "zucchini", "애호박", "Korean Zucchini",
        "채소", "된장찌개와 볶음 요리용",
        "300g", 1900, 60,
        "50g", 10,
    ),
    (
        "banana", "바나나", "Fresh Bananas",
        "과일", "요거트와 오트밀에 곁들이는 과일",
        "가식부 600g", 3900, 540,
        "가식부 100g", 90,
    ),
    (
        "apple", "사과", "Fresh Apples",
        "과일", "아침 식사에 곁들이는 과일",
        "가식부 600g", 6500, 312,
        "가식부 100g", 52,
    ),
    (
        "ham", "슬라이스 햄", "Sliced Ham",
        "육류·생선", "샌드위치와 볶음밥용",
        "200g", 3900, 500,
        "40g", 100,
    ),
    (
        "chicken", "닭가슴살", "Chicken Breast",
        "육류·생선", "샐러드와 카레용",
        "400g", 6900, 440,
        "100g", 110,
    ),
    (
        "pork", "돼지고기", "Pork Shoulder",
        "육류·생선", "김치찌개와 카레용",
        "400g", 7900, 1000,
        "100g", 250,
    ),
    (
        "tuna", "참치", "Canned Tuna",
        "육류·생선", "샌드위치와 볶음밥용",
        "150g", 2900, 300,
        "50g", 100,
    ),
    (
        "tofu", "두부", "Firm Tofu",
        "두부·콩", "찌개와 샐러드용",
        "300g", 1900, 240,
        "100g", 80,
    ),
    (
        "rice", "쌀", "White Rice",
        "쌀·면", "밥과 볶음밥용",
        "1kg · 생쌀", 4900, 3600,
        "생쌀 80g", 288,
    ),
    (
        "pasta", "스파게티", "Spaghetti",
        "쌀·면", "토마토 파스타와 크림 파스타용",
        "500g", 3200, 1750,
        "마른 면 100g", 350,
    ),
    (
        "oatmeal", "오트밀", "Rolled Oats",
        "쌀·면", "우유나 요거트와 함께 준비하는 오트밀",
        "500g", 4900, 1900,
        "40g", 152,
    ),
    (
        "cereal", "시리얼", "Breakfast Cereal",
        "간식", "우유와 함께 준비하는 시리얼",
        "300g", 4500, 1140,
        "30g", 114,
    ),
    (
        "tomato_sauce", "토마토 소스", "Tomato Pasta Sauce",
        "소스·양념", "토마토 파스타용",
        "400g", 3900, 280,
        "100g", 70,
    ),
    (
        "pesto", "바질 페스토", "Basil Pesto",
        "소스·양념", "파스타와 샌드위치용",
        "100g", 4900, 450,
        "20g", 90,
    ),
    (
        "dressing", "샐러드 드레싱", "Salad Dressing",
        "소스·양념", "채소에 곁들이는 드레싱",
        "200g", 3500, 600,
        "20g", 60,
    ),
    (
        "curry", "카레 소스", "Curry Sauce",
        "소스·양념", "고기와 채소를 더해 준비하는 카레",
        "200g", 2900, 200,
        "100g", 100,
    ),
    (
        "doenjang", "된장", "Soybean Paste",
        "소스·양념", "된장찌개용",
        "500g", 4900, 1000,
        "20g", 40,
    ),
    (
        "kimchi", "배추김치", "Cabbage Kimchi",
        "채소", "김치찌개와 볶음밥용",
        "500g", 5900, 150,
        "100g", 30,
    ),
    (
        "soy_sauce", "간장", "Soy Sauce",
        "소스·양념", "볶음밥과 달걀 요리의 간 맞추기",
        "500mL", 3500, 300,
        "10mL", 6,
    ),
    (
        "chips", "감자칩", "Potato Chips",
        "간식", "간편하게 준비하는 간식",
        "100g", 2200, 540,
        "30g", 162,
    ),
    (
        "chocolate", "밀크 초콜릿", "Milk Chocolate Bar",
        "간식", "조각으로 나눠 먹는 초콜릿",
        "100g", 2500, 550,
        "20g", 110,
    ),
    (
        "tea", "녹차", "Green Tea",
        "음료", "간식에 곁들이는 무가당 차",
        "500mL", 1500, 0,
        "250mL", 0,
    ),
]


def build_product(row):
    (
        product_id,
        name,
        analysis_name,
        category,
        description,
        unit,
        price,
        kcal_per_pack,
        serving_label,
        kcal_per_serving,
    ) = row

    return {
        "id": product_id,
        "name": name,
        "analysis_name": analysis_name,
        "category": category,
        "description": description,
        "unit": unit,
        "price": price,
        "kcal_per_pack": kcal_per_pack,
        "serving_label": serving_label,
        "kcal_per_serving": kcal_per_serving,
        "symbol": product_id.replace("_", " ").upper(),
        "color": CATEGORY_COLORS[category],
    }


PRODUCTS = [
    build_product(row)
    for row in PRODUCT_ROWS
]

PRODUCT_LOOKUP = {
    product["id"]: product
    for product in PRODUCTS
}

CATEGORIES = ["전체"] + list(CATEGORY_COLORS)


if __name__ == "__main__":
    print(f"등록 상품: {len(PRODUCTS)}개")
    print(f"카테고리: {len(CATEGORY_COLORS)}개")