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
    """개별 퀴즈를 표현하는 클래스"""

    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices  # 4개의 선택지 리스트
        self.answer = answer    # 1~4 사이의 정답 번호

    def display(self, index: int):
        """퀴즈를 화면에 출력한다"""
        print(f"\n----------------------------------------")
        print(f"[문제 {index}]")
        print(f"{self.question}\n")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        """사용자의 답이 정답인지 확인한다"""
        return user_answer == self.answer

    def to_dict(self) -> dict:
        """Quiz 객체를 딕셔너리로 변환한다 (JSON 저장용)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        """딕셔너리에서 Quiz 객체를 생성한다 (JSON 불러오기용)"""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes: list[Quiz] = []
        self.best_score: int = 0        # 최고 점수 (백분율)
        self.best_correct: int = 0      # 최고 점수 당시 정답 수
        self.best_total: int = 0        # 최고 점수 당시 총 문제 수
        self.load_state()

    # ── 파일 입출력 ──────────────────────────────────────────────

    def load_state(self):
        """state.json에서 퀴즈 데이터와 점수를 불러온다"""
        if not os.path.exists(STATE_FILE):
            self._use_default_quizzes()
            print("📂 저장된 파일이 없어 기본 퀴즈 데이터를 불러왔습니다.")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            self.best_correct = data.get("best_correct", 0)
            self.best_total = data.get("best_total", 0)

            print(f"📂 저장된 데이터를 불러왔습니다. "
                  f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

        except (json.JSONDecodeError, KeyError, TypeError):
            print("⚠️  데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            self._use_default_quizzes()
        except OSError as e:
            print(f"⚠️  파일을 읽는 중 오류가 발생했습니다: {e}")
            self._use_default_quizzes()

    def save_state(self):
        """현재 퀴즈 데이터와 점수를 state.json에 저장한다"""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"⚠️  파일 저장 중 오류가 발생했습니다: {e}")

    def _use_default_quizzes(self):
        """기본 퀴즈 데이터를 사용한다"""
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = 0
        self.best_correct = 0
        self.best_total = 0

    # ── 입력 헬퍼 ────────────────────────────────────────────────

    def _input_number(self, prompt: str, min_val: int, max_val: int) -> int:
        """유효한 범위의 숫자를 입력받을 때까지 반복한다"""
        while True:
            raw = input(prompt).strip()
            if not raw:
                print(f"⚠️  입력이 비어 있습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue
            try:
                value = int(raw)
            except ValueError:
                print(f"⚠️  잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue
            if not (min_val <= value <= max_val):
                print(f"⚠️  잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
                continue
            return value

    def _input_text(self, prompt: str) -> str:
        """빈 문자열이 아닌 텍스트를 입력받을 때까지 반복한다"""
        while True:
            raw = input(prompt).strip()
            if not raw:
                print("⚠️  입력이 비어 있습니다. 다시 입력해 주세요.")
                continue
            return raw

    # ── 메뉴 ─────────────────────────────────────────────────────

    def show_menu(self):
        """메인 메뉴를 출력한다"""
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
        """게임 메인 루프를 실행한다"""
        menu_actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.show_quiz_list,
            4: self.show_best_score,
            5: self._quit
        }

        while True:
            self.show_menu()
            choice = self._input_number("  선택: ", 1, 5)
            menu_actions[choice]()

    def _quit(self):
        """게임을 종료한다"""
        self.save_state()
        print("\n👋 게임을 종료합니다. 즐거운 시간이었기를 바랍니다!\n")
        raise SystemExit(0)

    # ── 퀴즈 풀기 ────────────────────────────────────────────────

    def play_quiz(self):
        """퀴즈 풀기 기능"""
        if not self.quizzes:
            print("\n⚠️  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct = 0

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")

        for i, quiz in enumerate(self.quizzes, 1):
            quiz.display(i)
            user_ans = self._input_number("\n  정답 입력: ", 1, 4)

            if quiz.check_answer(user_ans):
                print("  ✅ 정답입니다!")
                correct += 1
            else:
                print(f"  ❌ 오답입니다. 정답은 {quiz.answer}번이에요.")

        score = round(correct / total * 100)
        print(f"\n========================================")
        print(f"  🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")

        if score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            self.save_state()
            print("  🎉 새로운 최고 점수입니다!")
        else:
            print(f"  (최고 점수: {self.best_score}점)")

        print("========================================")

    # ── 퀴즈 추가 ────────────────────────────────────────────────

    def add_quiz(self):
        """새 퀴즈를 등록한다"""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self._input_text("  문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self._input_text(f"  선택지 {i}: ")
            choices.append(choice)

        answer = self._input_number("  정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()

        print("  ✅ 퀴즈가 추가되었습니다!")

    # ── 퀴즈 목록 ────────────────────────────────────────────────

    def show_quiz_list(self):
        """등록된 퀴즈 목록을 출력한다"""
        if not self.quizzes:
            print("\n⚠️  등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"  [{i}] {quiz.question}")
        print("----------------------------------------")

    # ── 점수 확인 ────────────────────────────────────────────────

    def show_best_score(self):
        """최고 점수를 출력한다"""
        print("\n========================================")
        if self.best_score == 0 and self.best_total == 0:
            print("  🏆 아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"  🏆 최고 점수: {self.best_score}점 "
                  f"({self.best_total}문제 중 {self.best_correct}문제 정답)")
        print("========================================")


# ── 진입점 ───────────────────────────────────────────────────────

def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️  프로그램이 중단되었습니다. 데이터를 저장합니다...")
        game.save_state()
        print("💾 저장 완료. 안전하게 종료합니다.\n")


if __name__ == "__main__":
    main()