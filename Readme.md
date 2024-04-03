# 실험4 - 열역학 (이성분계 혼합물의 기체-액체 상 평형)


## 시작 가이드 - 변형된 라울의 법칙을 통한 값 구하기
### Requirements
For building and running the application you need:
- [go 1.22.1]

### Installation
``` bash
$ git clone https://github.com/IHateChem/CBE_LAB4
$ cd CBE_LAB4
```

#### Build & Run
```
$ go build 
$ ./lab4
```
---
## Pseudo Code
```
1. Calibration Curve를 통해 계산된 Acetone, IsoPropanol의 액상 몰분율을 비롯해 계산에 필요한 값들을 기입. 
2. Antoines' Eq.를 통해 T1_sat, T2_sat계산
3. Raoult's law를 통해 initail T계산
4. while 직전계산한 T값과의 차이가 0.1이상
    a.  2.771 - 0.00523*T을 통해 A값 계산
    b. Initial Saturation Pressure를 계산. 
    c. γ1, γ2를 계산한다. 
    d. 새로운 P_sat계산
    e. 새로운 T게산.
5.계산결과 출력 

```


## 시작 가이드 - Peng Robinson Equation을 통한 T, y값 구하기. 
### Requirements
For building and running the application you need:
- [python  3.11.0]

### Installation
``` bash
$ git clone https://github.com/IHateChem/CBE_LAB4
$ cd CBE_LAB4
```

#### Run
```
$ python3 PR.py
```
---
## Pseudo Code
```
1. Calibration Curve를 통해 계산된 Acetone, IsoPropanol의 액상 몰분율을 비롯해 계산에 필요한 값들을 기입. 
2. 변형된 라울의 법칙을 통해 계산된 초기 T, y값 기입. 
4. while y1+y2가 1과의 차이가 0.001보다 커지거나 maxIteration도달. 
    a.  Z에 대한 방정식을 풀고, a,b,q,I등 여러 값의 계산을 바탕으로 새로운 y값 계산
5.계산결과 출력 

```
