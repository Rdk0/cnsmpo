package main

import (
	"fmt"
	"reflect"
)

type values struct {
	Clogp float64
	Clogd float64
	Mw    float64
	Pka   float64
	Tpsa  float64
	Hbd   float64
}

func MPO_Clogp(Clogp float64) float64 {
	if Clogp <= 3.0 {
		return 1.0
	} else if Clogp >= 5.0 {
		return 0.0
	} else {
		return (5.0 - Clogp) / 2.0
	}
}

func MPO_Clogd(Clogd float64) float64 {
	if Clogd <= 2.0 {
		return 1.0
	} else if Clogd >= 4.0 {
		return 0.0
	} else {
		return (Clogd - 2.0) / 2.0
	}
}

func MPO_Mw(Mw float64) float64 {
	if Mw <= 360.0 {
		return 1.0
	} else if Mw >= 500.0 {
		return 0.0
	} else {
		return (500.0 - Mw) / (500.0 - 360.0)
	}
}

func MPO_Pka(Pka float64) float64 {
	if Pka <= 8.0 {
		return 1.0
	} else if Pka >= 10.0 {
		return 0.0
	} else {
		return (10 - Pka) / 2.0
	}
}

func MPO_Hbd(Hbd float64) float64 {
	if Hbd == 0 {
		return 1.0
	} else if Hbd >= 3.5 {
		return 0.0
	} else {
		return (3.5 - Hbd) / 3.0
	}
}

func MPO_Tpsa(Tpsa float64) float64 {
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

func calcMpo(vals values) float64 {
	return MPO_Clogp(vals.Clogp) + MPO_Clogd(vals.Clogd) + MPO_Mw(vals.Mw) + MPO_Pka(vals.Pka) + MPO_Hbd(vals.Hbd)
}

func main() {
	var vals values
	var number float64

	for _, prop := range [6]string{"Clogp", "Clogd", "Mw", "Pka", "Tpsa", "Hbd"} {
		fmt.Println("input " + prop)
		fmt.Scanf("%d", &number)
		reflect.ValueOf(&vals).Elem().FieldByName(prop).SetFloat(number)

	}
	fmt.Printf("calculated MPO for %+v is %.2f\n", vals, calcMpo(vals))
}
