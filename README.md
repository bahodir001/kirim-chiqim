# 💰 Finance_01 – Kirim/Chiqim Hisoboti Ilovasi

`Finance_01` — bu foydalanuvchilar uchun oylik, haftalik va kunlik daromad/harajatlarni boshqarish imkonini beruvchi web ilova. U Django va Django Rest Framework asosida ishlab chiqilgan va mobil qurilmalar uchun ham moslashtirilgan.

---

## 🚀 Asosiy Imkoniyatlar

- 🔐 Foydalanuvchi autentifikatsiyasi (email, telefon, karta raqami)
- 💸 Kirimlar (oylik, avans, biznes daromad)
- 🧾 Chiqimlar (yo‘l, salomatlik, ko‘ngil ochish, soliqlar va h.k.)
- 📊 Kirim/chiqim grafiklari (Chart.js bilan)
- 👨‍👩‍👧‍👦 Family Mode – umumiy budjetni bo‘lishish
- 🌗 Dark Mode – yorug‘/qorong‘i interfeys
- 📤 PDF va Excel export (DRF endpoints orqali)
- 📱 Mobilga moslashtirilgan responsiv dizayn

---

## ⚙️ Texnologiyalar

- **Backend**: Python, Django, Django REST Framework
- **Frontend**: HTML, CSS (custom), Chart.js
- **Autentifikatsiya**: Email login, custom user modeli
- **Statistika**: Kunlik, oylik hisobotlar, grafiklar
- **Admin Panel**: Maxsus styling va previewlar
- **Login**: Email va password orqali
---

## 🔧 O‘rnatish

```bash
git clone https://github.com/YOUR_USERNAME/Finance_01.git
cd Finance_01
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
