import platform

import matplotlib.pyplot as plt
if platform.system() == "Windows":
    plt.rc("font", family="NanumGothic")
else:
    plt.rc("font", family="NanumGothicOTF")


def get(l, idx, val) -> list:
    lst = list()
    for i in l:
        if i[idx] == val:
            lst.append(i)
    return lst


def inn(l, idx, val) -> list:
    lst = list()
    for i in l:
        if val in i[idx]:
            lst.append(i)
    return lst


def make_histogram(title, dataset1, dataset2, label1, label2, xlabel="정답 개수(개)", ylabel="빈도(사람 수 / 전체 사람 수)"):
    plt.title(title)
    plt.hist(dataset1, color="r", alpha=0.5, bins=9, label=label1, density=True)
    if dataset2:
        plt.hist(dataset2, color="b", alpha=0.5, bins=9, label=label2, density=True)
    plt.xlabel(xlabel, loc="right")
    plt.ylabel(ylabel, loc="top")
    plt.legend()
    plt.show()


CORRECT_ANS = ["옳음", "틀림", "옳음", "옳음", "옳음", "그 분식집은 치즈떡볶이가 맛있다.", "그는 노래를 참 못해서 들어줄 수가 없다.", "그런 나쁜 행동은 따라 하지 마.", "한글 띄어쓰기", "한글 붙여쓰기"]
people = list()

with open("result.csv", "r", encoding="UTF-8") as csv:
    for line in csv.readlines():
        ans = line.replace('"', '').replace("\n", '').split(",")
        ans.pop(0)
        ans.pop(15)
        if ans[4] == "예":
            ans[-1] = ans[-1][1:]
            
            score = 0
            for i in range(7, len(ans)):
                try:
                    if ans[i] == CORRECT_ANS[i - 7]:
                        score += 1
                except IndexError:
                    break
            
            ans.append(score)
            people.append(ans)
    csv.close()

# 전체
hist = list()
score = 0

for i in people:
    hist.append(i[-1])
    score += i[-1]

print(f"전체 평균: {round(score / len(people), 1)}/9")
make_histogram("정답 개수 히스토그램", hist, False, "전체", '')

# 남녀
ml = get(people, 3, "남")
fl = get(people, 3, "여")
hist = {
    "male": list(),
    "female": list(),
}
score = {
    "male": 0,
    "female": 0,
}

for i in ml:
    hist["male"].append(i[-1])
    score["male"] += i[-1]
for i in fl:
    hist["female"].append(i[-1])
    score["female"] += i[-1]

print(f"남자 평균: {round(score['male'] / len(ml), 1)}/9")
print(f"여자 평균: {round(score['female'] / len(fl), 1)}/9")
make_histogram("남녀 별 정답 개수 히스토그램", hist["male"], hist["female"], "남", "여")

# 고등 / 중등
hil = inn(people, 1, "고등학교")
mil = inn(people, 1, "중학교")
hist = {
    "high": list(),
    "middle": list(),
}
score = {
    "high": 0,
    "middle": 0,
}

for i in hil:
    hist["high"].append(i[-1])
    score["high"] += i[-1]
for i in mil:
    hist["middle"].append(i[-1])
    score["middle"] += i[-1]

print(f"고등학생 평균: {round(score['high'] / len(hil), 1)}/9")
print(f"중학생 평균: {round(score['middle'] / len(mil), 1)}/9")
make_histogram("학교급 별 정답 개수 히스토그램", hist["high"], hist["middle"], "고등학교", "중학교")

# 교육 여부
yl = get(people, 6, "예")
nl = get(people, 6, "아니오")
hist = {
    "y": list(),
    "n": list(),
}
score = {
    "y": 0,
    "n": 0,
}

for i in yl:
    hist["y"].append(i[-1])
    score["y"] += i[-1]
for i in nl:
    hist["n"].append(i[-1])
    score["n"] += i[-1]

print(f"교육 경험 있는 사람 평균: {round(score['y'] / len(yl), 1)}/9")
print(f"교육 경험 없는 사람 평균: {round(score['n'] / len(nl), 1)}/9")
make_histogram("교육 여부 별 정답 개수 히스토그램", hist["y"], hist["n"], "교육 경험 있음", "교육 경험 없음")
