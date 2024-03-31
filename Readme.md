# 실험4 - 열역학 (이성분계 혼합물의 기체-액체 상 평형)


## 시작 가이드
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
3. Raoult's laq를 통해 initail T계산
4. while 직전계산한 T값과의 차이가 0.1이상
    a.  2.771 - 0.00523*T을 통해 A값 계산
    b. Initial Saturation Pressure를 계산. 
    c. γ1, γ2를 계산한다. 
    d. 새로운 P_sat계산
    e. 새로운 T게산.
5.계산결과 출력 

```