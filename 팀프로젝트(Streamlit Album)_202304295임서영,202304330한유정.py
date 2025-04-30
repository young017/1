import streamlit as st

print("page reload")
st.set_page_config(
    page_title="사진 앨범",
    page_icon="https://img.freepik.com/premium-vector/camera-icon_861234-1831.jpg"
)

st.title("📸 사진 앨범")
st.markdown("**사진**을 하나씩 추가해서 앨범을 채워보세요!")

# 사진 분류 옵션
type_emoji_set = {
    "인물", "풍경", "여행", "접사", "패션", "음식", "거리", "스포츠", "연예인", "기타"
}

# 초기 앨범 데이터
initial_albums = [
    {
        "name": "무뚝뚝 감자칩",
        "types": ["음식"],
        "image_url": "https://i.namu.wiki/i/Ztj7yW0WJv8UmsDRkIIjN6i1I6CKkGDLwEZFiT9JicteruGBILVrCQ-F5_jx5VRlTyN5D8ePmtgc58kc2EzPvT30-t1F1cTRXx8vkvfovJF_7jCTyuf2jyVmGjXYzxeNTPs-1wtW8-HVxR8T9-_X8A.webp",
        "date" : "2025-03-28"
    },
    {
        "name": "스위스",
        "types": ["여행"],
        "image_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTAzMjZfMTM2%2FMDAxNzQyOTgyNzA0OTU2.DQ302rnDdN1FfwmrlAltWL60KAMD3q-KP7HdNL3CPjcg.zHs-y747pHDbXntnGRmXS6QE8rhJqKyHA_PCo0TzmA8g.JPEG%2F33.jpg&type=sc960_832",
        "date" : "2024-12-18"
    },
    {
        "name": "고윤정",
        "types": ["인물"],
        "image_url": "https://i.namu.wiki/i/xl7WXBmp2VQ7mQRz53DlZ_7S1O4CEA_6RERhydKMTPYsdK9oXAcvqhtijh_rHQNw1fYt7skGA4vnMOJNg40jQA.webp",
        "date" : "1996-04-22"
    },
    {
        "name": "은행나무",
        "types": ["풍경"],
        "image_url": "https://i.pinimg.com/236x/7b/a8/47/7ba84701e6258cbf65c1f5d42685e2cc.jpg",
        "date" : "2025-04-05"
    },
]

# 세션 상태에 앨범 저장
if "albums" not in st.session_state:
    st.session_state.albums = initial_albums

# 자동 입력 예시
auto_complete = st.toggle("예시 데이터로 채우기")
print("page_reload.auto_complete", auto_complete)

example_album = {
    "name": "마라탕",
    "types": ["음식"],
    "date": "2025-04-30",
    "image_url": "https://m.피슈마라홍탕.net/img/page/menu/pick_01.png"
}

# 사진 추가 form
with st.form(key="form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input(
            label="사진 제목",
            value=example_album['name'] if auto_complete else "",
            key="name_input"
        )
    with col2:
        types = st.multiselect(
            label="사진 종류",
            options=list(type_emoji_set),
            max_selections=2,
            default=example_album['types'] if auto_complete else [],
            key="types_input"
        )
    with col3:
        date = st.text_input(
            label="날짜 (선택사항)",
            value=example_album['date'] if auto_complete else "",
            key="date_input"
        )
    image_url = st.text_input(
        label="사진 이미지 URL",
        value=example_album['image_url'] if auto_complete else "",
        key="image_url_input"
    )

    submit = st.form_submit_button(label="사진 추가")
    if submit:
        print("name", name)
        print("types", types)
        print("image url", image_url)

        if not name:
            st.error("사진 제목을 입력해주세요.")
        elif len(types) == 0:
            st.error("사진 종류를 선택해주세요.")
        else:
            st.success("사진을 추가하였습니다.")
            st.session_state.albums.append({
                'name': name,
                'types': types,
                'date': date,
                'image_url': image_url if image_url else 'https://blog.kakaocdn.net/dn/tToNP/btsvPnc77bN/0P5cqJMFM8hpaQcrIbK6v1/img.gif'
            })

# 사진 카드로 출력
st.subheader("📷 내 사진 목록")

for i in range(0, len(st.session_state.albums), 4):
    row_albums = st.session_state.albums[i:i+4]
    cols = st.columns(4)

    for j in range(len(row_albums)):
        album = row_albums[j]
        with cols[j]:
           with st.expander(label=f"**{i+j+1}. {album['name']}**", expanded=True):
                st.markdown(f"""
                    <div style="display: flex; justify-content: center;">
                        <img src="{album['image_url']}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px;" />
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<p style='text-align: center; color: gray;'> {album.get('date', '날짜 없음')}</p>", unsafe_allow_html=True)
                st.markdown(
                    f"<p style='text-align: center; font-size: 20px; color: #555;'> {' / '.join(album['types'])}</p>",
                    unsafe_allow_html=True
)

                
                delete_button = st.button(label="삭제", key=f"delete_{i+j}", use_container_width=True)

                if delete_button:
                    del st.session_state.albums[i + j]
                    st.rerun()
