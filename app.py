import streamlit as st

# إعداد الصفحة وتنزيل الـ CSS المتوافق مع الوضعين الداكن والمضيء
st.set_page_config(page_title="حاسبة الهندسة الكهربائية", layout="centered")

st.title("⚡ منصة الحسابات الكهربائية السريعة")
st.write("مرحباً بك يا هندسة. اختر الأداة المطلوبة من التبويبات بالأسفل لإجراء الحسابات فوراً:")

# إنشاء التبويبات (Tabs) لتنظيم الأدوات الثلاثة
tab1, tab2, tab3 = st.tabs([
    "📊 حساب الـ KVA", 
    "🔌 حساب تيار الحمل (Current)", 
    "🛡️ حساب القاطع الكهربائي (CB)"
])

# ------------------------------------------------------------------
# التبويب الأول: KVA CALCULATION
# ------------------------------------------------------------------
with tab1:
    st.header("📊 حساب القدرة الظاهرية (KVA)")
    
    power_val = st.number_input("أدخل قيمة القدرة (Power Value):", min_value=0.0, value=1.0, step=0.5, key="p_val")
    
    load_name = st.selectbox(
        "نوع الحمل (Load Name):",
        options=[('Motor', 'motor'), ('Motor with Inverter', 'motor with inverter'), ('Other', 'other')],
        format_func=lambda x: x[0],
        key="l_name"
    )
    
    power_unit = st.selectbox(
        "الوحدة (Unit):",
        options=[('KW', 'kw'), ('HP', 'hp')],
        format_func=lambda x: x[0],
        key="p_unit"
    )
    
    if st.button("Calculate KVA", type="primary"):
        a = power_val
        x = load_name[1]
        y = power_unit[1]

        if x == "motor" and y == 'kw':
            result = a / 0.8
        elif x == "motor with inverter" and y == 'kw':
            result = a / 0.7
        else:
            result = a

        st.markdown("---")
        st.success(f"🎯 **النتيجة:** Rated Power هي **{result:.2f} KVA**")

# ------------------------------------------------------------------
# التبويب الثاني: LOAD CURRENT CALCULATION
# ------------------------------------------------------------------
with tab2:
    st.header("🔌 حساب تيار الحمل (Load Current)")
    
    power_input = st.number_input("القدرة بالكيلو فولت أمبير Power (KVA):", min_value=0.0, value=1.0, step=0.5, key="p_input")
    
    phase_dropdown = st.selectbox(
        "نوع الفاز (Phase Type):",
        options=[('1-Phase', '1-phase'), ('3-Phase', '3-phase')],
        format_func=lambda x: x[0],
        key="phase_drop"
    )
    
    if st.button("Calculate Current", type="secondary"):
        t = power_input
        z = phase_dropdown[1]

        st.markdown("---")
        if z == "3-phase":
            current = t * 1.5
            st.warning(f"⚡ **تيار الحمل المستمر:** {current:.2f} Ampere")
        elif z == "1-phase":
            current = t * 4.5
            st.warning(f"⚡ **تيار الحمل المستمر:** {current:.2f} Ampere")
        else:
            st.error("خطأ في الاختيار")

# ------------------------------------------------------------------
# التبويب الثالث: CIRCUIT BREAKER CALCULATION
# ------------------------------------------------------------------
with tab3:
    st.header("🛡️ اختيار القاطع الحامي (Circuit Breaker)")
    
    u_input = st.number_input("القدرة بالكيلو فولت أمبير Power (KVA):", min_value=0.0, value=0.0, step=1.0, key="u_in")
    
    g_dropdown = st.selectbox(
        "نوع الفاز للشيكة (Phase Type):",
        options=[('1-Phase', '1-phase'), ('3-Phase', '3-phase')],
        format_func=lambda x: x[0],
        key="g_drop"
    )
    
    if st.button("Calculate CB"):
        u = u_input
        g = g_dropdown[1]

        st.markdown("---")
        if u > 25:
            result = 2 * u
            st.info(f"🛡️ **سعة القاطع المناسب (CB):** {result:.1f} Ampere")
        elif 0 < u <= 25:
            if g == "3-phase" and u > 5:
                result = round(u * 3.3, 1)
                st.info(f"🛡️ **سعة القاطع المناسب (CB):** {result} Ampere")
            elif g == "1-phase" and u < 10:
                result = round(u * 10, 1)
                st.info(f"🛡️ **سعة القاطع المناسب (CB):** {result} Ampere")
            else:
                st.error("تنبيه: خارج النطاق المحدد للمجال الصغير (Out of range).")
        else:
            st.error("خطأ: يجب أن يكون التيار أو القدرة أكبر من الصفر!")
