from cvzone.HandTrackingModule import HandDetector
import cv2

# Fungsi untuk mendeteksi tangan dan memberikan posisi ujung jari
detector = HandDetector(detectionCon=0.8, maxHands=1)

def detect_hands(frame):
    hands, img = detector.findHands(frame, flipType=False)
    return hands, img
