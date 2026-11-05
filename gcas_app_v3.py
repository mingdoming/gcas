from html import escape

import streamlit as st

from gcas_logic import (
    GOAL_RULES,
    MENU_OPTIONS,
    analyze_cart,
    matches_item,
    decide_intervention,
    infer_goal_from_sequence,
)
from gcas_products import (
    PRODUCTS,
    PRODUCT_LOOKUP,
    CATEGORIES,
)


st.set_page_config(
    page_title="G-CAS | 식재료 장보기",
    layout="wide",
)


# ─────────────────────────────────────
# 상태 관리
# ─────────────────────────────────────
if "shop_cart" not in st.session_state:
    st.session_state.shop_cart = {}

if "meal_items" not in st.session_state:
    st.session_state.meal_items = {}


def add_to_cart(product_id):
    cart = st.session_state.shop_cart
    cart[product_id] = cart.get(product_id, 0) + 1


def decrease_quantity(product_id):
    cart = st.session_state.shop_cart

    if product_id not in cart:
        return

    if cart[product_id] > 1:
        cart[product_id] -= 1
    else:
        cart.pop(product_id)


def remove_from_cart(product_id):
    st.session_state.shop_cart.pop(product_id, None)


def clear_cart():
    st.session_state.shop_cart = {}


def save_meal_choice(choice_key):
    st.session_state.meal_items[choice_key] = (
        st.session_state[choice_key]
    )


def select_inferred_menu(goal_id):
    st.session_state["selected_menu"] = (
        GOAL_RULES[goal_id]["name"]
    )


def menu_name(goal_id):
    if goal_id == "unknown":
        return "판단 보류"

    return GOAL_RULES[goal_id]["name"]


def format_kcal(value):
    return f"{value:,.0f} kcal"


def render_html(content):
    cleaned = "\n".join(
        line.lstrip()
        for line in content.splitlines()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


def matching_products_for(options):
    return [
        product
        for product in PRODUCTS
        if any(
            matches_item(product["analysis_name"], item_id)
            for item_id in options
        )
    ]


# ─────────────────────────────────────
# 디자인
# ─────────────────────────────────────
st.markdown(
    """
<style>
.stApp {
    background: #FAFAF7;
    color: #252C26;
    font-family: "Segoe UI", "Malgun Gothic", sans-serif;
}

.block-container {
    max-width: 1380px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

.shop-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    padding-bottom: 22px;
    border-bottom: 1px solid #E1E4DC;
    margin-bottom: 20px;
}

.brand {
    font-size: 28px;
    font-weight: 850;
    letter-spacing: -1.2px;
    color: #244C38;
}

.header-info {
    color: #747C70;
    font-size: 13px;
}

.shop-banner {
    background: #E9EEE3;
    border: 1px solid #DFE5D8;
    border-radius: 12px;
    padding: 28px 34px;
    margin: 12px 0 28px;
}

.banner-label {
    color: #586B4C;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
}

.banner-title {
    color: #293F2E;
    font-size: clamp(25px, 3vw, 34px);
    font-weight: 750;
    line-height: 1.4;
    letter-spacing: -1px;
    margin-bottom: 10px;
}

.banner-description {
    color: #68735F;
    font-size: 14px;
    line-height: 1.8;
}

.section-heading {
    font-size: 21px;
    font-weight: 750;
    letter-spacing: -0.6px;
    color: #29362A;
    margin-bottom: 6px;
}

.section-note {
    color: #7C8277;
    font-size: 12px;
    line-height: 1.8;
    margin-bottom: 18px;
}

.analysis-title {
    color: #2E4532;
    font-size: 19px;
    font-weight: 750;
    margin-bottom: 10px;
}

.product-card {
    background: white;
    border: 1px solid #E4E7DE;
    border-radius: 12px;
    overflow: hidden;
    margin-top: 6px;
    margin-bottom: 10px;
    transition:
        transform 180ms ease,
        box-shadow 180ms ease,
        border-color 180ms ease;
}

.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(38, 59, 35, 0.09);
    border-color: #A8BA9B;
}

.product-visual {
    height: 135px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.product-package {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 5px;
    padding: 22px 12px;
    color: #52604A;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    text-align: center;
    max-width: 90%;
    overflow-wrap: anywhere;
    transition: transform 220ms ease;
}

.product-card:hover .product-package {
    transform: scale(1.06) rotate(-2deg);
}

.product-body {
    padding: 16px;
}

.product-category {
    font-size: 11px;
    color: #89907F;
    margin-bottom: 7px;
}

.product-name {
    font-size: 16px;
    font-weight: 700;
    color: #2D352A;
    margin-bottom: 6px;
}

.product-description {
    font-size: 12px;
    color: #858A7D;
    min-height: 38px;
    line-height: 1.6;
}

.product-price {
    font-size: 17px;
    font-weight: 750;
    color: #2D352A;
    margin-top: 12px;
}

.product-unit {
    font-size: 12px;
    color: #8A8F82;
    margin-top: 4px;
    min-height: 20px;
}

.product-calorie {
    font-size: 12px;
    color: #65765D;
    margin-top: 8px;
    line-height: 1.8;
}

.cart-line {
    padding: 14px 0 6px;
    border-top: 1px solid #ECEEE6;
}

.cart-name {
    font-size: 14px;
    font-weight: 600;
    color: #34412F;
}

.cart-detail {
    font-size: 12px;
    color: #858C7C;
    margin: 5px 0;
    line-height: 1.8;
}

.cart-empty {
    padding: 28px 8px;
    color: #828A79;
    font-size: 14px;
    line-height: 1.9;
    text-align: center;
}

.cart-heading {
    font-size: 23px;
    font-weight: 750;
    letter-spacing: -0.7px;
    color: #29362A;
    margin-bottom: 6px;
}

.cart-heading-note {
    font-size: 12px;
    color: #818A78;
    margin-bottom: 18px;
}

div.stButton > button {
    border-radius: 7px;
    min-height: 40px;
    transition:
        transform 160ms ease,
        background-color 160ms ease,
        border-color 160ms ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #5A7750;
    color: #31532F;
    background-color: #EDF2E7;
}

/* 오른쪽 장바구니 고정 */
@media (min-width: 900px) {
    [data-testid="stHorizontalBlock"]:has(
        > [data-testid="stColumn"] .cart-sticky-marker
    ) {
        align-items: flex-start;
        overflow: visible;
    }

    [data-testid="stColumn"]:has(.cart-sticky-marker) {
        position: sticky;
        top: 4.5rem;
        align-self: flex-start;
        max-height: calc(100dvh - 5.5rem);
        overflow-y: auto;
        scrollbar-width: thin;
        padding-right: 4px;
    }
}

@media (max-width: 760px) {
    .shop-banner {
        padding: 24px;
    }

    .header-info {
        max-width: 150px;
        text-align: right;
        line-height: 1.7;
    }

    .product-visual {
        height: 110px;
    }
}

@media (prefers-reduced-motion: reduce) {
    .product-card,
    .product-package,
    div.stButton > button {
        transition: none;
    }

    .product-card:hover,
    .product-card:hover .product-package,
    div.stButton > button:hover {
        transform: none;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────
# 상단
# ─────────────────────────────────────
render_html(
    """
<header class="shop-header">
<div class="brand">G-CAS</div>
<div class="header-info">장바구니로 확인하는 식재료 구성</div>
</header>

<section class="shop-banner">
<div class="banner-label">오늘의 장보기</div>
<div class="banner-title">메뉴를 정하고 필요한 재료를 담아보세요.</div>
<div class="banner-description">
담은 재료에 맞는 메뉴와 구매 금액을 확인할 수 있습니다.
</div>
</section>
"""
)


# ─────────────────────────────────────
# 본문 배치
# ─────────────────────────────────────
main_column, cart_column = st.columns(
    [2.3, 1],
    gap="large",
)


with main_column:
    # ── 자동 메뉴 추론 ──
    # 현재 장바구니에 남아 있는 상품 종류의 최초 추가 순서 사용
    cart_sequence = [
        PRODUCT_LOOKUP[product_id]["analysis_name"]
        for product_id in st.session_state.shop_cart
    ]

    full_prediction = infer_goal_from_sequence(
        cart_sequence
    )

    initial_prediction = infer_goal_from_sequence(
        cart_sequence,
        initial_n=3,
    )

    with st.container(border=True):
        st.markdown("**장바구니에서 찾은 메뉴**")

        if not cart_sequence:
            st.caption(
                "상품을 담으면 재료에 맞는 메뉴를 확인할 수 있습니다."
            )

        else:
            full_column, initial_column = st.columns(2)

            with full_column:
                st.caption("전체 장바구니")
                st.markdown(
                    f"**{menu_name(full_prediction['goal_id'])}**"
                )

            with initial_column:
                st.caption("처음 담은 상품 최대 3개")
                st.markdown(
                    f"**{menu_name(initial_prediction['goal_id'])}**"
                )

            st.caption(full_prediction["reason"])

            if full_prediction["goal_id"] != "unknown":
                st.button(
                    "이 메뉴로 재료 확인",
                    key="apply_inferred_menu",
                    use_container_width=True,
                    on_click=select_inferred_menu,
                    args=(full_prediction["goal_id"],),
                )

            elif full_prediction["candidate_ids"]:
                st.caption(
                    "후보 메뉴를 선택해 재료를 확인하세요."
                )

                candidate_columns = st.columns(2)

                for index, goal_id in enumerate(
                    full_prediction["candidate_ids"]
                ):
                    with candidate_columns[index % 2]:
                        st.button(
                            GOAL_RULES[goal_id]["name"],
                            key=f"candidate_{goal_id}",
                            use_container_width=True,
                            on_click=select_inferred_menu,
                            args=(goal_id,),
                        )

            with st.expander("추론 기준 보기"):
                st.caption(
                    "필수 구성 일치에 2점과 선택 구성 일치에 "
                    "1점을 부여한 뒤 목표별 최대 점수로 나눕니다. "
                    "점수는 예측 확률이 아닙니다."
                )
                st.caption(
                    "핵심 재료와 최소 구성 조건을 확인합니다. "
                    "상위 후보의 점수 차이가 0.10 미만이면 "
                    "판단을 보류합니다."
                )
                st.caption(
                    "현재 장바구니에 남은 상품 종류의 추가 순서를 "
                    "사용합니다. 같은 상품의 수량 증가는 "
                    "새로운 순서로 기록하지 않습니다."
                )

    st.write("")

    # ── 직접 메뉴 선택 ──
    render_html(
        """
<div class="section-heading">어떤 메뉴를 준비하시나요?</div>
<div class="section-note">
직접 메뉴를 선택하거나 위의 추론 결과를 적용할 수 있습니다.
</div>
"""
    )

    selected_menu = st.selectbox(
        "준비할 메뉴",
        options=list(MENU_OPTIONS),
        key="selected_menu",
    )

    selected_goal_id = MENU_OPTIONS[selected_menu]

    if selected_goal_id is None:
        st.caption(
            "메뉴를 선택하거나 아래 상품을 둘러보세요."
        )

    elif selected_goal_id not in GOAL_RULES:
        st.info(
            "이 메뉴는 아직 분석 기능을 연결하지 않았습니다."
        )

    else:
        result = analyze_cart(
            cart_sequence,
            selected_goal_id,
        )

        completion = result["completion_rate"]

        required_details = [
            detail
            for detail in result["details"]
            if detail["required"]
        ]

        missing_count = sum(
            not detail["fulfilled"]
            for detail in required_details
        )

        missing_rate = (
            missing_count / len(required_details)
        )

        intervention = decide_intervention(
            selected_goal_id,
            missing_rate,
        )

        goal_config = GOAL_RULES[selected_goal_id]

        with st.container(border=True):
            title_column, metric_column = st.columns(
                [1.4, 1]
            )

            with title_column:
                render_html(
                    f"""
<div class="analysis-title">
{escape(result["goal_name"])}
</div>
"""
                )

                if result["missing_groups"]:
                    missing_text = " · ".join(
                        result["missing_groups"]
                    )
                    st.write(
                        f"필요한 구성: {missing_text}"
                    )
                else:
                    st.write(
                        "기본 구성이 갖춰졌습니다."
                    )

            with metric_column:
                st.metric(
                    "필수 구성 충족률",
                    f"{completion:.0%}",
                )

            st.progress(completion)

            st.caption(
                f"필수 구성 {len(required_details)}개 중 "
                f"{len(required_details) - missing_count}개 충족"
                f" · 누락률 {missing_rate:.0%}"
            )

            if intervention["type"] == "warning":
                st.warning(
                    intervention["message"]
                )

            elif intervention["type"] == "soft_suggest":
                st.info(
                    intervention["message"]
                )

            with st.expander(
                "재료 구성과 바로 담기",
                expanded=True,
            ):
                for detail in result["details"]:
                    label = (
                        "필수"
                        if detail["required"]
                        else "선택"
                    )

                    if detail["fulfilled"]:
                        status = "포함"
                    elif detail["required"]:
                        status = "필요"
                    else:
                        status = "추가 가능"

                    st.markdown(
                        f"**{detail['name']}**"
                        f" · {label} · {status}"
                    )

                    group_type = (
                        "required"
                        if detail["required"]
                        else "optional"
                    )

                    options = goal_config[group_type][
                        detail["name"]
                    ]

                    matching_products = (
                        matching_products_for(options)
                    )

                    if matching_products:
                        for start in range(
                            0,
                            len(matching_products),
                            2,
                        ):
                            button_columns = (
                                st.columns(2)
                            )

                            for column, product in zip(
                                button_columns,
                                matching_products[
                                    start:start + 2
                                ],
                            ):
                                quantity = (
                                    st.session_state.shop_cart.get(
                                        product["id"],
                                        0,
                                    )
                                )

                                if quantity:
                                    button_label = (
                                        f"{product['name']}"
                                        f" · {quantity}개 담음 +"
                                    )
                                else:
                                    button_label = (
                                        f"{product['name']} +"
                                    )

                                with column:
                                    st.button(
                                        button_label,
                                        key=(
                                            f"ingredient_"
                                            f"{selected_goal_id}_"
                                            f"{detail['name']}_"
                                            f"{product['id']}"
                                        ),
                                        use_container_width=True,
                                        on_click=add_to_cart,
                                        args=(
                                            product["id"],
                                        ),
                                    )
                    else:
                        st.caption(
                            "현재 등록된 상품이 없습니다."
                        )

                    st.caption(
                        "사용 가능한 재료: "
                        + " · ".join(
                            detail["alternatives"]
                        )
                    )

                st.caption(
                    "충족률은 재료 역할을 기준으로 계산합니다. "
                    "수량과 영양 균형은 평가하지 않습니다."
                )

        # ── 한 끼 예상 열량 ──
        eligible_products = [
            product
            for product in PRODUCTS
            if product["id"] in st.session_state.shop_cart
            and any(
                matches_item(
                    product["analysis_name"],
                    item_id,
                )
                for groups in (
                    goal_config["required"],
                    goal_config["optional"],
                )
                for options in groups.values()
                for item_id in options
            )
        ]

        if eligible_products:
            with st.expander(
                "한 끼 예상 열량 확인"
            ):
                st.caption(
                    "사용할 재료를 선택하세요. "
                    "표시된 사용량을 한 번씩 합산합니다."
                )

                meal_calories = 0
                selected_count = 0

                for product in eligible_products:
                    choice_key = (
                        f"meal_{selected_goal_id}_"
                        f"{product['id']}"
                    )

                    if choice_key not in st.session_state:
                        st.session_state[choice_key] = (
                            st.session_state.meal_items.get(
                                choice_key,
                                False,
                            )
                        )

                    include = st.checkbox(
                        (
                            f"{product['name']} "
                            f"{product['serving_label']} · "
                            f"{format_kcal(product['kcal_per_serving'])}"
                        ),
                        key=choice_key,
                        on_change=save_meal_choice,
                        args=(choice_key,),
                    )

                    if include:
                        selected_count += 1
                        meal_calories += (
                            product["kcal_per_serving"]
                        )

                st.metric(
                    "선택한 재료의 예상 열량",
                    format_kcal(meal_calories)
                    if selected_count
                    else "—",
                )

                st.caption(
                    "영양정보는 시연용 예시입니다. "
                    "선택하지 않은 재료와 조리용 기름 등은 "
                    "계산에 포함되지 않습니다."
                )

    st.divider()

    # ── 검색과 카테고리 ──
    render_html(
        """
<div class="section-heading">식재료 둘러보기</div>
<div class="section-note">
상품과 가격 및 영양정보는 시연용 예시입니다.
</div>
"""
    )

    search_query = st.text_input(
        "상품 검색",
        placeholder="찾는 식재료를 검색하세요",
        label_visibility="collapsed",
    )

    category = st.radio(
        "상품 카테고리",
        CATEGORIES,
        horizontal=True,
        label_visibility="collapsed",
    )

    query = search_query.strip().casefold()

    filtered_products = [
        product
        for product in PRODUCTS
        if (
            category == "전체"
            or product["category"] == category
        )
        and query in product["name"].casefold()
    ]

    st.caption(
        f"상품 {len(filtered_products)}개"
    )

    if not filtered_products:
        st.info(
            "검색한 상품이 없습니다."
        )

    # ── 상품 카드 ──
    for start in range(
        0,
        len(filtered_products),
        3,
    ):
        product_columns = st.columns(3)

        for column, product in zip(
            product_columns,
            filtered_products[start:start + 3],
        ):
            with column:
                serving_kcal = format_kcal(
                    product["kcal_per_serving"]
                )
                pack_kcal = format_kcal(
                    product["kcal_per_pack"]
                )

                render_html(
                    f"""
<article class="product-card">
<div class="product-visual" style="background: {product['color']};">
<div class="product-package">
{escape(product['symbol'])}
</div>
</div>
<div class="product-body">
<div class="product-category">
{escape(product['category'])}
</div>
<div class="product-name">
{escape(product['name'])}
</div>
<div class="product-description">
{escape(product['description'])}
</div>
<div class="product-price">
{product['price']:,}원
</div>
<div class="product-unit">
{escape(product['unit'])}
</div>
<div class="product-calorie">
{escape(product['serving_label'])} 기준 {serving_kcal}<br>
포장 전체 {pack_kcal}
</div>
</div>
</article>
"""
                )

                st.button(
                    "담기",
                    key=f"add_{product['id']}",
                    use_container_width=True,
                    on_click=add_to_cart,
                    args=(product["id"],),
                )


# ─────────────────────────────────────
# 오른쪽 장바구니
# ─────────────────────────────────────
with cart_column:
    render_html(
        '<span class="cart-sticky-marker"></span>'
    )

    with st.container(border=True):
        total_quantity = sum(
            st.session_state.shop_cart.values()
        )

        render_html(
            f"""
<div class="cart-heading">장바구니</div>
<div class="cart-heading-note">
상품 {len(st.session_state.shop_cart)}종 · 총 {total_quantity}개
</div>
"""
        )

        if not st.session_state.shop_cart:
            render_html(
                """
<div class="cart-empty">
아직 담은 상품이 없습니다.<br>
왼쪽의 재료 버튼이나 상품 목록에서<br>
필요한 상품을 담아주세요.
</div>
"""
            )

        total_price = 0
        total_calories = 0

        for product_id, quantity in list(
            st.session_state.shop_cart.items()
        ):
            product = PRODUCT_LOOKUP[product_id]

            subtotal = (
                product["price"] * quantity
            )

            product_calories = (
                product["kcal_per_pack"] * quantity
            )

            total_price += subtotal
            total_calories += product_calories

            render_html(
                f"""
<div class="cart-line">
<div class="cart-name">
{escape(product['name'])}
</div>
<div class="cart-detail">
{escape(product['unit'])} × {quantity}개<br>
{subtotal:,}원 · {format_kcal(product_calories)}
</div>
</div>
"""
            )

            minus_column, plus_column, delete_column = (
                st.columns([1, 1, 1.5])
            )

            with minus_column:
                st.button(
                    "−",
                    key=f"minus_{product_id}",
                    use_container_width=True,
                    on_click=decrease_quantity,
                    args=(product_id,),
                )

            with plus_column:
                st.button(
                    "＋",
                    key=f"plus_{product_id}",
                    use_container_width=True,
                    on_click=add_to_cart,
                    args=(product_id,),
                )

            with delete_column:
                st.button(
                    "삭제",
                    key=f"remove_{product_id}",
                    use_container_width=True,
                    on_click=remove_from_cart,
                    args=(product_id,),
                )

        st.divider()

        st.metric(
            "상품 합계",
            f"{total_price:,}원",
        )

        st.metric(
            "구매 상품 총열량",
            format_kcal(total_calories)
            if st.session_state.shop_cart
            else "—",
        )

        st.caption(
            "구매한 포장 전체의 열량입니다. "
            "한 끼 섭취 열량과는 다릅니다."
        )

        st.caption(
            "영양정보는 시연용 예시입니다."
        )

        if st.session_state.shop_cart:
            st.button(
                "장바구니 비우기",
                key="clear_cart",
                use_container_width=True,
                on_click=clear_cart,
            )

    st.caption(
        "배송과 결제 기능은 제공하지 않습니다."
    )