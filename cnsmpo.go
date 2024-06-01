package main

import (
	//"encoding/json"
	"fmt"
)

type values struct {
  clogp float32
  clogd float32
  mw float32
  pka float32
  tpsa float32
  hbd float32
}

const (
  clogpMax float32 = 5.0 
  clogpMin float32 = 3.0
  clogdMax float32 = 4.0
  clogdMin float32 =  2.0 
  mwMax    float32 =  500.0  
  mwMin    float32 =  360.0
  pkaMax   float32 = 10.0
  pkaMin   float32 = 8.0
  tpsaMax1 float32 = 40.0
  tpsaMax2 float32 = 90.0
  tpsaMin1 float32 = 20.0  
  tpsaMin2 float32 = 120 
  tpsMin   float32 = 40.0
  hbdMin   float32 = 0.0  
  hbdMax   float32 = 4.0
)


func stepFunctionOneSlope(prop string,  vals values) float32{
//all properties with a simple step function with linear slope
var break1 float32
var break2 float32
var val float32
var retVal float32

switch prop:=prop; prop  {
  case "clogp":  {
    break1 = clogpMax
    break2 = clogpMin 
    val    =  vals.clogp
    }
  case "clogd":  {
    break1 = clogdMax
    break2 = clogdMin  
    val    =  vals.clogd
    }
  case "mw":  {
    break1 = mwMax
    break2 = mwMin  
    val    =  vals.mw 
  }
  case "hbd":  {
    break1 = hbdMin
    break2 = hbdMax  
    val    =  vals.hbd 
    }
  default:  {
    return 0.0
    }
  }

  if val < break1 {
    retVal =  1.0
  } else if val > break2 {
    retVal = 0.0
  } else {
  retVal = (break2 - val)/(break2-break1)
  }
  fmt.Printf("contribution from %v is %0.2f\n", prop, retVal)
  return retVal
}

func stepFunctionTwoSlpes(val0 values) float32 {
// case for TPSA with trapezoid step function
//  tpsaMin1 float32 = 20.0 left most
// tpsaMax1 float32 = 40.0 second from the left
//  tpsaMax2 float32 = 90.0 third
//  tpsaMin2 float32 = 120 last
// the vertices are described by tpsaMin1 - tpsaMax1 - tpsaMax2 - tpsaMin2
val := val0.tpsa
var retVal float32
  if (val <  tpsaMin1  || val >  tpsaMin2){
    retVal = 0.0}
  if (val >  tpsaMin1  && val <  tpsaMax1){
    retVal = (val - tpsaMin1)/(tpsaMax1-tpsaMin1)}
  if (val >= tpsaMax1  && val <= tpsaMax2){
    retVal =  1.0}
  if (val >  tpsaMax2  && val <  tpsaMin2) {
    retVal = (val - tpsaMin2)/(tpsaMax2-tpsaMin2)
  }
  fmt.Printf("contribution from TPSA is %0.2f\n", retVal)
  return retVal
}


func calcMpo(vals values) float32{
  var mpoScore float32 = 0.0
  arr := [5]string{"clogp", "clogd", "mw",  "pka", "hbd"} 
  for _, prop := range arr { 
    mpoScore +=  stepFunctionOneSlope(prop, vals)  
    } 
  mpoScore += stepFunctionTwoSlpes(vals)
  return mpoScore
}

func main(){
vals := values{
  clogp: 2.5,
  clogd: 2.4, 
  mw: 300, 
  pka: 2.1,
  tpsa: 120,
  hbd: 2.0,
}
//byteArr, _ := json.Marshal(vals)
fmt.Printf("calculated MPO for %+v is %.2f\n", vals, calcMpo(vals))
}
