import cv2
import mediapipe as mp
import pyttsx3
import time

# 1. SETUP ENGINE SUARA
engine = pyttsx3.init()
# Mengatur kecepatan bicara agar lebih natural
engine.setProperty('rate', 150)

# 2. SETUP MEDIAPIPE
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

# Variabel untuk cooldown agar suara tidak menumpuk
last_speak_time = 0
cooldown_seconds = 1  # Jeda 2 detik antar suara


# Fungsi bantu untuk mengecek status jari (Naik/Turun)
# Mengembalikan True jika jari naik, False jika turun
def is_finger_up(landmarks, tip_id, pip_id):
    # Perhatikan: Di layar, Y makin ke bawah makin besar.
    # Jadi jika Y ujung (tip) < Y ruas (pip), berarti jari sedang NAIK.
    return landmarks[tip_id].y < landmarks[pip_id].y


while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip dan Konversi Warna
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # --- LOGIKA DETEKSI POSISI JARI ---
            # ID Landmark MediaPipe:
            # Telunjuk: Ujung = 8, Ruas Bawah = 6
            # Tengah:   Ujung = 12, Ruas Bawah = 10

            telunjuk_naik = is_finger_up(hand_landmarks.landmark, 8, 6)
            tengah_naik = is_finger_up(hand_landmarks.landmark, 12, 10)

            # Kita juga cek jari manis & kelingking agar gerakan lebih akurat
            # (opsional, tapi disarankan agar gesture 'v' benar-benar 'v')
            manis_naik = is_finger_up(hand_landmarks.landmark, 16, 14)
            kelingking_naik = is_finger_up(hand_landmarks.landmark, 20, 18)

            pesan = ""

            # --- LOGIKA PEMETAAN PERINTAH ---
            # Logika 1: Telunjuk & Tengah NAIK (Gesture "Peace"/V) -> TEMAN
            if telunjuk_naik and tengah_naik and not manis_naik:
                pesan = "Teman"

            # Logika 2: HANYA Telunjuk NAIK -> HALO
            elif telunjuk_naik and not tengah_naik and not manis_naik:
                pesan = "Halo"

            # Logika 3: HANYA Tengah NAIK -> BANGSA
            elif not telunjuk_naik and tengah_naik and not manis_naik:
                pesan = "Cinta"

            # --- EKSEKUSI SUARA ---
            if pesan != "":
                # Tampilkan teks di layar
                cv2.putText(image, f"Perintah: {pesan}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Cek waktu sekarang vs waktu terakhir bicara
                current_time = time.time()
                if current_time - last_speak_time > cooldown_seconds:
                    print(f"Mengucapkan: {pesan}")
                    engine.say(pesan)
                    engine.runAndWait()
                    last_speak_time = current_time

    cv2.imshow('Gesture Recognition', image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
