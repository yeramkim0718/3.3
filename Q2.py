import os
import json
import jwt
import datetime

TOKEN_FILE = 'token.txt'
TESTER_CONF_FILE = 'testerconf.json'
TEST_CONF_FILE = 'testconf.json'


def read_json_file(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def menu_main():
    while True:
        print("1. 토큰 획득")
        print("2. 테스터 정보 관리")
        print("3. 테스트 관리")
        print("4. 테스트 시작")
        print("5. 종료")
        choice = input("번호를 선택하세요: ").strip()
        if choice == "1":
            handle_token_acquisition()
        elif choice == "2":
            handle_tester_info_management()
        elif choice == "3":
            handle_test_management()
        elif choice == "4":
            handle_test_start()
        elif choice == "5":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다.")


def handle_token_acquisition():
    email = input("사용자 이메일을 입력하세요: ").strip()
    token = generate_token(email)
    with open(TOKEN_FILE, 'w') as file:
        file.write(f'{email}:{token}')
    print(f"토큰이 생성되어 {TOKEN_FILE}에 저장되었습니다.")


def generate_token(email):
    SECRET_KEY = 'abcd11221'

    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def handle_tester_info_management():
    while True:
        print("1. 저장된 테스터 정보")
        print("2. 테스터 정보 추가")
        print("3. 테스터 정보 삭제")
        print("4. 뒤로가기")
        choice = input("번호를 선택하세요: ").strip()
        if choice == "1":
            display_tester_info()
        elif choice == "2":
            add_tester_info()
        elif choice == "3":
            delete_tester_info()
        elif choice == "4":
            return
        else:
            print("잘못된 선택입니다.")


def display_tester_info():
    testers = read_json_file(TESTER_CONF_FILE)
    if not testers:
        print("저장된 테스터 정보가 없습니다.")
        return
    for email, info in testers.items():
        print(f"이메일: {email}, 이름: {info['name']}, 핸드폰 번호: {info['phone']}, 생년월일: {info['dob']}")


def add_tester_info():
    testers = read_json_file(TESTER_CONF_FILE)
    email = input("이메일을 입력하세요: ").strip()
    if email in testers:
        print("이메일이 중복되었습니다.")
        return
    name = input("이름을 입력하세요: ").strip()
    phone = input("핸드폰 번호를 입력하세요: ").strip()
    dob = input("생년월일을 입력하세요: ").strip()
    testers[email] = {"name": name, "phone": phone, "dob": dob}
    write_json_file(TESTER_CONF_FILE, testers)
    print("테스터 정보가 추가되었습니다.")


def delete_tester_info():
    testers = read_json_file(TESTER_CONF_FILE)
    email = input("삭제할 이메일을 입력하세요: ").strip()
    if email not in testers:
        print("해당 이메일의 테스터 정보가 없습니다.")
        return
    confirmation = input("정말 삭제하시겠습니까? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        del testers[email]
        write_json_file(TESTER_CONF_FILE, testers)
        print("테스터 정보가 삭제되었습니다.")
    else:
        print("삭제가 취소되었습니다.")


def handle_test_management():
    while True:
        print("1. 저장된 테스트 정보")
        print("2. 테스트 추가")
        print("3. 테스트 삭제")
        print("4. 뒤로가기")
        choice = input("번호를 선택하세요: ").strip()
        if choice == "1":
            display_test_info()
        elif choice == "2":
            add_test_info()
        elif choice == "3":
            delete_test_info()
        elif choice == "4":
            return
        else:
            print("잘못된 선택입니다.")


def display_test_info():
    tests = read_json_file(TEST_CONF_FILE)
    if not tests:
        print("저장된 테스트 정보가 없습니다.")
        return
    for test_name in tests:
        print(f"테스트 명: {test_name}")


def add_test_info():
    tests = read_json_file(TEST_CONF_FILE)
    test_name = input("테스트 명을 입력하세요: ").strip()
    if test_name in tests:
        print("테스트 명이 중복되었습니다.")
        return
    tests[test_name] = {}  # 빈 딕셔너리로 추가
    write_json_file(TEST_CONF_FILE, tests)
    print("테스트 정보가 추가되었습니다.")


def delete_test_info():
    tests = read_json_file(TEST_CONF_FILE)
    test_name = input("삭제할 테스트 명을 입력하세요: ").strip()
    if test_name not in tests:
        print("해당 테스트 명이 없습니다.")
        return
    confirmation = input("정말 삭제하시겠습니까? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        del tests[test_name]
        write_json_file(TEST_CONF_FILE, tests)
        print("테스트 정보가 삭제되었습니다.")
    else:
        print("삭제가 취소되었습니다.")


def handle_test_start():
    email = input("이메일을 입력하세요: ").strip()
    if not os.path.exists(TOKEN_FILE):
        print("토큰 파일이 없습니다. 먼저 [토큰 획득]을 수행하세요.")
        return

    with open(TOKEN_FILE, 'r') as file:
        token_data = file.read().strip().split(':')
        if len(token_data) != 2 or token_data[0] != email:
            print("이메일에 해당하는 토큰이 없습니다.")
            return

    token = token_data[1]
    print(f"이메일: {email}, 토큰: {token}")

    testers = read_json_file(TESTER_CONF_FILE)
    if email in testers:
        info = testers[email]
        print(f"이름: {info['name']}, 핸드폰 번호: {info['phone']}, 생년월일: {info['dob']}")
    else:
        print("해당 이메일의 테스터 정보가 없습니다.")

    tests = read_json_file(TEST_CONF_FILE)
    if not tests:
        print("저장된 테스트가 없습니다.")
        return

    for test_name in tests:
        print(f"테스트 명: {test_name}")


if __name__ == "__main__":
    menu_main()