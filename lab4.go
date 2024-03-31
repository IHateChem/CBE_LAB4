package main

import (
	"fmt"
	"math"
	"strconv"
)

var ACETONE_T_SAT = ACETONE_B/(ACETONE_A-math.Log10(P)) - ACETONE_C
var ISO_PROPANOL_T_SAT = ISO_PROPANOL_B/(ISO_PROPANOL_A-math.Log10(P)) - ISO_PROPANOL_C
var x_acetones = []float64{0.092027467, 0.150737506, 0.233719893, 0.340767172}
var x_isos []float64

// gamma_acetonne, gamma_iso구하기
func getGamma(A float64, sample int) (float64, float64) {
	return math.Exp(A * math.Pow(x_isos[sample], 2)), math.Exp(A * math.Pow(x_acetones[sample], 2))
}

// P_sat_acetonne, P_sat_iso구하기
func getPsat1(T float64) (float64, float64) {
	return math.Pow(10, ACETONE_A-(ACETONE_B/(T+ACETONE_C))), math.Pow(10, ISO_PROPANOL_A-(ISO_PROPANOL_B/(T+ISO_PROPANOL_C)))
}

// P_sat_acetonne 구하기
func getNewPsat(P1, P2, gam1, gam2, x1, x2 float64) float64 {
	return P / (x1*gam1 + x2*gam2*P2/P1)
}

// 새로운 T값 구하기
func getNewT(P1 float64) float64 {
	return ACETONE_B/(ACETONE_A-math.Log10(P1)) - ACETONE_C
}
func main() {
	// experience_x_acetone에서 각 요소를 1에서 빼서 experience_x_iso에 추가
	for _, value := range x_acetones {
		x_isos = append(x_isos, 1-value)
	}
	// 각 샘플별 결과 구하기
	for i := 0; i < 4; i++ {
		// initail T 계산
		var T_init = x_acetones[i]*ACETONE_T_SAT + x_isos[i]*ISO_PROPANOL_T_SAT
		var P_sat_acetonne, P_sat_iso, gamma_acetonne, gamma_iso, A float64 = 0, 0, 0, 0, 0
		var delT = 1.0
		var T = T_init
		// P값 수렴시키기.
		for delT > 0.1 {
			A = 2.771 - 0.00523*T
			gamma_acetonne, gamma_iso = getGamma(A, i)
			P_sat_acetonne, P_sat_iso = getPsat1(T)
			new_Psat_acetone := getNewPsat(P_sat_acetonne, P_sat_iso, gamma_acetonne, gamma_iso, x_acetones[i], x_isos[i])
			delT = math.Abs(T - getNewT(new_Psat_acetone))
			T = getNewT(new_Psat_acetone)

		}
		sample := "Sample " + strconv.Itoa(i+1) + ": "
		// 열 제목 출력
		fmt.Printf("%-12s%-12s%-12s%-12s%-12s%-12s%-12s%-12s%-12s%-12s\n", sample, "P(bar)", "T(K)", "x1", "y1", "P1_sat(bar)", "P2_sat(bar)", "γ_1", "γ_2", "A")

		// 실험 결과 출력
		fmt.Printf("%-12s%-12.3f%-12.3f%-12.3f%-12.3f%-12.3f%-12.3f%-12.3f%-12.3f%-12.3f\n", "", P, T, x_acetones[i], gamma_acetonne*x_acetones[i]*P_sat_acetonne, P_sat_acetonne, P_sat_acetonne, gamma_acetonne, gamma_iso, A)

	}

}
