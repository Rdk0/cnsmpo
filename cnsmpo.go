package main

import (
	"example.com/cnsmpo/tviewtui"
	"fmt"
)

func MpoClogp(Clogp float64) float64 {
	if Clogp <= 3.0 {
		return 1.0
	} else if Clogp >= 5.0 {
		return 0.0
	} else {
		return (5.0 - Clogp) / 2.0
	}
}

func MpoClogd(Clogd float64) float64 {
	if Clogd <= 2.0 {
		return 1.0
	} else if Clogd >= 4.0 {
		return 0.0
	} else {
		return (Clogd - 2.0) / 2.0
	}
}

func MpoMw(Mw float64) float64 {
	if Mw <= 360.0 {
		return 1.0
	} else if Mw >= 500.0 {
		return 0.0
	} else {
		return (500.0 - Mw) / (500.0 - 360.0)
	}
}

func MpoPka(Pka float64) float64 {
	if Pka <= 8.0 {
		return 1.0
	} else if Pka >= 10.0 {
		return 0.0
	} else {
		return (10 - Pka) / 2.0
	}
}

func MpoHbd(Hbd float64) float64 {
	if Hbd == 0 {
		return 1.0
	} else if Hbd >= 3.5 {
		return 0.0
	} else {
		return (3.5 - Hbd) / 3.0
	}
}

func MpoTpsa(Tpsa float64) float64 {
	if Tpsa <= 20 || Tpsa >= 120 {
		return 0.0
	} else if Tpsa > 20 && Tpsa < 40 {
		return (Tpsa - 20.0) / 20.0
	} else if Tpsa > 90.0 && Tpsa < 120.0 {
		return (Tpsa - 90.0) / 30.0
	} else {
		return 1.0
	}
}

func calcMpo(vals []float64) float64 {
	return MpoClogp(vals[0]) + MpoClogd(vals[1]) + MpoMw(vals[2]) + MpoPka(vals[3]) + MpoTpsa(vals[4]) + MpoHbd(vals[5])
}

func contributions(vals []float64) {
	fmt.Printf("clogP|      %.1f        |    %.1f\nclogD|      %.1f        |    %.1f\nmw   |      %.1f        |    %.0f\npKa  |      %.1f        |    %.1f\ntpsa |      %.1f        |    %.0f\nhbd  |      %.1f        |    %.0f\n",
		MpoClogp(vals[0]), vals[0], MpoClogd(vals[1]), vals[1], MpoMw(vals[2]), vals[2], MpoPka(vals[3]), vals[3], MpoTpsa(vals[4]), vals[4], MpoHbd(vals[5]), vals[5])
}

func main() {
	vals := tviewtui.GetValues()
	fmt.Println("\n******************************************************")
	fmt.Printf("calculated MPO for %+v is %.1f\n\n", vals, calcMpo(vals))
	fmt.Println("individual contributions for each property are")
	fmt.Println("------------------------------------")
	fmt.Println("prop | MPO contrib     | input value")
	fmt.Println("------------------------------------")
	contributions(vals)
	fmt.Println("\n******************************************************")
	//fmt.Println("press Ctrl-C to exit the program")
}

//}
