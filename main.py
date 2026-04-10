import json
import os

STATE_FILE = "state.json"

DEFAULT_QUIZZES = [
    {
        "question": "영화 '기생충'으로 아카데미 작품상을 수상한 감독은?",
        "choices": ["박찬욱", "봉준호", "홍상수", "이창동"],
        "answer": 2
    },
    {
        "question": "드라마 '오징어 게임'에서 참가자들이 받는 총 상금액은?",
        "choices": ["123억 원", "234억 원", "345억 원", "456억 원"],
        "answer": 4
    },
    {
        "question": "드라마 '이상한 변호사 우영우'에서 우영우가 좋아하는 동물은?",
        "choices": ["얼룩말", "고래", "사자", "펭귄"],
        "answer": 2
    },
    {
        "question": "드라마 '도깨비'에서 도깨비 역할을 맡은 배우는?",
        "choices": ["이민호", "현빈", "공유", "송중기"],
        "answer": 3
    },
    {
        "question": "영화 '극한직업'에서 주연을 맡은 배우가 아닌 사람은?",
        "choices": ["조정석", "이하늬", "류승룡", "진선규"], # 류승룡, 이하늬, 진선규
        "answer": 1
    }
]

class Quiz:
    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index: int):
        print(f"\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer: int):
        return user_answer == self.answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    def quiz_from_dict(data: dict):
        return Quiz(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )
    
class QuizGame:
    def __init__(self):
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]

    def show_menu(self):
        print("\n========================================")
        print("       🎬 한국 영화·드라마 퀴즈 게임 🎬")
        print("========================================")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 점수 확인")
        print("  5. 종료")
        print("========================================")

    def run(self):
        while True:
            self.show_menu()
            user_input = input("  선택: ").strip()

            # 입력이 없는 경우
            if not user_input:
                print("  입력이 비어 있습니다.")
                continue

            # 잘못된 입력 예외처리
            try:
                choice = int(user_input)
            except ValueError:
                print("  잘못된 입력입니다.")
                continue
            
            # 1~5 범위의 입력이 아닌 경우
            if not (1 <= choice <= 5):
                print("  1~5 사이의 숫자를 입력하세요.")
                continue

            # 종료(5)를 선택한 경우
            if choice == 5:
                print("\n  게임을 종료합니다.\n")
                break

def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n퀴즈가 중단되었습니다. 안전하게 종료합니다.\n")

if __name__ == "__main__":
    main()