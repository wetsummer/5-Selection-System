#입력형식:
#1기: 이름, 소속, 연락처, 1지망, 2지망, 3지망, 4지망, 5지망, 선정1, 선정2
#2기: 이름, 소속, 연락처

import json
from pprint import pprint
import random

def uniqeMember(dt): #고윳값 찾기
	return list(set(dt))

def onlyOne(dt): #유일무이한 값 찾기
	count = {}
	for i in dt:
		try: count[i] += 1
		except: count[i]=1
	
	rt = []
	for i in dt:
		if count[i] == 1:
			rt.append(i)
	
	return rt

def straws(rand): #제비뽑기
	return True if random.random() <= (1/rand) else False

def findIt(called, data2, data1name, col1, col2, priority = None): #특정 값을 찾고 그 값이 있으면 선정1 또는 2로 보내기
	uniqename = uniqeMember(called)

	while len(uniqename) > uniqename.count(None):
		for row, data in enumerate(data2, start=0):
			for name in uniqename:
				rand = called.count(name)
				if name is not None and name in data[col1:col2] and straws(rand) and not((priority is not None) ^ (data2[row][10] == priority)):
					if data2[row][8] is None:
						data2[row][8] = name
					elif data2[row][9] is None:
						data2[row][9] = name
					else:
						break

					data1name.remove(name)
					data2[row][10] -= 1 #우선권 감소
					uniqename[uniqename.index(name)] = None

def readJson(fname):
	with open(fname, "r", encoding="UTF-8") as f:
		jsonori = json.load(f)

	jsondt = []
	for n in range(len(jsonori)):
		jsondt.append(list(jsonori[n].values()) + [0])
	
	return jsondt

def removeDuplicatedMajor(data1, data2): #같은 학과 제거
	for index, dt2 in enumerate(data2, start=0):
		for dt1 in data1:
			if dt2[1] == dt1[1]:
				try:
					data2[index][data2[index].index(dt1[0])] = None
				except:
					pass

def realignment(dt, pos): #다른 사람이 미리 선발하여 구멍이 난 후보 목록을 앞으로 당김
	for i in dt:
		if dt[pos] == None and pos < 7:
			dt[pos] = dt[pos+1]
			dt[pos+1] = None

def removeDuplicatedCall(data2, dl, pos): #한 번 할당된 사람은 후보군에서 제거
	for index, i in enumerate(data2, start=0):
		for x in dl:
			tmp = i[3:8].count(x)
			while tmp > 0:
				data2[index][data2[index].index(x)] = None
				tmp -= 1


	realignment(data2, pos)


if __name__ == '__main__':
	#자료 불러오기
	data1 = readJson("1기 정보.json")
	data2 = readJson("2기 정보.json")

	#같은 학과 제거
	removeDuplicatedMajor(data1, data2)

	#이름 목록
	name1 = []
	for data in data1:
		name1.append(data[0])

	isOnly = True
	for rank in range(1,6): #1지망부터 5지망까지
		rankcol = rank + 2

		priority = []
		for i in data2:
			priority.append(i[10])

		for priority in range(max(priority), min(priority) - 1, -1): #우선 지망 높은 것부터 낮은 것으로
			#해당 우선권자의 해당 지망의 후보 추출
			called = []
			for i in data2:
				if i[10] == priority:
					called.append(i[rankcol])

			findIt(called.copy(), data2, name1, rankcol, rankcol + 1, priority)
			removeDuplicatedCall(data2, uniqeMember(called), rankcol + 1)
	
	pprint(data2)
