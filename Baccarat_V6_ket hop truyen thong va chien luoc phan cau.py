
import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Baccarat V6 - Truyền Thống & Phản Cầu", layout="wide")
st.title("♟️ Baccarat V6: Kết Hợp Cầu Truyền Thống & Chiến Lược Phản Cầu")

st.write("🔤 Nhập nhiều chuỗi kết quả Baccarat (mỗi dòng 1 bàn, ví dụ: BBPPBPBBP)")

input_text = st.text_area("📥 Nhập dữ liệu bàn:", height=200)

# Phân tích từng bàn
def analyze_table(results, table_id):
    last = results[-1]
    traps = []
    streak = 1
    for i in range(len(results) - 2, -1, -1):
        if results[i] == last:
            streak += 1
        else:
            break
    cau_truyen_thong = ""
    if streak >= 3:
        cau_truyen_thong = f"Cầu Bệt {last} ({streak})"
    elif len(results) >= 6:
        if all(results[-i] != results[-i - 1] for i in range(1, 4)):
            cau_truyen_thong = "Cầu 1-1"

    if streak >= 5:
        traps.append(f"Bệt {last} ({streak})")
    if len(results) >= 6:
        last6 = results[-6:]
        if last6[0] != last6[1] and last6[1] != last6[2] and last6[2] != last6[3]:
            traps.append("1-1 lặp")

    counter = Counter(results)
    total = len(results)
    b_pct = counter['B'] / total * 100 if 'B' in counter else 0
    p_pct = counter['P'] / total * 100 if 'P' in counter else 0
    diff = abs(b_pct - p_pct)
    bias = "Cân bằng"
    if diff >= 30:
        bias = "Lệch mạnh"
    elif diff >= 15:
        bias = "Lệch nhẹ"

    rhythm = ""
    if len(results) >= 4:
        last4 = results[-4:]
        if last4.count(last4[0]) == 4:
            rhythm = "1 màu 4 lần"
        elif len(set(last4)) == 4:
            rhythm = "Nhiễu cao"
        else:
            rhythm = "Ổn định"

    score = 0
    if traps: score += 3
    if bias == "Lệch mạnh": score += 2
    elif bias == "Lệch nhẹ": score += 1
    if "1 màu" in rhythm: score += 2
    elif "Nhiễu" in rhythm: score += 1

    # Gợi ý truyền thống
    if cau_truyen_thong:
        theo_cau = f"🟢 Theo {cau_truyen_thong}"
    else:
        theo_cau = "⚪ Chưa hình thành cầu"

    # Gợi ý phản cầu
    if score >= 6:
        phan_cau = "🧨 Đánh NGƯỢC mạnh"
    elif score >= 3:
        phan_cau = "⚠️ Cân nhắc đánh ngược"
    else:
        phan_cau = "🟢 Không nên phản cầu"

    return {
        "Bàn": f"Bàn {table_id}",
        "Dài": len(results),
        "Cầu truyền thống": cau_truyen_thong or "Không rõ",
        "Theo cầu": theo_cau,
        "Bẫy cầu": ", ".join(traps) if traps else "Không",
        "Lệch B/P": f"B: {b_pct:.1f}% - P: {p_pct:.1f}%",
        "Nhịp bàn": rhythm,
        "Điểm phản cầu": score,
        "Gợi ý phản cầu": phan_cau
    }

# Phân tích toàn bộ
if input_text.strip():
    rows = input_text.strip().splitlines()
    all_results = []
    for idx, line in enumerate(rows, 1):
        clean = [c for c in line.upper() if c in ['B', 'P']]
        if len(clean) >= 6:
            result = analyze_table(clean, idx)
            all_results.append(result)

    if all_results:
        df = pd.DataFrame(all_results)
        st.subheader("📋 Tổng hợp Cầu Truyền Thống & Phản Cầu:")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Tải bảng phân tích CSV", data=csv, file_name="cau_truyen_thong_vs_phan_cau.csv", mime="text/csv")
    else:
        st.warning("⚠️ Mỗi bàn cần ít nhất 6 kết quả!")
