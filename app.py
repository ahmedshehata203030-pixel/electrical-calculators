import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="حاسبة الهندسة الكهربائية الاحترافية", layout="centered")

st.title("⚡ منصة الحسابات الكهربائية المتكاملة")
st.write("مرحباً بك يا هندسة. تم إضافة قسم اختيار المقاسات القياسية (Standard Size) بناءً على طلبك:")

# إنشاء التبويبات الأربعة
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 حساب الـ KVA", 
    "🔌 تيار الحمل (Current)", 
    "🛡️ حساب القاطع (CB)",
    "📏 المقاس القياسي (Standard)"
])

# ------------------------------------------------------------------
# التبويب الأول: KVA CALCULATION
# ------------------------------------------------------------------
with tab1:
    st.header("📊 حساب القدرة الظاهرية (KVA)")
    power_val = st.number_input("أدخل قيمة القدرة:", min_value=0.0, value=1.0, step=0.5, key="tab1_val")
    load_name = st.selectbox("نوع الحمل:", [('Motor', 'motor'), ('Motor with Inverter', 'motor with inverter'), ('Other', 'other')], format_func=lambda x: x[0])
    power_unit = st.selectbox("الوحدة:", [('KW', 'kw'), ('HP', 'hp')], format_func=lambda x: x[0])
    
    if st.button("Calculate KVA"):
        result = power_val / 0.8 if load_name[1] == "motor" and power_unit[1] == 'kw' else (power_val / 0.7 if load_name[1] == "motor with inverter" and power_unit[1] == 'kw' else power_val)
        st.success(f"🎯 النتيجة: **{result:.2f} KVA**")

# ------------------------------------------------------------------
# التبويب الثاني: LOAD CURRENT CALCULATION
# ------------------------------------------------------------------
with tab2:
    st.header("🔌 حساب تيار الحمل")
    power_input = st.number_input("القدرة (KVA):", min_value=0.0, value=1.0, step=0.5, key="tab2_val")
    phase_dropdown = st.selectbox("نوع الفاز:", [('1-Phase', '1-phase'), ('3-Phase', '3-phase')], format_func=lambda x: x[0])
    
    if st.button("Calculate Current"):
        current = power_input * (1.5 if phase_dropdown[1] == "3-phase" else 4.5)
        st.warning(f"⚡ تيار الحمل: **{current:.2f} Ampere**")

# ------------------------------------------------------------------
# التبويب الثالث: CIRCUIT BREAKER CALCULATION
# ------------------------------------------------------------------
with tab3:
    st.header("🛡️ حساب سعة القاطع (Theoretical)")
    u_input = st.number_input("تيار الحمل المحسوب:", min_value=0.0, value=0.0, step=1.0, key="tab3_val")
    g_dropdown = st.selectbox("الفاز للشيكة:", [('1-Phase', '1-phase'), ('3-Phase', '3-phase')], format_func=lambda x: x[0], key="tab3_drop")
    
    if st.button("Calculate CB Capacity"):
        if u_input > 25: result = 2 * u_input
        elif 0 < u_input <= 25:
            if g_dropdown[1] == "3-phase" and u_input > 5: result = round(u_input * 3.3, 1)
            elif g_dropdown[1] == "1-phase" and u_input < 10: result = round(u_input * 10, 1)
            else: result = "Out of range"
        else: result = "Error"
        st.info(f"🛡️ سعة القاطع (نظرياً): **{result} Ampere**")

# ------------------------------------------------------------------
# التبويب الرابع: NEW - STANDARD CB SELECTION
# ------------------------------------------------------------------
with tab4:
    st.header("📏 اختيار المقاس القياسي (Standard Size)")
    st.write("أدخل القيمة المحسوبة للقاطع، وسأقوم باقتراح أقرب مقاس standard متاح في السوق:")

    # إدخال القيمة المحسوبة (من التبويب السابق)
    calculated_amp = st.number_input("أدخل قيمة الأمبير المحسوبة (Calculated Ampere):", min_value=0.0, value=0.0, step=1.0)
    
    # اختيار نوع القاطع
    cb_type = st.radio("اختر نوع القاطع المطلوب:", ["MCB", "MCCB", "ACB"], horizontal=True)

    # القوائم القياسية (Standard Lists)
    MCB_standards = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125,150]
    MCCB_standards = [16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600]
    ACB_standards = [630, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6300]

    if st.button("Find Standard Size"):
        if calculated_amp <= 0:
            st.error("يرجى إدخال قيمة أكبر من الصفر.")
        else:
            # اختيار القائمة بناء على النوع
            if cb_type == "MCB":
                standards = MCB_standards
            elif cb_type == "MCCB":
                standards = MCCB_standards
            else:
                standards = ACB_standards

            # البحث عن أقرب مقاس أكبر من أو يساوي القيمة المحسوبة
            standard_selection = next((x for x in standards if x >= calculated_amp), None)

            if standard_selection:
                st.markdown("---")
                st.success(f"✅ المقاس القياسي المقترح لـ **{cb_type}** هو: **{standard_selection} Ampere**")
                st.info(f"ملاحظة: تم اختيار أقرب مقاس متوفر في السوق المصري والعالمي يغطي القيمة {calculated_amp} أمبير.")
            else:
                st.error(f"عفواً، القيمة المحسوبة تتخطى أكبر مقاس متاح في فئة {cb_type}.")
